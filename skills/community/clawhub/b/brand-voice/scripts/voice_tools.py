#!/usr/bin/env python3
"""Measure and check brand voice (standard library only).

Commands
  profile FILE [FILE ...] [--out profile.json]
      Measure writing habits from real samples. Each file may hold several posts separated by a line with ---.
  check DRAFT.txt --profile profile.json [--rules rules.json] [--strict] [--json out.json]
      Compare a draft with the measured profile and with explicit rules; flag stock AI phrases.
  cliches
      Print the built-in list of stock phrases that often make text sound machine-written.

rules.json (all keys optional)
  {"banned": ["synergy"], "preferred": {"utilize": "use"}, "must_include": ["Botvee"],
   "max_sentence_words": 25, "max_emoji": 2, "max_hashtags": 5}

The numbers describe habits in the samples. They do not capture meaning, humour or taste; a person must still
read the draft. Fewer than 10 posts or 1,000 words gives an unreliable profile and the tool says so.
"""
import argparse
import json
import math
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆↔-↪⬅-⬇©®‼⁉"
                   "⌚-⏿\U0001F000-\U0001F2FF]")
WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
HASHTAG = re.compile(r"(?<!\w)#\w+", re.UNICODE)
URL = re.compile(r"https?://\S+")
STOP_EN = set("the a an and or but if of to in on at for with is are was were be been it this that these those as by from "
              "so not no do does did have has had i you he she we they me my your our their his her its will would can "
              "could should just about into than then there here what which who when where how all any more most".split())
# DATA, not prose: the lists below hold common Roman Urdu words (pronouns, "is/was", "and/or", verb endings).
# They let the profile and check commands measure posts written in Roman Urdu or Hinglish (language share,
# "we"/"you" usage, calls to action). Removing them breaks those measurements for mixed-language brands.
STOP_UR = set("hai hain tha thi the ka ki ke ko se me mein par pe to bhi ye wo yeh woh aur ya kya nahi nahin hi ho kar "
              "karo kare karna raha rahi rahe hota hoti hote lekin magar toh aap main mera meri mere hum tum apna apni "
              "apne is us in un jo jab tak sirf bohat bahut".split())
ROMAN_URDU = set("hai hain nahi nahin kya aur mein hum aap yeh woh bohat bahut ka ki ke ko se mera meri apna karo kar hota raha rahi".split())
FIRST = {"i", "me", "my", "mine", "myself", "we", "our", "us", "main", "mera", "meri", "mere", "hum", "hamara", "hamari"}
SECOND = {"you", "your", "yours", "aap", "aapka", "aapki", "aapke", "tum", "tumhara", "tera", "teri"}
CTA = {"click", "subscribe", "follow", "join", "download", "try", "start", "get", "book", "buy", "learn", "register",
       "comment", "share", "save", "dm", "message", "visit", "sign", "shuru", "karein", "dekhein", "jaiye"}
CLICHES = [
    "in today's fast-paced world", "in today's digital age", "in the ever-evolving", "ever-evolving landscape",
    "game-changer", "game changer", "unlock the power", "unlock your", "take it to the next level", "revolutionize",
    "delve into", "dive into", "dive in", "it's important to note", "it is important to note", "tapestry",
    "seamless", "seamlessly", "elevate your", "leverage", "cutting-edge", "state-of-the-art", "robust solution",
    "harness the power", "look no further", "navigate the complexities", "in the realm of", "at the end of the day",
    "supercharge", "skyrocket", "mind-blowing", "you won't believe", "here's the thing", "let that sink in",
    "thread below", "🧵👇", "i'm excited to announce", "thrilled to announce", "humbled to",
]


class Fail(RuntimeError):
    pass


def split_posts(text):
    parts = re.split(r"(?m)^\s*---+\s*$", text)
    return [p.strip() for p in parts if p.strip()]


def sentences(text):
    t = URL.sub(" ", text)
    out = [s.strip() for s in re.split(r"(?<=[.!?۔…])\s+|\n+", t) if s.strip()]
    return [s for s in out if WORD.search(s)]


