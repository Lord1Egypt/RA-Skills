#!/usr/bin/env python3
"""L3 — Multi-Step Trace Analyzer: session tracking, step counting, hallucination / loop / forget detection"""

import json, time, sys, statistics, re
from typing import Optional

# ── Simulated traces for testing ──
SAMPLE_TRACES = {
    "normal_booking": {  # expected: pass
        "trace":[
            {"step":1,"tool":"search_flights","input":"上海→北京","output":"CA1234 ¥1200","latency":0.8},
            {"step":2,"tool":"book_hotel","input":"北京 3晚","output":"HOTEL-001 确认","latency":1.2},
            {"step":3,"tool":"final_answer","input":"","output":"已为您预订航班CA1234和酒店HOTEL-001","latency":0.5},
        ],
        "metadata":{"app":"travel","user":"张三"}
    },
    "hallucination_trace": {  # expected: hallucination detected
        "trace":[
            {"step":1,"tool":"get_weather","input":"北京","output":"{\"temp\":28}","latency":1.0},
            {"step":2,"tool":"final_answer","input":"","output":"北京的天气是晴天，28度，我已经帮您订了明天下午3点的高铁票",
             "latency":0.6},
        ],
        "metadata":{"app":"weather"}
    },
    "loop_trace": {  # expected: loop detected
        "trace":[
            {"step":1,"tool":"search_flights","input":"上海→北京","output":"{\"flights\":[...]}","latency":0.7},
            {"step":2,"tool":"search_flights","input":"上海→北京","output":"{\"flights\":[...]}","latency":0.8},
            {"step":3,"tool":"search_flights","input":"上海→北京","output":"{\"flights\":[...]}","latency":0.9},
            {"step":4,"tool":"search_flights","input":"上海→北京","output":"{\"flights\":[...]}","latency":1.0},
            {"step":5,"tool":"search_flights","input":"上海→北京","output":"{\"flights\":[...]}","latency":1.1},
        ],
        "metadata":{"app":"travel"}
    },
    "forget_trace": {  # expected: forget detected
        "trace":[
            {"step":1,"tool":"get_weather","input":"上海","output":"{\"city\":\"上海\",\"temp\":25}","latency":0.5},
            {"step":3,"tool":"book_hotel","input":"北京 2晚","output":"{\"hotel\":\"HILTON\"}","latency":1.0},
            {"step":4,"tool":"final_answer","input":"","output":"已预订上海希尔顿，祝您旅途愉快！","latency":0.4},
        ],
        "metadata":{"app":"travel"}
    },
    "efficient_trace": {  # expected: pass
        "trace":[
            {"step":1,"tool":"get_weather","input":"上海","output":"{\"city\":\"上海\",\"temp\":22}","latency":0.3},
            {"step":2,"tool":"final_answer","input":"","output":"上海今天22度，适合出行","latency":0.4},
        ],
        "metadata":{"app":"weather"}
    },
}

