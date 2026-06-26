"""
LLM-as-Judge for evaluating skill improvement candidates.

Supports multiple backends:
- Claude API (anthropic SDK)
- OpenAI API
- Local/mock (for testing without API keys)

The judge evaluates candidates on dimensions that rules cannot capture:
- Semantic quality of proposed changes
- Instruction clarity and specificity
- Consistency with existing skill style
- Potential for unintended side effects
"""

from __future__ import annotations

import json
import os
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class JudgeVerdict:
    """Structured verdict from an LLM judge."""
    score: float  # 0.0-1.0
    decision: str  # "approve" | "conditional" | "reject"
    reasoning: str
    dimensions: dict[str, float] = field(default_factory=dict)
    # Per-dimension scores: clarity, specificity, consistency, safety
    confidence: float = 0.8
    suggestions: list[str] = field(default_factory=list)


@dataclass
class JudgeConfig:
    """Configuration for the LLM judge."""
    backend: str = "mock"  # "claude" | "openai" | "mock"
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.0  # Deterministic for reproducibility
    max_tokens: int = 1024
    base_url: str | None = None  # Custom API base URL (e.g. DashScope proxy)
    dimensions: list[str] = field(default_factory=lambda: [
        "clarity", "specificity", "consistency", "safety"
    ])
    # Thresholds
    approve_threshold: float = 0.75
    reject_threshold: float = 0.40


JUDGE_PROMPT_TEMPLATE = """You are an expert skill evaluator. Assess this proposed improvement to a skill.

## Target Skill
{target_content}

## Proposed Change
- Category: {category}
- Risk Level: {risk_level}
- Description: {description}
- Proposed Content:
{proposed_content}

## Evaluation Dimensions
Rate each dimension 0.0-1.0:

1. **Clarity**: Is the proposed change clear and unambiguous? Will an AI agent understand exactly what to do?
2. **Specificity**: Does it use concrete examples/values instead of vague language ("various", "etc.")?
3. **Consistency**: Does it match the existing skill's style, terminology, and structure?
4. **Safety**: Could this change cause unintended behavior or break existing functionality?

## Output Format
Respond with ONLY a JSON object:
{{
  "clarity": 0.X,
  "specificity": 0.X,
  "consistency": 0.X,
  "safety": 0.X,
  "overall": 0.X,
  "decision": "approve|conditional|reject",
  "reasoning": "one paragraph explaining your assessment",
  "suggestions": ["improvement suggestion 1", "..."]
}}"""


class LLMJudge:
    """LLM-based judge for evaluating skill improvement candidates."""

    def __init__(self, config: JudgeConfig | None = None):
        self.config = config or JudgeConfig()
        self._backend = self._init_backend()

    def _init_backend(self) -> Callable:
        if self.config.backend == "claude":
            return self._call_claude
        elif self.config.backend == "openai":
            return self._call_openai
        else:
            return self._call_mock

    def evaluate(self, candidate: dict, target_content: str = "") -> JudgeVerdict:
        """Evaluate a candidate using the configured LLM backend."""
        prompt = self._build_prompt(candidate, target_content)
        raw_response = self._backend(prompt)
        return self._parse_response(raw_response)

    def evaluate_batch(self, candidates: list[dict], target_content: str = "") -> list[JudgeVerdict]:
        """Evaluate multiple candidates."""
        return [self.evaluate(c, target_content) for c in candidates]

    def _build_prompt(self, candidate: dict, target_content: str) -> str:
        plan = candidate.get("execution_plan", {})
        proposed_content = "\n".join(plan.get("content_lines", ["(no content specified)"]))
        return JUDGE_PROMPT_TEMPLATE.format(
            target_content=target_content[:2000] if target_content else "(not available)",
            category=candidate.get("category", "unknown"),
            risk_level=candidate.get("risk_level", "unknown"),
            description=candidate.get("proposed_change_summary", candidate.get("title", "")),
            proposed_content=proposed_content[:1000],
        )

    def _call_claude(self, prompt: str) -> str:
        """Call Claude API. Supports custom base_url (e.g. DashScope proxy) via config or env."""
        try:
            import anthropic
            kwargs = {}
            base_url = self.config.base_url or os.environ.get("ANTHROPIC_BASE_URL")
            if base_url:
                kwargs["base_url"] = base_url
            client = anthropic.Anthropic(**kwargs)  # Uses ANTHROPIC_API_KEY env var
            response = client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except ImportError:
            logger.warning("anthropic SDK not installed, falling back to mock")
            return self._call_mock(prompt)
        except Exception as e:
            logger.warning(f"Claude API call failed: {e}, falling back to mock")
            return self._call_mock(prompt)

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            import openai
            client = openai.OpenAI()  # Uses OPENAI_API_KEY env var
            response = client.chat.completions.create(
                model=self.config.model if "gpt" in self.config.model else "gpt-4o-mini",
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except ImportError:
            logger.warning("openai SDK not installed, falling back to mock")
            return self._call_mock(prompt)
        except Exception as e:
            logger.warning(f"OpenAI API call failed: {e}, falling back to mock")
            return self._call_mock(prompt)

    def _call_mock(self, prompt: str) -> str:
        """Deterministic mock for testing without API keys."""
        # Analyze the prompt content to produce meaningful mock scores
        has_content = "(no content specified)" not in prompt
        is_low_risk = "low" in prompt.lower()
        is_docs = any(cat in prompt.lower() for cat in ["docs", "reference", "guardrail"])

        clarity = 0.8 if has_content else 0.4
        specificity = 0.7 if has_content else 0.3
        consistency = 0.8 if is_docs else 0.5
        safety = 0.9 if is_low_risk else 0.5
        overall = (clarity + specificity + consistency + safety) / 4

        if overall >= 0.75:
            decision = "approve"
        elif overall >= 0.40:
            decision = "conditional"
        else:
            decision = "reject"

        result = {
            "clarity": clarity,
            "specificity": specificity,
            "consistency": consistency,
            "safety": safety,
            "overall": overall,
            "decision": decision,
            "reasoning": f"Mock evaluation: content={'present' if has_content else 'missing'}, risk={'low' if is_low_risk else 'elevated'}, category={'docs' if is_docs else 'other'}.",
            "suggestions": [] if decision == "approve" else ["Add more specific content"],
        }
        return json.dumps(result)

    def _parse_response(self, raw: str) -> JudgeVerdict:
        """Parse LLM response into structured verdict."""
        try:
            # Extract JSON from response (handle markdown code blocks)
            text = raw.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            data = json.loads(text)
            dimensions = {
                d: data.get(d, 0.5) for d in self.config.dimensions
            }
            overall = data.get("overall", sum(dimensions.values()) / len(dimensions))
            decision = data.get("decision", "conditional")

            # Validate decision against thresholds
            if overall >= self.config.approve_threshold and decision != "reject":
                decision = "approve"
            elif overall < self.config.reject_threshold:
                decision = "reject"

            return JudgeVerdict(
                score=max(0.0, min(1.0, overall)),
                decision=decision,
                reasoning=data.get("reasoning", ""),
                dimensions=dimensions,
                confidence=0.9 if self.config.backend != "mock" else 0.5,
                suggestions=data.get("suggestions", []),
            )
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.warning(f"Failed to parse LLM response: {e}")
            return JudgeVerdict(
                score=0.5,
                decision="conditional",
                reasoning=f"Parse error: {e}. Raw: {raw[:200]}",
                dimensions={d: 0.5 for d in self.config.dimensions},
                confidence=0.2,
                suggestions=["Manual review recommended — LLM response parsing failed"],
            )
