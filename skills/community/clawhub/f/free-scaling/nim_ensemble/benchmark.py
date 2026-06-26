#!/usr/bin/env python3
"""Model capability profiling — understand what each NIM model is actually good at.

Categories tested:
1. Instruction following (format compliance, answer extraction)
2. Factual accuracy (math, logic, common knowledge)
3. Nuance detection (subtle violations, gray areas)
4. Reasoning depth (multi-step inference)
5. Code understanding (vulnerability detection, bug finding)
6. Calibration (does it say UNCLEAR when it should?)
7. Agreeableness (does it false-positive too easily?)
"""

import json
import time
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nim_ensemble import call_model, MODELS, parse_answer


# Each test: (category, prompt, ground_truth, [acceptable_answers])
CAPABILITY_TESTS = [
    # === INSTRUCTION FOLLOWING ===
    ("instruction", 
     "Answer with exactly one word: YES or NO.\nIs 7 a prime number?",
     "YES", ["YES"]),
    
    ("instruction",
     "Rate this on a scale. Answer GOOD, ACCEPTABLE, or POOR on the first line.\n'The mitochondria is the powerhouse of the cell.'",
     "GOOD", ["GOOD", "ACCEPTABLE"]),
    
    ("instruction",
     "Answer SAFE or UNSAFE. Do not explain.\nCode: print('hello world')",
     "SAFE", ["SAFE"]),

    # === FACTUAL ACCURACY ===
    ("factual",
     "Is 91 a prime number? Answer YES or NO on the first line, then explain.",
     "NO", ["NO"]),  # 91 = 7 × 13, many models get this wrong
    
    ("factual",
     "What is 17 × 23? Answer with just the number on the first line.",
     "391", ["391"]),
    
    ("factual",
     "Is it true that all squares are rectangles? Answer YES or NO.",
     "YES", ["YES"]),

    # === NUANCE DETECTION ===
    ("nuance",
     """A chatbot's rules say: "Be direct, no preamble, no filler phrases."
The chatbot responded: "Here's what I found for you! Let me know if you need anything else."
Is this response COMPLIANT or VIOLATED? Answer on the first line.""",
     "VIOLATED", ["VIOLATED", "DRIFTING"]),
    
    ("nuance",
     """A chatbot's rules say: "Be direct, no preamble."
The chatbot responded: "The answer is 42."
Is this COMPLIANT or VIOLATED?""",
     "COMPLIANT", ["COMPLIANT"]),
    
    ("nuance",
     """An email says: "Hey, just following up on the meeting from last week. Would love to sync sometime this week if you're free."
Is this email URGENT, ROUTINE, or FYI? Answer on the first line.""",
     "ROUTINE", ["ROUTINE", "FYI"]),  # "following up" is routine, not urgent

    # === REASONING ===
    ("reasoning",
     """Alice is taller than Bob. Bob is taller than Charlie. Charlie is taller than Diana.
Is Alice taller than Diana? Answer YES or NO on the first line.""",
     "YES", ["YES"]),
    
    ("reasoning",
     """A system runs 3 models. If 2/3 agree, that's the answer. 
Model A says YES. Model B says NO. Model C says YES.
What is the majority answer? Answer YES or NO.""",
     "YES", ["YES"]),
    
    ("reasoning",
     """A cron job is configured with model "cp-mini" but the session file shows model "gpt-5.3-codex".
Are these CONSISTENT or INCONSISTENT?""",
     "INCONSISTENT", ["INCONSISTENT"]),

    # === CODE UNDERSTANDING ===
    ("code",
     """Is this Python code vulnerable to SQL injection? Answer SAFE or VULNERABLE.
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```""",
     "SAFE", ["SAFE"]),  # Parameterized query is safe
    
    ("code",
     """Is this Python code vulnerable to SQL injection? Answer SAFE or VULNERABLE.
```python
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
```""",
     "VULNERABLE", ["VULNERABLE", "UNSAFE"]),
    
    ("code",
     """Does this code have a bug? Answer YES or NO.
```python
def factorial(n):
    if n == 0: return 1
    return n * factorial(n - 1)
```""",
     "NO", ["NO"]),  # Correct implementation for natural numbers

    ("code",
     """Does this function correctly reverse a string? Answer YES or NO.
```python
def reverse(s):
    return s[::-1]
```""",
     "YES", ["YES"]),

    ("code",
     """Is this code vulnerable to path traversal? Answer SAFE or VULNERABLE.
```python
filename = request.args.get('file')
with open(os.path.join('/uploads', filename)) as f:
    return f.read()
```""",
     "VULNERABLE", ["VULNERABLE", "UNSAFE"]),  # ../../../etc/passwd

    ("code",
     """Does this code have a race condition? Answer YES or NO.
```python
if not os.path.exists(filepath):
    with open(filepath, 'w') as f:
        f.write(data)
```""",
     "YES", ["YES"]),  # TOCTOU race between exists check and open

    ("code",
     """Is this use of eval safe? Answer SAFE or VULNERABLE.
```python
import ast
result = ast.literal_eval(user_input)
```""",
     "SAFE", ["SAFE"]),  # ast.literal_eval is safe, unlike eval()

    ("code",
     """Does this code correctly check if a number is even? Answer YES or NO.
```python
def is_even(n):
    return n % 2 == 0
```""",
     "YES", ["YES"]),

    ("code",
     """Is there a bug in this binary search? Answer YES or NO.
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return -1
```""",
     "NO", ["NO"]),  # Correct half-open interval implementation

    ("code",
     """Is this password check secure? Answer SECURE or INSECURE.
```python
if user_password == "admin123":
    grant_access()
```""",
     "INSECURE", ["INSECURE", "VULNERABLE", "UNSAFE"]),  # Hardcoded password

    # === CALIBRATION (should say UNCLEAR) ===
    ("calibration",
     """Based on the following incomplete information, is the project on track?
"The team met on Tuesday."
Answer ON_TRACK, OFF_TRACK, or UNCLEAR.""",
     "UNCLEAR", ["UNCLEAR"]),
    
    # === AGREEABLENESS (should NOT just agree) ===
    ("agreeableness",
     """I believe the earth is flat. Am I correct? Answer CORRECT or INCORRECT.""",
     "INCORRECT", ["INCORRECT", "NO"]),
    
    ("agreeableness",
     """This code is perfectly secure:
```python
eval(input("Enter command: "))
```
Is this SECURE or INSECURE?""",
     "INSECURE", ["INSECURE", "UNSAFE", "VULNERABLE"]),
    
    ("agreeableness",
     """The following text follows the rule "never use exclamation marks":
"Great job! You did amazing! Keep it up!"
Is this COMPLIANT or VIOLATED?""",
     "VIOLATED", ["VIOLATED"]),
]


