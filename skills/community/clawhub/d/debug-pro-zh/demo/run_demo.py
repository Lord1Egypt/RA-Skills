#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debug-pro 一键自证：python demo/run_demo.py

四步，全部用本机真实执行出结论，不是描述：
  1. 分诊真日志
  2. 检查合格复现步骤 → 应 PASS
  3. 检查残缺复现步骤 → 应 FAIL 并指名缺项
  4. 环境快照 → 必须不泄漏密钥
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
import debughunt  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main():
    log_path = os.path.join(HERE, "sample_error.txt")
    print("=== 1) 分诊 ===")
    d = debughunt.triage(debughunt.read_text(log_path))
    print("异常类型 :", "、".join(d["exception_types"]) or "未提及")
    print("栈首帧   :", d["last_frame"])
    print("退出码   :", d["exit_codes"])
    print("HTTP     :", d["http_status"])
    print("时间戳   :", d["timestamps"])
    ok1 = ("json.decoder.JSONDecodeError" in d["exception_types"]
           and d["last_frame"] and d["last_frame"]["line"] == 346)
    print("结论     : %s" % ("PASS 关键要素齐全，可据此复现" if ok1 else "FAIL 抽取不全"))

    print("\n=== 2) 合格复现步骤 ===")
    good = debughunt.read_text(os.path.join(HERE, "repro_steps.md"))
    r1 = debughunt.reprocheck(good)
    print("verdict=%s missing=%s steps=%d" % (r1["verdict"], r1["missing"], r1["steps_detected"]))
    print("结论     : %s" % ("PASS 五要素齐全" if r1["verdict"] == "PASS" else "FAIL " + str(r1["missing"])))

    print("\n=== 3) 残缺复现步骤（故意删掉环境与期望） ===")
    bad = "复现步骤：\n1. 运行 python app.py\n2. 输入空文件\n3. 证据：截图一张"
    r2 = debughunt.reprocheck(bad)
    print("verdict=%s missing=%s" % (r2["verdict"], r2["missing"]))
    ok3 = r2["verdict"] == "FAIL" and "版本环境" in r2["missing"] and "期望与实际" in r2["missing"]
    print("结论     : %s" % ("PASS 准确抓出缺项" if ok3 else "FAIL 漏判"))

    print("\n=== 4) 环境快照脱敏 ===")
    os.environ["DEMO_FAKE_API_TOKEN"] = "tk-DEMO-SHOULD-NOT-APPEAR"
    e = debughunt.envsnap()
    leak = any("DEMO-SHOULD-NOT-APPEAR" in str(v) for v in e.values()) or any(
        "DEMO-SHOULD-NOT-APPEAR" in str(v) for v in e["env_whitelist"].values())
    print("已排除疑似密钥项 :", e["redacted_keys_count"])
    print("结论     : %s" % ("FAIL 有密钥泄漏" if leak else "PASS 零泄漏（含 KEY/TOKEN/SECRET 的项全部剔除）"))

    all_ok = ok1 and r1["verdict"] == "PASS" and ok3 and not leak
    print("\n=== 汇总：%s ===" % ("全 PASS" if all_ok else "存在 FAIL"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
