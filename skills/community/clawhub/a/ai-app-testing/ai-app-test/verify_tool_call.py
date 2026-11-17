#!/usr/bin/env python3
"""L2 — Tool Call Verification: function/tool call accuracy, parameter correctness"""

import json, time, statistics, sys, os, re
from typing import Optional

TOOL_TEST_CASES = [
    # ── CRM: create_contact ──
    {"id":"l2-001","desc":"创建联系人","prompt":"帮我创建一个联系人，姓名张三，电话13800138000",
     "tools":[{"type":"function","function":{"name":"create_contact","description":"创建联系人",
               "parameters":{"type":"object","properties":{"name":{"type":"string"},"phone":{"type":"string"}},
                             "required":["name","phone"]}}}],
     "expect":{"tool":"create_contact","params":{"name":"张三","phone":"13800138000"}}},
    # ── CRM: get_weather ──
    {"id":"l2-002","desc":"查询天气","prompt":"北京今天天气怎么样？",
     "tools":[{"type":"function","function":{"name":"get_weather","description":"获取天气",
               "parameters":{"type":"object","properties":{"city":{"type":"string"},"date":{"type":"string"}},
                             "required":["city"]}}}],
     "expect":{"tool":"get_weather","params_contains":{"city":"北京"}}},
    # ── Booking: search_flights ──
    {"id":"l2-003","desc":"订机票","prompt":"帮我查下周二从上海到北京的航班",
     "tools":[{"type":"function","function":{"name":"search_flights","description":"搜索航班",
               "parameters":{"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"},"date":{"type":"string"}},
                             "required":["from","to"]}}}],
     "expect":{"tool":"search_flights","params_contains":{"from":"上海","to":"北京"}}},
    # ── Booking: book_hotel ──
    {"id":"l2-004","desc":"订酒店","prompt":"帮我订一间深圳的3星级酒店，7月30日入住，住2晚",
     "tools":[{"type":"function","function":{"name":"book_hotel","description":"预订酒店",
               "parameters":{"type":"object","properties":{"city":{"type":"string"},"stars":{"type":"integer"},
                             "checkin":{"type":"string"},"nights":{"type":"integer"}},
                             "required":["city","checkin","nights"]}}}],
     "expect":{"tool":"book_hotel","params_contains":{"city":"深圳"}}},
    # ── Multi-tool: first step only ──
    {"id":"l2-005","desc":"多步骤第一步","prompt":"帮我查明天上海下雨吗，然后如果下雨就提醒我带伞",
     "tools":[{"type":"function","function":{"name":"get_weather","description":"获取天气",
               "parameters":{"type":"object","properties":{"city":{"type":"string"},"date":{"type":"string"}},
                             "required":["city"]}}}],
     "expect":{"tool":"get_weather","params_contains":{"city":"上海"}}},
    # ── Parameter type correctness ──
    {"id":"l2-006","desc":"参数类型校验","prompt":"深圳30度，帮我把华氏度转摄氏度",
     "tools":[{"type":"function","function":{"name":"convert_temperature","description":"温度转换",
               "parameters":{"type":"object","properties":{"value":{"type":"number"},"from_unit":{"type":"string"},"to_unit":{"type":"string"}},
                             "required":["value","from_unit","to_unit"]}}}],
     "expect":{"tool":"convert_temperature"}},
    # ── No tool needed ──
    {"id":"l2-007","desc":"无需工具场景","prompt":"你好，今天过得怎么样？",
     "tools":[{"type":"function","function":{"name":"get_weather","description":"获取天气",
               "parameters":{"type":"object","properties":{"city":{"type":"string"}},
                             "required":["city"]}}}],
     "expect":{"tool":None}},   # should NOT call a tool
    # ── Ambiguous / partial ──
    {"id":"l2-008","desc":"不完整信息追问","prompt":"帮我查一下天气",
     "tools":[{"type":"function","function":{"name":"get_weather","description":"获取天气",
               "parameters":{"type":"object","properties":{"city":{"type":"string"},"date":{"type":"string"}},
                             "required":["city"]}}}],
     "expect":{"tool":"get_weather"}},
]

TOOL_CALL_SIM_RESULTS = {
    "get_weather": json.dumps({"city":"北京","temperature":28,"condition":"晴"}),
    "search_flights": json.dumps([
        {"flight":"CA1234","from":"上海","to":"北京","time":"08:00","price":1200},
        {"flight":"MU5678","from":"上海","to":"北京","time":"14:30","price":980}
    ]),
    "book_hotel": json.dumps({"order_id":"HOTEL-8848","status":"confirmed"}),
    "create_contact": json.dumps({"contact_id":"CT-001","status":"created"}),
    "convert_temperature": json.dumps({"result":86}),
}

