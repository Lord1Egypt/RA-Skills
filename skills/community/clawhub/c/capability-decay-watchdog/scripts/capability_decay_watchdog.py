#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""capability-decay-watchdog —— 能力退化预警与自愈

监测技能生态的运行时健康：扫描各技能的 learned_patterns.json，检测
  - 成功率滑落（totalOps 足够后 success_rate 跌破阈值）
  - 陈旧停滞（长期无任何操作 -> 可能已失效/被遗忘）
对退化技能输出告警 + 推荐自愈动作（重注入 learner / 标 repair 缺口 / 重跑回归），
让元进化引擎能"在能力悄悄变弱前"主动干预——一线大模型完全不具备的元治理能力。

纯标准库；`python capability_decay_watchdog.py --selftest` 跑内置断言（喂模拟 pattern 文件）。
"""
import argparse
import json
import os
import sys
import time


# 默认阈值
SUCCESS_FLOOR = 0.7      # 成功率低于此值即告警
MIN_OPS = 5              # 至少这么多操作才统计成功率（避免早期噪声）
STALE_DAYS = 30          # 超过此天数无操作即陈旧


def success_rate(data):
    ops = data.get("totalOps", 0)
    fails = data.get("totalErrors", data.get("total_fails", 0))
    if ops == 0:
        return None
    return (ops - fails) / ops


def last_op_age_days(data):
    lu = data.get("lastUpdated", "")
    if not lu:
        return None
    try:
        # 兼容 "2026-07-23T09:18" 与 iso
        fmt = "%Y-%m-%dT%H:%M" if "T" in lu else "%Y-%m-%d %H:%M:%S"
        ts = time.mktime(time.strptime(lu, fmt))
        return (time.time() - ts) / 86400
    except Exception:
        return None


def check_skill(skill_dir, now=None):
    """检查单个技能目录，返回告警列表（空=健康）。"""
    now = now or time.time()
    lp = os.path.join(skill_dir, "learned_patterns.json")
    if not os.path.isfile(lp):
        return [{"level": "info", "reason": "no_learner", "action": "inject_learner"}]
    try:
        data = json.load(open(lp, encoding="utf-8"))
    except Exception:
        return [{"level": "warn", "reason": "corrupt_pattern", "action": "repair"}]
    alerts = []
    sr = success_rate(data)
    if sr is not None and data.get("totalOps", 0) >= MIN_OPS and sr < SUCCESS_FLOOR:
        alerts.append({
            "level": "critical",
            "reason": "success_rate_drop",
            "success_rate": round(sr, 3),
            "action": "repair_or_reinject",
        })
    age = last_op_age_days(data)
    if age is not None and age > STALE_DAYS:
        alerts.append({
            "level": "warn",
            "reason": "stale",
            "age_days": round(age, 1),
            "action": "rerun_regression",
        })
    return alerts


def watch(skills_root, now=None):
    """扫描生态，返回 {decayed:[...], healthy:n, alerts_summary}。"""
    now = now or time.time()
    decayed = []
    healthy = 0
    for name in sorted(os.listdir(skills_root)):
        sd = os.path.join(skills_root, name)
        if not os.path.isdir(sd) or name.startswith("_"):
            continue
        if not os.path.isfile(os.path.join(sd, "learned_patterns.json")):
            continue
        alerts = check_skill(sd, now=now)
        if alerts:
            decayed.append({"skill": name, "alerts": alerts})
        else:
            healthy += 1
    return {
        "root": skills_root,
        "decayed": decayed,
        "healthy": healthy,
        "decayed_count": len(decayed),
    }


def selftest():
    print("== capability-decay-watchdog selftest ==")
    import tempfile, shutil
    tmp = tempfile.mkdtemp(prefix="decay_")
    try:
        # 健康技能：高成功率 + 近期操作
        healthy = {
            "totalOps": 20, "totalErrors": 1,
            "lastUpdated": time.strftime("%Y-%m-%dT%H:%M", time.localtime(time.time() - 1 * 86400)),
        }
        # 退化技能：成功率跌破阈值
        decayed = {
            "totalOps": 12, "totalErrors": 8,
            "lastUpdated": time.strftime("%Y-%m-%dT%H:%M", time.localtime(time.time() - 2 * 86400)),
        }
        # 陈旧技能：长期无操作
        stale = {
            "totalOps": 30, "totalErrors": 2,
            "lastUpdated": time.strftime("%Y-%m-%dT%H:%M", time.localtime(time.time() - 60 * 86400)),
        }
        for n, d in (("healthy_skill", healthy), ("decayed_skill", decayed), ("stale_skill", stale)):
            sd = os.path.join(tmp, n)
            os.makedirs(sd)
            json.dump(d, open(os.path.join(sd, "learned_patterns.json"), "w"), ensure_ascii=False)

        rep = watch(tmp, now=time.time())
        by_name = {x["skill"]: x for x in rep["decayed"]}
        assert "healthy_skill" not in by_name, by_name
        assert "decayed_skill" in by_name, by_name
        assert "stale_skill" in by_name, by_name
        assert any(a["reason"] == "success_rate_drop" for a in by_name["decayed_skill"]["alerts"])
        assert any(a["reason"] == "stale" for a in by_name["stale_skill"]["alerts"])
        print(f"  [1] 健康技能无误报 / 退化+陈旧技能均告警  PASS (decayed={rep['decayed_count']})")
        print(f"  [2] 退化技能 action={by_name['decayed_skill']['alerts'][0]['action']}  PASS")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="能力退化预警与自愈")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=os.path.expanduser("~/.workbuddy/skills"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    rep = watch(args.root)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"能力退化监测（{args.root}）：健康 {rep['healthy']} ｜ 退化/陈旧 {rep['decayed_count']}")
        for d in rep["decayed"]:
            print(f"  ⚠ {d['skill']}: " + ", ".join(a["reason"] for a in d["alerts"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
