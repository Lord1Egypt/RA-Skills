#!/usr/bin/env python3
"""Generate AgentScope benchmark configs and runner scripts."""

import argparse
import json
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def latency_benchmark(output_dir: Path) -> None:
    config = {
        "scenario": "latency",
        "model": "gpt-4o",
        "prompt": "Reply with OK.",
        "runs": 5,
        "warmup": True,
    }
    runner = '''#!/usr/bin/env python3
import json, time
from pathlib import Path

cfg = json.loads(Path(__file__).with_name("latency.json").read_text())
print(f"Running latency benchmark: {cfg['runs']} runs")
results = []
for i in range(cfg.get("warmup", False) and cfg['runs'] + 1 or cfg['runs']):
    start = time.perf_counter()
    # Placeholder for actual agent call
    duration = time.perf_counter() - start
    results.append({"run": i, "duration_s": duration})
print(json.dumps({"scenario": cfg["scenario"], "results": results}, indent=2))
'''
    write(output_dir / "latency" / "latency.json", json.dumps(config, indent=2, ensure_ascii=False))
    write(output_dir / "latency" / "run_benchmark.py", runner)


def throughput_benchmark(output_dir: Path) -> None:
    config = {
        "scenario": "throughput",
        "model": "gpt-4o",
        "concurrency": 4,
        "prompt": "Reply with OK.",
        "runs": 20,
    }
    runner = '''#!/usr/bin/env python3
import json, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

cfg = json.loads(Path(__file__).with_name("throughput.json").read_text())
print(f"Running throughput benchmark: concurrency={cfg['concurrency']}, runs={cfg['runs']}")
results = []

def task(index: int) -> dict:
    start = time.perf_counter()
    # Placeholder for actual agent call
    duration = time.perf_counter() - start
    return {"run": index, "duration_s": duration}

with ThreadPoolExecutor(max_workers=cfg["concurrency"]) as executor:
    for i, result in enumerate(executor.map(task, range(cfg["runs"]))):
        results.append(result)

print(json.dumps({"scenario": cfg["scenario"], "results": results}, indent=2))
'''
    write(output_dir / "throughput" / "throughput.json", json.dumps(config, indent=2, ensure_ascii=False))
    write(output_dir / "throughput" / "run_benchmark.py", runner)


def compare_benchmark(output_dir: Path) -> None:
    config = {
        "scenario": "compare",
        "variants": [
            {"name": "baseline", "prompt": "Reply with OK."},
            {"name": "verbose", "prompt": "Please reply with OK and a short explanation."},
        ],
        "runs_per_variant": 3,
    }
    runner = '''#!/usr/bin/env python3
import json, time
from pathlib import Path

cfg = json.loads(Path(__file__).with_name("compare.json").read_text())
print(f"Running compare benchmark: {len(cfg['variants'])} variants")
results = []
for variant in cfg["variants"]:
    for i in range(cfg["runs_per_variant"]):
        start = time.perf_counter()
        # Placeholder for actual agent call using variant["prompt"]
        duration = time.perf_counter() - start
        results.append({"variant": variant["name"], "run": i, "duration_s": duration})
print(json.dumps({"scenario": cfg["scenario"], "results": results}, indent=2))
'''
    write(output_dir / "compare" / "compare.json", json.dumps(config, indent=2, ensure_ascii=False))
    write(output_dir / "compare" / "run_benchmark.py", runner)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate AgentScope benchmarks")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--scenario", default="all", choices=["all", "latency", "throughput", "compare"])
    args = parser.parse_args()

    generators = {
        "latency": latency_benchmark,
        "throughput": throughput_benchmark,
        "compare": compare_benchmark,
    }

    targets = generators.values() if args.scenario == "all" else [generators[args.scenario]]
    for generator in targets:
        generator(args.output)

    print(f"Generated benchmarks in: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
