#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes 调度看门狗 —— 由 systemd 独立驱动，不依赖 Hermes 进程。

为什么需要它：Hermes 的 cron 和被监控的任务在同一进程树下，Hermes 挂了就一起挂。
本脚本由 systemd timer 拉起（独立 systemd 单元），检查 jobs.json 里
关键任务是否按时跑过，只在异常时发飞书告警。

🔴 设计原则（静默优先）：
   - 一切正常 → 一个字都不发，不发邮件
   - 发现异常 → 发飞书交互卡片给用户

覆盖故障：
   ✅ Hermes 进程死了        → 任务没跑，last_run 停滞
   ✅ 调度器静默失效          → last_run 停滞
   ✅ 任务连续失败            → failure_streak > 0
   ✅ jobs.json 损坏/丢失     → 读不到即视为故障
   🔴 VM 断电/断网            → 覆盖不了（本工作流裁定不补外部心跳，已接受）

不覆盖：VM 挂、断网、断电 —— 这些必须由本机之外的东西发现，而用户已明确
不采用云端探活方案。此为已知且已接受的边界；断档后靠下次进 VM 时查
last_run / cron last_run_at 判断，不再作为待办跟踪。
"""
from __future__ import annotations

import json
import pathlib
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
import os
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )

# ── Hermes 主目录（可选；未设置时依赖它的功能跳过，不报错）──────────────
_H = os.environ.get("HERMES_HOME", "").rstrip("/")


TZ = timezone(timedelta(hours=8))
JOBS = pathlib.Path(_H + "/cron/jobs.json")
ENV = pathlib.Path(_H + "/.env")
STATE = pathlib.Path(_D + "/.watchdog_state.json")
CHAT = os.environ.get("FEISHU_CHAT_ID", "")     # 告警投递目标（未配置则只打印到 stdout）

# 只有这几条关键任务值得盯（no_agent 纯脚本 + 每日核心扫描）。
# 不监控 LLM 型任务：它们失败通常会自己告警，且响应慢、噪音大。
# 🔴 改用 **任务 ID** 匹配，不再用任务全名。
#   原按名字匹配有个真 bug：我把两个任务从「盈利保护」改名为「持仓三模块」后，
#   WATCHED 里的旧名匹配不上 → watchdog 报「找不到该任务」，
#   而真实故障（脚本不存在）反而被这条噪音盖住了。改名就失联。
#   ID 在 hermes cron edit --name 改名时保持不变，是稳定键。
WATCHED = {
    # ⚠️ 示例 ID：换成你自己 `cron list` 里的真实任务 ID（12 位十六进制）。
    "YOURCRONID01": {"name": "持仓监控｜持仓三模块11:20 盘中", "max_lag_min": 24 * 60},
    "YOURCRONID02": {"name": "持仓监控｜持仓三模块14:40 尾盘观察", "max_lag_min": 24 * 60},
}
# 按全名匹配的（台账同步任务名稳定，用名字更易读）
WATCHED_BY_NAME = {
    "台账同步｜第5/6步台账＋流程状态表→飞书（no_agent·零token）": {"max_lag_min": 8 * 24 * 60},
}

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def _now():
    return datetime.now(TZ)


def _parse(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def check():
    """返回问题列表；空列表 = 一切正常。"""
    problems = []

    if not JOBS.exists():
        return [{"sev": "🔴", "task": "jobs.json", "msg": f"文件不存在：{JOBS}"}]
    try:
        data = json.loads(JOBS.read_text())
    except Exception as exc:
        return [{"sev": "🔴", "task": "jobs.json", "msg": f"解析失败（可能被写坏）：{exc}"}]

    jobs = data if isinstance(data, list) else data.get("jobs", [])
    by_name = {j.get("name"): j for j in jobs}

    # 0a) 🔴 全量扫描所有 no_agent 任务：script 文件必须真实存在
    #     不依赖 WATCHED 名单 —— 名单外的任务坏掉同样静默（实测抓到 version-watch.sh 缺失）。
    #     只扫启用中的；主动停用的不算故障。
    # 🔴 IGNORE_NOAGENT 按 **任务 ID** 白名单排除（不是名字，改名后仍生效）。
    #     本工作流裁定：版本盯哨任务与 A 股工作流无关，缺失脚本属已知状态、不查不报。
    #     🔴 别把它扩成「所有非股票任务都忽略」—— 那样新加的坏任务又静默了。
    IGNORE_NOAGENT = {"YOURCRONID03"}   # 示例：与 A 股工作流无关、已知缺失脚本的任务 ID，白名单排除
    for j in jobs:
        if not j.get("no_agent") or not j.get("enabled"):
            continue
        if j.get("id") in IGNORE_NOAGENT:
            continue
        script = j.get("script")
        if not script:
            continue
        path = pathlib.Path(j.get("workdir") or "") / script
        if not path.is_file():
            problems.append({
                "sev": "🔴", "task": j.get("name", "?"),
                "msg": (f"🔴 no_agent 脚本不存在：{path}｜script={script!r}、"
                        f"workdir={j.get('workdir')!r}。触发时只会空跑并记 ok，故障完全静默。"
                        f"修法：hermes cron edit {j.get('id')} --script <真实文件名> "
                        f"--workdir <真实目录>"),
            })

    now = _now()
    by_id = {j.get("id"): j for j in jobs}
    # 🔴 两个清单合并成 (task_label, job, rule) 三元组，判定逻辑只有一份。
    watch_list = [(rule.get("name", jid), by_id.get(jid), rule)
                  for jid, rule in WATCHED.items()]
    watch_list += [(nm, by_name.get(nm), rule)
                   for nm, rule in WATCHED_BY_NAME.items()]

    for name, job, rule in watch_list:
        if job is None:
            problems.append({"sev": "🔴", "task": name,
                             "msg": "在 jobs.json 中找不到该任务（可能被删除，或 ID 已变）"})
            continue
        if not job.get("enabled"):
            continue  # 主动禁用不算故障

        # 1) 连续失败
        # （脚本存在性已由上面的 0a 全量扫描统一判定，这里不再重复）
        streak = job.get("failure_streak") or 0
        if streak:
            problems.append({
                "sev": "🔴", "task": name,
                "msg": f"连续失败 {streak} 次｜last_status={job.get('last_status')}｜last_error={str(job.get('last_error'))[:120]}",
            })
            continue

        # 2) 跑得太久没跑（按首次应执行时间判断，没到点不算故障）
        last = _parse(job.get("last_run_at"))
        next_run = _parse(job.get("next_run_at"))
        lag_min = (now - last).total_seconds() / 60 if last else None

        if last is None:
            # 从没跑过：只有已经过了首次应执行时间才算故障
            if next_run and next_run < now:
                overdue_h = (now - next_run).total_seconds() / 3600
                if overdue_h > rule["max_lag_min"] / 60:
                    problems.append({
                        "sev": "🟡", "task": name,
                        "msg": f"从未执行过，且已逾期 {overdue_h:.1f} 小时（next_run={job.get('next_run_at')}）",
                    })
        elif lag_min > rule["max_lag_min"]:
            # 🔴 调度感知（新增）：下一轮还没到点（周末/休市空隙），不算故障。
            #   根因：纯看时间差，周六调休（非交易日）11:20 的 cron 本来就不会跑，
            #   last_run 停在周五，时间差超 24h 即误报。每周一开盘前同理（从上周五算起）。
            #   看 next_run 而不是放宽阈值：调度器真死了 next_run 会变旧（过期），照样报警，不漏真故障。
            if next_run and next_run > now:
                continue
            problems.append({
                "sev": "🟡", "task": name,
                "msg": f"已 {lag_min/60:.1f} 小时没跑（阈值 {rule['max_lag_min']/60:.0f} 小时）｜last_run={job.get('last_run_at')}",
            })

    return problems


def notify(problems):
    """发飞书交互卡片（格式规范见 skills/feishu/feishu-im-message）。"""
    env = {}
    for line in ENV.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": env["FEISHU_APP_ID"], "app_secret": env["FEISHU_APP_SECRET"]}).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"})
    tok = json.loads(urllib.request.urlopen(req, timeout=25, context=CTX).read())["tenant_access_token"]

    now = _now()
    rows = []
    for p in problems:
        rows.append([
            {"tag": "markdown", "content": f"**{p['sev']}** {p['task']}"},
            {"tag": "markdown", "content": p["msg"]},
        ])

    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": "red" if any(p["sev"] == "🔴" for p in problems) else "orange",
            "title": {"tag": "plain_text", "content": f"🔔 Hermes 调度看门狗告警（{len(problems)} 项异常）"},
        },
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": f"**检测时间**：{now:%Y-%m-%d %H:%M} CST\n**判断依据**：jobs.json 中关键任务的 last_run / failure_streak / next_run"}},
            {"tag": "hr"},
            {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": f"**{p['sev']} {p['task']}**\n{p['msg']}"}} for p in problems]},
            {"tag": "hr"},
            {"tag": "note", "elements": [{"tag": "lark_md", "content": "由 systemd 独立驱动，不依赖 Hermes 进程。覆盖不了 VM 断电/断网（已知边界，未补外部探活）。"}]},
        ],
    }

    payload = {"receive_id": CHAT, "msg_type": "interactive",
               "content": json.dumps(card, ensure_ascii=False)}
    # 🔴 坑（实测）：card 与 content 必须同时传且内容相同，否则 99992402
    payload["card"] = card
    r = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=json.dumps(payload, ensure_ascii=False).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=utf-8"})
    resp = json.loads(urllib.request.urlopen(r, timeout=25, context=CTX).read())
    return resp


def main():
    if not _H:
        # 未设 HERMES_HOME → 本机没有 Hermes profile / cron，看门狗无事可做。
        print("ℹ️ 未配置 HERMES_HOME → 未检测到 Hermes profile，看门狗跳过（本工具仅在"
              "用 Hermes cron 驱动本工作流时才有意义）。")
        return
    if not CHAT:
        print("⚠️ 未配置 FEISHU_CHAT_ID → 检测到异常时无法投递飞书告警，"
              "将只打印到 stdout。")

    dry = "--dry" in sys.argv
    force = "--force" in sys.argv  # 强制发一张卡，验证通道

    if force:
        probs = [{"sev": "🔴", "task": "【自检】强制告警测试", "msg": "这是一张手动触发的测试卡片，用于验证飞书通道是否正常。"}]
    else:
        probs = check()

    # 🔴 静默规则：正常时什么都不发（含邮件）
    if not probs:
        print(f"[{_now():%Y-%m-%d %H:%M}] ✅ 全部正常（{len(WATCHED)} 项检查），静默。")
        return 0

    print(f"[{_now():%Y-%m-%d %H:%M}] 🔴 发现 {len(probs)} 项异常：")
    for p in probs:
        print(f"  {p['sev']} {p['task']}\n      {p['msg']}")

    if dry:
        return 0

    try:
        resp = notify(probs)
        ok = resp.get("code") == 0
        print(f"{'✅ 已发飞书' if ok else '🔴 发送失败'}：code={resp.get('code')} msg={resp.get('msg')}")
        if not ok:
            print(f"   完整响应: {str(resp)[:300]}")
            return 1
    except Exception as exc:
        print(f"🔴 发送异常（看门狗自身故障）: {type(exc).__name__}: {exc}")
        return 1

    STATE.write_text(json.dumps({"last_alert": _now().isoformat(), "problems": probs},
                                ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())