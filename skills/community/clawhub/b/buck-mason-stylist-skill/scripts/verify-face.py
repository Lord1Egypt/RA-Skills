#!/usr/bin/env python3
"""Verify a gpt-image-2 try-on output's face against the customer's reference
photos using GPT-4o-vision with a strict rubric.

Spec: references/image-generation.md § "Face verification gate".

Why this exists
---------------
gpt-image-2 has a known "make this person generically photogenic" prior that
text prompts only partially suppress. Without a post-generation verification
gate, a single off-putting AI-face can ship to the customer in a hosted
lookbook — the trust-damaging failure mode the whole pipeline exists to
avoid. This script is the second-line defense after prompt rules.

Usage
-----
  scripts/verify-face.py \\
      --generated runs/2026-05-09-mellow-la/looks/look1.png \\
      --reference ~/Pictures/me-portrait.jpg ~/Pictures/me-fullbody.jpg \\
      [--threshold 6] [--off-putting-cap 4] [--model gpt-4o]

Stdout (JSON, pretty-printed):
  {
    "overall_pass": true | false,
    "scores": {
      "hair_match": 0-10, "beard_match": 0-10, "eye_color_match": 0-10,
      "skin_tone_match": 0-10, "age_match": 0-10, "asymmetry_match": 0-10
    },
    "off_putting": 0-10,    // higher = MORE AI-generic / uncanny
    "reason": "one sentence describing the worst dimension"
  }

Exit codes
----------
  0  pass — face matches reference well enough to ship
  1  fail — face drift; regenerate or fall back to Editorial tier
  2  inconclusive — low-quality refs, missing key, vision call errored

Defaults
--------
  --threshold 6           every match score must be >= this
  --off-putting-cap 4     off_putting must be <= this
  --model gpt-4o          OpenAI vision-capable model

Cost: ~$0.01–0.03/run (one vision call, three images at 1024px).
"""
import argparse, base64, json, os, pathlib, sys, urllib.request, urllib.error

# ── CLI ─────────────────────────────────────────────────────────────────────
ap = argparse.ArgumentParser(
    description="Face verification gate for Premium-tier lookbook outputs.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=__doc__.split("Usage")[1] if "Usage" in __doc__ else "",
)
ap.add_argument("--generated", type=pathlib.Path, required=True,
                help="The gpt-image-2 output PNG to verify.")
ap.add_argument("--reference", type=pathlib.Path, nargs="+", required=True,
                help="One or more reference photos of the customer (face / portrait / full-body crops).")
ap.add_argument("--threshold", type=int, default=6,
                help="Minimum acceptable score on every match dimension (0-10). Default 6.")
ap.add_argument("--off-putting-cap", type=int, default=4,
                help="Maximum acceptable off_putting score (0-10). Higher means more AI-generic. Default 4.")
ap.add_argument("--model", default="gpt-4o",
                help="OpenAI model to use for the vision call. Default gpt-4o.")
ap.add_argument("--api-key-env", default="OPENAI_API_KEY",
                help="Env var holding the OpenAI key. Default OPENAI_API_KEY.")
args = ap.parse_args()

api_key = os.environ.get(args.api_key_env)
if not api_key or not api_key.startswith("sk-"):
    print(f"error: {args.api_key_env} not set or not an OpenAI key (sk-...)", file=sys.stderr)
    sys.exit(2)

if not args.generated.exists():
    print(f"error: --generated not found: {args.generated}", file=sys.stderr)
    sys.exit(2)
for r in args.reference:
    if not r.exists():
        print(f"error: --reference not found: {r}", file=sys.stderr)
        sys.exit(2)

# ── Encode images as data URLs ──────────────────────────────────────────────
def data_url(path: pathlib.Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "gif": "image/gif"}.get(suffix, "image/png")
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"

