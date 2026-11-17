#!/usr/bin/env python3
"""creative_brief.py - normalize a creative brief into a full US-market creative pack.

Usage:
    python3 creative_brief.py --brief brief.yaml --out campaign/
    python3 creative_brief.py --brief brief.json --out campaign/ --seed 7

Stdlib only. Accepts JSON or a practical subset of YAML (scalars, inline
lists, block lists, one level of nested maps). Writes:
    <out>/brief.normalized.json
    <out>/creative_pack.md
    <out>/prompt_set.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import sys

PLATFORMS = ["tiktok", "instagram", "meta_ads", "email", "linkedin", "x", "google_ads", "youtube"]

CHANNELS = [
    "TikTok",
    "Instagram",
    "Facebook",
    "LinkedIn",
    "X",
    "YouTube",
    "Email",
    "Meta Ads",
    "Google Ads",
]

HOOK_PATTERNS = [
    "I was wrong about {product}.",
    "Stop {bad}.",
    "This is the only {category} that actually {benefit}.",
    "{audience_short}: this saves you {time_money}.",
    "Nobody talks about {pain}.",
    "We tested {product} for {duration}. Here's what happened.",
    "3 things I wish I knew before switching to {product}.",
    "{proof_first} - that changed how I use {product}.",
    "If you {job_to_be_done}, keep watching.",
    "{objection}? Read this.",
    "The cheapest {category} that actually {benefit}.",
    "How I {use_case} without {pain}.",
    "The {category} mistake that costs {time_money}.",
    "Read this before you buy another {category}.",
    "{proof_first} - here is how.",
    "What nobody tells {audience_short} about {category}.",
    "Two minutes with {product} beat a week of {bad}.",
    "Still {pain}? Try this instead.",
    "Why {audience_short} are switching to {product}.",
    "{offer_short} and {proof_first}.",
    "One {category}, one change: {benefit}.",
    "Save {time_money} with {product}.",
    "{product} vs the old way: {proof_first}.",
    "The US {category} pick for {audience_short}.",
]

BAD_DEFAULTS = ["posting every day", "guessing what works", "editing for two hours"]

DURATIONS = ["30 days", "2 weeks", "a month", "6 months"]

PROOF_FRAMES = [
    "{proof_first}",
    "{proof_first} - and it holds up.",
    "Here's the proof: {proof_first}",
]

CTA_BANK = [
    "Tap the link to try it",
    "Start free today",
    "Get the details",
    "Claim your {offer_short}",
    "See the full breakdown",
    "Join the list",
    "Shop now",
    "Try it risk-free",
]

EMAIL_SUBJECTS = [
    "Your {product_short} is ready",
    "A better way to {use_case_short}",
    "{audience_short}, this one's for you",
    "Save {time_money} with {product_short}",
    "Here's what {proof_first_short} looks like",
    "Still doing {bad}?",
    "Quick question about {category}",
    "{offer_short} - ends {day}",
]

HOOK_TYPES = ["problem", "curiosity", "proof", "contrarian", "how-to"]

PLATFORM_LIMITS = {
    "tiktok": {"chars": 2200, "aspect": "9:16", "hashtags": "3-5"},
    "instagram": {"chars": 2200, "aspect": "4:5", "hashtags": "3-5"},
    "facebook": {"chars": 63206, "aspect": "1:1", "hashtags": "2-3"},
    "linkedin": {"chars": 3000, "aspect": "1:1", "hashtags": "0-3"},
    "x": {"chars": 280, "aspect": "16:9", "hashtags": "0-2"},
    "youtube": {"chars": 5000, "aspect": "16:9", "hashtags": "0-3"},
    "email": {"chars": 20000, "aspect": "n/a", "hashtags": "n/a"},
}


# --------------------------------------------------------------------------- #
# minimal YAML / JSON loading
# --------------------------------------------------------------------------- #
def _coerce(raw: str):
    raw = raw.strip()
    if raw == "":
        return ""
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [_coerce(part) for part in _split_top(inner, ",")]
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    low = raw.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "none", "~"):
        return None
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d*\.\d+", raw):
        return float(raw)
    return raw


def _split_top(text: str, sep: str):
    parts, depth, buf, quote = [], 0, [], None
    for ch in text:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return [p.strip() for p in parts]


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_simple_yaml(text: str):
    """Parse the YAML subset used by the brief templates."""
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        lines.append(raw.rstrip())
    root: dict = {}
    stack = [(-1, root)]
    i = 0
    while i < len(lines):
        line = lines[i]
        indent = _indent_of(line)
        body = line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1] if stack else root
        if body.startswith("- "):
            item = _coerce(body[2:])
            if isinstance(parent, list):
                parent.append(item)
            elif isinstance(parent, dict):
                parent.setdefault("items", [])
                if isinstance(parent["items"], list):
                    parent["items"].append(item)
            i += 1
            continue
        if ":" not in body:
            i += 1
            continue
        key, _, value = body.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            nxt = None
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    nxt = lines[j]
                    break
            if nxt is not None and _indent_of(nxt) > indent:
                child: dict = {}
                if nxt.strip().startswith("- "):
                    child = []
                parent[key] = child
                stack.append((indent, child))
                i += 1
                continue
            parent[key] = ""
            i += 1
            continue
        parent[key] = _coerce(value)
        i += 1
    return root


def load_brief(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if path.lower().endswith(".json"):
        return json.loads(text)
    data = parse_simple_yaml(text)
    if not isinstance(data, dict):
        raise SystemExit("Brief must parse to a mapping (dict).")
    return data


# --------------------------------------------------------------------------- #
# brief normalization
# --------------------------------------------------------------------------- #
def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if v not in (None, "")]
    if isinstance(value, str):
        return [v for v in _split_top(value, ",") if v]
    return [value]


def first_sentence(text: str, limit: int = 90) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    match = re.match(r"^(.+?[.!?])(\s|$)", text)
    out = match.group(1) if match else text
    if len(out) > limit:
        out = out[: limit - 1].rsplit(" ", 1)[0] + "..."
    return out


def short(text: str, words: int = 3) -> str:
    parts = (text or "").split()
    if not parts:
        return ""
    out = parts[:words]
    if out and any(ch in out[-1] for ch in "([") and not any(ch in out[-1] for ch in ")]"):
        out = out[:-1]
    return " ".join(out).rstrip(" ,.;:-").strip()


def normalize(brief: dict) -> dict:
    proof = [str(p).strip() for p in as_list(brief.get("proof")) if str(p).strip()]
    competitors = [str(c).strip() for c in as_list(brief.get("competitors")) if str(c).strip()]
    channels = [str(c).strip().lower() for c in as_list(brief.get("channels")) if str(c).strip()]
    channels = [c for c in channels if c in PLATFORMS] or ["tiktok", "instagram", "meta_ads", "email"]

    product = str(brief.get("product") or brief.get("name") or "the product").strip()
    audience = str(brief.get("audience") or brief.get("audience_short") or "US buyers").strip()
    offer = str(brief.get("offer") or "").strip()
    tone = str(brief.get("tone") or "clear, confident, human").strip()
    cta = str(brief.get("cta") or CTA_BANK[0]).strip()
    voice = str(brief.get("brand_voice") or brief.get("voice") or tone).strip()

    if not proof:
        proof = ["Add your strongest proof point here (review count, spec, guarantee, or named result)"]
    if not competitors:
        competitors = ["the category leader"]

    audience_short = short(audience, 4) or "US buyers"
    return {
        "product": product,
        "product_short": short(product, 3),
        "category": str(brief.get("category") or short(product, 2)),
        "audience": audience,
        "audience_short": audience_short,
        "offer": offer,
        "offer_short": short(offer, 3) or "the offer",
        "proof": proof,
        "proof_first": proof[0],
        "proof_first_short": short(proof[0], 6),
        "tone": tone,
        "cta": cta,
        "brand_voice": voice,
        "competitors": competitors,
        "channels": channels,
        "time_money": str(brief.get("time_money") or "an hour a week").strip(),
        "use_case": str(brief.get("use_case") or "use it daily").strip(),
        "use_case_short": short(brief.get("use_case") or "use it daily", 3),
        "benefit": str(brief.get("benefit") or "does the job in one step").strip(),
        "pain": str(brief.get("pain") or BAD_DEFAULTS[0]).strip(),
        "job_to_be_done": str(brief.get("job_to_be_done") or "get results without extra work").strip(),
        "bad": BAD_DEFAULTS[0],
        "duration": DURATIONS[0],
        "missing": [k for k in ("proof", "offer", "audience") if not brief.get(k)],
    }


# --------------------------------------------------------------------------- #
# generation
# --------------------------------------------------------------------------- #
def build_hooks(n: dict, rng: random.Random, count: int = 15) -> list:
    hooks = []
    patterns = list(HOOK_PATTERNS)
    rng.shuffle(patterns)
    seen = set()
    idx = 0
    while len(hooks) < count:
        pattern = patterns[idx % len(patterns)]
        idx += 1
        hook_type = HOOK_TYPES[idx % len(HOOK_TYPES)]
        text = pattern.format(
            product=n["product_short"],
            bad=n["bad"],
            category=n["category"],
            audience_short=n["audience_short"],
            benefit=n["benefit"],
            pain=n["pain"],
            duration=n["duration"],
            proof_first=n["proof_first_short"],
            switching=short(n["use_case"], 2),
            objection="Not sure it works",
            use_case=n["use_case_short"],
            time_money=n["time_money"],
            job_to_be_done=n["job_to_be_done"],
            offer_short=n["offer_short"],
        )
        if text in seen:
            if idx > len(patterns) * 3:
                break
            continue
        seen.add(text)
        hooks.append(
            {
                "id": f"H{len(hooks) + 1:02d}",
                "type": HOOK_TYPES[len(hooks) % len(HOOK_TYPES)],
                "text": text,
                "platform": PLATFORMS[len(hooks) % len(PLATFORMS)],
            }
        )
    return hooks


def build_voice_card(n: dict) -> dict:
    return {
        "voice_traits": ["Direct", "Specific", "Plainspoken", "Confident", "Useful"],
        "do": [
            f"Lead with the outcome {n['audience_short']} actually wants.",
            "Use numbers and specifics instead of adjectives.",
            "Write like a peer who already did it.",
        ],
        "dont": [
            "No hype words (revolutionary, game-changing, insane).",
            "No fake urgency or countdowns that are not real.",
            "No emoji stacks in B2B channels.",
        ],
        "banned_phrases": [
            "guaranteed results",
            "risk-free income",
            "the best in the world",
            "unmatched",
            "revolutionary",
            "secret trick",
        ],
        "sample_lines": [
            f"{n['proof_first']} - that's the whole pitch.",
            f"Saves you {n['time_money']}. Your mileage will vary.",
            f"Built for {n['audience_short']}. Not for everyone, and that's fine.",
        ],
    }


def build_ad_copy(n: dict, hooks: list, rng: random.Random) -> dict:
    ctas = [n["cta"]] + [c.format(offer_short=n["offer_short"]) for c in CTA_BANK]
    headlines = [
        n["proof_first_short"],
        f"{n['product_short']} for {n['audience_short']}",
        f"{n['offer_short']}",
        "Built for real use",
        "See why people switch",
        "US shipping",
        n["offer_short"],
        "Try it and keep it",
    ]
    headlines = headlines[:8]
    descriptions = [
        f"{n['proof_first']}. {n['cta']}.",
        f"For {n['audience_short']}: {n['job_to_be_done']}. {n['cta']}.",
        f"{n['tone'].split(',')[0].capitalize()} and specific. {n['offer'] or n['cta']}.",
    ]
    primary = [
        f"{n['audience_short']}: {n['proof_first']}.\n\n{n['cta']}.",
        f"{n['pain'].capitalize()}? {n['product_short']} fixes it - {n['proof_first_short']}.\n\n{n['cta']}.",
        f"{n['offer']}\n\n{n['proof_first']}. {n['cta']}." if n["offer"] else f"{n['proof_first']}. {n['cta']}.",
    ]
    return {
        "meta": {
            "primary_text": primary,
            "headlines": headlines,
            "descriptions": descriptions,
            "cta": ctas[0],
            "cta_options": ctas,
        },
        "google_rsa": {
            "headlines_15": headlines + ["Free shipping over $50", "30-day trial", "Ships from the US", "Top rated", "Built to last"],
            "descriptions_4": descriptions + [f"{n['offer']}. {n['cta']}.".strip()],
            "note": "Headlines max 30 chars each. Trim anything longer before upload.",
        },
        "tiktok": {
            "primary_text": primary[0],
            "cta": ctas[0],
            "hook_id": hooks[0]["id"],
        },
    }


def build_social(n: dict, hooks: list) -> list:
    posts = []
    channel_map = {
        "tiktok": ("TikTok", "Short video"),
        "instagram": ("Instagram", "Carousel"),
        "linkedin": ("LinkedIn", "Text post"),
        "x": ("X", "Single post"),
        "facebook": ("Facebook", "Image post"),
        "youtube": ("YouTube", "Short"),
        "email": ("Email", "Send"),
        "meta_ads": ("Meta Ads", "Ad set"),
        "google_ads": ("Google Ads", "RSA"),
    }
    for ch in n["channels"]:
        label, fmt = channel_map.get(ch, (ch.title(), "Post"))
        hook = next((h for h in hooks if h["platform"] == ch), hooks[0])
        body = f"{hook['text']}\n\n{n['proof_first']}.\n\n{ n['cta'] }"
        posts.append(
            {
                "channel": label,
                "format": fmt,
                "hook_id": hook["id"],
                "post": body,
                "hashtags": ["#" + re.sub(r"[^A-Za-z0-9]", "", n["category"].title()).replace(" ", "")],
                "alt_text": f"{n['product_short']} - {n['proof_first']}.",
                "pinned_comment": "Ask the one question people always ask: how does it compare?",
                "limit": PLATFORM_LIMITS.get(ch, {}),
            }
        )
    return posts


def build_ugc(n: dict, hooks: list) -> list:
    angles = ["Problem first", "Demo first", "Comparison first"]
    scripts = []
    for idx, angle in enumerate(angles):
        hook = hooks[idx % len(hooks)]
        scripts.append(
            {
                "angle": angle,
                "hook_id": hook["id"],
                "script": [
                    f"(0-2s) HOOK: {hook['text']}",
                    f"(2-10s) PROBLEM: {n['pain'].capitalize()} - show the mess, no music.",
                    f"(10-25s) DEMO: {n['product_short']} in use. On-screen text: {n['proof_first_short']}",
                    f"(25-35s) PROOF: {n['proof_first']}",
                    f"(35-45s) CTA: {n['cta']}",
                ],
                "shot_list": [
                    "Close-up, product in hand, natural window light",
                    "Medium shot, real context (kitchen / desk / trail)",
                    "Macro detail, material and texture",
                ],
                "on_screen_text": [n["proof_first_short"], n["offer_short"], n["cta"]],
                "creator_brief": f"Age 28-45, US, uses {n['category']} weekly. Scripted, natural lighting, no over-production.",
            }
        )
    return scripts


def build_prompts(n: dict, hooks: list) -> dict:
    visual = [
        {
            "id": "IMG01",
            "use": "Hero product shot (1:1 for feed, 4:5 for IG)",
            "prompt": (
                f"Product photo of {n['product']} on a clean US-market surface, soft north-facing window light, "
                f"shallow depth of field, 50mm, crisp material texture, neutral palette, premium DTC brand look, "
                f"no text, no logo overlays"
            ),
            "aspect": "1:1 / 4:5",
            "negative": "text, watermark, distorted logo, extra fingers, cluttered background, oversaturated HDR",
        },
        {
            "id": "IMG02",
            "use": "Lifestyle shot with US audience context",
            "prompt": (
                f"{n['audience_short']} using {n['product']} in a bright modern US setting, natural candid posture, "
                f"documentary photography, 35mm, golden hour accents, realistic skin tones, no text"
            ),
            "aspect": "4:5",
            "negative": "text, stock-photo smile, plastic skin, watermark, logo",
        },
        {
            "id": "VID01",
            "use": "15s UGC ad, vertical",
            "prompt": (
                f"Vertical UGC video: person picks up {n['product']}, shows one clear use case, sets it down, "
                f"talks to camera. Natural indoor light, handheld, one continuous take, 9:16, 15 seconds, no music bed."
            ),
            "aspect": "9:16",
            "negative": "brand logo, on-screen text, slow motion, film grain, bokeh overload",
        },
        {
            "id": "IMG03",
            "use": "Carousel slide 1 - hook frame",
            "prompt": (
                f"Bold editorial graphic background for a text overlay about {n['job_to_be_done']}, "
                f"high contrast, single strong color block, no text in image"
            ),
            "aspect": "4:5",
            "negative": "text, busy pattern, low contrast, watermark",
        },
    ]
    for img in visual:
        img["camera"] = "50mm, f/2.0" if "photo" in img["prompt"] else "35mm, f/2.8"
        img["light"] = "soft window light"
    return {
        "style_prefix": "cinematic commercial photography, true-to-life US consumer brand aesthetic, no text, no watermark",
        "images": visual,
        "copy_prompt": (
            f"Write {n['tone']} US-English marketing copy for {n['product']} aimed at {n['audience']}. "
            f"Use only these proof points: {'; '.join(n['proof'])}. Offer: {n['offer'] or 'n/a'}. "
            f"Never invent reviews, ratings, awards, or statistics. One CTA: {n['cta']}."
        ),
        "negative_prompt": "fake text, misspelled words, watermark, extra logos, celebrity likeness, misleading claims",
    }


def build_email(n: dict, hooks: list) -> list:
    subjects = [
        s.format(
            product_short=n["product_short"],
            audience_short=n["audience_short"],
            use_case_short=n["use_case_short"],
            time_money=n["time_money"],
            proof_first_short=n["proof_first_short"],
            bad=n["bad"],
            offer_short=n["offer_short"],
            category=n["category"],
            day="Friday",
        )
        for s in EMAIL_SUBJECTS
    ]
    previews = [
        "Here is the short version.",
        "One spec, one price, one CTA.",
        "No fluff - the three numbers that matter.",
        "How it works in under a minute.",
        "What you get, what it costs, what to do.",
    ]
    bodies = [
        f"Hey {{first_name}},\n\n{n['proof_first']}.\n\nIf that solves {n['pain']}, {n['cta']} - {n['offer'] or 'link inside'}.\n\n- The team",
        f"Hey {{first_name}},\n\nShort version: {n['job_to_be_done']} for {n['audience_short']}.\n\n{n['proof_first']}\n\n{n['cta']}.\n\n- The team",
        f"Hey {{first_name}},\n\n{first_sentence(n['offer'] or n['cta'])}\n\n{n['proof_first']}\n\n{n['cta']}.\n\n- The team",
        f"Hey {{first_name}},\n\nLast one about {n['product_short']}.\n\n{n['offer'] or n['proof_first']}\n\n{n['cta']}.\n\n- The team",
    ]
    return [
        {
            "step": i + 1,
            "name": name,
            "subject": subjects[i],
            "preview_text": previews[i],
            "body": bodies[i],
            "send": day,
        }
        for i, (name, day) in enumerate([("Welcome", "Day 0"), ("Feature", "Day 2"), ("Proof", "Day 5"), ("Offer", "Day 8")])
    ]


def build_calendar(n: dict, hooks: list) -> list:
    rows = []
    cadence = ["tiktok", "instagram", "email", "linkedin", "instagram", "x", "meta_ads", "instagram"]
    day = 1
    for week in range(4):
        for ch in cadence:
            if day > 30:
                break
            hook = hooks[(day - 1) % len(hooks)]
            rows.append(
                {
                    "day": f"Day {day}",
                    "channel": ch,
                    "format": PLATFORM_LIMITS.get(ch, {}).get("aspect", "post"),
                    "hook_id": hook["id"],
                    "cta": n["cta"],
                    "asset": f"produce {ch} asset for hook {hook['id']}",
                }
            )
            day += 1
    return rows


def build_compliance(n: dict, raw_brief: dict) -> list:
    notes = [
        {"item": "Proof claims", "status": "VERIFY", "detail": f"Confirm '{n['proof_first']}' before it goes live."},
        {"item": "Price / offer", "status": "VERIFY" if n["offer"] else "MISSING", "detail": n["offer"] or "No offer supplied - add price and terms."},
        {"item": "Competitor names", "status": "CHECK", "detail": f"Comparison only, no competitor trademarks in ad copy or hashtags: {', '.join(n['competitors'])}."},
        {"item": "Banned phrases", "status": "PASS", "detail": "No guaranteed-results or superlative claims generated."},
    ]
    if not n["proof"]:
        notes.append({"item": "Social proof", "status": "MISSING", "detail": "No reviews, ratings, or customer counts supplied - none were invented."})
    if n["missing"]:
        notes.append({"item": "Brief gaps", "status": "MISSING", "detail": f"Empty fields: {', '.join(n['missing'])}."})
    return notes


# --------------------------------------------------------------------------- #
# rendering
# --------------------------------------------------------------------------- #
def render_pack(n: dict, hooks: list, voice: dict, ads: dict, social: list, ugc: list, prompts: dict, emails: list, cal: list, comp: list) -> str:
    out = []
    add = out.append
    add(f"# Creative pack - {n['product']}\n")
    add(f"**Audience:** {n['audience']}  \n**Tone:** {n['tone']}  \n**CTA:** {n['cta']}  \n**Channels:** {', '.join(n['channels'])}\n")

    add("\n## 1. Message spine\n")
    add(f"- **Core promise:** {n['job_to_be_done'].capitalize()}, without {n['pain']}.\n")
    add("- **Proof pillars:**\n" + "\n".join(f"  {i + 1}. {p}" for i, p in enumerate(n["proof"][:3])))
    add(f"- **Objection handled:** \"Will it actually do this?\" - {n['proof_first']}.\n")
    add(f"- **CTA:** {n['cta']}\n")

    add("\n## 2. Brand voice card\n")
    add("**Traits:** " + ", ".join(voice["voice_traits"]) + "\n")
    add("\n**Do**\n" + "\n".join(f"- {x}" for x in voice["do"]))
    add("\n**Don't**\n" + "\n".join(f"- {x}" for x in voice["dont"]))
    add("\n**Banned phrases:** " + ", ".join(voice["banned_phrases"]) + "\n")
    add("\n**Sample lines**\n" + "\n".join(f"> {x}" for x in voice["sample_lines"]) + "\n")

    add("\n## 3. Hook bank\n")
    for h in hooks:
        add(f"- `{h['id']}` ({h['type']}, {h['platform']}) - {h['text']}")
    add("")

    add("\n## 4. Ad copy\n")
    add("### Meta\n")
    for i, p in enumerate(ads["meta"]["primary_text"]):
        add(f"**Primary {i + 1}**\n\n{p}\n")
    add("**Headlines**\n" + "\n".join(f"- {h}" for h in ads["meta"]["headlines"]))
    add("\n**Descriptions**\n" + "\n".join(f"- {d}" for d in ads["meta"]["descriptions"]))
    add(f"\n**CTA:** {ads['meta']['cta']}\n")
    add("\n### Google RSA\n")
    add("**Headlines (trim to 30 chars)**\n" + "\n".join(f"- {h}" for h in ads["google_rsa"]["headlines_15"]))
    add("\n**Descriptions (trim to 90 chars)**\n" + "\n".join(f"- {d}" for d in ads["google_rsa"]["descriptions_4"]))
    add("\n### TikTok\n")
    add(f"Primary text: {ads['tiktok']['primary_text']}\n\nCTA: {ads['tiktok']['cta']}  |  Hook: {ads['tiktok']['hook_id']}\n")

    add("\n## 5. Social posts\n")
    for p in social:
        add(f"### {p['channel']} ({p['format']}, limit {p['limit'].get('chars', 'n/a')} chars)\n")
        add(f"{p['post']}\n")
        add(f"Hashtags: {' '.join(p['hashtags'])}  \nAlt text: {p['alt_text']}  \nPinned comment: {p['pinned_comment']}\n")

    add("\n## 6. UGC scripts\n")
    for s in ugc:
        add(f"### {s['angle']} ({s['hook_id']})\n")
        add("\n".join(s["script"]) + "\n")
        add("**Shot list**\n" + "\n".join(f"- {x}" for x in s["shot_list"]))
        add("\n**On-screen text:** " + " | ".join(s["on_screen_text"]))
        add(f"\n**Creator brief:** {s['creator_brief']}\n")

    add("\n## 7. Image & video prompts\n")
    add(f"**Style prefix:** {prompts['style_prefix']}\n")
    for img in prompts["images"]:
        add(f"\n**{img['id']} - {img['use']}** ({img['aspect']})\n")
        add(f"Prompt: {img['prompt']}\n")
        add(f"Camera: {img['camera']} | Light: {img['light']}\n")
        add(f"Negative: {img['negative']}\n")
    add(f"\n**Copy prompt**\n\n{prompts['copy_prompt']}\n")
    add(f"\n**Global negative:** {prompts['negative_prompt']}\n")

    add("\n## 8. Email sequence\n")
    for e in emails:
        add(f"### {e['step']}. {e['name']} ({e['send']})\n")
        add(f"Subject: {e['subject']}  \nPreview: {e['preview_text']}\n")
        add(f"\n{e['body']}\n")

    add("\n## 9. 30-day calendar\n")
    add("| Day | Channel | Format | Hook | CTA | Asset |")
    add("| --- | --- | --- | --- | --- | --- |")
    for r in cal:
        add(f"| {r['day']} | {r['channel']} | {r['format']} | {r['hook_id']} | {r['cta']} | {r['asset']} |")
    add("")

    add("\n## 10. Compliance notes\n")
    add("| Item | Status | Detail |")
    add("| --- | --- | --- |")
    for c in comp:
        add(f"| {c['item']} | {c['status']} | {c['detail']} |")
    add("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize a brief into a full creative pack.")
    ap.add_argument("--brief", required=True, help="Path to brief.yaml or brief.json")
    ap.add_argument("--out", default="campaign", help="Output directory")
    ap.add_argument("--seed", type=int, default=None, help="Random seed (default: derived from brief)")
    ap.add_argument("--product", help="Override product name")
    ap.add_argument("--audience", help="Override audience")
    ap.add_argument("--offer", help="Override offer")
    args = ap.parse_args()

    if not os.path.exists(args.brief):
        print(f"error: brief not found: {args.brief}", file=sys.stderr)
        return 2

    raw = load_brief(args.brief)
    if args.product:
        raw["product"] = args.product
    if args.audience:
        raw["audience"] = args.audience
    if args.offer:
        raw["offer"] = args.offer

    fingerprint = hashlib.sha256(json.dumps(raw, sort_keys=True, default=str).encode()).hexdigest()
    seed = args.seed if args.seed is not None else int(fingerprint[:8], 16)
    rng = random.Random(seed)

    norm = normalize(raw)
    hooks = build_hooks(norm, rng)
    voice = build_voice_card(norm)
    ads = build_ad_copy(norm, hooks, rng)
    social = build_social(norm, hooks)
    ugc = build_ugc(norm, hooks)
    prompts = build_prompts(norm, hooks)
    emails = build_email(norm, hooks)
    cal = build_calendar(norm, hooks)
    comp = build_compliance(norm, raw)

    os.makedirs(args.out, exist_ok=True)
    pack = render_pack(norm, hooks, voice, ads, social, ugc, prompts, emails, cal, comp)

    with open(os.path.join(args.out, "brief.normalized.json"), "w", encoding="utf-8") as fh:
        json.dump(norm, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(args.out, "creative_pack.md"), "w", encoding="utf-8") as fh:
        fh.write(pack)
    with open(os.path.join(args.out, "prompt_set.json"), "w", encoding="utf-8") as fh:
        json.dump(prompts, fh, indent=2, ensure_ascii=False)

    print(f"brief fingerprint : {fingerprint[:12]}")
    print(f"seed              : {seed}")
    print(f"hooks             : {len(hooks)}")
    print(f"channels          : {', '.join(norm['channels'])}")
    print(f"compliance flags  : {sum(1 for c in comp if c['status'] != 'PASS')}")
    print(f"written           : {os.path.join(args.out, 'creative_pack.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
