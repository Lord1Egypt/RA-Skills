#!/usr/bin/env python3
"""
Content Scorer — score_content.py
ClawHub skill: content-scorer v1.0.0

Scores marketing copy on 6 dimensions → 0-100 Content Resonance Score.
Uses local MLX server (free) by default; falls back to Claude Haiku.

Usage:
    python3 score_content.py --demo                           # zero API cost demo
    python3 score_content.py --version                        # print version
    python3 score_content.py "Your copy here"
    python3 score_content.py "Your copy" --platform=linkedin --audience="first-time buyers"
    python3 score_content.py "Your copy" --rewrite
    python3 score_content.py --compare "Hook A" "Hook B" "Hook C"
    python3 score_content.py "Your copy" --compliance-only
    python3 score_content.py "Your copy" --format=json
    LLM_BACKEND=local python3 score_content.py "Your copy"   # free local
    LLM_BACKEND=haiku python3 score_content.py "Your copy"   # Claude Haiku
"""
import argparse
import json
import os
import sys
import re

VERSION = "1.0.2"

# ---------------------------------------------------------------------------
# Demo mode — zero API cost, built-in sample copy + pre-canned scores
# ---------------------------------------------------------------------------

DEMO_COPY = (
    "Most buyers don't realize they're losing $340/month by waiting. "
    "If you've been browsing homes in your target area, you already know what you want — "
    "the only question is whether you'll be the one who gets it. "
    "Drop your zip below and I'll pull your numbers in 5 minutes."
)

DEMO_RESULT = {
    "hook_strength": {
        "score": 9,
        "reason": "Strong loss-framing pattern interrupt with concrete dollar figure.",
        "improvement": "Already strong — could add a curiosity gap before the number."
    },
    "emotional_resonance": {
        "score": 8,
        "reason": "Speaks directly to the browser's identity and aspiration.",
        "improvement": "Add a brief future-pacing line to deepen the ownership vision."
    },
    "nlp_technique": {
        "score": 8,
        "detected": ["presupposition", "future_pacing", "embedded_command"],
        "missing": "pacing_leading — could open with a 'most people' statement to create social proof.",
        "improvement": "Open with: 'Most buyers in your situation are doing X right now...' before the hook."
    },
    "specificity": {
        "score": 9,
        "reason": "$340/month, 5 minutes — all concrete.",
        "improvement": "Could add a timeframe: 'before the rate window closes Thursday'."
    },
    "cta_strength": {
        "score": 9,
        "reason": "Assume-the-close CTA with no exit ramp.",
        "improvement": "Already strong."
    },
    "compliance": {
        "score": 10,
        "violations": []
    },
    "overall_comment": "Strong hook and CTA. Weakest point is the missing pacing/leading opener — add social proof framing at the top.",
    "composite": 88,
    "backend": "demo (no API call)"
}

# ---------------------------------------------------------------------------
# Compliance check — local, no API call
# ---------------------------------------------------------------------------

FORBIDDEN_WORDS = [
    "pre-approval", "pre-approved", "pre-qualify", "specialist",
    "mortgage", "lending", "rates", "loan", "showings", "tours",
    "transfer", "connect", "team", "agent", "department",
    "qualify for", "AWESOME",
]

def compliance_check(copy: str) -> list:
    violations = []
    copy_lower = copy.lower()
    for word in FORBIDDEN_WORDS:
        if re.search(r'\b' + re.escape(word.lower()) + r'\b', copy_lower):
            violations.append(word)
    return violations


# ---------------------------------------------------------------------------
# LLM backend selection
# ---------------------------------------------------------------------------

LLM_BACKEND = os.environ.get("LLM_BACKEND", "auto")

def get_client():
    if LLM_BACKEND == "local":
        import openai
        return openai.OpenAI(base_url="http://localhost:8800/v1", api_key="local"), "local"
    elif LLM_BACKEND == "haiku":
        import anthropic
        return anthropic.Anthropic(), "haiku"
    else:
        # auto: try local first, fall back to haiku
        try:
            import openai
            import urllib.request
            urllib.request.urlopen("http://localhost:8800/health", timeout=1)
            return openai.OpenAI(base_url="http://localhost:8800/v1", api_key="local"), "local"
        except Exception:
            import anthropic
            return anthropic.Anthropic(), "haiku"


