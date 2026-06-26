"""OpenClaw-local turn generation for negotiated SAFE offers.

This module owns the "brain" side of one negotiation turn. The shared
orchestrator still handles leases, turn order, delivery, signing, and
finalization; this module asks the local OpenClaw-side model to draft the
actual offer JSON for the current user's role.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass
from json import JSONDecoder
from typing import Any, Callable


MAX_MODEL_RETRIES = 3


def _constraint_value(constraints: dict, field: str, bound: str, default: Any = None) -> Any:
    nested = constraints.get(field)
    if isinstance(nested, dict) and bound in nested:
        return nested[bound]
    flat_key = f"{field}_{bound}"
    if flat_key in constraints:
        return constraints[flat_key]
    return default


def _required_value(constraints: dict, field: str) -> bool:
    nested = constraints.get(field)
    if isinstance(nested, dict):
        return bool(nested.get("required", False))
    return bool(constraints.get(f"{field}_required", False))


def _amount_bounds(constraints: dict) -> tuple[Any, Any]:
    amount_min = _constraint_value(constraints, "investment_amount", "min", None)
    amount_max = _constraint_value(constraints, "investment_amount", "max", None)
    if amount_min is not None or amount_max is not None:
        return amount_min, amount_max if amount_max is not None else amount_min
    amount = constraints.get("investment_amount")
    return amount, amount


def _amount_constraint_line(amount_min: Any, amount_max: Any) -> str:
    if amount_min is None and amount_max is None:
        return "- Investment amount / check size: no private bound provided"
    return f"- Investment amount / check size: {_money(amount_min)} to {_money(amount_max)}"


def _money(value: Any) -> str:
    try:
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return "$0"


def _percent(value: Any) -> str:
    try:
        return f"{float(value):.0%}"
    except (TypeError, ValueError):
        return "0%"


def _strip_fences(text: str) -> str:
    text = (text or "").strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
        if text.startswith("json\n"):
            text = text[5:].strip()
    return text


def parse_offer_text(text: str) -> dict:
    """Parse the model's JSON-only offer response."""
    cleaned = _strip_fences(text)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        payload = json.loads(cleaned[start:end + 1])
    if not isinstance(payload, dict):
        raise ValueError("offer response must be a JSON object")
    return payload


