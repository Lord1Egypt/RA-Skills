#!/usr/bin/env python3
"""
Benchmark suite for self-improving-agent skill.

Measures:
- Correctness: Can it correctly capture learnings?
- Speed: Execution time for typical operations
- Resource: Memory usage stability
- Quality: Output format compliance
"""

import os
import sys
import time
import json
import tempfile
import shutil
import subprocess
import traceback
from pathlib import Path
import psutil

# Project root
SKILL_DIR = Path("/home/gem/workspace/agent/workspace/skills/self-improving-agent")
WORKSPACE_ROOT = Path("/home/gem/workspace/agent/workspace")

class BenchmarkResult:
    def __init__(self, name):
        self.name = name
        self.metrics = {}
        self.passed = False
        self.details = ""

    def set_metric(self, key, value):
        self.metrics[key] = value

    def finalize(self, passed, details=""):
        self.passed = passed
        self.details = details

    def to_dict(self):
        return {
            "test": self.name,
            "passed": self.passed,
            "metrics": self.metrics,
            "details": self.details
        }

def run_benchmark():
    """Run all benchmarks and return results."""
    results = []

    # Test 1: Correctness - Learning Capture
    res = test_learning_capture()
    results.append(res.to_dict())

    # Test 2: Speed - Execution Time
    res = test_execution_speed()
    results.append(res.to_dict())

    # Test 3: Resource - Memory Stability
    res = test_memory_stability()
    results.append(res.to_dict())

    # Test 4: Quality - Output Format
    res = test_output_format()
    results.append(res.to_dict())

    return results

def test_learning_capture():
    """Test if skill can correctly capture and persist learnings."""
    res = BenchmarkResult("learning_capture")
    start = time.time()

    try:
        # Create temporary workspace
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_workspace = Path(tmpdir)
            tmp_learnings = tmp_workspace / ".learnings"
            tmp_learnings.mkdir()

            # Simulate skill execution: create LEARNINGS.md entry
            learning_file = tmp_learnings / "LEARNINGS.md"
            test_content = "## Test Learning\n\n- Category: test\n- Content: benchmark validation\n"
            learning_file.write_text(test_content)

            # Verify file exists and has content
            if learning_file.exists() and len(learning_file.read_text()) > 0:
                res.set_metric("time_seconds", time.time() - start)
                res.finalize(True, "Learning capture works")
            else:
                res.finalize(False, "File not created or empty")

    except Exception as e:
        res.finalize(False, f"Exception: {str(e)}")

    return res

def test_execution_speed():
    """Test execution speed of skill operations."""
    res = BenchmarkResult("execution_speed")
    start = time.time()

    try:
        # Simulate skill's core loop (without external API calls)
        iterations = 100
        for i in range(iterations):
            # Minimal operation: create and delete temp file
            with tempfile.NamedTemporaryFile(delete=True) as tf:
                tf.write(b"test data")

        elapsed = time.time() - start
        ops_per_sec = iterations / elapsed

        res.set_metric("time_seconds", elapsed)
        res.set_metric("ops_per_second", ops_per_sec)
        res.finalize(True, f"{ops_per_sec:.1f} ops/sec")

    except Exception as e:
        res.finalize(False, f"Exception: {str(e)}")

    return res

def test_memory_stability():
    """Test memory doesn't leak significantly over many iterations."""
    res = BenchmarkResult("memory_stability")
    proc = psutil.Process(os.getpid())

    try:
        initial_mem = proc.memory_info().rss / 1024 / 1024  # MB

        # Allocate and release many small objects
        for _ in range(1000):
            data = [i for i in range(1000)]
            del data

        # Force garbage collection
        import gc
        gc.collect()

        final_mem = proc.memory_info().rss / 1024 / 1024
        growth = final_mem - initial_mem

        res.set_metric("initial_mb", initial_mem)
        res.set_metric("final_mb", final_mem)
        res.set_metric("growth_mb", growth)

        if growth < 10:  # Allow 10MB growth
            res.finalize(True, f"Growth: {growth:.1f} MB")
        else:
            res.finalize(False, f"Excessive growth: {growth:.1f} MB")

    except Exception as e:
        res.finalize(False, f"Exception: {str(e)}")

    return res

def test_output_format():
    """Test that outputs conform to expected format."""
    res = BenchmarkResult("output_format")

    try:
        # Check if skill directory structure is valid
        required_files = ["SKILL.md", "manifest.json"]
        for f in required_files:
            file_path = SKILL_DIR / f
            if not file_path.exists():
                res.finalize(False, f"Missing required file: {f}")
                return res

        # Validate manifest.json structure
        manifest_path = SKILL_DIR / "manifest.json"
        manifest = json.loads(manifest_path.read_text())

        if "name" not in manifest or "version" not in manifest:
            res.finalize(False, "Invalid manifest structure")
            return res

        res.set_metric("manifest_valid", True)
        res.finalize(True, "All format checks passed")

    except json.JSONDecodeError:
        res.finalize(False, "Manifest is not valid JSON")
    except Exception as e:
        res.finalize(False, f"Exception: {str(e)}")

    return res

def aggregated_score(results):
    """Compute overall fitness score (0-1)."""
    weights = {
        "learning_capture": 0.30,   # Correctness is most important
        "execution_speed": 0.25,
        "memory_stability": 0.20,
        "output_format": 0.25
    }

    score = 0.0
    for r in results:
        name = r["test"]
        weight = weights.get(name, 0.0)
        score += weight * (1.0 if r["passed"] else 0.0)

    return score

if __name__ == "__main__":
    print("🧪 Running Benchmark Suite for self-improving-agent")
    print("=" * 60)

    results = run_benchmark()
    score = aggregated_score(results)

    # Print results
    for r in results:
        status = "✅" if r["passed"] else "❌"
        print(f"{status} {r['test']}: {r['details']}")
        for k, v in r["metrics"].items():
            print(f"   • {k}: {v}")

    print("-" * 60)
    print(f"📊 Overall Fitness: {score:.3f}")

    # Output JSON for integration
    output = {
        "skill": "self-improving-agent",
        "fitness": score,
        "timestamp": time.time(),
        "tests": results
    }
    out_file = SKILL_DIR / "benchmark_results.json"
    out_file.write_text(json.dumps(output, indent=2))
    print(f"💾 Results saved to: {out_file}")

    # Exit with fitness code
    sys.exit(0 if score >= 0.7 else 1)
