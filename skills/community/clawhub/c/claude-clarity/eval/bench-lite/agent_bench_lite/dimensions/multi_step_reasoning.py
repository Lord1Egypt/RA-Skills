"""
Multi-step Reasoning dimension.

Evaluates the agent's ability to chain multiple logical steps together to
reach a correct conclusion.  Tasks require deduction, arithmetic chains,
or logical inference that cannot be answered in a single step.
"""

from __future__ import annotations

import re

from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult


class MultiStepReasoningDimension(BaseDimension):
    """Can the agent chain logical steps to reach a conclusion?"""

    name = "multi_step_reasoning"
    display_name = "Multi-step Reasoning"
    description = (
        "Measures the agent's ability to perform chains of logical "
        "deduction, arithmetic, or inference that require multiple steps."
    )

    def get_tasks(self) -> list[Task]:
        return [
            # 1. Arithmetic chain.
            Task(
                task_id="msr_arithmetic_chain",
                description="Multi-step arithmetic word problem",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "A store sells notebooks for $4 each. If you buy 5 or more, "
                            "you get a 20% discount on the total. I bought 7 notebooks "
                            "and paid with a $50 bill. How much change do I receive? "
                            "Show your work step by step."
                        ),
                    },
                ],
                expected={
                    "correct_answer": "27.6",
                    "alt_answers": ["27.60", "$27.60", "$27.6"],
                    "reasoning_terms": ["discount", "total", "change"],
                },
            ),
            # 2. Logical deduction.
            Task(
                task_id="msr_logic_puzzle",
                description="Logical deduction puzzle",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "There are three boxes: A, B, and C.\n"
                            "- Box A says: 'The prize is in Box B.'\n"
                            "- Box B says: 'The prize is not in this box.'\n"
                            "- Box C says: 'The prize is in this box.'\n\n"
                            "Exactly one box tells the truth. Which box has the prize? "
                            "Explain your reasoning step by step."
                        ),
                    },
                ],
                expected={
                    # If A is true → prize in B → but B says "not in B" → B lies (ok)
                    #   C says "in C" → C lies (ok since prize is in B) → consistent!
                    # If B is true → prize not in B → A says "in B" → A lies (ok)
                    #   C says "in C" → need to check: if prize not in B and A lies,
                    #   prize could be in A or C. If C is also true that's 2 truths. contradiction.
                    #   So prize must be in A, C lies. but then only B tells truth. ✓
                    # Wait, let me re-examine: if B tells truth
                    # ("not in B"), A lies ("in B" is false, consistent),
                    #   prize is in A or C. If in C, then C also tells truth → 2 truths → contradiction.
                    #   So prize in A, only B tells truth.
                    # If C is true → prize in C → A says "in B" → A lies (ok, since in C)
                    #   B says "not in B" → prize is in C, not B, so B tells truth → 2 truths → contradiction.
                    # Answer: prize is in Box B (only A tells truth) OR in Box A (only B tells truth).
                    # Actually with "exactly one tells truth":
                    # Case A true: prize in B.
                    # B says "not in B" → false ✓. C says "in C" → false ✓. ONE truth. ✓
                    # Case B true: prize not in B. A says "in B" → false ✓. C says "in C" → must be false,
                    #   so prize not in C → prize in A. ONE truth. ✓
                    # Two valid answers depending on interpretation. Accept both.
                    "correct_answer": "b",
                    "alt_answers": ["box b", "box a", "a"],
                    "reasoning_terms": [
                        "truth", "lies", "contradict", "if",
                        "then", "assume", "therefore", "means",
                    ],
                },
            ),
            # 3. Unit conversion chain.
            Task(
                task_id="msr_unit_conversion",
                description="Multi-step unit conversion",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "A car travels at 90 kilometers per hour. How many meters "
                            "does it travel in 45 seconds? Show your step-by-step work."
                        ),
                    },
                ],
                expected={
                    # 90 km/h = 90000 m / 3600 s = 25 m/s
                    # 25 m/s × 45 s = 1125 m
                    "correct_answer": "1125",
                    "alt_answers": ["1,125", "1125 meters", "1125m", "1,125 meters"],
                    "reasoning_terms": ["meters per second", "m/s", "convert", "multiply", "per second"],
                },
            ),
            # 4. Age puzzle.
            Task(
                task_id="msr_age_puzzle",
                description="Multi-step age word problem",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Sarah is twice as old as Tom. In 6 years, Sarah will be "
                            "1.5 times as old as Tom. How old is Tom now? "
                            "Show your reasoning step by step."
                        ),
                    },
                ],
                expected={
                    # Let Tom = t, Sarah = 2t
                    # In 6 years: 2t + 6 = 1.5(t + 6)
                    # 2t + 6 = 1.5t + 9 → 0.5t = 3 → t = 6
                    # Tom is 6 years old, Sarah is 12.
                    "correct_answer": "6",
                    "alt_answers": ["6 years", "six", "tom is 6"],
                    "reasoning_terms": ["twice", "equation", "solve", "let", "years"],
                },
            ),
            # 5. Probability chain.
            Task(
                task_id="msr_probability",
                description="Multi-step probability problem",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "A bag contains 3 red balls and 5 blue balls. You draw two "
                            "balls without replacement. What is the probability that both "
                            "balls are blue? Express your answer as a simplified fraction. "
                            "Show your step-by-step work."
                        ),
                    },
                ],
                expected={
                    # P(first blue) = 5/8
                    # P(second blue | first blue) = 4/7
                    # P(both) = 5/8 × 4/7 = 20/56 = 5/14
                    "correct_answer": "5/14",
                    "alt_answers": ["5 / 14", "5/14", "five fourteenths"],
                    "reasoning_terms": ["first", "second", "without replacement", "multiply", "simplif"],
                },
            ),
        ]

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Check the final answer and the presence of reasoning steps."""
        response = await adapter.send_message(messages=task.input_messages)
        text = response.lower()

        correct: str = task.expected["correct_answer"].lower()
        alternatives: list[str] = [a.lower() for a in task.expected["alt_answers"]]
        reasoning_terms: list[str] = task.expected["reasoning_terms"]

        # Check if the correct answer appears in the response.
        all_answers = [correct] + alternatives
        answer_found = any(ans in text for ans in all_answers)

        # Check for reasoning / work shown.
        terms_found = sum(1 for term in reasoning_terms if term.lower() in text)
        reasoning_ratio = terms_found / len(reasoning_terms) if reasoning_terms else 1.0

        # Check for step structure (numbered steps, "step 1", bullet points, etc.)
        step_indicators = len(re.findall(r"(?:step\s*\d|^\s*\d+[\.\)]|\n-\s)", text, re.MULTILINE))
        has_structure = step_indicators >= 2

        # Scoring: answer correctness (50%), reasoning quality (30%), structure (20%).
        answer_score = 1.0 if answer_found else 0.0
        reasoning_score = min(reasoning_ratio, 1.0)
        structure_score = 1.0 if has_structure else 0.3

        score = 0.5 * answer_score + 0.3 * reasoning_score + 0.2 * structure_score

        message = (
            f"Answer {'found' if answer_found else 'NOT found'}, "
            f"reasoning terms: {terms_found}/{len(reasoning_terms)}, "
            f"step indicators: {step_indicators}"
        )

        return TaskResult(
            task_id=task.task_id,
            score=round(score, 4),
            passed=score >= 0.5,
            message=message,
            raw_response=response,
        )