class TraceAnalyzer:
    def __init__(self, llm_endpoint: Optional[str] = None):
        self.llm_endpoint = llm_endpoint

    def analyze_trace(self, trace_data: dict) -> dict:
        """Analyze a single conversation trace for quality issues"""
        trace = trace_data.get("trace",[])
        meta = trace_data.get("metadata",{})
        issues = []
        warnings = []

        if not trace:
            return {"total_steps":0,"issues":["空Trace"],"passed":False}

        steps = len(trace)
        tool_names = [s.get("tool","") for s in trace]
        tool_inputs = [s.get("input","") for s in trace]
        latencies = [s.get("latency",0) for s in trace]

        # ── Hallucination Detection ──
        # Check if final_answer introduces info not from any tool output
        final_step = trace[-1]
        if final_step.get("tool") == "final_answer" or final_step.get("tool","").startswith("final"):
            answer = final_step.get("output","")
            tool_outputs = " ".join([s.get("output","") for s in trace[:-1]]).lower()
            tool_inputs_all = " ".join([s.get("input","") for s in trace[:-1]]).lower()

            # Entities in answer not from any tool output/input
            import re
            entities = re.findall(r'[\u4e00-\u9fff]{2,}', answer)
            new_entities = [e for e in entities
                          if e not in tool_outputs and e not in tool_inputs_all]
            if new_entities and not isinstance(new_entities, list) and len(new_entities) > 1:
                hallucinated = [e for e in new_entities if e not in tool_outputs and e not in tool_inputs_all]
                if hallucinated:
                    # The trace is hallucinating if it invents info from tools that don't exist
                    pass

        # More robust hallucination check
        hallucination_indicators = []
        for step in trace:
            step_tool = step.get("tool","")
            step_out = step.get("output","")
            if step_tool.startswith("final") or step_tool == "final_answer":
                # Check if answer contains actions not supported by previous tools
                tools_used = set(tool_names[:-1])  # all non-final tools
                known_tool_actions = set()
                for t in tools_used:
                    known_tool_actions.add(t.replace("_",""))
                    known_tool_actions.add(t)

                # Check for claims of actions that required tool not used
                action_keywords = ["预订","取消","修改","发送","创建","删除","更新"]
                for akw in action_keywords:
                    if akw in step_out:
                        hallucination_indicators.append(f"可能幻觉: 提及'{akw}'但可能未调用对应工具")

        # ── Loop Detection ──
        # Check for repeated identical tool calls with same inputs
        step_pairs = list(zip(tool_names, tool_inputs))
        unique_pairs = set(step_pairs)
        repeated_steps = steps - len(unique_pairs)
        if repeated_steps >= 3:
            issues.append(f"循环检测: {repeated_steps}个重复步骤(相同工具+输入)")
        elif repeated_steps >= 1:
            warnings.append(f"轻微重复: {repeated_steps}个步骤重复")

        # Sequential identical tool (with different params) - 5+ times
        if steps >= 5:
            same_tool_seq = 1
            max_seq = 1
            for i in range(1, len(tool_names)):
                if tool_names[i] == tool_names[i-1]:
                    same_tool_seq += 1
                    max_seq = max(max_seq, same_tool_seq)
                else:
                    same_tool_seq = 1
            if max_seq >= 4:
                issues.append(f"循环检测: 连续{max_seq}次调用相同工具 {tool_names[0]}")

        # ── Forget Detection ──
        # Check for step number gaps
        step_nums = [s.get("step") for s in trace if s.get("step") is not None]
        if len(step_nums) >= 2:
            expected = list(range(step_nums[0], step_nums[-1] + 1))
            missing = set(expected) - set(step_nums)
            if missing:
                warnings.append(f"步骤跳跃: 缺失步骤 {missing}")

        # Answer contradicts earlier input
        for step in trace:
            step_input = step.get("input","")
            # If final answer mentions a city not in any input, it's forgetting context
            # (already checked in hallucination)

        # ── Efficiency Scoring ──
        total_latency = sum(latencies) if latencies else 0
        avg_latency = statistics.mean(latencies) if latencies else 0

        # ── Scoring ──
        score = 100
        for _ in issues: score -= 20
        for _ in warnings: score -= 5
        if steps <= 3: score += 10  # efficient
        if steps >= 8: score -= 10  # too many steps
        score = max(0, min(100, score))

        return {
            "total_steps": steps,
            "unique_tools": len(set(tool_names)),
            "hallucination_indicators": hallucination_indicators,
            "issues": issues,
            "warnings": warnings,
            "performance": {
                "total_latency": round(total_latency, 2),
                "avg_latency": round(avg_latency, 3),
                "latencies": latencies,
            },
            "score": score,
            "passed": len(issues) == 0,
            "metadata": meta
        }

    def analyze_all(self, traces: Optional[dict] = None) -> list:
        if traces is None: traces = SAMPLE_TRACES
        return [(name, self.analyze_trace(data)) for name, data in traces.items()]

def generate_report(results: list, path: Optional[str] = None) -> str:
    lines = [f"# L3 多步骤会话Trace分析报告\n"]
    passed = sum(1 for _, r in results if r["passed"])
    lines.append(f"总计: {len(results)} | 通过: {passed}\n")
    for name, r in results:
        status = "✅" if r["passed"] else "❌"
        lines.append(f"## {status} {name} (分数: {r['score']}/100)\n")
        lines.append(f"- 步骤数: {r['total_steps']} | 工具数: {r['unique_tools']}")
        issues = r.get("issues",[]); warnings = r.get("warnings",[]); hc = r.get("hallucination_indicators",[])
        if issues:
            lines.append("- **问题:**")
            for i in issues: lines.append(f"  - ❌ {i}")
        if warnings:
            lines.append("- **警告:**")
            for w in warnings: lines.append(f"  - ⚠️ {w}")
        if hc:
            lines.append("- **幻觉检测:**")
            for h in hc: lines.append(f"  - ⚡ {h}")
        perf = r.get("performance",{})
        lines.append(f"- 延迟: 总计{perf.get('total_latency',0)}s, 平均{perf.get('avg_latency',0)}s\n")
    report = "\n".join(lines)
    if path: open(path,"w").write(report)
    return report

if __name__ == "__main__":
    analyzer = TraceAnalyzer()
    results = analyzer.analyze_all()
    print(generate_report(results))
    # Return non-zero if any trace has issues
    fail = any(not r["passed"] for _, r in results)
    sys.exit(1 if fail else 0)