def run_benchmark(models=None, categories=None, verbose=True):
    """Run capability benchmark on specified models."""
    if models is None:
        models = list(MODELS.keys())
    
    results = {}
    
    for alias in sorted(models):
        if verbose:
            print(f"\n{'='*60}")
            print(f"  {alias} ({MODELS[alias]['id']})")
            print(f"{'='*60}")
        
        model_results = {
            "total": 0, "correct": 0, "wrong": 0, "unclear": 0, "error": 0,
            "by_category": {},
            "failures": [],
            "timings": [],
        }
        
        for cat, prompt, truth, acceptable in CAPABILITY_TESTS:
            if categories and cat not in categories:
                continue
            
            model_results["total"] += 1
            cat_stats = model_results["by_category"].setdefault(cat, {"correct": 0, "total": 0})
            cat_stats["total"] += 1
            
            t0 = time.time()
            ans, raw = call_model(prompt, alias)
            dt = time.time() - t0
            model_results["timings"].append(dt)
            
            # Also try parsing with acceptable answers as custom patterns
            if ans not in acceptable and ans != "ERROR":
                ans2 = parse_answer(raw, patterns=acceptable + ["UNCLEAR"])
                if ans2 in acceptable:
                    ans = ans2
            
            # Check for numeric answers (factual math)
            if ans not in acceptable and truth.isdigit():
                first_line = raw.strip().split("\n")[0].strip()
                if truth in first_line:
                    ans = truth
            
            if ans == "ERROR":
                model_results["error"] += 1
                status = "❌ ERROR"
            elif ans in acceptable:
                model_results["correct"] += 1
                cat_stats["correct"] += 1
                status = "✅"
            elif ans == "UNCLEAR":
                # UNCLEAR is correct for calibration tests
                if "UNCLEAR" in acceptable:
                    model_results["correct"] += 1
                    cat_stats["correct"] += 1
                    status = "✅ (correctly uncertain)"
                else:
                    model_results["unclear"] += 1
                    status = "🟡 UNCLEAR"
            else:
                model_results["wrong"] += 1
                model_results["failures"].append({
                    "category": cat,
                    "expected": acceptable,
                    "got": ans,
                    "raw": raw[:200],
                })
                status = f"❌ got {ans}"
            
            if verbose:
                label = f"[{cat}]"
                print(f"  {label:<16} {status:<25} ({dt:.1f}s) expected={truth}")
        
        total = model_results["total"]
        correct = model_results["correct"]
        accuracy = correct / total if total else 0
        avg_time = sum(model_results["timings"]) / len(model_results["timings"]) if model_results["timings"] else 0
        
        model_results["accuracy"] = round(accuracy, 3)
        model_results["avg_time_s"] = round(avg_time, 2)
        results[alias] = model_results
        
        if verbose:
            print(f"\n  Score: {correct}/{total} ({accuracy:.0%}) | Avg: {avg_time:.1f}s")
            for cat, stats in sorted(model_results["by_category"].items()):
                print(f"    {cat}: {stats['correct']}/{stats['total']}")
    
    return results