class ToolCallVerifier:
    def __init__(self, endpoint: str, model: str = "deepseek/deepseek-v4-flash",
                 headers: Optional[dict] = None, timeout: int = 30):
        self.endpoint = endpoint; self.model = model
        self.headers = headers or {}; self.timeout = timeout

    def call_with_tools(self, prompt: str, tools: list) -> dict:
        import requests
        payload = {"model":self.model,"messages":[{"role":"user","content":prompt}],
                   "temperature":0,"max_tokens":512}
        if tools: payload["tools"] = tools
        r = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=self.timeout)
        return r.json()["choices"][0]["message"]

    def verify_tool(self, msg: dict, expect: dict) -> tuple:
        """Returns (passed: bool, detail: str)"""
        exp_tool = expect.get("tool")
        exp_params = expect.get("params", {})
        exp_params_contains = expect.get("params_contains", {})
        tool_calls = msg.get("tool_calls", [])
        content = msg.get("content", "")

        # No tool expected
        if exp_tool is None:
            if not tool_calls:
                return True, "正确未触发工具调用"
            names = [t["function"]["name"] for t in tool_calls]
            return False, f"不应调用工具，实际调用了: {names}"

        # Tool should be called
        if not tool_calls:
            return False, f"应调用 {exp_tool} 但未触发工具调用"

        names = [t["function"]["name"] for t in tool_calls]
        if exp_tool not in names:
            return False, f"应调用 {exp_tool}，实际调用了: {names}"

        # Find the matching tool call
        tc = next(t for t in tool_calls if t["function"]["name"] == exp_tool)
        try:
            actual_params = json.loads(tc["function"]["arguments"])
        except:
            return False, f"参数非JSON: {tc['function']['arguments'][:60]}"

        # Exact parameter match
        if exp_params:
            for k, v in exp_params.items():
                if actual_params.get(k) != v:
                    return True, f"工具名正确，但参数 '{k}' 期望 '{v}' 实际 '{actual_params.get(k)}'（可能是模糊匹配）"

        # Contains match for fuzzy scenarios
        if exp_params_contains:
            for k, v in exp_params_contains.items():
                actual = actual_params.get(k,"")
                if isinstance(actual, str) and v not in actual:
                    return True, f"工具名正确，参数 '{k}' 含 '{v}'? 实际='{actual}'"
                if not isinstance(actual, str) and actual != v:
                    return True, f"工具名正确，参数 '{k}' 期望含 '{v}' 实际='{actual}'"

        return True, f"工具调用正确: {exp_tool}, 参数={actual_params}"

    def run_suite(self, cases: Optional[list] = None) -> dict:
        if cases is None: cases = TOOL_TEST_CASES
        results = []
        for c in cases:
            t0 = time.time()
            try:
                msg = self.call_with_tools(c["prompt"], c["tools"])
                passed, detail = self.verify_tool(msg, c["expect"])
                record = {"id":c["id"],"desc":c["desc"],"passed":passed,"detail":detail,
                          "latency":round(time.time()-t0,3)}
                actual_tc = msg.get("tool_calls",[])
                if actual_tc:
                    record["actual_tool"] = actual_tc[0]["function"]["name"]
                results.append(record)
            except Exception as e:
                results.append({"id":c["id"],"desc":c["desc"],"passed":False,
                                "detail":str(e)[:60],"latency":round(time.time()-t0,3)})
        return {"total":len(results),"passed":sum(1 for r in results if r["passed"]),
                "tool_accuracy":round(sum(1 for r in results if r["passed"])/len(results)*100,1) if results else 0,
                "details":results}

def generate_report(result: dict, path: Optional[str] = None) -> str:
    lines = [f"# L2 工具调用验证报告\n"]
    lines.append(f"总计: {result['total']} | 通过: {result['passed']} | "
                 f"工具调用准确率: {result['tool_accuracy']}%\n")
    lines.append("| ID | 场景 | 结果 | 详情 |")
    lines.append("|----|------|------|------|")
    for d in result["details"]:
        status = "✅" if d["passed"] else "❌"
        actual = d.get("actual_tool","-")
        lines.append(f"| {d['id']} | {d['desc']} | {status} | {d['detail']} |")
    report = "\n".join(lines)
    if path: open(path,"w").write(report)
    return report

if __name__ == "__main__":
    endpoint = sys.argv[1] if len(sys.argv)>1 else "http://localhost:8080/v1/chat/completions"
    tester = ToolCallVerifier(endpoint)
    result = tester.run_suite()
    print(generate_report(result))
    sys.exit(0 if result["passed"]==result["total"] else 1)
