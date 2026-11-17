#!/usr/bin/env python3
"""L4 — End-to-End Session Tester: multi-turn conversation flows, full-use-case journeys"""

import json, time, sys, statistics, re
from typing import Optional

E2E_SCENARIOS = {
    "travel_booking": {
        "id":"e2e-001","name":"完整旅游预订流程",
        "required_steps": ["城市查询","航班搜索","酒店预订","最终确认"],
        "constraints": {"max_steps":8,"min_steps":3},
        "test_prompts": [
            ("用户","我想去北京旅游，帮我看看有什么航班"),
            ("用户","帮我订最近的一班"),
            ("用户","再帮我订个3晚的酒店，离市中心近的"),
            ("用户","确认下单"),
        ],
        "success_signals": [
            "订单","确认","预订","已为您"
        ]
    },
    "customer_service": {
        "id":"e2e-002","name":"客服售后流程",
        "required_steps": ["问题识别","订单查询","处理方案","确认"],
        "test_prompts": [
            ("用户","我昨天买的手机到了，但是屏幕有划痕"),
            ("用户","订单号是 ORD-20260728-001"),
            ("用户","可以换货吗？"),
            ("用户","好的，那换货流程是怎样的？"),
        ],
        "success_signals": [
            "抱歉","换货","退款","售后服务","订单","处理"
        ]
    },
    "info_collection": {
        "id":"e2e-003","name":"多轮信息收集",
        "required_steps": ["信息收集","确认"],
        "test_prompts": [
            ("用户","我想开个银行账户"),
            ("用户","我叫张三"),
            ("用户","手机号 13800138000"),
            ("用户","身份证号 110101199001011234"),
            ("用户","好的，确认"),
        ],
        "success_signals": [
            "确认","信息","完成","成功"
        ]
    },
    "rag_knowledge_query": {
        "id":"e2e-004","name":"RAG知识库查询",
        "required_steps": ["问题接收","知识检索","回答生成"],
        "test_prompts": [
            ("用户","XX科技是哪一年成立的？"),
            ("用户","2024年营收是多少？"),
            ("用户","他们用的是什么加密技术？"),
        ],
        "success_signals": [
            "2018","8.2亿","TLS","AES","加密"
        ]
    },
}

class E2ESessionTester:
    def __init__(self, endpoint: str = "http://localhost:8080/v1/chat/completions",
                 model: str = "deepseek/deepseek-v4-flash", timeout: int = 30):
        self.endpoint = endpoint; self.model = model; self.timeout = timeout

    def simulate_session(self, scenario: dict) -> dict:
        """Simulate a multi-turn session and analyze"""
        import requests
        steps = []
        total_latency = 0
        session_id = f"e2e-{int(time.time())}"
        conversation = []

        for i, (role, text) in enumerate(scenario["test_prompts"]):
            t0 = time.time()
            conversation.append({"role":"user","content":text})
            try:
                r = requests.post(self.endpoint, json={
                    "model":self.model,"messages":conversation,
                    "temperature":0,"max_tokens":512
                }, timeout=self.timeout)
                reply = r.json()["choices"][0]["message"]["content"]
                conversation.append({"role":"assistant","content":reply})
                latency = round(time.time()-t0, 3)
                total_latency += latency
                steps.append({"turn":i+1,"input":text[:30],"output":reply[:60],"latency":latency})
            except Exception as e:
                steps.append({"turn":i+1,"input":text[:30],"error":str(e)[:40],"latency":round(time.time()-t0,3)})

        # Analyze results
        num_steps = len(steps)
        success = num_steps == len(scenario["test_prompts"])
        all_outputs = " ".join(s.get("output","") for s in steps)

        # Check success signals
        signals_found = []
        signals_missing = []
        for sig in scenario.get("success_signals",[]):
            if sig in all_outputs:
                signals_found.append(sig)
            else:
                signals_missing.append(sig)

        # Determine outcome
        if not success:
            outcome = "FAILED"
        elif len(signals_missing) == 0:
            outcome = "PASS"
        else:
            outcome = "PARTIAL"

        return {
            "session_id": session_id,
            "scenario_id": scenario.get("id","unknown"),
            "num_turns": num_steps,
            "expected_turns": len(scenario["test_prompts"]),
            "latency_total": round(total_latency,2),
            "latency_avg": round(total_latency/num_steps,3) if num_steps else 0,
            "success_signals_found": signals_found,
            "success_signals_missing": signals_missing,
            "outcome": outcome,
            "steps": steps
        }

    def run_suite(self, scenarios: Optional[dict] = None) -> dict:
        if scenarios is None: scenarios = E2E_SCENARIOS
        results = []
        for name, sc in scenarios.items():
            r = self.simulate_session(sc)
            r["name"] = sc.get("name",name)
            results.append(r)
        return {
            "total": len(results),
            "passed": sum(1 for r in results if r["outcome"] == "PASS"),
            "partial": sum(1 for r in results if r["outcome"] == "PARTIAL"),
            "failed": sum(1 for r in results if r["outcome"] == "FAILED"),
            "results": results
        }

    def dry_run(self) -> dict:
        """Run analysis without actual API calls (using scenario analysis only)"""
        results = []
        for name, sc in E2E_SCENARIOS.items():
            prompts = sc["test_prompts"]
            results.append({
                "name": sc.get("name",name),
                "id": sc.get("id",""),
                "turns": len(prompts),
                "required_steps": sc.get("required_steps",[]),
                "constraints": sc.get("constraints",{}),
                "signals_to_check": len(sc.get("success_signals",[])),
                "ready": True
            })
        return {"total":len(results),"scenarios":results}

def generate_report(result: dict, path: Optional[str] = None) -> str:
    lines = [f"# L4 端到端会话测试报告\n"]
    if "scenarios" in result:
        # Dry run mode
        lines.append(f"场景总量: {result['total']}\n")
        for r in result["scenarios"]:
            lines.append(f"  ✅ [{r['id']}] {r['name']}")
            lines.append(f"     对话轮次: {r['turns']}")
            lines.append(f"     必须步骤: {r['required_steps']}")
            lines.append(f"     成功信号: {r['signals_to_check']}个\n")
    else:
        lines.append(f"总计: {result['total']} | 通过: {result['passed']} | "
                     f"部分通过: {result['partial']} | 失败: {result['failed']}\n")
        for r in result["results"]:
            icon = {"PASS":"✅","PARTIAL":"⚠️","FAILED":"❌"}.get(r["outcome"],"❓")
            lines.append(f"{icon} [{r['scenario_id']}] {r['name']}")
            lines.append(f"   轮次: {r['num_turns']}/{r['expected_turns']} | "
                         f"延迟P50: {r['latency_avg']}s")
            if r.get("success_signals_missing"):
                lines.append(f"   缺失信号: {r['success_signals_missing']}")
            lines.append("")
    report = "\n".join(lines)
    if path: open(path,"w").write(report)
    return report

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "dry"
    tester = E2ESessionTester()
    if mode == "dry":
        result = tester.dry_run()
    else:
        ep = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8080/v1/chat/completions"
        tester.endpoint = ep
        result = tester.run_suite()
    print(generate_report(result))