def measure(posts):
    all_words, sent_lens, openers, trigrams = [], [], Counter(), Counter()
    emoji = hashtags = excl = ques = caps = contractions = ellipsis = dashes = ctas = links = 0
    first = second = 0
    n_sent = 0
    per_post_words = []
    sw = Counter()
    ur = 0
    for p in posts:
        words = WORD.findall(p)
        low = [w.lower() for w in words]
        all_words += low
        per_post_words.append(len(words))
        emoji += len(EMOJI.findall(p))
        hashtags += len(HASHTAG.findall(p))
        links += len(URL.findall(p))
        ellipsis += p.count("...") + p.count("…")
        dashes += p.count("—") + p.count(" - ")
        caps += sum(1 for w in words if len(w) > 2 and w.isupper())
        contractions += sum(1 for w in words if "'" in w or "’" in w)
        ss = sentences(p)
        n_sent += len(ss)
        for s in ss:
            sent_lens.append(len(WORD.findall(s)))
            excl += s.count("!")
            ques += s.count("?") + s.count("؟")
        if ss:
            first_words = WORD.findall(ss[0])[:3]
            if first_words:
                openers[" ".join(first_words).lower()] += 1
        for i in range(len(low) - 2):
            tri = tuple(low[i:i + 3])
            if not all(w in STOP_EN or w in STOP_UR for w in tri):
                trigrams[" ".join(tri)] += 1
        first += sum(1 for w in low if w in FIRST)
        second += sum(1 for w in low if w in SECOND)
        ctas += sum(1 for w in low if w in CTA)
        for w in low:
            if len(w) > 3 and w not in STOP_EN and w not in STOP_UR:
                sw[w] += 1
        ur += sum(1 for w in low if w in ROMAN_URDU)
    nw = max(1, len(all_words))
    ns = max(1, n_sent)
    npost = max(1, len(posts))
    return {
        "posts": len(posts), "words": len(all_words),
        "avg_post_words": round(statistics.mean(per_post_words), 1) if per_post_words else 0,
        "avg_sentence_words": round(statistics.mean(sent_lens), 1) if sent_lens else 0,
        "median_sentence_words": statistics.median(sent_lens) if sent_lens else 0,
        "short_sentence_share": round(sum(1 for x in sent_lens if x <= 8) / ns, 2),
        "long_sentence_share": round(sum(1 for x in sent_lens if x >= 25) / ns, 2),
        "emoji_per_post": round(emoji / npost, 2), "hashtags_per_post": round(hashtags / npost, 2),
        "links_per_post": round(links / npost, 2),
        "exclaim_per_sentence": round(excl / ns, 2), "question_per_sentence": round(ques / ns, 2),
        "caps_words_per_100w": round(caps * 100 / nw, 2), "contractions_per_100w": round(contractions * 100 / nw, 2),
        "ellipsis_per_post": round(ellipsis / npost, 2), "dashes_per_post": round(dashes / npost, 2),
        "first_person_per_100w": round(first * 100 / nw, 2), "second_person_per_100w": round(second * 100 / nw, 2),
        "cta_verbs_per_100w": round(ctas * 100 / nw, 2), "roman_urdu_share": round(ur / nw, 3),
        "top_openers": openers.most_common(5),
        "signature_phrases": [(k, v) for k, v in trigrams.most_common(40) if v >= 3][:10],
        "top_words": sw.most_common(15),
    }


def cmd_profile(a):
    posts = []
    for f in a.files:
        p = Path(f)
        if not p.exists():
            raise Fail(f"{f} not found.")
        posts += split_posts(p.read_text(encoding="utf-8-sig"))
    if not posts:
        raise Fail("No text found in the samples.")
    m = measure(posts)
    warn = []
    if m["posts"] < 10 or m["words"] < 1000:
        warn.append(f"Only {m['posts']} posts and {m['words']} words: aim for 10+ posts and 1,000+ words; treat this profile as a rough sketch.")
    if m["roman_urdu_share"] > 0.12:
        warn.append(f"About {m['roman_urdu_share']:.0%} of words look like Roman Urdu/Hinglish; spelling varies, so word counts are approximate.")
    m["warnings"] = warn
    for k, v in m.items():
        if k not in ("warnings",):
            print(f"{k:26} {v}")
    for w in warn:
        print(f"[NOTE] {w}")
    if a.out:
        Path(a.out).write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved {a.out}")


