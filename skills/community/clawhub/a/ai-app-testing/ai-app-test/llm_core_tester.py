#!/usr/bin/env python3
"""L0 — LLM Core Functionality Tester"""
import json, time, statistics, sys, os

LLM_CORE_CASES = [
    {"id":"l0-001","dim":"知识","input":"中国的首都是什么？","expected":{"contains":"北京"}},
    {"id":"l0-002","dim":"知识","input":"水的化学式是什么？","expected":{"contains":"H2O"}},
    {"id":"l0-003","dim":"推理","input":"鸡兔同笼，头共35，脚共94，问鸡兔各几只？","expected":{"contains":"23"}},
    {"id":"l0-004","dim":"数学","input":"计算 2^10 的值","expected":{"contains":"1024"}},
    {"id":"l0-005","dim":"编码","input":"用Python写一个斐波那契数列函数","expected":{"contains":"def","code":"fibonacci"}},
    {"id":"l0-006","dim":"语言","input":"今天天气很好 翻译成英文","expected":{"contains":"weather"}},
]

class LLMCoreTester:
    def __init__(self, endpoint, model="deepseek/deepseek-v4-flash", system_prompt=""):
        self.endpoint=endpoint; self.model=model; self.system_prompt=system_prompt

    def call(self, user_input, temperature=0):
        import requests
        msgs=[]
        if self.system_prompt: msgs.append({"role":"system","content":self.system_prompt})
        msgs.append({"role":"user","content":user_input})
        r=requests.post(self.endpoint, json={"model":self.model,"messages":msgs,"temperature":temperature}, timeout=30)
        return r.json()["choices"][0]["message"]["content"]

    def verify(self, output, expected):
        if "contains" in expected:
            return expected["contains"] in output
        if "reject" in expected:
            return any(kw in output for kw in ["抱歉","不能","无法","拒绝","sorry","cannot"])
        return True

    def test_case(self, case):
        start=time.time()
        try:
            out=self.call(case["input"])
            ok=self.verify(out, case["expected"])
        except Exception as e:
            return {"id":case["id"],"dim":case["dim"],"pass":False,"latency":round(time.time()-start,3),"error":str(e)}
        return {"id":case["id"],"dim":case["dim"],"pass":ok,"latency":round(time.time()-start,3),
                "input":case["input"][:30],"output":out[:60]}

    def run_suite(self, cases=None):
        if cases is None: cases=LLM_CORE_CASES
        results=[self.test_case(c) for c in cases]
        by_dim={}
        for r in results:
            by_dim.setdefault(r["dim"],[]).append(r)
        return {"total":len(results),"passed":sum(1 for r in results if r["pass"]),
                "by_dimension":{d:{"total":len(v),"passed":sum(1 for r in v if r["pass"])} for d,v in by_dim.items()},
                "details":results}

    def run_stability(self, n_runs=3):
        outputs=[self.call(LLM_CORE_CASES[0]["input"]) for _ in range(n_runs)]
        unique=len(set(outputs))
        return {"n_runs":n_runs,"consistency_pct":round((1-(unique-1)/n_runs)*100,1) if n_runs>1 else 100}

if __name__=="__main__":
    import requests
    # Try to find an available LLM endpoint
    endpoint = sys.argv[1] if len(sys.argv)>1 else "http://localhost:8080/v1/chat/completions"
    print(f"Testing endpoint: {endpoint}")
    t=LLMCoreTester(endpoint)
    r=t.run_suite()
    print(f"=== L0 LLM Core Test Result ===")
    print(f"Total: {r['total']} | Passed: {r['passed']} | Rate: {round(r['passed']/r['total']*100,1)}%")
    for d,v in r['by_dimension'].items():
        print(f"  {d}: {v['passed']}/{v['total']}")
    for d in r['details']:
        status="✅" if d['pass'] else "❌"
        print(f"  {status} [{d['id']}] input={d.get('input','')[:30]} | output={d.get('output','')[:50]}" if d['pass'] else f"  {status} [{d['id']}] {d.get('error','')[:60]}")
