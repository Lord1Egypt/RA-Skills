#!/usr/bin/env python3
"""
Discriminator: Evaluates skill variants via performance metrics.

Metrics:
- Correctness (accuracy on benchmark tasks)
- Speed (execution time)
- Resource usage (memory, CPU)
- User feedback (if available via feishu messages)

Scores normalized to 0-1 fitness.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import psutil


class Discriminator:
    """Performance-based fitness evaluator."""

    def __init__(self, benchmark_suite: str = None):
        self.benchmark_suite = benchmark_suite or "benchmarks/standard"
        self.weights = {
            "correctness": 0.4,
            "speed": 0.3,
            "resource": 0.2,
            "feedback": 0.1
        }

    def evaluate_population(self, population) -> List[float]:
        """Evaluate all variants and return fitness scores."""
        scores = []
        for variant in population.variants:
            score = self.evaluate_variant(variant)
            scores.append(score)
        return scores

    def evaluate_variant(self, variant) -> float:
        """Compute fitness score for a single variant (0-1)."""
        metrics = self.collect_metrics(variant)

        # Normalize to 0-1 (higher is better)
        normalized = self.normalize_metrics(metrics)

        # Weighted sum
        fitness = (
            self.weights["correctness"] * normalized["correctness"] +
            self.weights["speed"] * normalized["speed"] +
            self.weights["resource"] * normalized["resource"] +
            self.weights["feedback"] * normalized["feedback"]
        )

        return round(fitness, 4)

    def collect_metrics(self, variant) -> Dict:
        """Run variant and collect performance metrics."""
        skill_path = variant.path

        # 1. Correctness: Run tests if available
        correctness = self._run_tests(skill_path)

        # 2. Speed: Execution time of main function
        speed = self._measure_speed(skill_path)

        # 3. Resource: Memory/CPU usage
        resource = self._measure_resources(skill_path)

        # 4. Feedback: Recent user message sentiment (optional)
        feedback = self._get_feedback(variant)

        return {
            "correctness": correctness,
            "speed": speed,
            "resource": resource,
            "feedback": feedback
        }

    def _run_tests(self, skill_path: Path) -> float:
        """Run skill's benchmark suite and return fitness score (0-1)."""
        benchmark_script = skill_path / "scripts" / "benchmark.py"
        if not benchmark_script.exists():
            # No benchmark → use simple correctness check
            return self._simple_correctness_check(skill_path)

        try:
            # Run benchmark in skill's workspace context
            result = subprocess.run(
                ["python3", str(benchmark_script)],
                cwd=skill_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Parse JSON output from benchmark script
            output_file = skill_path / "benchmark_results.json"
            if output_file.exists():
                data = json.loads(output_file.read_text())
                overall_fitness = data.get("fitness", 0.5)
                return overall_fitness

            # Fallback: parse console output for score
            output = result.stdout + result.stderr
            if "Overall Fitness:" in output:
                import re
                match = re.search(r'Overall Fitness: ([\d.]+)', output)
                if match:
                    return float(match.group(1))

            return 0.5
        except Exception as e:
            print(f"[Discriminator] Benchmark error: {e}")
            return 0.0

    def _simple_correctness_check(self, skill_path: Path) -> float:
        """Fallback simple check when no benchmark exists."""
        # Check if skill has required files
        required = ["SKILL.md", "manifest.json"]
        score = 0.0
        for f in required:
            if (skill_path / f).exists():
                score += 0.5
        return min(score, 1.0)

    def _measure_speed(self, skill_path: Path) -> float:
        """Measure execution speed (normalized 0-1, higher is faster)."""
        main_script = skill_path / "scripts" / "run.py"
        if not main_script.exists():
            return 0.5

        try:
            # Warm-up run
            subprocess.run(
                ["python3", str(main_script), "--benchmark"],
                capture_output=True,
                timeout=10
            )

            # Timed run
            start = time.time()
            subprocess.run(
                ["python3", str(main_script), "--benchmark"],
                capture_output=True,
                timeout=30
            )
            elapsed = time.time() - start

            # Normalize: faster → higher score. Baseline 5s = 0.5
            # Score = baseline / elapsed, capped at 1.0
            baseline = 5.0
            score = min(1.0, baseline / max(elapsed, 0.1))
            return score
        except Exception as e:
            print(f"[Discriminator] Speed test error: {e}")
            return 0.0

    def _measure_resources(self, skill_path: Path) -> float:
        """Measure memory/CPU efficiency (0-1)."""
        main_script = skill_path / "scripts" / "run.py"
        if not main_script.exists():
            return 0.5

        try:
            process = subprocess.Popen(
                ["python3", str(main_script), "--benchmark"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            p = psutil.Process(process.pid)

            # Monitor memory for 5 seconds
            max_memory = 0
            start_time = time.time()
            while time.time() - start_time < 5 and process.poll() is None:
                try:
                    mem = p.memory_info().rss / 1024 / 1024  # MB
                    max_memory = max(max_memory, mem)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                time.sleep(0.1)

            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            # Normalize: <100MB → 1.0, >500MB → 0.0
            memory_mb = max_memory
            if memory_mb <= 100:
                return 1.0
            elif memory_mb >= 500:
                return 0.0
            else:
                return 1.0 - (memory_mb - 100) / 400.0
        except Exception as e:
            print(f"[Discriminator] Resource measurement error: {e}")
            return 0.5

    def _get_feedback(self, variant) -> float:
        """Optional: Get user feedback from message history."""
        # Placeholder: can query feishu messages for manual ratings
        # For now: return neutral 0.5
        return 0.5

    def normalize_metrics(self, metrics: Dict) -> Dict:
        """Ensure all metrics are 0-1 floats."""
        normalized = {}
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                normalized[key] = max(0.0, min(1.0, float(value)))
            else:
                normalized[key] = 0.5
        return normalized


if __name__ == "__main__":
    # Quick self-test
    from scripts.population import Variant

    disc = Discriminator()
    test_variant = Variant(
        variant_id="test",
        path=Path("/home/gem/workspace/agent/workspace/skills/self-improving-agent"),
        generation=0
    )
    score = disc.evaluate_variant(test_variant)
    print(f"Test variant fitness: {score:.3f}")