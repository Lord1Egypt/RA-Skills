#!/usr/bin/env bash
# NOTE: On CIFS/SMB mounts, run with: bash scaffold.sh
# Creates a prompt engineering project structure with evaluation framework

set -euo pipefail

PROJECT_NAME="${1:-my-prompt-project}"
echo "Creating prompt engineering project: $PROJECT_NAME"

mkdir -p "$PROJECT_NAME"/{prompts,tests,evaluations,scripts}

# README with project structure
cat > "$PROJECT_NAME/prompts/system-v1.md" << 'SYSEOF'
# System Prompt v1

```
You are a helpful assistant that answers questions concisely.

Rules:
- Keep answers under 3 sentences unless more detail is requested
- If you don't know something, say so
- Use specific examples when helpful
```
SYSEOF

# Test cases
cat > "$PROJECT_NAME/tests/test_cases.jsonl" << 'TCEOF'
{"input": "What is Python?", "expected_contains": ["programming language"], "tags": ["basic"]}
{"input": "Explain recursion", "expected_contains": ["function", "calls itself"], "tags": ["concept"]}
{"input": "What is the meaning of life?", "expected_behavior": "acknowledge_uncertainty", "tags": ["edge_case"]}
TCEOF

# Evaluation script
cat > "$PROJECT_NAME/scripts/evaluate.py" << 'EVALEOF'
"""
Simple prompt evaluation runner.
Usage: python scripts/evaluate.py
"""

import json
import os
from openai import OpenAI

client = OpenAI()

def load_test_cases(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]

def run_evaluation(system_prompt: str, test_cases: list[dict], model: str = "gpt-4o-mini"):
    results = []
    for test in test_cases:
        response = client.chat.completions.create(
            model=model,
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test["input"]},
            ],
        )
        output = response.choices[0].message.content or ""

        passed = True
        if "expected_contains" in test:
            for term in test["expected_contains"]:
                if term.lower() not in output.lower():
                    passed = False
                    break

        results.append({
            "input": test["input"],
            "output": output[:200],
            "passed": passed,
            "tags": test.get("tags", []),
        })
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {test['input'][:60]}")

    pass_rate = sum(1 for r in results if r["passed"]) / len(results) * 100
    print(f"\nPass rate: {pass_rate:.0f}% ({sum(1 for r in results if r['passed'])}/{len(results)})")
    return results

if __name__ == "__main__":
    # Load system prompt
    with open("prompts/system-v1.md") as f:
        content = f.read()
    # Extract prompt from markdown code block
    import re
    match = re.search(r"```\n(.*?)```", content, re.DOTALL)
    system_prompt = match.group(1).strip() if match else content

    test_cases = load_test_cases("tests/test_cases.jsonl")
    print(f"Running {len(test_cases)} tests...\n")
    run_evaluation(system_prompt, test_cases)
EVALEOF

# .gitignore
cat > "$PROJECT_NAME/.gitignore" << 'GIEOF'
.env
evaluations/*.json
__pycache__/
GIEOF

# .env template
cat > "$PROJECT_NAME/.env.example" << 'ENVEOF'
OPENAI_API_KEY=sk-your-key-here
ENVEOF

echo ""
echo "Project '$PROJECT_NAME' created!"
echo ""
echo "Structure:"
echo "  prompts/      — System prompt versions (v1, v2, etc.)"
echo "  tests/        — Test cases in JSONL format"
echo "  evaluations/  — Evaluation results"
echo "  scripts/      — Evaluation and utility scripts"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  cp .env.example .env  # Add your API key"
echo "  pip install openai"
echo "  python scripts/evaluate.py"