def llm_complete(client, backend: str, system: str, user: str, max_tokens: int = 1200) -> str:
    if backend == "local":
        response = client.chat.completions.create(
            model="qwen3.5-9b",
            max_tokens=max_tokens,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content
    else:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

WEIGHTS = {
    "hook_strength": 0.25,
    "emotional_resonance": 0.25,
    "nlp_technique": 0.20,
    "specificity": 0.15,
    "cta_strength": 0.10,
    "compliance": 0.05,
}

SCORING_SYSTEM = """You are a direct-response copywriting analyst trained in:
- Hormozi (value stacking, urgency, no-brainer offers)
- Belfort straight-line persuasion (tonality, certainty, trust)
- Cardone 10X (boldness, assumptive language, commitment)
- NLP persuasion (presuppositions, embedded commands, pacing/leading, reframes, future pacing, scarcity/urgency)

Be strict — 9-10 means elite direct-response copy. 5-6 is average. Below 4 is actively weak.
Respond ONLY with valid JSON. No markdown fences, no explanation outside the JSON."""

SCORING_USER = """Score this {platform} marketing copy for audience: {audience}.

COPY:
{copy}

Return ONLY this JSON structure:
{{
  "hook_strength": {{"score": N, "reason": "one sentence", "improvement": "specific fix"}},
  "emotional_resonance": {{"score": N, "reason": "one sentence", "improvement": "specific fix"}},
  "nlp_technique": {{"score": N, "detected": ["list of techniques found"], "missing": "what would help", "improvement": "specific addition"}},
  "specificity": {{"score": N, "reason": "one sentence", "improvement": "specific fix"}},
  "cta_strength": {{"score": N, "reason": "one sentence", "improvement": "specific fix"}},
  "overall_comment": "one sentence summary of the copy's biggest strength and weakness"
}}"""

REWRITE_SYSTEM = """You are a direct-response copywriter. Rewrite the given copy to improve the weak dimensions.
Apply: Hormozi value stacking, Belfort assume-the-close, NLP techniques (embedded commands, presuppositions).
Keep the same platform/audience/format. Return ONLY the rewritten copy, no explanation."""

REWRITE_USER = """Original {platform} copy (audience: {audience}):
{copy}

Weakest dimensions to fix: {weaknesses}

Rewrite the copy to score 85+/100. Return ONLY the rewritten copy."""


def composite_score(dimensions: dict) -> int:
    total = 0.0
    for key, weight in WEIGHTS.items():
        if key == "compliance":
            total += dimensions[key]["score"] * weight
        else:
            total += dimensions[key]["score"] * weight
    return round(total * 10)


def score_copy(copy: str, platform: str = "any", audience: str = "general",
               rewrite: bool = False, fmt: str = "human") -> dict:
    violations = compliance_check(copy)
    compliance_score = 10 if not violations else max(0, 10 - len(violations) * 3)

    client, backend = get_client()

    user_msg = SCORING_USER.format(copy=copy, platform=platform, audience=audience)
    raw = llm_complete(client, backend, SCORING_SYSTEM, user_msg)

    # Strip markdown fences if model wrapped anyway
    raw = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract JSON block
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(f"Could not parse LLM response as JSON:\n{raw}")

    result["compliance"] = {"score": compliance_score, "violations": violations}
    result["composite"] = composite_score(result)
    result["backend"] = backend

    if rewrite and result["composite"] < 90:
        weaknesses = [
            f"{k} ({v['score']}/10)" for k, v in result.items()
            if isinstance(v, dict) and "score" in v and v["score"] < 7
            and k not in ("compliance",)
        ]
        rewrite_user = REWRITE_USER.format(
            copy=copy, platform=platform, audience=audience,
            weaknesses=", ".join(weaknesses) if weaknesses else "CTA and hook"
        )
        result["rewrite"] = llm_complete(client, backend, REWRITE_SYSTEM, rewrite_user, max_tokens=800)

    return result


def compare_hooks(hooks: list, platform: str = "any", audience: str = "general") -> dict:
    client, backend = get_client()

    hook_block = "\n".join(f"HOOK {chr(65+i)}: {h}" for i, h in enumerate(hooks))
    system = """You are a direct-response hook analyst. Compare hooks on: pattern interrupt strength, specificity, curiosity gap, and emotional trigger. Be concise and direct."""
    user = f"""Compare these {platform} hooks for audience: {audience}

{hook_block}

For each hook give: score (0-10), one-sentence reason, one-word weakness.
Then declare the winner and explain why in one sentence.

Return ONLY this JSON:
{{
  "hooks": [
    {{"label": "A", "copy": "...", "score": N, "reason": "...", "weakness": "..."}},
    ...
  ],
  "winner": "A",
  "winner_reason": "..."
}}"""

    raw = llm_complete(client, backend, system, user)
    raw = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
    result = json.loads(raw)
    result["backend"] = backend

    # Fill in actual copy
    for i, h in enumerate(result.get("hooks", [])):
        if i < len(hooks):
            h["copy"] = hooks[i]

    return result


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def icon(score: int) -> str:
    if score >= 8:
        return "✓ "
    elif score >= 6:
        return "→ "
    else:
        return "⚠ "


def format_score(result: dict, copy: str) -> str:
    lines = []
    lines.append(f"\nContent Resonance Score: {result['composite']}/100")
    lines.append("")
    lines.append("Dimension Breakdown:")
    dim_labels = {
        "hook_strength": "Hook Strength",
        "emotional_resonance": "Emotional Resonance",
        "nlp_technique": "NLP Technique",
        "specificity": "Specificity",
        "cta_strength": "CTA Strength",
        "compliance": "Compliance",
    }
    for key, label in dim_labels.items():
        if key not in result:
            continue
        d = result[key]
        s = d["score"]
        reason = d.get("reason", "")
        if key == "compliance":
            violations = d.get("violations", [])
            reason = "Clean" if not violations else f"Violations: {', '.join(violations)}"
        lines.append(f"  {label:<22} {s}/10  {icon(s)}{reason}")

    if result.get("overall_comment"):
        lines.append("")
        lines.append(f"Summary: {result['overall_comment']}")

    # NLP details
    nlp = result.get("nlp_technique", {})
    if nlp.get("detected"):
        lines.append(f"\nNLP detected: {', '.join(nlp['detected'])}")
    if nlp.get("missing"):
        lines.append(f"NLP missing: {nlp['missing']}")

    # Top improvement
    worst_key = min(
        [k for k in WEIGHTS if k in result and k != "compliance"],
        key=lambda k: result[k]["score"]
    )
    worst = result[worst_key]
    lines.append(f"\nTop fix ({dim_labels[worst_key]}): {worst.get('improvement', worst.get('missing', ''))}")

    if result.get("rewrite"):
        lines.append("\n--- REWRITE ---")
        lines.append(result["rewrite"])
        lines.append("--- END REWRITE ---")

    lines.append(f"\n(scored via {result.get('backend', 'unknown')})")
    return "\n".join(lines)


def format_compare(result: dict) -> str:
    lines = ["\nHook Comparison:"]
    for h in result.get("hooks", []):
        lines.append(f"\n  Hook {h['label']}: {h['score']}/10")
        lines.append(f"    \"{h['copy'][:80]}{'...' if len(h['copy']) > 80 else ''}\"")
        lines.append(f"    {icon(h['score'])}{h['reason']} | Weakness: {h.get('weakness', '—')}")
    winner = result.get("winner", "?")
    lines.append(f"\nWinner: Hook {winner}")
    lines.append(f"Why: {result.get('winner_reason', '')}")
    lines.append(f"\n(scored via {result.get('backend', 'unknown')})")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Score marketing copy for resonance (content-scorer v{})".format(VERSION)
    )
    parser.add_argument("copy", nargs="?", help="Copy to score")
    parser.add_argument("--platform", default="any",
                        choices=["any", "email", "linkedin", "x", "facebook", "instagram", "sms", "ad", "script"])
    parser.add_argument("--audience", default="general")
    parser.add_argument("--rewrite", action="store_true", help="Generate improved rewrite")
    parser.add_argument("--compliance-only", action="store_true", help="Fast compliance check, no API")
    parser.add_argument("--compare", nargs="+", metavar="HOOK", help="Compare multiple hooks")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--demo", action="store_true", help="Run on built-in demo copy (zero API cost)")
    parser.add_argument("--version", action="store_true", help="Print version and exit")

    args = parser.parse_args()

    if args.version:
        print(f"content-scorer v{VERSION}")
        return

    if args.demo:
        result = DEMO_RESULT.copy()
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print("\n[DEMO MODE — no API call, built-in sample copy]")
            print(f'Copy: "{DEMO_COPY[:80]}..."')
            print(format_score(result, DEMO_COPY))
        return

    if args.compare:
        result = compare_hooks(args.compare, args.platform, args.audience)
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(format_compare(result))
        return

    if not args.copy:
        parser.print_help()
        sys.exit(1)

    if args.compliance_only:
        violations = compliance_check(args.copy)
        if args.format == "json":
            print(json.dumps({"violations": violations, "pass": not violations}))
        else:
            if violations:
                print(f"FAIL — {len(violations)} violation(s): {', '.join(violations)}")
            else:
                print("PASS — No forbidden words detected")
        return

    result = score_copy(args.copy, args.platform, args.audience, args.rewrite)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(format_score(result, args.copy))


if __name__ == "__main__":
    main()
