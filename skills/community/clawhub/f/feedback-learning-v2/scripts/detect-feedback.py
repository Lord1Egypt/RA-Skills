#!/usr/bin/env python3
"""
detect-feedback.py v2 — Detect user feedback signals from text.
Returns JSON with type and details. No LLM needed — pure regex/pattern matching.
Supports Russian and English. Bilingual by design.

Usage:
  echo "переделай это" | python3 detect-feedback.py
  python3 detect-feedback.py "не так, сделай по-другому"
  python3 detect-feedback.py --pipe  # reads stdin, outputs nothing if "none"
"""
import re
import sys
import json

# === NLP TRIGGERS ===

NEGATIVE_RU = [
    r'\bфигня\b', r'\bпеределай\b', r'\bне\s+так\b', r'\bстоп\b',
    r'\bнеправильно\b', r'\bзаново\b', r'\bне\s+то\b', r'\bотмени\b',
    r'\bверни\b', r'\bоткати\b', r'\bне\s+надо\b', r'\bубери\b',
    r'\bхрень\b', r'\bфиг\w*\b', r'\bбред\b', r'\bчушь\b',
    r'\bне\s+работает\b', r'\bсломал\b', r'\bопять\b',
    r'\bужас\b', r'\bкошмар\b', r'\bплохо\b', r'\bневерно\b',
]

POSITIVE_RU = [
    r'\bкруто\b', r'\bтоп\b', r'\bзашло\b', r'\bкрасава\b',
    r'\bспасибо\b', r'\bогонь\b', r'\bимба\b', r'\bсупер\b',
    r'\bотлично\b', r'\bмолодец\b', r'\bкласс\b', r'\bпушка\b',
    r'\bидеально\b', r'\bчётко\b', r'\bзаебись\b', r'\bахуенно\b',
    r'\bнорм\b', r'\bгуд\b', r'\bлайк\b', r'\bволшебно\b',
    r'\bшикарно\b', r'\bбомба\b', r'\bпрекрасно\b',
]

CORRECTION_RU = [
    r'не\s+\w+[,\s]+а\s+\w+',            # "не X, а Y"
    r'я\s+имел\s+в\s+виду',               # "я имел в виду"
    r'нет[,\s]+сделай',                    # "нет, сделай"
    r'нет[,\s]+я\s+про',                   # "нет, я про"
    r'не\s+это[,\s]+а',                    # "не это, а"
    r'я\s+говорил\s+про',                  # "я говорил про"
    r'я\s+имею\s+в\s+виду',               # "я имею в виду"
    r'точнее[,\s]',                        # "точнее,"
]

NEGATIVE_EN = [
    r'\bwrong\b', r'\bredo\b', r'\bfix\s+it\b', r'\bnot\s+right\b',
    r'\bstop\b', r'\brevert\b', r'\bundo\b', r'\bnot\s+that\b',
    r'\btry\s+again\b', r'\bbroken\b', r'\bthat.s\s+wrong\b',
    r'\bno[,\s]', r'\bincorrect\b',
]

POSITIVE_EN = [
    r'\bthanks\b', r'\bthank\s+you\b', r'\bgreat\b', r'\bperfect\b',
    r'\bnice\b', r'\bawesome\b', r'\bgood\s+job\b', r'\blgtm\b',
    r'\bcool\b', r'\bexcellent\b', r'\bnailed\s+it\b',
]

EMOJI_POSITIVE = ['👍', '❤️', '🔥', '👏', '💯', '😍', '🎉', '🤩', '❤', '❤‍🔥', '⚡', '🏆', '✅']
EMOJI_NEGATIVE = ['👎', '🤦', '😤', '🤬', '💩', '❌', '🚫']

REQUERY_PATTERNS = [
    r'ещё\s+раз',
    r'повтори',
    r'снова\s+попробуй',
    r'опять\s+то\s+же',
    r'again',
    r'retry',
]


def detect(text: str) -> dict:
    text_lower = text.lower().strip()

    # Check emoji first (highest confidence)
    for e in EMOJI_POSITIVE:
        if e in text:
            return {"type": "positive", "source": "user_emoji", "signal": e, "confidence": 0.95}
    for e in EMOJI_NEGATIVE:
        if e in text:
            return {"type": "correction", "source": "user_emoji", "signal": e, "confidence": 0.95}

    # Check corrections (most specific patterns)
    for pat in CORRECTION_RU:
        m = re.search(pat, text_lower)
        if m:
            return {"type": "correction", "source": "user_nlp", "signal": m.group(), "confidence": 0.9}

    # Check requery
    for pat in REQUERY_PATTERNS:
        m = re.search(pat, text_lower)
        if m:
            return {"type": "requery", "source": "requery", "signal": m.group(), "confidence": 0.7}

    # Check negative
    for pat in NEGATIVE_RU + NEGATIVE_EN:
        m = re.search(pat, text_lower)
        if m:
            return {"type": "correction", "source": "user_nlp", "signal": m.group(), "confidence": 0.8}

    # Check positive
    for pat in POSITIVE_RU + POSITIVE_EN:
        m = re.search(pat, text_lower)
        if m:
            return {"type": "positive", "source": "user_nlp", "signal": m.group(), "confidence": 0.8}

    return {"type": "none", "source": "none", "signal": "", "confidence": 0.0}


if __name__ == "__main__":
    pipe_mode = "--pipe" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        text = " ".join(args)
    else:
        text = sys.stdin.read()

    result = detect(text)

    if pipe_mode and result["type"] == "none":
        # In pipe mode, output nothing if no signal detected
        sys.exit(0)

    print(json.dumps(result, ensure_ascii=False))
