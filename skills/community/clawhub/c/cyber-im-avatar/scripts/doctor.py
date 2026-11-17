#!/usr/bin/env python3
"""doctor.py — 一屏体检 + 自愈引导（故障处理入口）。

设计目标：**故障时 agent 不需要猜**。每一处异常都直接给出「下一步该跑什么」，
并指向 references/troubleshooting.md 的对应小节。

检查项
------
1. cli       : 命令是否存在、版本号
2. doctor    : 调用 CLI 自带体检（lark-cli doctor / dws doctor；企微无）
3. auth      : 登录态与 token 过期时间（能否自动刷新 → 要不要重新授权）
4. env       : ~/.im-standin/env.json 是否可解析、self_id 是否已抓
5. state     : 水位目录可写、水位文件 JSON 合法
6. path      : 可选，给 --chat-id/--user-id 时真跑 3 秒监听验证通路

用法
----
  python3 scripts/doctor.py                          # 全平台体检
  python3 scripts/doctor.py feishu                   # 只查一个平台
  python3 scripts/doctor.py feishu --chat-id oc_xxx  # 附带通路自检
  python3 scripts/doctor.py --check-update           # 额外查新版
  python3 scripts/doctor.py --repair-state           # 隔离损坏的水位文件
  python3 scripts/doctor.py --json                   # 机器可读
  python3 scripts/doctor.py --show-ids               # 不脱敏（默认打码）

退出码：0=无 fail · 2=存在 fail（warn 不影响退出码）
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bootstrap as bs  # noqa: E402  复用同一份平台配置，避免两套真相

ENV_PATH = bs.ENV_PATH
ENV_DIR = bs.ENV_DIR
STATE_DIR = os.path.join(ENV_DIR, "states")

TS = "references/troubleshooting.md"


# ---------------------------------------------------------------- 基础工具
def run(argv, timeout=30):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return 127, "", f"not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def json_of(text):
    try:
        obj, _ = json.JSONDecoder().raw_decode(text.lstrip())
        return obj
    except Exception:
        return None


def mask(v, show=False):
    if not v:
        return ""
    s = str(v)
    if show or len(s) <= 10:
        return s
    return s[:6] + "…" + s[-4:]


class Report:
    """一个平台的检查结果。检查项统一四态：ok / warn / fail / skip。"""

    def __init__(self, platform, cli):
        self.platform = platform
        self.cli = cli
        self.items = []

    def add(self, name, status, detail="", fix="", ref=""):
        self.items.append({"check": name, "status": status,
                           "detail": detail, "fix": fix, "ref": ref})
        return status

    def worst(self):
        st = {i["status"] for i in self.items}
        return "fail" if "fail" in st else ("warn" if "warn" in st else "ok")

    def has_fail(self):
        return any(i["status"] == "fail" for i in self.items)


MARK = {"ok": "[ok]  ", "warn": "[warn]", "fail": "[fail]", "skip": "[skip]"}


def emit(rep, show_ids=False):
    print(f"\n== {rep.platform} ({rep.cli}) ==")
    for it in rep.items:
        det = it["detail"]
        if not show_ids:
            det = re.sub(r"(ou_[0-9a-f]{6})[0-9a-f]+([0-9a-f]{4})", r"\1…\2", det)
            det = re.sub(r"(oc_[0-9a-f]{6})[0-9a-f]+([0-9a-f]{4})", r"\1…\2", det)
            det = re.sub(r"(aib[A-Za-z0-9_-]{6})[A-Za-z0-9_-]+", r"\1…", det)
        print(f"  {MARK[it['status']]} {it['check']}: {det}")
        if it["status"] in ("fail", "warn") and it["fix"]:
            print(f"         → 修复: {it['fix']}")
        if it["status"] == "fail" and it["ref"]:
            print(f"         → 手册: {TS}#{it['ref']}")


# ---------------------------------------------------------------- 各检查项
def check_cli(rep):
    path = shutil.which(rep.cli)
    if not path:
        rep.add("cli", "fail", f"未找到 {rep.cli}",
                fix=f"安装 {rep.cli}（见手册 A.1）", ref="a")
        return False
    rep.add("cli", "ok", path)
    vcmd = ["--version"] if rep.platform != "dingtalk" else ["version"]
    rc, out, err = run([rep.cli] + vcmd, timeout=20)
    ver = (out.splitlines()[0] if out else "") or err.splitlines()[:1]
    if rc == 0 and out:
        rep.add("version", "ok", ver[:80])
    else:
        rep.add("version", "warn", f"取版本失败 rc={rc}",
                fix=f"{rep.cli} {'--version' if rep.platform != 'dingtalk' else 'version'}",
                ref="a")
    return True


def check_cli_doctor(rep):
    """优先用 CLI 自带体检——它比我们更清楚自己该检查什么。"""
    if rep.platform == "wecom":
        rep.add("cli doctor", "skip", "wecom-cli 无 doctor 子命令",
                fix="用 auth show + 手动拉一条消息代替", ref="b")
        return
    argv = [rep.cli, "doctor", "--json"] if rep.platform == "dingtalk" else [rep.cli, "doctor"]
    rc, out, err = run(argv, timeout=45)
    obj = json_of(out)
    if rc != 0 or not isinstance(obj, dict):
        rep.add("cli doctor", "warn", f"rc={rc} {(err or out)[:120]}",
                fix=f"{rep.cli} doctor", ref="a")
        return
    checks = obj.get("checks") or []
    bad = [c for c in checks if c.get("status") not in ("pass", "ok", "skip")]
    if not bad:
        rep.add("cli doctor", "ok", f"{len(checks)} 项全过")
        return
    detail = "; ".join(f"{c.get('name')}={c.get('status')}({c.get('message') or ''})"[:90]
                       for c in bad)
    hint = next((c.get("hint") for c in bad if c.get("hint")), "")
    rep.add("cli doctor", "fail", detail,
            fix=hint or f"{rep.cli} doctor 看完整输出", ref="b" if "auth" in detail.lower() else "a")


def _fmt_eta(dt):
    delta = dt - datetime.now(timezone.utc)
    secs = int(delta.total_seconds())
    if secs <= 0:
        return "已过期"
    if secs < 3600:
        return f"{secs // 60} 分钟后"
    if secs < 86400:
        return f"{secs // 3600} 小时后"
    return f"{secs // 86400} 天后"


def _parse_dt(s):
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def check_auth(rep, env):
    st = (env.get("platforms", {}).get(rep.platform) or {})
    cached = st.get("self_id")

    if rep.platform == "feishu":
        rc, out, _ = run([rep.cli, "auth", "status"], timeout=25)
        obj = json_of(out) or {}
        user = (obj.get("identities") or {}).get("user") or {}
        tok = user.get("tokenStatus")
        refresh = _parse_dt(user.get("refreshExpiresAt"))
        access = _parse_dt(user.get("expiresAt"))
        if tok == "valid" and (refresh is None or refresh > datetime.now(timezone.utc)):
            eta = f"，access {_fmt_eta(access)}到期" if access else ""
            rep.add("auth", "ok", f"tokenStatus=valid{eta}，refresh {_fmt_eta(refresh) if refresh else '未知'}")
        elif refresh and refresh <= datetime.now(timezone.utc):
            rep.add("auth", "fail", f"refresh token {_fmt_eta(refresh)}过期，无法自动续期",
                    fix="python3 scripts/reauth.py feishu"
                        "（直接把授权卡片发到你飞书，点一下就续期，不用扫码）", ref="b")
        else:
            rep.add("auth", "warn", f"tokenStatus={tok}，会自动刷新；若连续 401 再重新授权",
                    fix="python3 scripts/reauth.py feishu --force", ref="b")
        sid = user.get("openId")
        if sid:
            rep.add("self_id", "ok", mask(sid))
        else:
            rep.add("self_id", "fail", "auth status 里没有 openId",
                    fix="python3 scripts/bootstrap.py", ref="b")
        return

    if rep.platform == "wecom":
        rc, out, err = run([rep.cli, "auth", "show"], timeout=25)
        text = out or err
        m = re.search(r"Bot ID:\s*(\S+)", text)
        if "authorized" in text.lower() and m:
            rep.add("auth", "ok", "authorized")
            rep.add("self_id", "ok", mask(m.group(1)))
        else:
            # 未授权时 self_id 必然取不到，不重复报一次 fail
            rep.add("auth", "fail", (text or "无输出").splitlines()[0][:80],
                    fix=f"{rep.cli} auth init --noninteractive --output-qrcode /tmp/wecom-qr.png "
                        "（把二维码发给用户）或 auth init --manual", ref="b")
        return

    # dingtalk
    rc, out, _ = run([rep.cli, "auth", "status"], timeout=25)
    obj = json_of(out) or {}
    if obj.get("authenticated"):
        rep.add("auth", "ok", "authenticated=true")
        rc2, out2, _ = run([rep.cli, "profile", "list"], timeout=25)
        p = json_of(out2) or {}
        profs = p.get("profiles") if isinstance(p, dict) else None
        uid = profs[0].get("userId") if profs else None
        if uid:
            rep.add("self_id", "ok", mask(uid))
        else:
            rep.add("self_id", "warn", "已登录但 profile list 为空",
                    fix="dws profile list 确认组织；必要时 dws auth login 重选", ref="b")
    else:
        rep.add("auth", "fail", obj.get("message") or "未登录",
                fix=f"{rep.cli} auth login（无头环境加 --device）；"
                    "若登录一路到「授权成功」后报「您暂无 CLI 数据访问权限」，"
                    "是组织未开通 CLI 访问，找该组织主管理员，重试设备码不会变", ref="b")

    if cached and not rep.has_fail():
        pass  # env 里的缓存值由 check_env 校验


def check_scope(rep):
    """权限能力检查（仅飞书有 scope 概念）：本 skill 必需的权限是否齐备。

    只报事实，不自动补 —— 补权限属于扩权，必须用户显式同意（见 troubleshooting §B.3）。
    """
    if rep.platform != "feishu":
        return
    try:
        import reauth
    except Exception:
        return
    cur = reauth.granted_scopes()
    if not cur:
        return
    missing = [s for s in reauth.REQUIRED_SCOPES if s not in cur]
    need = set(reauth.REQUIRED_SCOPES)
    extra = sorted({s.split(":")[0] for s in cur} - {s.split(":")[0] for s in need})
    if missing:
        rep.add("scope", "warn",
                f"缺 {len(missing)} 项必需权限（{'、'.join(missing[:3])}"
                f"{'…' if len(missing) > 3 else ''}），相关功能会失败",
                fix="python3 scripts/reauth.py feishu --policy minimal --allow-add"
                    "（只补必需项，不碰其它业务域）", ref="b3")
    else:
        rep.add("scope", "ok",
                f"必需 {len(need)} 项齐备（共授予 {len(cur)} 项，另含 "
                f"{len(extra)} 个业务域，非本 skill 申请）")


def check_env(rep, env):
    if not os.path.exists(ENV_PATH):
        rep.add("env.json", "warn", "不存在（还没跑过 bootstrap）",
                fix="python3 scripts/bootstrap.py", ref="i")
        return
    try:
        json.load(open(ENV_PATH))
    except Exception as e:
        rep.add("env.json", "fail", f"解析失败: {e}",
                fix=f"mv {ENV_PATH} {ENV_PATH}.corrupt && python3 scripts/bootstrap.py", ref="i")
        return
    st = (env.get("platforms", {}).get(rep.platform) or {})
    rep.add("env.json", "ok", f"{len(env.get('targets', {}).get(rep.platform, {}))} 个别名")
    if st.get("self_id"):
        rep.add("cached self_id", "ok", mask(st.get("self_id")))
    elif not rep.has_fail():  # 已因未授权失败时不再叠加噪音
        rep.add("cached self_id", "warn", "未缓存（每次监听都要调 whoami）",
                fix="python3 scripts/bootstrap.py", ref="b")


def check_state(rep, repair=False):
    os.makedirs(STATE_DIR, exist_ok=True)
    probe = os.path.join(STATE_DIR, f".doctor_{os.getpid()}")
    try:
        with open(probe, "w") as f:
            f.write("{}")
        os.remove(probe)
        rep.add("state dir", "ok", STATE_DIR)
    except Exception as e:
        rep.add("state dir", "fail", f"不可写: {e}",
                fix=f"chmod -R u+rw {ENV_DIR}", ref="i")
        return
    files = [f for f in os.listdir(STATE_DIR)
             if f.startswith(rep.platform + "_") and f.endswith(".pos")]
    bad = []
    for f in files:
        p = os.path.join(STATE_DIR, f)
        try:
            d = json.load(open(p))
            if "last_id" not in d:
                bad.append(f)
        except Exception:
            bad.append(f)
    if bad:
        if repair:
            for f in bad:
                os.replace(os.path.join(STATE_DIR, f), os.path.join(STATE_DIR, f + ".bad"))
            rep.add("state files", "warn", f"已隔离 {len(bad)} 个损坏文件 → *.bad",
                    fix="重挂监听即可（会以最新消息为基线）", ref="e")
        else:
            rep.add("state files", "fail", f"{len(bad)} 个损坏: {', '.join(bad[:3])}",
                    fix="python3 scripts/doctor.py --repair-state", ref="e")
    else:
        rep.add("state files", "ok", f"{len(files)} 个水位文件正常")


def check_path(rep, chat_id="", user_id=""):
    target = chat_id or user_id
    if not target:
        rep.add("通路", "skip", "未给 --chat-id/--user-id",
                fix="加 --chat-id <目标> 可跑 3 秒真实自检", ref="k")
        return
    cfg = bs.PLATFORMS[rep.platform]
    script = os.path.join(HERE, cfg["listen_script"])
    argv = [sys.executable, script,
            "--chat-id" if chat_id else "--user-id", target,
            "--interval", "2", "--timeout", "3"]
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        rep.add("通路", "fail", "自检超时（>90s）",
                fix="检查网络/CLI 卡死；单独跑一次该 CLI 命令看耗时", ref="d")
        return
    if p.returncode in (0, 3):
        rep.add("通路", "ok", "3 秒内拉取正常" + ("（命中存量）" if p.returncode == 0 else "，无新消息"))
    else:
        err = (p.stderr or "").strip().splitlines()
        first = err[0][:160] if err else f"rc={p.returncode}"
        ref = "c" if "SCHEMA_MISMATCH" in (p.stderr or "") else "b"
        rep.add("通路", "fail", first, fix=f"python3 scripts/bootstrap.py --probe {rep.platform}", ref=ref)


def check_update(rep):
    if rep.platform == "feishu":
        rc, out, err = run([rep.cli, "update", "--check"], timeout=60)
    elif rep.platform == "dingtalk":
        rc, out, err = run([rep.cli, "upgrade", "--check"], timeout=60)
    else:
        rc, out, err = run(["npm", "view", "@wecom/cli", "version"], timeout=60)
    text = (out or err).strip().replace("\n", " ")
    if rc != 0 or not text:
        rep.add("update", "warn", f"查新版失败 rc={rc}", fix="网络问题，忽略即可", ref="a")
        return
    low = text.lower()
    if rep.platform == "wecom":
        rc2, cur, _ = run([rep.cli, "--version"], timeout=20)
        latest = text.split()[-1]
        installed = re.search(r"(\d+\.\d+\.\d+)", cur or "")
        installed = installed.group(1) if installed else "?"
        if installed == latest:
            rep.add("update", "ok", f"已是最新 {latest}")
        else:
            rep.add("update", "warn", f"本地 {installed} → 最新 {latest}",
                    fix="npm install -g @wecom/cli", ref="a")
    elif any(k in low for k in ("up to date", "latest", "已是最新", "no update", "最新版本")):
        rep.add("update", "ok", text[:80])
    elif any(k in low for k in ("available", "new version", "可升级", "发现新版本", "update available")):
        rep.add("update", "warn", text[:100],
                fix=f"{rep.cli} {'update' if rep.platform == 'feishu' else 'upgrade'}", ref="a")
    else:
        rep.add("update", "ok", text[:80])


# ---------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser(description="cyber-im-avatar 体检与自愈引导")
    ap.add_argument("platform", nargs="?", choices=["feishu", "wecom", "dingtalk"],
                    help="只查一个平台；省略=全查")
    ap.add_argument("--chat-id", default="", help="附带 3 秒通路自检（群/会话 ID）")
    ap.add_argument("--user-id", default="", help="附带 3 秒通路自检（私聊对象 ID）")
    ap.add_argument("--check-update", action="store_true", help="额外查各 CLI 是否有新版")
    ap.add_argument("--repair-state", action="store_true", help="隔离损坏的水位文件（不改其它数据）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    ap.add_argument("--show-ids", action="store_true", help="不脱敏显示 ID")
    args = ap.parse_args()

    env = bs.load_env()
    targets = [args.platform] if args.platform else ["feishu", "wecom", "dingtalk"]
    reps, explicit = [], bool(args.platform)

    for name in targets:
        cfg = bs.PLATFORMS[name]
        rep = Report(name, cfg["cli"])
        if not check_cli(rep):
            rep.items[-1]["status"] = "fail"
            reps.append(rep)
            if not args.json:
                emit(rep, args.show_ids)
            continue
        check_cli_doctor(rep)
        check_auth(rep, env)
        check_scope(rep)
        check_env(rep, env)
        check_state(rep, args.repair_state)
        check_path(rep, args.chat_id, args.user_id)
        if args.check_update:
            check_update(rep)
        reps.append(rep)
        if not args.json:
            emit(rep, args.show_ids)

    fails = [(r.platform, i) for r in reps for i in r.items if i["status"] == "fail"]
    warns = [(r.platform, i) for r in reps for i in r.items if i["status"] == "warn"]
    healthy = [r.platform for r in reps if not r.has_fail()]
    broken = [r.platform for r in reps if r.has_fail()]
    # 退出码语义 = 「现在能不能用」：
    #   指定平台 → 该平台必须全绿；全量体检 → 只要有一个平台可用就不阻塞
    blocking = bool(args.platform and broken) or (not healthy)
    if args.json:
        print(json.dumps({
            "ok": not blocking,
            "platforms": {r.platform: {"status": r.worst(), "checks": r.items} for r in reps},
            "summary": {"fail": len(fails), "warn": len(warns),
                        "healthy": healthy, "broken": broken},
        }, ensure_ascii=False, indent=2))
    else:
        print("\n== 结论 ==")
        if args.platform:
            if not broken:
                print(f"  [ok] {reps[0].platform} 可用"
                      + (f"；{len(warns)} 项提醒不影响使用" if warns else ""))
            else:
                print(f"  [fail] {reps[0].platform} 有 {len(fails)} 项阻塞：")
                for _plat, it in fails:
                    print(f"    - {it['check']}: {it['detail'][:100]}")
                    if it["fix"]:
                        print(f"      修复: {it['fix']}")
                    if it["ref"]:
                        print(f"      手册: {TS}#{it['ref']}")
        else:
            if healthy:
                print(f"  [ok] 可用平台: {', '.join(healthy)}")
            if broken:
                lvl = "[warn]" if healthy else "[fail]"
                print(f"  {lvl} 不可用平台: {', '.join(broken)}"
                      + ("（不影响上面可用的平台）" if healthy else ""))
                for plat, it in fails:
                    print(f"    - {plat}/{it['check']}: {it['detail'][:100]}")
                    if it["fix"]:
                        print(f"      修复: {it['fix']}")
                    if it["ref"]:
                        print(f"      手册: {TS}#{it['ref']}")
            if warns:
                print(f"  [warn] {len(warns)} 项提醒（不阻塞）")
        print(f"\n  分诊表: {TS}#triage    回归清单: {TS}#k")
        if broken:
            print("  提示: 任何一项 fail 都不要在该平台上挂监听——会静默失效（能拉取但永不命中）。")

    sys.exit(2 if blocking else 0)


if __name__ == "__main__":
    main()
