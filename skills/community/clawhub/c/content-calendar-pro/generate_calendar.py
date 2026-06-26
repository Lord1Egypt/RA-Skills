#!/usr/bin/env python3
"""
Content Calendar Generator — generate_calendar.py
ClawHub skill: content-calendar v1.0.0

Generates 7-day or 30-day social media content calendars for any niche.
Local MLX (free) by default; falls back to Claude Haiku.

Usage:
    python3 generate_calendar.py --demo                     # zero API cost demo
    python3 generate_calendar.py --version                  # print version
    python3 generate_calendar.py --niche="real estate agent" --audience="first-time buyers"
    python3 generate_calendar.py --niche="crypto trader" --platform=x --days=30
    python3 generate_calendar.py --niche="SaaS" --days=30 --ab-variants --csv
    python3 generate_calendar.py --niche="mortgage broker" --platform=all --days=7
    LLM_BACKEND=local python3 generate_calendar.py --niche="..."   # free
    LLM_BACKEND=haiku python3 generate_calendar.py --niche="..."   # Claude Haiku
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime

VERSION = "1.0.1"

# ---------------------------------------------------------------------------
# Demo mode — zero API cost, built-in 7-day real estate sample
# ---------------------------------------------------------------------------

DEMO_CALENDAR = {
    "metadata": {
        "niche": "Real Estate Agent",
        "audience": "First-time homebuyers",
        "platform": "linkedin",
        "days": 7,
        "tone": "conversational",
        "generated_at": "2026-03-27T00:00:00Z",
        "backend": "demo (no API call)"
    },
    "weeks": [
        {
            "week": 1,
            "theme": "Market Reality",
            "posts": [
                {
                    "day": 1, "weekday": "Mon", "platform": "linkedin",
                    "content_type": "market_education",
                    "hook": "Most first-time buyers are waiting for the perfect moment. There isn't one.",
                    "body": "Here's what the data actually shows: buyers who waited 12 months in 2023 paid an average of $22,000 more for the same home. The 'perfect time' myth costs real money. The buyers winning right now are the ones who ran their numbers and moved when it made sense for them — not when the headlines said so.",
                    "cta": "Drop 'NUMBERS' in the comments and I'll pull what's actually moving in your target zip this week.",
                    "hashtags": ["#RealEstate", "#FirstTimeHomeBuyer", "#HomeOwnership", "#BuyersMarket"],
                    "char_count": 521,
                    "hook_b": None
                },
                {
                    "day": 2, "weekday": "Tue", "platform": "linkedin",
                    "content_type": "social_proof",
                    "hook": "My client said she'd never be able to afford a home in her target neighborhood. She closed last month.",
                    "body": "She was renting at $2,100/month. Her mortgage payment? $1,940. Same neighborhood, better schools, building equity instead of someone else's. The math shifted when she stopped comparing her situation to the national headlines and started looking at her specific numbers. That's the only comparison that matters.",
                    "cta": "If you're renting right now, DM me your zip — I'll show you the side-by-side.",
                    "hashtags": ["#RealEstate", "#RentVsBuy", "#ClientWin", "#HomeOwnership"],
                    "char_count": 498,
                    "hook_b": None
                },
                {
                    "day": 3, "weekday": "Wed", "platform": "linkedin",
                    "content_type": "objection_bust",
                    "hook": "'I need 20% down.' I hear this every week. It's not true for most buyers.",
                    "body": "Conventional loans go as low as 3% down. FHA is 3.5%. VA is zero for eligible veterans. Down payment assistance programs exist in most counties. The 20% rule made sense in 1985. Today it's a myth that keeps qualified buyers renting longer than they need to. Know what you actually need before you assume.",
                    "cta": "Want the real breakdown for your situation? Drop your city below.",
                    "hashtags": ["#Homebuying", "#FirstTimeHomeBuyer", "#DownPayment", "#RealEstateTips"],
                    "char_count": 489,
                    "hook_b": None
                },
                {
                    "day": 4, "weekday": "Thu", "platform": "linkedin",
                    "content_type": "community",
                    "hook": "The most underrated neighborhood in my market right now — and why buyers keep overlooking it.",
                    "body": "Lake access, new construction, sub-$350K entry points, and it's 30 minutes from the business district. Most buyers overlook it because they don't know it. The ones who looked at it 2 years ago are now sitting on $60K+ in equity. Local knowledge is the edge that no algorithm gives you.",
                    "cta": "Comment 'HIDDEN GEM' and I'll send you what's currently listed there under $375K.",
                    "hashtags": ["#RealEstate", "#LocalMarket", "#HiddenGem", "#HomeSearch"],
                    "char_count": 461,
                    "hook_b": None
                },
                {
                    "day": 5, "weekday": "Fri", "platform": "linkedin",
                    "content_type": "market_education",
                    "hook": "3 things about today's housing market most buyers get wrong.",
                    "body": "1. It's not overpriced — it's repriced. The fundamentals (jobs, population, infrastructure) justify current values. 2. Inventory is not 'back to normal' — it's still 40% below 2019 levels in most zip codes. 3. New construction isn't always cheaper — builder incentives are negotiable, and resale often wins on location. Knowing the real data changes every decision you make.",
                    "cta": "Which of these surprised you most? Drop it below.",
                    "hashtags": ["#RealEstateFacts", "#HomeBuying", "#MarketUpdate", "#HousingMarket"],
                    "char_count": 534,
                    "hook_b": None
                },
                {
                    "day": 6, "weekday": "Sat", "platform": "linkedin",
                    "content_type": "direct_cta",
                    "hook": "If you've been browsing homes for more than 3 months, something's stopping you.",
                    "body": "It's usually one of three things: not knowing your real budget, not knowing what neighborhoods actually fit your life, or waiting for a signal that never comes. All three are fixable in one conversation. The buyers who close are the ones who had that conversation early — not the ones who waited until everything felt 'perfect.'",
                    "cta": "DM me 'READY' and let's figure out what's actually in your way.",
                    "hashtags": ["#RealEstate", "#TakeAction", "#HomeBuying", "#BuyNow"],
                    "char_count": 502,
                    "hook_b": None
                },
                {
                    "day": 7, "weekday": "Sun", "platform": "linkedin",
                    "content_type": "social_proof",
                    "hook": "Weekend reading: the question I get asked most by first-time buyers.",
                    "body": "'How do I know when I'm actually ready?' My answer: you're ready when you know your number, your must-have list, and your timeline. Everything else is noise. The buyers I've worked with who closed happily all had those three things clear before we looked at a single home. The ones who didn't had a much harder time. Clarity beats timing every time.",
                    "cta": "What's your #1 question about buying? Drop it below — I read every comment.",
                    "hashtags": ["#FirstTimeHomeBuyer", "#RealEstateTips", "#WeekendReads", "#HomeBuying"],
                    "char_count": 517,
                    "hook_b": None
                }
            ]
        }
    ]
}

# ---------------------------------------------------------------------------
# Compliance check
# ---------------------------------------------------------------------------

FORBIDDEN_BY_NICHE = {
    "mortgage": [
        "pre-approval", "pre-approved", "pre-qualify", "specialist",
        "rates", "loan", "lender", "qualify for",
    ],
    "real_estate": [
        "showings", "tours",
    ],
    # Universal — always checked regardless of niche
    "general": [
        "AWESOME", "transfer", "connect to",
    ],
}

def compliance_check(copy: str, niche_type: str = "all") -> list:
    """Check copy for forbidden words. niche_type='all' checks every category."""
    violations = []
    copy_lower = copy.lower()
    if niche_type == "all":
        words = [w for ws in FORBIDDEN_BY_NICHE.values() for w in ws]
    else:
        words = FORBIDDEN_BY_NICHE.get(niche_type, []) + FORBIDDEN_BY_NICHE["general"]
    for word in words:
        if re.search(r'\b' + re.escape(word.lower()) + r'\b', copy_lower):
            violations.append(word)
    return violations

# ---------------------------------------------------------------------------
# LLM backend
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
        try:
            import openai, urllib.request
            urllib.request.urlopen("http://localhost:8800/health", timeout=1)
            return openai.OpenAI(base_url="http://localhost:8800/v1", api_key="local"), "local"
        except Exception:
            import anthropic
            return anthropic.Anthropic(), "haiku"

def llm_complete(client, backend: str, system: str, user: str, max_tokens: int = 4096) -> str:
    if backend == "local":
        response = client.chat.completions.create(
            model="qwen3.5-9b", max_tokens=max_tokens, temperature=0.7,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return response.choices[0].message.content
    else:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001", max_tokens=max_tokens,
            system=system, messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

# ---------------------------------------------------------------------------
# Calendar generation
# ---------------------------------------------------------------------------

CONTENT_MIX = {
    "market_education": 0.25,
    "social_proof":     0.20,
    "objection_bust":   0.20,
    "community":        0.15,
    "direct_cta":       0.20,
}

WEEK_THEMES = [
    "Market Reality",
    "Social Proof",
    "Education & Expertise",
    "Urgency & Action",
]

PLATFORM_LIMITS = {
    "linkedin":  {"chars": 3000, "hashtags": 5,  "tone": "professional and direct"},
    "x":         {"chars": 280,  "hashtags": 2,  "tone": "punchy and bold"},
    "facebook":  {"chars": 500,  "hashtags": 3,  "tone": "conversational and community-oriented"},
    "instagram": {"chars": 300,  "hashtags": 10, "tone": "visual-first, lifestyle-driven"},
}

TONE_INSTRUCTIONS = {
    "conversational": "Write like you're talking to a friend. No jargon. Short sentences.",
    "educational":    "Lead with insight. Back claims with data or specifics. Build authority.",
    "urgent":         "Create time pressure. Opportunity cost framing. Bold CTAs.",
    "luxury":         "Aspirational language. Premium positioning. Never cheapen the brand.",
    "bold":           "Confident, assertive, no hedging. Make strong claims. No 'maybe' or 'might'.",
}

CALENDAR_SYSTEM = """You are a social media strategist and direct-response copywriter.
Generate {days} days of {platform} content. Be specific, varied, and hook-first.
Never repeat a topic within 7 days. Every post must open with a pattern interrupt.
Respond ONLY with valid JSON. No markdown fences, no preamble."""

CALENDAR_USER = """Generate a {days}-day {platform} content calendar.

