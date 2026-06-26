#!/usr/bin/env python3
"""Score a calendar event for "should we build a lookbook?"

See references/event-suitability.md for the rubric.

Usage:
  echo '{"title": "...", "description": "...", "duration_days": 3, "is_travel": true}' \
    | scripts/score-calendar-event.py

  # or pass a file
  scripts/score-calendar-event.py --file event.json

Output (stdout, JSON):
  {
    "score":  9,
    "breakdown": {"type": 4, "dress_code": 3, "duration": 1, "location": 1, "signal": 0},
    "action": "premium",   // skip | soft | editorial | premium
    "reason": "wedding · smart-casual · multi-day · travel"
  }

Exit codes:
  0  always (this script never fails the calling pipeline; an unrecognized
     event scores 0 → action: skip, which is the right outcome)
"""
import argparse, json, re, sys, pathlib

# ── Type classifier ────────────────────────────────────────────────────────

VETO_PATTERNS = [
    r"\b(dr\.?|doctor)\s+\w+", r"physical", r"appointment", r"check[- ]?up",
    r"dentist", r"dental", r"orthodontist", r"therapy", r"therapist",
    r"counsel(?:or|ing)", r"colonoscopy", r"mammo", r"obgyn", r"primary care",
]

TYPE_PATTERNS = [
    # (regex, weight, label)
    (r"\bwedding\b|engagement|black[- ]tie|gala|bar mitzvah|bat mitzvah|quinceañera", 4, "formal-event"),
    (r"\b(vacation|trip|travel)\b|\b(weekend|getaway)\b", 3, "travel"),
    (r"\b(concert|show|festival|theater|opera)\b|\bnightclub\b|speakeasy", 2, "show"),
    (r"\b(party|birthday|dinner|drinks|brunch|cocktails?)\b", 2, "social"),
    (r"\b(conference|sessions?|summit|keynote|panel|on[- ]stage|podcast|headshot)\b", 2, "professional"),
    (r"\b(school pickup|soccer practice|practice|carpool)\b", 0, "family-logistics"),
    (r"^\s*(block|focus|reminder|todo|task)\b", 0, "block"),
    (r"\b1[ \-:]on[ \-:]?1\b|\bone[ \-]on[ \-]one\b|\bcheck[- ]in\b|sync\b|coffee with\b|\bcatch up\b", 0, "meeting"),
    (r"\b(errand|costco|grocery|target run|dmv|cleaner|pharmacy)\b", 0, "errand"),
]

DRESS_CODE_EXPLICIT = re.compile(
    r"\b(black[- ]tie|white[- ]tie|smart[- ]casual|business casual|festive|cocktail|creative attire|formal attire)\b",
    re.I,
)
VENUE_HINTS = [
    r"\bbestia\b", r"\bn/?naka\b", r"\bcasa madera\b", r"\brepublique\b",
    r"\bspeakeasy\b", r"\brooftop\b", r"\bthe standard\b", r"\bsohohouse\b",
    r"\bchateau\b", r"\bnomad\b", r"\b1 hotel\b", r"\bproper\b",
]

# ── Scoring ────────────────────────────────────────────────────────────────

def classify_type(title: str, description: str):
    text = f"{title}\n{description}".lower()
    for p in VETO_PATTERNS:
        if re.search(p, text, re.I):
            return -10, "medical-or-therapy"
    for pat, weight, label in TYPE_PATTERNS:
        if re.search(pat, text, re.I):
            return weight, label
    return 0, "unclassified"

def dress_code_weight(title: str, description: str, type_label: str):
    text = f"{title}\n{description}"
    if DRESS_CODE_EXPLICIT.search(text):
        return 3
    for p in VENUE_HINTS:
        if re.search(p, text, re.I):
            return 2
    if type_label == "travel":
        return 2
    return 0

def duration_weight(duration_days: int):
    return 1 if duration_days and duration_days >= 2 else 0

def location_weight(is_travel: bool, home_metro: str | None, event_location: str | None):
    if is_travel:
        return 1
    if home_metro and event_location and home_metro.lower() not in event_location.lower():
        return 1
    return 0

def customer_signal(opt_in: bool, opt_out: bool, prior_positive: bool):
    if opt_out:
        return -2
    if opt_in:
        return 2
    if prior_positive:
        return 1
    return 0

def action_for(score: int) -> str:
    if score <= 5:  return "skip"
    if score == 6:  return "soft"
    if score <= 8:  return "editorial"
    return "premium"

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=pathlib.Path, help="Read JSON event from file (else stdin)")
    args = ap.parse_args()

    raw = args.file.read_text() if args.file else sys.stdin.read()
    if not raw.strip():
        print(json.dumps({"score": 0, "action": "skip", "reason": "empty input"}))
        return
    ev = json.loads(raw)

    title       = (ev.get("title") or "").strip()
    description = (ev.get("description") or "").strip()
    duration    = int(ev.get("duration_days", 0) or 0)
    is_travel   = bool(ev.get("is_travel", False))
    home_metro  = ev.get("home_metro")
    event_loc   = ev.get("event_location")
    opt_in      = bool(ev.get("customer_opt_in_for_this_event", False))
    opt_out     = bool(ev.get("customer_opt_out_for_this_class", False))
    prior_pos   = bool(ev.get("customer_prior_positive", False))

    type_w, type_label = classify_type(title, description)

    # Hard veto: medical / therapy → -10 dominates everything
    if type_w == -10:
        out = {
            "score": -10,
            "breakdown": {"type": -10, "dress_code": 0, "duration": 0, "location": 0, "signal": 0},
            "action": "skip",
            "reason": f"hard-veto:{type_label}",
        }
        print(json.dumps(out, indent=2))
        return

    dress_w = dress_code_weight(title, description, type_label)
    dur_w   = duration_weight(duration)
    loc_w   = location_weight(is_travel, home_metro, event_loc)
    sig_w   = customer_signal(opt_in, opt_out, prior_pos)

    score = type_w + dress_w + dur_w + loc_w + sig_w
    score = max(0, score)  # clamp at 0 below the hard-veto path

    out = {
        "score": score,
        "breakdown": {"type": type_w, "dress_code": dress_w, "duration": dur_w, "location": loc_w, "signal": sig_w},
        "action": action_for(score),
        "reason": f"{type_label}{('·dress_code' if dress_w > 0 else '')}{('·multi-day' if dur_w else '')}{('·travel' if loc_w else '')}",
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
