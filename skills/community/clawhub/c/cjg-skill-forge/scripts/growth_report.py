#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能成长报告（本地可见化"越用越牛"）。

读本机 signals-log.jsonl，输出用户自身用法的轻量成长摘要：
  - 时间窗（默认 30 天）内信号条数
  - 覆盖的方法层（L1–L7）数
  - 建设性事件占比（helpful / suggestion vs 其余）
  - 熟练度等级 Lv.1–5（覆盖层数 + 信号总数 + 连续使用天数）

仅陈述用户自身行为，不谎称"已自动优化"（那属创作者侧云端动作）。
--with-cloud 钩子预留（默认不调，待 Wave B 聚合后端就绪后接入互惠回执）。
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.dirname(HERE)
LAYER_KEYS = ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]
POSITIVE = ("helpful", "suggestion")
NEGATIVE = ("unhelpful", "confusion", "misdiagnosis", "abandoned")


def _read_lines(dir_):
    path = os.path.join(dir_, "signals-log.jsonl")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
    except Exception:
        return []


def _parse_ts(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s)
        # 本地信号 ts 常无时区（naive）；与 aware 的 now 比较前统一视为 UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def cmd_report(dir_, days=30, with_cloud=False):
    lines = _read_lines(dir_)
    if not lines:
        print("[growth] 本机暂无信号记录。用一阵子后，说\"我的技能成长\"就能看到你的用法沉淀。")
        # --with-cloud：云端 L3/L4 补全独立于本地日志展示（社区杠杆不因本机空数据而消失）
        if with_cloud:
            _print_cloud_extras(dir_, [])
        return
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    recent = [l for l in lines if (_parse_ts(l.get("ts")) or now) >= cutoff]
    if not recent:
        print(f"[growth] 最近 {days} 天没有新信号（历史共 {len(lines)} 条）。")
        return
    layers = {l.get("method_layer") for l in recent if l.get("method_layer")}
    positive = sum(1 for l in recent if l.get("event") in POSITIVE)
    negative = sum(1 for l in recent if l.get("event") in NEGATIVE)
    days_used = {
        (_parse_ts(l.get("ts")).date().isoformat() if _parse_ts(l.get("ts")) else "?")
        for l in recent
    }
    cov = len(layers & set(LAYER_KEYS))
    total = len(recent)
    distinct_days = len(days_used - {"?"})
    score = cov * 3 + min(total, 50) // 10 + min(distinct_days, 14) // 3
    lv = max(1, min(5, score // 6 + 1))
    print(f"[growth] 过去 {days} 天，你为本技能贡献了 {total} 条方法层反馈，")
    print(f"         覆盖了 {cov} 个能力层（L1–L7），熟练度 Lv.{lv}。")
    if positive or negative:
        ratio = positive / (positive + negative) * 100 if (positive + negative) else 0
        tone = "建设性为主" if ratio >= 50 else "探索为主"
        print(f"         其中建设性反馈占 {ratio:.0f}%（采纳/建议 vs 纠正/卡住/误判/放弃）——你的用法以{tone}。")
    print("         这些线索让本技能更懂你的用法（本地记录，零原文零身份）。")
    _print_loop_metrics(recent)
    if with_cloud:
        _print_cloud_extras(dir_, recent)


def _cloud_base(dir_):
    """聚合端点外部化（环境变量 → cloud_config.json → secrets），零硬编码。"""
    env = os.environ.get("CJG_AGGREGATE_URL")
    if env:
        return env.strip().rstrip("/")
    for cand in (os.path.join(dir_, "cloud_config.json"),
                 os.path.expanduser("~/.workbuddy/secrets/cjg-evo/cloud_config.json")):
        if os.path.exists(cand):
            try:
                with open(cand, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                u = (cfg.get("aggregate_url") or "").strip()
                if u:
                    return u.rstrip("/")
            except Exception:
                pass
    return None


def _cloud_get(url, timeout=10):
    import urllib.request
    import urllib.error
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _print_cloud_extras(dir_, recent):
    """L3/L4 云端补全（需已开启云同步）：同类发现卡 + 互惠回执。默认不调云端。"""
    optin = None
    try:
        with open(os.path.join(dir_, ".cloud_optin"), encoding="utf-8") as f:
            optin = f.read().strip()
    except Exception:
        pass
    if optin != "on":
        print("[growth] （--with-cloud 需已开启云同步：说\"开启云同步\"后本报告才能带同类用法与本周改进）")
        return
    base = _cloud_base(dir_)
    if not base:
        print("[growth] （未配置聚合端点 aggregate_url，跳过云端补全）")
        return
    slug = "cjg-skill-forge"
    anon = None
    try:
        with open(os.path.join(dir_, ".anon_id"), encoding="utf-8") as f:
            anon = f.read().strip()
    except Exception:
        pass
    # L4 互惠回执
    impr = _cloud_get(f"{base}/aggregate/improvements_last_week?slug={slug}")
    if impr and impr.get("ok"):
        n = impr.get("improved_count", 0)
        hs = impr.get("highlights") or []
        print(f"         本周因用户反馈，技能改进了 {n} 处" + (f"（{hs[0] if hs else '—'} 等）" if n else "（暂无）"))
    else:
        print("[growth] （本周改进数据暂不可用，稍后再试）")
    # L3 同类发现卡：对已覆盖层查社区使用率，提示未用的层
    used_layers = {l.get("method_layer") for l in recent if l.get("method_layer")}
    got = False
    for layer in sorted(used_layers):
        pb = _cloud_get(f"{base}/aggregate/peer_benchmark?slug={slug}&method_layer={layer}")
        if pb and pb.get("ok") and pb.get("community_used_pct") is not None:
            got = True
            print(f"         社区里 {pb['community_used_pct']:.0f}% 的人用过 L{layer[1:]}（样本 {pb.get('sample_size')}）——"
                  f"{'你也在用' if layer in used_layers else '你还没用过，可试'}")
    if not got:
        print("[growth] （社区同类数据样本不足，暂不展示——样本≥30 后自动出现）")
    if anon:
        # L2 同步入口提示（不自动拉取，避免意外改写本地日志）
        print("[growth] 提示：说\"同步我的信号\"可把云端历史合并回这台电脑（download_signals.py pull）")


def loop_metrics(recent):
    """P1 三指标（loop 级，N2）计算：采纳率 / 平均修订轮数 / 重复反馈率。
    数据不足返回 None（显示"数据不足"而非 0%——T-CLI-03 / U1 语义）。"""
    m = {}
    closed = [l for l in recent if l.get("accepted") is not None]
    if closed:
        adopted = sum(1 for l in closed if l["accepted"] in (1, True, "1", "true"))
        m["adopt_rate"] = (adopted, len(closed))
    rounds = [l["revision_rounds"] for l in recent
              if isinstance(l.get("revision_rounds"), (int, float))
              and not isinstance(l.get("revision_rounds"), bool)]
    if rounds:
        m["avg_rounds"] = (round(sum(rounds) / len(rounds) * 10) / 10, len(rounds))
    rec = [l for l in recent if l.get("recurrence") is not None]
    if rec:
        repeat = sum(1 for l in rec if l["recurrence"] in (1, True, "1", "true"))
        m["recur_rate"] = (round(repeat / len(rec) * 100), repeat, len(rec))
    return m


def _print_loop_metrics(recent):
    m = loop_metrics(recent)
    if not m:
        return
    print("         闭环质量（P0 · 采纳/轮次/复发）：")
    if "adopt_rate" in m:
        a, n = m["adopt_rate"]
        print(f"           · 采纳率 {a / n * 100:.0f}%（{a}/{n} 次采纳判断）")
    else:
        print("           · 采纳率 数据不足（尚无采纳/驳回记录）")
    if "avg_rounds" in m:
        avg, n = m["avg_rounds"]
        print(f"           · 平均修订轮数 {avg:.1f} 轮（{n} 次修订）")
    else:
        print("           · 平均修订轮数 数据不足（尚无迭代记录）")
    if "recur_rate" in m:
        pct, r, n = m["recur_rate"]
        print(f"           · 重复反馈率 {pct}%（{r}/{n} 次标记复发）")
    else:
        print("           · 重复反馈率 数据不足（尚无复发标记）")


def main():
    args = sys.argv[1:]
    dir_ = DEFAULT_DIR
    with_cloud = "--with-cloud" in args
    rest = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--dir":
            if i + 1 < len(args):
                dir_ = args[i + 1]
            i += 2
        else:
            rest.append(a)
            i += 1
    days = 30
    if "--days" in rest:
        try:
            days = int(rest[rest.index("--days") + 1])
        except Exception:
            pass
    if not rest or rest[0] in ("report", "growth"):
        cmd_report(dir_, days=days, with_cloud=with_cloud)
    else:
        print(__doc__)
        print("用法：python growth_report.py [report] [--days 30] [--with-cloud] [--dir <技能目录>]")


if __name__ == "__main__":
    main()