def cmd_check(a):
    draft = Path(a.draft).read_text(encoding="utf-8-sig")
    profile = json.loads(Path(a.profile).read_text(encoding="utf-8")) if a.profile else None
    rules = json.loads(Path(a.rules).read_text(encoding="utf-8")) if a.rules else {}
    d = measure([draft.strip()])
    issues = []

    def add(level, msg):
        issues.append({"level": level, "text": msg})

    low = draft.lower()
    for c in CLICHES:
        if c in low:
            add("WARN", f"Stock phrase: '{c}'. Say the specific thing instead.")
    for b in rules.get("banned", []):
        if re.search(rf"(?<!\w){re.escape(b.lower())}(?!\w)", low):
            add("FAIL", f"Banned word/phrase: '{b}'.")
    for bad, good in (rules.get("preferred") or {}).items():
        if re.search(rf"(?<!\w){re.escape(bad.lower())}(?!\w)", low):
            add("WARN", f"Use '{good}' instead of '{bad}'.")
    for m in rules.get("must_include", []):
        if m.lower() not in low:
            add("WARN", f"Expected '{m}' (brand name or required term) is missing.")
    if rules.get("max_sentence_words"):
        for s in sentences(draft):
            n = len(WORD.findall(s))
            if n > rules["max_sentence_words"]:
                add("WARN", f"Sentence of {n} words: '{s[:60]}...'")
    if rules.get("max_emoji") is not None and d["emoji_per_post"] > rules["max_emoji"]:
        add("WARN", f"{d['emoji_per_post']:.0f} emoji (limit {rules['max_emoji']}).")
    if rules.get("max_hashtags") is not None and d["hashtags_per_post"] > rules["max_hashtags"]:
        add("WARN", f"{d['hashtags_per_post']:.0f} hashtags (limit {rules['max_hashtags']}).")
    if re.search(r"\b(\w+)\s+\1\b", low):
        add("INFO", "A word is repeated twice in a row.")
    if draft.count("—") >= 3:
        add("INFO", "Several em dashes; check that this is the brand's habit and not a machine-writing tell.")
    if profile:
        spec = [("avg_sentence_words", 3, "average sentence length (words)"),
                ("emoji_per_post", 1.5, "emoji per post"), ("hashtags_per_post", 1.5, "hashtags per post"),
                ("exclaim_per_sentence", 0.2, "exclamation marks per sentence"),
                ("question_per_sentence", 0.2, "questions per sentence"),
                ("caps_words_per_100w", 2, "ALL-CAPS words per 100 words")]
        for key, floor, label in spec:
            ref, cur = profile.get(key, 0), d[key]
            if abs(cur - ref) > max(floor, abs(ref) * 0.6):
                add("INFO", f"{label}: draft {cur} vs your usual {ref}.")
        if profile.get("posts", 0) < 10:
            add("INFO", "The profile is built from fewer than 10 posts, so comparisons are weak.")
    fails = sum(1 for i in issues if i["level"] == "FAIL")
    warns = sum(1 for i in issues if i["level"] == "WARN")
    for i in issues:
        print(f"[{i['level']}] {i['text']}")
    if not issues:
        print("No mechanical issues found. Read it aloud: does it sound like the brand?")
    print(f"\n{fails} fail, {warns} warn. Mechanical checks only; they cannot judge tone, humour or accuracy.")
    if a.json:
        Path(a.json).write_text(json.dumps({"measures": d, "issues": issues}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if fails or (a.strict and warns) else 0


def cmd_cliches(_):
    print("\n".join(CLICHES))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("profile")
    s.add_argument("files", nargs="+")
    s.add_argument("--out")
    s.set_defaults(fn=cmd_profile)
    c = sub.add_parser("check")
    c.add_argument("draft")
    c.add_argument("--profile")
    c.add_argument("--rules")
    c.add_argument("--strict", action="store_true")
    c.add_argument("--json")
    c.set_defaults(fn=cmd_check)
    l = sub.add_parser("cliches")
    l.set_defaults(fn=cmd_cliches)
    a = p.parse_args(argv)
    try:
        return a.fn(a) or 0
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