Niche: {niche}
Audience: {audience}
Tone: {tone_instruction}
Platform limits: max {char_limit} chars, max {hashtag_limit} hashtags
Week themes (rotate): {week_themes}
Content mix: 25% market_education, 20% social_proof, 20% objection_bust, 15% community, 20% direct_cta
AB variants: {ab_variants}

Return ONLY this JSON structure:
{{
  "metadata": {{
    "niche": "{niche}",
    "audience": "{audience}",
    "platform": "{platform}",
    "days": {days}
  }},
  "weeks": [
    {{
      "week": 1,
      "theme": "...",
      "posts": [
        {{
          "day": 1,
          "weekday": "Mon",
          "platform": "{platform}",
          "content_type": "market_education",
          "hook": "...",
          "body": "...",
          "cta": "...",
          "hashtags": ["#Tag1", "#Tag2"],
          "char_count": 0,
          "hook_b": null
        }}
      ]
    }}
  ]
}}

Generate all {days} posts across the correct number of weeks. Populate char_count with the actual character count of hook+body+cta combined. If ab_variants=true, populate hook_b with an alternative hook."""

def generate_calendar(niche: str, audience: str, platform: str, days: int,
                      tone: str, ab_variants: bool) -> dict:
    client, backend = get_client()

    platforms = list(PLATFORM_LIMITS.keys()) if platform == "all" else [platform]
    all_weeks = []

    for plat in platforms:
        plat_config = PLATFORM_LIMITS[plat]
        week_themes = " → ".join(WEEK_THEMES[:((days // 7) + 1)])
        system = CALENDAR_SYSTEM.format(days=days, platform=plat)
        user = CALENDAR_USER.format(
            days=days, platform=plat, niche=niche, audience=audience,
            tone_instruction=TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["conversational"]),
            char_limit=plat_config["chars"],
            hashtag_limit=plat_config["hashtags"],
            week_themes=week_themes,
            ab_variants=str(ab_variants).lower(),
        )
        raw = llm_complete(client, backend, system, user, max_tokens=min(4096, days * 150))
        raw = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        try:
            cal = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                cal = json.loads(match.group())
            else:
                raise ValueError(f"Could not parse calendar JSON:\n{raw[:500]}")

        # Fill char_counts if model left them as 0
        for week in cal.get("weeks", []):
            for post in week.get("posts", []):
                if post.get("char_count", 0) == 0:
                    total = len(post.get("hook","")) + len(post.get("body","")) + len(post.get("cta",""))
                    post["char_count"] = total

        if platform == "all":
            all_weeks.extend(cal.get("weeks", []))
        else:
            cal["metadata"]["backend"] = backend
            return cal

    return {
        "metadata": {"niche": niche, "audience": audience, "platform": "all",
                     "days": days, "backend": backend},
        "weeks": all_weeks
    }

# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_human(cal: dict) -> str:
    m = cal["metadata"]
    lines = [f"\n=== {m.get('days',7)}-Day {m.get('platform','').title()} Calendar: {m.get('niche')} → {m.get('audience')} ==="]
    for week in cal.get("weeks", []):
        lines.append(f"\nWeek {week['week']} Theme: {week.get('theme','')}")
        for post in week.get("posts", []):
            lines.append(f"\n--- Day {post['day']} ({post.get('weekday','')}) | {post['platform'].title()} | {post.get('content_type','').replace('_',' ').title()} ---")
            lines.append(f"HOOK:     {post.get('hook','')}")
            if post.get("hook_b"):
                lines.append(f"HOOK B:   {post['hook_b']}")
            lines.append(f"BODY:     {post.get('body','')}")
            lines.append(f"CTA:      {post.get('cta','')}")
            lines.append(f"HASHTAGS: {' '.join(post.get('hashtags', []))}")
            lines.append(f"CHARS:    {post.get('char_count', 0)}")
    backend = m.get("backend", "unknown")
    lines.append(f"\n(generated via {backend})")
    return "\n".join(lines)

def format_csv(cal: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["day", "weekday", "platform", "content_type", "hook", "hook_b", "body", "cta", "hashtags", "char_count"])
    for week in cal.get("weeks", []):
        for post in week.get("posts", []):
            writer.writerow([
                post.get("day", ""), post.get("weekday", ""), post.get("platform", ""),
                post.get("content_type", ""), post.get("hook", ""), post.get("hook_b") or "",
                post.get("body", ""), post.get("cta", ""),
                " ".join(post.get("hashtags", [])), post.get("char_count", 0)
            ])
    return output.getvalue()

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=f"Generate social media content calendars (content-calendar v{VERSION})"
    )
    parser.add_argument("--niche", help="Your brand/industry (e.g. 'real estate agent', 'mortgage broker')")
    parser.add_argument("--audience", default="general", help="Target reader")
    parser.add_argument("--platform", default="linkedin",
                        choices=["linkedin", "x", "facebook", "instagram", "all"])
    parser.add_argument("--days", type=int, default=7, choices=[7, 30])
    parser.add_argument("--tone", default="conversational",
                        choices=["conversational", "educational", "urgent", "luxury", "bold"])
    parser.add_argument("--ab-variants", action="store_true", help="Generate 2 hook variants per post")
    parser.add_argument("--csv", action="store_true", help="Export as CSV")
    parser.add_argument("--output", help="Write output to file (e.g. calendar.json or calendar.csv)")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    parser.add_argument("--demo", action="store_true", help="Run built-in sample (zero API calls)")
    parser.add_argument("--version", action="store_true", help="Print version and exit")
    parser.add_argument("--compliance-only", help="Check copy string for forbidden words (no API)")

    args = parser.parse_args()

    if args.version:
        print(f"content-calendar v{VERSION}")
        return

    if args.compliance_only:
        violations = compliance_check(args.compliance_only)
        if violations:
            print(f"FAIL — {len(violations)} violation(s): {', '.join(violations)}")
        else:
            print("PASS — No forbidden words detected")
        return

    if args.demo:
        cal = DEMO_CALENDAR
        if args.format == "json":
            print(json.dumps(cal, indent=2))
        elif args.csv:
            print(format_csv(cal))
        else:
            print("\n[DEMO MODE — no API call, built-in 7-day real estate sample]")
            print(format_human(cal))
        return

    if not args.niche:
        parser.error("--niche is required (or use --demo to see sample output)")

    cal = generate_calendar(
        niche=args.niche,
        audience=args.audience,
        platform=args.platform,
        days=args.days,
        tone=args.tone,
        ab_variants=args.ab_variants,
    )

    if args.csv:
        output = format_csv(cal)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Wrote {args.days}-day CSV → {args.output}")
        else:
            print(output)
    elif args.format == "json":
        output = json.dumps(cal, indent=2)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Wrote {args.days}-day JSON calendar → {args.output}")
        else:
            print(output)
    else:
        output = format_human(cal)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Wrote {args.days}-day calendar → {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()
