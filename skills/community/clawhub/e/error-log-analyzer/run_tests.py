#!/usr/bin/env python3
"""
Test Runner for Error Log Analyzer
Runs all tests and generates accuracy reports.
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.feedback import AccuracyTracker, print_accuracy_report, FeedbackCollector


def run_pytest(test_type: str = "all") -> bool:
    """Run pytest for specified test type."""
    test_files = {
        "parsers": "tests/test_parsers.py",
        "accuracy": "tests/test_ai_accuracy.py",
        "all": "tests/"
    }
    
    test_target = test_files.get(test_type, "tests/")
    
    print(f"\n🧪 Running {test_type} tests...")
    print("=" * 70)
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_target, "-v", "--tb=short"],
        cwd=Path(__file__).parent
    )
    
    return result.returncode == 0


def run_accuracy_benchmark() -> dict:
    """Run accuracy benchmark and return results."""
    print("\n📊 Running Accuracy Benchmark...")
    print("=" * 70)
    
    # Import test module
    from tests.test_ai_accuracy import TestAIAccuracy, TestCase
    
    analyzer = AIAnalyzer(api_key=None)
    test = TestAIAccuracy()
    test_cases = test._load_test_cases()
    
    results = {
        "total_tests": len(test_cases),
        "error_type_correct": 0,
        "severity_correct": 0,
        "severity_off_by_one": 0,
        "keyword_hits": 0,
        "keyword_total": 0,
        "suggestion_hits": 0,
        "suggestion_total": 0,
        "by_category": {},
        "by_difficulty": {},
        "failures": []
    }
    
    severity_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
    
    for case in test_cases:
        analysis = analyzer.analyze(case.error_message, case.stack_trace)
        
        # Error type accuracy
        is_type_correct = (
            case.expected_error_type.lower() in analysis.error_type.lower() or
            analysis.error_type.lower() in case.expected_error_type.lower()
        )
        if is_type_correct:
            results["error_type_correct"] += 1
        else:
            results["failures"].append({
                "id": case.id,
                "expected": case.expected_error_type,
                "got": analysis.error_type
            })
        
        # Severity accuracy
        expected_level = severity_order.get(case.expected_severity, 1)
        actual_level = severity_order.get(analysis.severity, 1)
        if expected_level == actual_level:
            results["severity_correct"] += 1
        elif abs(expected_level - actual_level) == 1:
            results["severity_off_by_one"] += 1
        
        # Keyword coverage
        explanation_lower = analysis.explanation.lower()
        for keyword in case.expected_keywords:
            results["keyword_total"] += 1
            if keyword.lower() in explanation_lower:
                results["keyword_hits"] += 1
        
        # Suggestion quality
        all_suggestions = " ".join(analysis.suggestions).lower()
        for keyword in case.expected_fix_keywords:
            results["suggestion_total"] += 1
            if keyword.lower() in all_suggestions:
                results["suggestion_hits"] += 1
        
        # By category
        cat = case.category
        if cat not in results["by_category"]:
            results["by_category"][cat] = {"total": 0, "correct": 0}
        results["by_category"][cat]["total"] += 1
        if is_type_correct:
            results["by_category"][cat]["correct"] += 1
        
        # By difficulty
        diff = case.difficulty
        if diff not in results["by_difficulty"]:
            results["by_difficulty"][diff] = {"total": 0, "correct": 0}
        results["by_difficulty"][diff]["total"] += 1
        if is_type_correct:
            results["by_difficulty"][diff]["correct"] += 1
    
    # Calculate percentages
    results["error_type_accuracy"] = results["error_type_correct"] / results["total_tests"]
    results["severity_accuracy"] = results["severity_correct"] / results["total_tests"]
    results["severity_acceptable"] = (results["severity_correct"] + results["severity_off_by_one"]) / results["total_tests"]
    results["keyword_coverage"] = results["keyword_hits"] / results["keyword_total"] if results["keyword_total"] > 0 else 0
    results["suggestion_quality"] = results["suggestion_hits"] / results["suggestion_total"] if results["suggestion_total"] > 0 else 0
    
    # Record results
    tracker = AccuracyTracker()
    tracker.record_test_results(results)
    
    return results


def print_benchmark_results(results: dict):
    """Print formatted benchmark results."""
    print("\n" + "=" * 70)
    print(" 📈 Accuracy Benchmark Results")
    print("=" * 70)
    
    print(f"\nTotal test cases: {results['total_tests']}")
    
    print("\n🎯 Core Metrics:")
    print(f"  Error Type Accuracy: {results['error_type_accuracy']:.1%}")
    print(f"  Severity Accuracy: {results['severity_accuracy']:.1%} (±1: {results['severity_acceptable']:.1%})")
    print(f"  Keyword Coverage: {results['keyword_coverage']:.1%}")
    print(f"  Suggestion Quality: {results['suggestion_quality']:.1%}")
    
    # Calculate overall score
    overall = (
        results['error_type_accuracy'] * 0.4 +
        results['severity_accuracy'] * 0.2 +
        results['keyword_coverage'] * 0.2 +
        results['suggestion_quality'] * 0.2
    )
    
    grade = "A" if overall >= 0.9 else "B" if overall >= 0.8 else "C" if overall >= 0.7 else "D" if overall >= 0.6 else "F"
    
    print(f"\n🏆 Overall Score: {overall:.1%} (Grade: {grade})")
    
    print("\n📂 By Category:")
    for cat, data in sorted(results["by_category"].items()):
        acc = data["correct"] / data["total"]
        print(f"  {cat}: {acc:.1%} ({data['correct']}/{data['total']})")
    
    print("\n📊 By Difficulty:")
    for diff, data in sorted(results["by_difficulty"].items()):
        acc = data["correct"] / data["total"]
        print(f"  {diff}: {acc:.1%} ({data['correct']}/{data['total']})")
    
    if results["failures"]:
        print("\n❌ Failures:")
        for f in results["failures"][:5]:  # Show first 5
            print(f"  {f['id']}: expected '{f['expected']}', got '{f['got']}'")
        if len(results["failures"]) > 5:
            print(f"  ... and {len(results['failures']) - 5} more")
    
    print("\n" + "=" * 70)


def show_feedback_stats():
    """Show current feedback statistics."""
    collector = FeedbackCollector()
    stats = collector.get_feedback_stats()
    print_accuracy_report(stats)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Error Log Analyzer Test Runner")
    parser.add_argument(
        "command",
        choices=["test", "benchmark", "feedback", "all"],
        help="What to run: test (unit tests), benchmark (accuracy), feedback (stats), all"
    )
    parser.add_argument(
        "--type",
        choices=["parsers", "accuracy", "all"],
        default="all",
        help="Type of tests to run (for 'test' command)"
    )
    
    args = parser.parse_args()
    
    if args.command == "test":
        success = run_pytest(args.type)
        sys.exit(0 if success else 1)
    
    elif args.command == "benchmark":
        results = run_accuracy_benchmark()
        print_benchmark_results(results)
    
    elif args.command == "feedback":
        show_feedback_stats()
    
    elif args.command == "all":
        # Run everything
        print("\n" + "=" * 70)
        print(" 🔧 Error Log Analyzer - Full Test Suite")
        print("=" * 70)
        
        # Unit tests
        test_success = run_pytest("all")
        
        # Accuracy benchmark
        benchmark_results = run_accuracy_benchmark()
        print_benchmark_results(benchmark_results)
        
        # Feedback stats
        print("\n")
        show_feedback_stats()
        
        # Summary
        print("\n" + "=" * 70)
        print(" 📋 Summary")
        print("=" * 70)
        print(f"  Unit tests: {'✅ PASSED' if test_success else '❌ FAILED'}")
        print(f"  Accuracy: {benchmark_results['error_type_accuracy']:.1%}")
        print("=" * 70)
        
        sys.exit(0 if test_success else 1)


if __name__ == "__main__":
    # Need to import AIAnalyzer for benchmark
    from src.analyzers import AIAnalyzer
    main()
