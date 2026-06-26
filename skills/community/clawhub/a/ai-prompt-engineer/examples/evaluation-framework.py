"""
Prompt evaluation framework.
Compares prompt variations using automated metrics and LLM-as-judge.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Callable
from openai import OpenAI

client = OpenAI()

# ── Data Types ────────────────────────────────────────────────


@dataclass
class TestCase:
    """A single test case with input and expected output."""

    input: str
    expected: str
    tags: list[str] = field(default_factory=list)


@dataclass
class PromptVariant:
    """A prompt variant to evaluate."""

    name: str
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.0


@dataclass
class EvalResult:
    """Result of evaluating one test case with one prompt variant."""

    variant: str
    test_input: str
    expected: str
    actual: str
    scores: dict[str, float]
    latency_ms: float


# ── Test Cases ────────────────────────────────────────────────

EXTRACTION_TESTS = [
    TestCase(
        input="Contact us at hello@acme.com or call 555-0123. We're at 123 Main St, Portland, OR 97201.",
        expected='{"company_name": "Acme", "contact_email": "hello@acme.com", "phone": "+15550123"}',
        tags=["complete"],
    ),
    TestCase(
        input="Visit our website at example.com for more info.",
        expected='{"company_name": null, "contact_email": null, "confidence": 0.2}',
        tags=["minimal"],
    ),
    TestCase(
        input="The weather is nice today.",
        expected='{"error": "No business information found"}',
        tags=["negative"],
    ),
]

# ── Evaluation Metrics ────────────────────────────────────────


def json_valid(actual: str) -> float:
    """Check if output is valid JSON. Returns 1.0 or 0.0."""
    try:
        json.loads(actual)
        return 1.0
    except (json.JSONDecodeError, TypeError):
        return 0.0


def field_accuracy(actual: str, expected: str) -> float:
    """Compare JSON fields between actual and expected."""
    try:
        actual_obj = json.loads(actual)
        expected_obj = json.loads(expected)
    except (json.JSONDecodeError, TypeError):
        return 0.0

    if not isinstance(actual_obj, dict) or not isinstance(expected_obj, dict):
        return 0.0

    expected_keys = set(expected_obj.keys())
    if not expected_keys:
        return 1.0

    matches = sum(
        1
        for key in expected_keys
        if key in actual_obj and actual_obj[key] == expected_obj[key]
    )
    return matches / len(expected_keys)


def llm_judge(actual: str, expected: str, test_input: str) -> float:
    """Use GPT-4 as a judge to rate output quality 0-1."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evaluation judge. Rate how well the 'Actual Output' "
                    "matches the intent of the 'Expected Output' for the given input. "
                    "Return ONLY a number between 0.0 and 1.0."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Input: {test_input}\n"
                    f"Expected Output: {expected}\n"
                    f"Actual Output: {actual}\n\n"
                    "Score (0.0-1.0):"
                ),
            },
        ],
    )
    try:
        return float(response.choices[0].message.content.strip())
    except (ValueError, AttributeError):
        return 0.0


# ── Runner ────────────────────────────────────────────────────


def evaluate(
    variants: list[PromptVariant],
    test_cases: list[TestCase],
    metrics: dict[str, Callable] | None = None,
) -> list[EvalResult]:
    """Run all variants against all test cases and score them."""

    if metrics is None:
        metrics = {
            "json_valid": lambda a, e, i: json_valid(a),
            "field_accuracy": lambda a, e, i: field_accuracy(a, e),
            "llm_judge": llm_judge,
        }

    results: list[EvalResult] = []

    for variant in variants:
        print(f"\nEvaluating: {variant.name}")
        for i, test in enumerate(test_cases):
            start = time.monotonic()

            response = client.chat.completions.create(
                model=variant.model,
                temperature=variant.temperature,
                messages=[
                    {"role": "system", "content": variant.system_prompt},
                    {"role": "user", "content": test.input},
                ],
            )
            actual = response.choices[0].message.content or ""
            latency = (time.monotonic() - start) * 1000

            scores = {
                name: fn(actual, test.expected, test.input)
                for name, fn in metrics.items()
            }

            result = EvalResult(
                variant=variant.name,
                test_input=test.input[:80],
                expected=test.expected[:80],
                actual=actual[:80],
                scores=scores,
                latency_ms=round(latency, 1),
            )
            results.append(result)
            print(f"  Test {i + 1}: {scores}")

    return results


def summarize(results: list[EvalResult]) -> None:
    """Print summary table of evaluation results."""
    from collections import defaultdict

    variant_scores: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )

    for r in results:
        for metric, score in r.scores.items():
            variant_scores[r.variant][metric].append(score)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    for variant, metrics in variant_scores.items():
        print(f"\n{variant}:")
        for metric, scores in metrics.items():
            avg = sum(scores) / len(scores)
            print(f"  {metric}: {avg:.2f} (n={len(scores)})")


# ── Example Usage ─────────────────────────────────────────────

if __name__ == "__main__":
    variants = [
        PromptVariant(
            name="v1-basic",
            system_prompt="Extract business information as JSON from the text.",
        ),
        PromptVariant(
            name="v2-structured",
            system_prompt=(
                "Extract business information from the text. "
                "Output ONLY valid JSON with keys: company_name, contact_email, phone. "
                "Use null for missing fields. "
                'If no business info found, return: {"error": "No business information found"}'
            ),
        ),
    ]

    results = evaluate(variants, EXTRACTION_TESTS)
    summarize(results)