def _json_suffix(text: str) -> dict:
    """Return the last full JSON object in a noisy CLI output string."""
    decoder = JSONDecoder()
    best = None
    envelope = None
    for i, ch in enumerate(text or ""):
        if ch != "{":
            continue
        try:
            obj, end = decoder.raw_decode(text[i:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            best = obj
            if "payloads" in obj or "outputs" in obj or (
                isinstance(obj.get("meta"), dict)
                and obj["meta"].get("finalAssistantVisibleText")
            ):
                envelope = obj
    if envelope is not None:
        return envelope
    if best is None:
        raise ValueError("no trailing JSON object found in OpenClaw output")
    return best


def _openclaw_text_from_json(payload: dict) -> str:
    for key in ("payloads", "outputs"):
        values = payload.get(key)
        if isinstance(values, list) and values:
            first = values[0] if isinstance(values[0], dict) else {}
            if first.get("text"):
                return str(first["text"])
    meta = payload.get("meta")
    if isinstance(meta, dict) and meta.get("finalAssistantVisibleText"):
        return str(meta["finalAssistantVisibleText"])
    raise ValueError("OpenClaw JSON output did not contain text")


def build_turn_prompt(
    *,
    role: str,
    constraints: dict,
    history: list[dict],
    feedback: list[str] | None = None,
) -> str:
    """Build the negotiation turn request for the local OpenClaw agent."""
    cap_min = _constraint_value(constraints, "valuation_cap", "min", 0)
    cap_max = _constraint_value(constraints, "valuation_cap", "max", 0)
    discount_min = _constraint_value(constraints, "discount_rate", "min", 0)
    discount_max = _constraint_value(constraints, "discount_rate", "max", 0.25)
    amount_min, amount_max = _amount_bounds(constraints)
    pro_rata_required = _required_value(constraints, "pro_rata")
    mfn_required = _required_value(constraints, "mfn")
    counterparty = "investor" if role == "founder" else "founder"
    history_json = json.dumps(history, indent=2, sort_keys=True)
    feedback_text = "\n".join(f"- {item}" for item in (feedback or [])) or "- none"

    return f"""You are the user's OpenClaw agent negotiating a SAFE as the {role}.

APOA authorization constraints are hard boundaries. You may not propose or accept
terms outside them:
- Valuation cap: {_money(cap_min)} to {_money(cap_max)}
{_amount_constraint_line(amount_min, amount_max)}
- Discount rate: {_percent(discount_min)} to {_percent(discount_max)}
- Pro-rata rights required: {str(pro_rata_required).lower()}
- MFN required: {str(mfn_required).lower()}

Negotiation strategy:
- Be concise, professional, and commercially realistic.
- Every move should have commercial substance: acknowledge the other side's
  position, explain the business rationale for your response, and make a
  concrete offer, concession, or acceptance.
- If the {counterparty}'s latest offer already matches your stated goals or is
  clearly favorable inside your APOA boundaries, accept it. Avoid unnecessary extra rounds.
- If the latest offer is acceptable but not obviously excellent, consider one
  final constructive counter before accepting.
- Keep each message polished and substantive: 3 to 5 sentences, no boilerplate,
  no legal disclaimers, and keep authorization details out of counterparty-facing text.
- The founder generally prefers a higher valuation cap and lower discount.
- The investor generally prefers a lower valuation cap and adequate discount.
- Keep your private authorization range confidential.

Validation feedback to fix from prior attempts:
{feedback_text}

History so far, oldest first:
{history_json}

Respond with a JSON object using this exact shape:
{{
  "type": "offer" | "counter" | "accept",
  "terms": {{
    "valuation_cap": <integer dollars>,
    "investment_amount": <integer dollars or null>,
    "discount_rate": <decimal between 0 and 1>,
    "pro_rata": <boolean>,
    "mfn": <boolean>
  }},
  "message": "<short message to the {counterparty}>"
}}
"""


@dataclass
class OpenClawTurnAgent:
    role: str
    constraints: dict
    runner: Callable = subprocess.run
    backend: str = ""
    model: str = ""

    async def make_offer(self, history: list[dict], feedback: list[str] | None = None) -> dict:
        prompt = build_turn_prompt(
            role=self.role,
            constraints=self.constraints,
            history=history,
            feedback=feedback,
        )
        return await self._make_offer_openclaw(prompt)

    async def _make_offer_openclaw(self, prompt: str) -> dict:
        session_id = f"negotiate-turn-{self.role}-{uuid.uuid4().hex[:8]}"
        cmd = [
            "openclaw",
            "agent",
            "--local",
            "--json",
            "--session-id",
            session_id,
            "--message",
            prompt,
        ]
        if self.model or os.environ.get("NEGOTIATE_SAFE_TURN_MODEL"):
            cmd.extend(["--model", self.model or os.environ["NEGOTIATE_SAFE_TURN_MODEL"]])

        def _run() -> subprocess.CompletedProcess:
            return self.runner(cmd, capture_output=True, text=True, timeout=180)

        result = await asyncio.to_thread(_run)
        if result.returncode != 0:
            err = (result.stderr or result.stdout or "").strip()
            raise RuntimeError(f"openclaw agent turn failed: {err[:500]}")
        payload = _json_suffix((result.stdout or "") + "\n" + (result.stderr or ""))
        return parse_offer_text(_openclaw_text_from_json(payload))


async def make_validated_offer(
    *,
    agent: OpenClawTurnAgent,
    history: list[dict],
    validate: Callable[[dict], tuple[bool, str]],
    constraint_validate: Callable[[dict], tuple[bool, list[str]]],
) -> dict:
    """Ask the local OpenClaw turn agent until the offer validates."""
    feedback: list[str] = []
    for _attempt in range(MAX_MODEL_RETRIES):
        offer = await agent.make_offer(history, feedback=feedback)
        ok, reason = validate(offer)
        if not ok:
            feedback.append(f"Your previous response was invalid: {reason}")
            continue
        if offer.get("type") == "accept" and not offer.get("terms"):
            for prior in reversed(history):
                if prior.get("terms"):
                    offer["terms"] = prior["terms"]
                    break
        if offer.get("type") in ("offer", "counter", "accept"):
            constraint_ok, violations = constraint_validate(offer.get("terms") or {})
            if not constraint_ok:
                feedback.append(
                    "Your previous offer violated APOA constraints: "
                    + ", ".join(violations)
                )
                continue
        return offer
    raise RuntimeError("local OpenClaw turn agent failed to produce a valid offer")
