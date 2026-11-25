#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debug-pro 黄金集跑分器：python tests/run_golden.py [--id D01]

任何人在任何机器上都能复跑；输出 PASS/FAIL 计数，退出码非 0 即不合格。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import debughunt  # noqa: E402


def check_triage(case):
    try:
        d = debughunt.triage(case["input"])
    except SystemExit:
        if case["expect"].get("expect_error") == "D004":
            return "PASS: 正确拒答为 D004"
        return "FAIL: 意外拒答"
    e = case["expect"]
    for t in e.get("exception_types_contain", []):
        if t not in d["exception_types"]:
            return "FAIL: 未抽到异常类型 %s（得到 %s）" % (t, d["exception_types"])
    if "last_frame_file_contain" in e:
        lf = d["last_frame"]
        if not lf or e["last_frame_file_contain"] not in lf["file"]:
            return "FAIL: 栈首帧不符（%s）" % lf
    if "last_frame_line" in e and (not d["last_frame"] or d["last_frame"]["line"] != e["last_frame_line"]):
        return "FAIL: 栈首帧行号不符"
    if e.get("frames_min") and len(d["frames"]) < e["frames_min"]:
        return "FAIL: 帧数 %d < %d" % (len(d["frames"]), e["frames_min"])
    for c in e.get("exit_codes_contain", []):
        if c not in d["exit_codes"]:
            return "FAIL: 未抽到退出码 %s（得到 %s）" % (c, d["exit_codes"])
    for c in e.get("http_status_contain", []):
        if c not in d["http_status"]:
            return "FAIL: 未抽到 HTTP 状态 %s（得到 %s）" % (c, d["http_status"])
    if e.get("timestamps_min") and len(d["timestamps"]) < e["timestamps_min"]:
        return "FAIL: 时间戳 %d < %d" % (len(d["timestamps"]), e["timestamps_min"])
    return "PASS"


def check_repro(case):
    d = debughunt.reprocheck(case["input"])
    e = case["expect"]
    if d["verdict"] != e["verdict"]:
        return "FAIL: verdict=%s 期望 %s" % (d["verdict"], e["verdict"])
    for m in e.get("missing_contain", []):
        if m not in d["missing"]:
            return "FAIL: 缺项未含 %s（得到 %s）" % (m, d["missing"])
    if e.get("steps_min") and d["steps_detected"] < e["steps_min"]:
        return "FAIL: 步骤数 %d < %d" % (d["steps_detected"], e["steps_min"])
    return "PASS"


def check_envsnap(case):
    os.environ["GP_FAKE_SECRET_TOKEN"] = "REDACTED-SECRET"
    d = debughunt.envsnap()
    blob = json.dumps(d, ensure_ascii=False).lower()
    e = case["expect"]
    if e.get("no_secret_leak") and ("do-not-leak" in blob or "gp_fake_secret" in blob):
        return "FAIL: 密钥泄漏到环境块"
    if e.get("redacted_min") and d["redacted_keys_count"] < e["redacted_min"]:
        return "FAIL: 脱敏计数 %d < %d" % (d["redacted_keys_count"], e["redacted_min"])
    return "PASS"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    only = None
    if "--id" in sys.argv:
        only = sys.argv[sys.argv.index("--id") + 1]
    cases = json.load(open(os.path.join(HERE, "golden.json"), encoding="utf-8"))["cases"]
    npass = 0
    for c in cases:
        if only and c["id"] != only:
            continue
        fn = {"triage": check_triage, "reprocheck": check_repro, "envsnap": check_envsnap}[c["kind"]]
        r = fn(c)
        npass += r.startswith("PASS")
        print("%-22s %s" % (c["id"], r))
    total = 1 if only else len(cases)
    print("--- %d/%d PASS" % (npass, total))
    sys.exit(0 if npass == total else 1)


if __name__ == "__main__":
    main()
