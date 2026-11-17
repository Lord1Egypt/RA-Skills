#!/usr/bin/env python3
"""Performance / Stress Tester: concurrency, latency, throughput, resource monitoring"""

import json, time, statistics, sys, os, threading, concurrent.futures
from datetime import datetime
from typing import Optional

STRESS_PROFILES = {
    "light":  {"concurrency":2, "total_requests":10, "timeout":15, "label":"轻量测试"},
    "medium": {"concurrency":5, "total_requests":25, "timeout":20, "label":"中等压力"},
    "heavy":  {"concurrency":10,"total_requests":50, "timeout":30, "label":"高负载"},
}

SAMPLE_QUERIES = [
    "中国的首都是什么？",
    "用Python写一个快排算法",
    "翻译：Hello world to Chinese",
    "鸡兔同笼，头35脚94",
    "简单解释一下量子计算",
    "写一首关于秋天的诗",
    "圆周率前20位是什么",
    "推荐3本必读的编程书籍",
]

class StressTester:
    def __init__(self, endpoint: str = "http://localhost:8080/v1/chat/completions",
                 model: str = "deepseek/deepseek-v4-flash", headers: Optional[dict] = None):
        self.endpoint = endpoint; self.model = model; self.headers = headers or {}

    def single_request(self, prompt: str, timeout: int = 15, idx: int = 0) -> dict:
        """Execute a single LLM request and return metrics"""
        import requests
        t_start = time.time()
        try:
            r = requests.post(self.endpoint, json={
                "model":self.model,
                "messages":[{"role":"user","content":prompt}],
                "temperature":0,"max_tokens":128
            }, headers=self.headers, timeout=timeout)
            data = r.json()
            content = data.get("choices",[{}])[0].get("message",{}).get("content","")
            t_elapsed = time.time() - t_start
            return {
                "idx": idx, "prompt": prompt[:20], "success": r.status_code == 200,
                "status": r.status_code, "latency": round(t_elapsed,3),
                "output_len": len(content), "error": None
            }
        except Exception as e:
            t_elapsed = time.time() - t_start
            return {
                "idx": idx, "prompt": prompt[:20], "success": False,
                "status": 0, "latency": round(t_elapsed,3),
                "output_len": 0, "error": str(e)[:60]
            }

    def run_concurrent(self, profile: str = "light", queries: Optional[list] = None) -> dict:
        """Run concurrent requests with given stress profile"""
        if queries is None: queries = SAMPLE_QUERIES
        cfg = STRESS_PROFILES.get(profile, STRESS_PROFILES["light"])

        concurrency = cfg["concurrency"]
        total = cfg["total_requests"]
        timeout = cfg["timeout"]

        # Round-robin through queries
        prompts = [queries[i % len(queries)] for i in range(total)]

        results = []
        t_global_start = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = {
                executor.submit(self.single_request, p, timeout, i): i
                for i, p in enumerate(prompts)
            }
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        t_global = time.time() - t_global_start

        # Sort by idx for chronological order
        results.sort(key=lambda r: r["idx"])

        latencies = [r["latency"] for r in results]
        successes = sum(1 for r in results if r["success"])
        failures = total - successes

        sorted_lat = sorted(latencies)
        p50 = statistics.median(latencies) if latencies else 0
        p95 = sorted_lat[int(len(sorted_lat)*0.95)] if len(sorted_lat) > 1 else 0
        p99 = sorted_lat[int(len(sorted_lat)*0.99)] if len(sorted_lat) > 5 else 0

        return {
            "profile": profile, "label": cfg["label"],
            "concurrency": concurrency, "total": total,
            "actual_completed": len(results),
            "success": successes, "failures": failures,
            "success_rate": round(successes/total*100,1) if total else 0,
            "total_duration": round(t_global, 2),
            "throughput": round(total/t_global, 2) if t_global else 0,
            "latency_p50": round(p50, 3),
            "latency_p95": round(p95, 3),
            "latency_p99": round(p99, 3) if p99 else None,
            "latency_min": round(min(latencies), 3) if latencies else 0,
            "latency_max": round(max(latencies), 3) if latencies else 0,
            "latency_std": round(statistics.stdev(latencies), 3) if len(latencies) > 1 else 0,
            "details": results
        }

    def run_multi_profile(self, profiles: Optional[list] = None) -> dict:
        """Run multiple stress profiles"""
        if profiles is None: profiles = list(STRESS_PROFILES.keys())
        results = {}
        for p in profiles:
            print(f"  运行 {p} ({STRESS_PROFILES[p]['label']})...", file=sys.stderr)
            results[p] = self.run_concurrent(p)
        return {
            "timestamp": datetime.now().isoformat(),
            "profiles_run": profiles,
            "results": results
        }

def generate_report(result: dict, path: Optional[str] = None) -> str:
    lines = [f"# 性能/压力测试报告\n"]
    lines.append(f"时间: {result.get('timestamp',datetime.now().isoformat())}\n")
    for pname, r in result.get("results",{}).items():
        lines.append(f"## [{pname}] {r.get('label','')}\n")
        lines.append(f"- 并发: {r['concurrency']} | 请求数: {r['success']}/{r['total']} | "
                     f"成功: {r['success_rate']}%")
        lines.append(f"- 总耗时: {r['total_duration']}s | 吞吐: {r['throughput']} req/s")
        lines.append(f"- 延迟: P50={r['latency_p50']}s, P95={r['latency_p95']}s, "
                     f"P99={r.get('latency_p99','-')}s")
        lines.append(f"  Min={r['latency_min']}s, Max={r['latency_max']}s, "
                     f"Std={r['latency_std']}s\n")
    report = "\n".join(lines)
    if path: open(path,"w").write(report)
    return report

def generate_json_report(result: dict, path: str) -> None:
    with open(path,"w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    import sys
    profiles = sys.argv[1:] if len(sys.argv) > 1 else ["light"]
    endpoint = "http://localhost:8080/v1/chat/completions"
    tester = StressTester(endpoint)
    result = tester.run_multi_profile(profiles)
    print(generate_report(result))
