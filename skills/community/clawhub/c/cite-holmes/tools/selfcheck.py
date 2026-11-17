#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cite-holmes 随包自检（v6.1.0 F52；v6.5.0 F57 扩展）——安装完整性验证，一条命令：

    python3 tools/selfcheck.py            # 标准自检（零外呼，offline 口径）
    python3 tools/selfcheck.py --mcp      # 加测 mcp/ 嵌入式副本独立加载+CLI
    python3 tools/selfcheck.py --tests    # 加测随包 sealed 测试子集（F57：
                                          #   run_tests.sh --shipped，清单 tests/shipped_manifest.json）

验证四件事：①引擎可导入（壳+七层模块化布局完整）②核心判定 API 在位
（五态判定/导出/审计包）③内置金标集 offline 全流程真跑且伪造全数落网
（capture 100% 判据——与 docs/benchmark.md 同口径）④GB/T 导出通路冒烟。
退出码 0=自检通过；1=任一失败（agent 宿主可当安装验证钩子）。

与 tests/ 的分工（ADR-0011 修订 ADR-0010 边界）：随包 sealed 子集
（tests/shipped_manifest.json 清单）随包分发可复验；全量回归矩阵仍为
开发侧。本脚本是用户/宿主侧安装验证（随包、真跑、无测试框架依赖）。"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(HERE)
ENGINE = os.path.join(SK, "scripts", "verify_refs.py")

PASS, FAIL = [], []


def check(name, fn):
    try:
        fn()
        PASS.append(name)
        print(f"  ✅ {name}")
    except Exception as e:
        FAIL.append(f"{name}: {type(e).__name__}: {e}")
        print(f"  ❌ {name} — {type(e).__name__}: {e}")


def t_engine_import():
    sys.path.insert(0, os.path.join(SK, "scripts"))
    import verify_refs as vr  # noqa: F401
    assert vr.VERSION, "VERSION 缺失"
    for layer in ("ch_text", "ch_netio", "ch_registry", "ch_semantic",
                  "ch_verify", "ch_reports", "ch_cli"):
        assert hasattr(vr, layer), f"模块层 {layer} 缺失（安装不完整？）"


def t_core_api():
    sys.path.insert(0, os.path.join(SK, "scripts"))
    import verify_refs as vr
    for name in ("verify_one", "check_url", "doi_metadata_match",
                 "render_md", "render_audit_report", "build_submission_index",
                 "submission_readiness", "export_gbt7714", "main",
                 "main_with_args"):
        assert callable(getattr(vr, name)), f"{name} 不存在/不可调用"
    for v in ("verified", "partial", "unreachable", "unverified", "invalid"):
        assert v in vr.VERDICT_ZH, f"五态 {v} 不在判定表"


def t_golden_capture():
    # 内置金标集 offline 全流程真跑：3 处预埋伪造必须全部非 verified
    # （capture 100%，docs/benchmark.md 同口径；offline 对良构伪造诚实降
    # partial——只断言「非 verified」，不要求 invalid）
    demo = os.path.join(SK, "examples", "demo_refs.json")
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "selfcheck_report.md")
        rc = subprocess.run([sys.executable, ENGINE, "--refs", demo,
                             "--offline", "--out", out],
                            capture_output=True, text=True, timeout=180)
        assert rc.returncode in (0, 1), f"引擎退出码异常: {rc.returncode}"
        doc = json.load(open(out.rsplit(".", 1)[0] + ".json", encoding="utf-8"))
        results = doc["results"]
        assert len(results) == 8, f"金标集应 8 条，实得 {len(results)}"
        planted = (6, 7, 8)
        for r in results:
            if r["index"] in planted:
                assert r["verdict"] != "verified", \
                    f"伪造 #{r['index']} 判 verified（判定可信度受损）"
        clean_killed = [r["index"] for r in results
                        if r["index"] not in planted
                        and r["verdict"] == "invalid"]
        assert not clean_killed, f"干净条目误杀: {clean_killed}"


def t_gbt_export_smoke():
    sys.path.insert(0, os.path.join(SK, "scripts"))
    import verify_refs as vr
    demo = os.path.join(SK, "examples", "demo_refs.json")
    refs = json.load(open(demo, encoding="utf-8"))
    refs = refs["refs"] if isinstance(refs, dict) else refs
    results = [{"index": i + 1, "verdict": "partial" if r.get("doi") else "unverified",
                "title": r.get("title", ""), "doi": r.get("doi") or "",
                "url": r.get("url") or "", "note": "", "checks": {}}
               for i, r in enumerate(refs)]
    n = vr.export_gbt7714(results, os.path.join(tempfile.gettempdir(),
                                                "cite_selfcheck_gbt.txt"))
    assert isinstance(n, int), "GB/T 导出返回非计数"


def t_mcp_standalone():
    mcp_engine = os.path.join(SK, "mcp", "verify_refs.py")
    assert os.path.isfile(mcp_engine), "mcp/verify_refs.py 缺失"
    with tempfile.TemporaryDirectory() as td:
        rc = subprocess.run([sys.executable, mcp_engine, "--demo", "--offline",
                             "--out", os.path.join(td, "mcp_probe.md")],
                            capture_output=True, text=True, timeout=180)
        assert rc.returncode in (0, 1), f"mcp 副本 CLI rc={rc.returncode}"


def t_shipped_tests():
    # F57：随包 sealed 子集真跑（清单缺文件=部分拷贝损坏，直接 FAIL）
    rt = os.path.join(SK, "tools", "run_tests.sh")
    assert os.path.isfile(rt), "tools/run_tests.sh 缺失"
    rc = subprocess.run(["bash", rt, "--shipped"],
                        capture_output=True, text=True, timeout=600)
    assert rc.returncode == 0, \
        f"随包子集 rc={rc.returncode}\n{rc.stdout[-600:]}{rc.stderr[-200:]}"
    assert "RESULT: PASS" in rc.stdout, rc.stdout[-300:]


def main():
    ap = argparse.ArgumentParser(description="cite-holmes 安装自检（随包）")
    ap.add_argument("--mcp", action="store_true",
                    help="加测 mcp/ 嵌入式副本独立加载与 CLI（uvx/子目录分发形态）")
    ap.add_argument("--tests", action="store_true",
                    help="加测随包 sealed 测试子集（F57；run_tests.sh --shipped）")
    args = ap.parse_args()
    print(f"cite-holmes 自检（v? 引擎版本见下）——{SK}")
    check("引擎导入（壳+七层布局）", t_engine_import)
    check("核心判定 API 在位", t_core_api)
    sys.path.insert(0, os.path.join(SK, "scripts"))
    import verify_refs as vr
    print(f"  引擎版本：{vr.VERSION}")
    check("金标集 offline 真跑（伪造全落网+零误杀）", t_golden_capture)
    check("GB/T 导出通路冒烟", t_gbt_export_smoke)
    if args.mcp:
        check("mcp 副本独立加载+CLI", t_mcp_standalone)
    if args.tests:
        check("随包 sealed 测试子集（F57）", t_shipped_tests)
    print(f"\n汇总: {len(PASS)} PASS / {len(FAIL)} FAIL")
    if FAIL:
        for f in FAIL:
            print(f"  FAIL: {f}")
        return 1
    print("自检通过——安装完整，判定通路可用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
