#!/usr/bin/env python3
"""AI App Test Runner — Orchestrator for all test levels"""

import json, sys, os, time, argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LEVELS = {
    "l0":    {"module":"llm_core_tester",       "class":"LLMCoreTester",      "desc":"LLM核心功能"},
    "l1":    {"module":"prompt_tester",          "class":"PromptTester",       "desc":"Prompt测试"},
    "l1-sec":{"module":"prompt_security_auditor","class":"PromptSecurityAuditor","desc":"Prompt安全审计"},
    "l2":    {"module":"verify_tool_call",       "class":"ToolCallVerifier",   "desc":"工具调用验证"},
    "l2-sch":{"module":"schema_checker",         "class":"SchemaChecker",      "desc":"Schema校验"},
    "l25":   {"module":"mcp_tester",             "class":"MCPTester",          "desc":"MCP审计"},
    "l3":    {"module":"trace_analyzer",         "class":"TraceAnalyzer",      "desc":"Trace分析"},
    "l4":    {"module":"e2e_session_tester",     "class":"E2ESessionTester",   "desc":"端到端会话"},
    "rag":   {"module":"rag_tester",             "class":"RAGTester",          "desc":"RAG准确性"},
    "judge": {"module":"auto_judge",             "class":"AutoJudge",          "desc":"自动评分"},
    "stress":{"module":"stress_tester",          "class":"StressTester",       "desc":"压力测试"},
    "reg":   {"module":"regression_compare",     "class":"RegressionComparator","desc":"回归对比"},
    "gen":   {"module":"test_case_generator",     "fn":"generate_all",         "desc":"测试用例生成"},
}

def import_level(level_key: str):
    info = LEVELS[level_key]
    mod = __import__(info["module"])
    if "class" in info:
        cls = getattr(mod, info["class"])
        return cls, info
    return None, info

def run_level(level_key: str, endpoint: str, model: str, report_dir: str) -> dict:
    info = LEVELS[level_key]
    print(f"\n{'='*60}")
    print(f"  [{level_key}] {info['desc']}")
    print(f"{'='*60}")

    t0 = time.time()

    if level_key == "gen":
        from test_case_generator import generate_all
        counts = generate_all(f"{report_dir}/../test_cases")
        result = {"status":"PASS","counts":counts}
    elif level_key == "reg":
        from regression_compare import RegressionComparator, SAMPLE_BASELINE, SAMPLE_CURRENT
        comp = RegressionComparator()
        result = comp.compare(SAMPLE_BASELINE, SAMPLE_CURRENT)
        from regression_compare import generate_report as gen_reg
        rep = gen_reg(result)
        print(rep)
    elif level_key == "stress":
        from stress_tester import StressTester
        tester = StressTester(f"{endpoint}/v1/chat/completions", model)
        result = tester.run_multi_profile(["light"])
        from stress_tester import generate_report as gen_str
        rep = gen_str(result)
        print(rep)
    elif level_key == "l2-sch":
        from schema_checker import SchemaChecker, generate_report as gen_sch
        checker = SchemaChecker()
        stats = checker.run_all()
        rep = gen_sch(stats)
        print(rep)
        result = stats
    elif level_key == "l3":
        from trace_analyzer import TraceAnalyzer, generate_report as gen_tr
        analyzer = TraceAnalyzer()
        results = analyzer.analyze_all()
        rep = gen_tr(results)
        print(rep)
        result = {"total":len(results),"passed":sum(1 for _,r in results if r["passed"])}
    elif level_key == "l4":
        from e2e_session_tester import E2ESessionTester, generate_report as gen_e2e
        tester = E2ESessionTester()
        result = tester.dry_run()
        rep = gen_e2e(result)
        print(rep)
    elif level_key == "judge":
        from auto_judge import AutoJudge, generate_report as gen_jg
        judge = AutoJudge(endpoint)
        result = judge.run_suite()
        rep = gen_jg(result)
        print(rep)
    else:
        # Levels that need endpoint
        cls, _ = import_level(level_key)
        ep = f"{endpoint}/v1/chat/completions" if endpoint else "http://localhost:8080/v1/chat/completions"
        instance = cls(ep, model) if level_key in ("l0","l1","l1-sec","l2","l25","rag") else cls()
        result = instance.run_suite() if hasattr(instance,"run_suite") else instance.audit()
        # Print result
        print(f"  通过: {result.get('passed',0)}/{result.get('total',0)} = "
              f"{round(result.get('passed',0)/max(result.get('total',1),1)*100,1)}%")
        if "by_dimension" in result:
            for d,v in result["by_dimension"].items():
                print(f"    {d}: {v['passed']}/{v['total']}")

    elapsed = round(time.time()-t0, 2)
    print(f"  ⏱ {elapsed}s")
    return {"level":level_key,"desc":info["desc"],"elapsed":elapsed,"result":result}

def main():
    parser = argparse.ArgumentParser(description="AI App Test Runner")
    parser.add_argument("--endpoint", default="http://localhost:8080",
                       help="LLM API endpoint base URL")
    parser.add_argument("--model", default="deepseek/deepseek-v4-flash",
                       help="Model name")
    parser.add_argument("--levels", nargs="+", default=list(LEVELS.keys()),
                       choices=list(LEVELS.keys())+["all"],
                       help="Test levels to run")
    parser.add_argument("--report-dir", default="reports",
                       help="Report output directory")
    parser.add_argument("--skip-online", action="store_true",
                       help="Skip online-dependent tests")
    args = parser.parse_args()

    os.makedirs(args.report_dir, exist_ok=True)
    levels = [l for l in LEVELS if l in args.levels or "all" in args.levels]

    skip_online = {"l0","l1","l1-sec","l2","l25","rag","stress","judge"}
    if args.skip_online:
        levels = [l for l in levels if l not in skip_online]

    print(f"AI App Test Runner — {datetime.now().isoformat()}")
    print(f"Endpoint: {args.endpoint} | Model: {args.model}")
    print(f"Levels: {levels}")

    results = []
    for lv in levels:
        r = run_level(lv, args.endpoint, args.model, args.report_dir)
        results.append(r)

    # Summary
    print(f"\n{'='*60}")
    print("  汇总")
    print(f"{'='*60}")
    total_passed = 0
    total_all = 0
    for r in results:
        res = r.get("result",{})
        p = res.get("passed",0) if isinstance(res.get("passed"),(int,float)) else None
        t = res.get("total",0) if isinstance(res.get("total"),(int,float)) else None
        if p is not None and t:
            total_passed += p; total_all += t
        status = "✅" if (p is None or (t and p>=t)) else "❌"
        print(f"  {status} [{r['level']}] {r['desc']}: {r['elapsed']}s")
    if total_all > 0:
        print(f"\n  总计: {total_passed}/{total_all} = {round(total_passed/total_all*100,1)}%")

    # Save summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_levels": len(results),
        "results": results
    }
    with open(f"{args.report_dir}/test_summary.json","w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n报告已保存到 {args.report_dir}/")

if __name__ == "__main__":
    main()