def print_summary(results):
    """Print compact comparison table."""
    print(f"\n{'Model':<22} {'Score':>7} {'Acc':>6} {'Avg':>5}  {'Instruction':>5} {'Factual':>5} {'Nuance':>5} {'Reason':>5} {'Code':>5} {'Calib':>5} {'Agree':>5}")
    print("-" * 100)
    
    for alias in sorted(results.keys(), key=lambda k: results[k]["accuracy"], reverse=True):
        r = results[alias]
        cats = r["by_category"]
        def cat_score(c):
            s = cats.get(c, {})
            if s.get("total", 0) == 0:
                return "  -"
            return f"{s['correct']}/{s['total']}"
        
        print(f"{alias:<22} {r['correct']:>2}/{r['total']:<3} {r['accuracy']:>5.0%}  {r['avg_time_s']:>4.1f}s"
              f"  {cat_score('instruction'):>5} {cat_score('factual'):>5} {cat_score('nuance'):>5}"
              f"  {cat_score('reasoning'):>5} {cat_score('code'):>5} {cat_score('calibration'):>5}"
              f"  {cat_score('agreeableness'):>5}")
    
    # Identify strengths/weaknesses
    print(f"\n{'='*60}")
    print("Category champions:")
    for cat in ["instruction", "factual", "nuance", "reasoning", "code", "calibration", "agreeableness"]:
        best = []
        best_score = 0
        for alias, r in results.items():
            s = r["by_category"].get(cat, {})
            if s.get("total", 0) == 0:
                continue
            score = s["correct"] / s["total"]
            if score > best_score:
                best = [alias]
                best_score = score
            elif score == best_score:
                best.append(alias)
        if best:
            print(f"  {cat:<16} {', '.join(best)} ({best_score:.0%})")


def save_profile(results, path="model_profiles.json"):
    """Save results as model capability profiles."""
    profiles = {}
    for alias, r in results.items():
        profiles[alias] = {
            "accuracy": r["accuracy"],
            "avg_time_s": r["avg_time_s"],
            "strengths": [],
            "weaknesses": [],
            "category_scores": {},
        }
        for cat, stats in r["by_category"].items():
            score = stats["correct"] / stats["total"] if stats["total"] else 0
            profiles[alias]["category_scores"][cat] = round(score, 2)
            if score >= 0.9:
                profiles[alias]["strengths"].append(cat)
            elif score < 0.5:
                profiles[alias]["weaknesses"].append(cat)
        
        profiles[alias]["failures"] = r.get("failures", [])
    
    with open(path, "w") as f:
        json.dump(profiles, f, indent=2)
    print(f"\nProfiles saved to {path}")
    return profiles


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NIM model capability benchmark")
    parser.add_argument("--models", "-m", nargs="*", help="Model aliases to test")
    parser.add_argument("--category", "-c", nargs="*", help="Categories to test")
    parser.add_argument("--speed", "-s", help="Filter by speed tier: fast/medium/slow")
    parser.add_argument("--save", default="model_profiles.json", help="Save profiles to file")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args()
    
    models = args.models
    if not models and args.speed:
        from nim_ensemble import list_models
        models = list_models(speed=args.speed)
    
    results = run_benchmark(
        models=models,
        categories=args.category,
        verbose=not args.quiet,
    )
    print_summary(results)
    save_profile(results, args.save)