# ── Vision call ─────────────────────────────────────────────────────────────
SYSTEM = """\
You are a strict face-verification gate for an AI-generated try-on lookbook.
Your job is to compare the FIRST image (a generated lookbook hero) against
all subsequent images (the actual customer's reference photos) and decide
whether the generated face faithfully matches the customer.

The customer paid for this lookbook to see THEM in the clothes — not a
better-looking AI version of someone who shares their hair color. A face
that looks "improved" or "more conventionally photogenic" than the reference
is a wrong face.

Score conservatively. The cost of shipping a bad face is higher than the
cost of asking the agent to regenerate.

Return JSON only — no prose preamble, no code fences, no commentary outside
the JSON object."""

USER_PROMPT = """\
Verify the face in image 1 (the generated lookbook hero) against the
person in images 2 onward (the customer's reference photos).

Score each dimension 0–10 (10 = perfect match, 0 = totally wrong):
- hair_match: color, length, density, parting, style
- beard_match: presence, density, length, shape, greying pattern
- eye_color_match: color and eye shape
- skin_tone_match: undertone, contrast, tan/fair, freckles or pigmentation
- age_match: apparent age — DO NOT reward de-aging; older-looking matches
  the reference better than younger
- asymmetry_match: facial asymmetry from the references is preserved
  (not smoothed to bilateral symmetry, not made conventionally even)

Then score 0–10 for off_putting: how much does the generated face have
the "smooth-symmetric AI-male-model" / uncanny / mannequin look?
(0 = none, looks like a real human; 10 = clearly AI-generic).

Then set overall_pass: true ONLY IF
  - every match score >= {threshold}, AND
  - off_putting <= {off_putting_cap}.

Return JSON only:
{{
  "scores": {{
    "hair_match": <0-10>, "beard_match": <0-10>, "eye_color_match": <0-10>,
    "skin_tone_match": <0-10>, "age_match": <0-10>, "asymmetry_match": <0-10>
  }},
  "off_putting": <0-10>,
  "overall_pass": <true|false>,
  "reason": "<one sentence describing the worst dimension or why it passes>"
}}
""".format(threshold=args.threshold, off_putting_cap=args.off_putting_cap)

content = [{"type": "text", "text": USER_PROMPT}]
content.append({"type": "image_url", "image_url": {"url": data_url(args.generated), "detail": "high"}})
for r in args.reference:
    content.append({"type": "image_url", "image_url": {"url": data_url(r), "detail": "high"}})

payload = {
    "model": args.model,
    "messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": content},
    ],
    "response_format": {"type": "json_object"},
    "max_tokens": 400,
    "temperature": 0,
}

req = urllib.request.Request(
    "https://api.openai.com/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
    },
)

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")[:400]
    print(f"error: vision call returned HTTP {e.code}: {body}", file=sys.stderr)
    sys.exit(2)
except Exception as e:
    print(f"error: vision call failed: {e}", file=sys.stderr)
    sys.exit(2)

try:
    raw = resp["choices"][0]["message"]["content"]
    result = json.loads(raw)
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print(f"error: couldn't parse vision response: {e}", file=sys.stderr)
    print(f"raw response: {resp}", file=sys.stderr)
    sys.exit(2)

# Belt-and-suspenders: re-validate overall_pass server-side rather than
# trusting the model to apply the threshold correctly.
scores = result.get("scores", {}) or {}
required_dims = ["hair_match", "beard_match", "eye_color_match",
                 "skin_tone_match", "age_match", "asymmetry_match"]
all_present = all(d in scores for d in required_dims)
all_above_threshold = all_present and all(scores.get(d, 0) >= args.threshold for d in required_dims)
off_putting = result.get("off_putting", 10)
under_cap = off_putting <= args.off_putting_cap

# Override the model's overall_pass with our own evaluation of the rubric.
result["overall_pass"] = bool(all_above_threshold and under_cap)

print(json.dumps(result, indent=2))
sys.exit(0 if result["overall_pass"] else 1)
