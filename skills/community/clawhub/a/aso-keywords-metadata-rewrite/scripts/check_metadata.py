"""Check App Store / Google Play metadata against the store limits.

Usage:
  python3 check_metadata.py --store apple --title "Streaks: Habit Tracker" \
      --subtitle "Build routines that stick" --keywords "routine,daily,goals"
  python3 check_metadata.py --store play --title "…" --short "…" --full-file description.txt

Prints one line per check and exits 1 when any error is found (warnings do not fail).
"""

import argparse
import re
import sys

LIMITS = {
    "apple": {"title": 30, "subtitle": 30, "keywords_bytes": 100, "full": 4000},
    "play": {"title": 30, "short": 80, "full": 4000},
}

# Words Apple ignores or that waste keyword-field space
FILLER = {"app", "apps", "free", "the", "and", "for", "with", "a", "an", "of", "to", "&"}


def words(text):
    return {w for w in re.findall(r"[\w']+", (text or "").lower()) if w}


def check(args):
    errors, warnings, ok = [], [], []
    limits = LIMITS[args.store]

    def length(field, value, limit):
        n = len(value)
        line = f"{field}: {n}/{limit} characters"
        if n > limit:
            errors.append(f"{line} - over by {n - limit}")
        elif n < limit * 0.7 and field in ("title", "subtitle", "short"):
            warnings.append(f"{line} - uses under 70% of the space")
        else:
            ok.append(line)

    if args.title is not None:
        length("title", args.title, limits["title"])
        if args.title.isupper() and len(args.title) > 3:
            warnings.append("title: all caps")

    if args.store == "apple":
        if args.subtitle is not None:
            length("subtitle", args.subtitle, limits["subtitle"])
            repeated = (words(args.title) & words(args.subtitle)) - FILLER
            if repeated:
                warnings.append(f"subtitle repeats title words: {', '.join(sorted(repeated))}")
        if args.keywords is not None:
            kw = args.keywords
            size = len(kw.encode("utf-8"))
            line = f"keywords: {size}/{limits['keywords_bytes']} bytes"
            if size > limits["keywords_bytes"]:
                errors.append(f"{line} - over by {size - limits['keywords_bytes']}")
            elif size < 90:
                warnings.append(f"{line} - {limits['keywords_bytes'] - size} bytes unused")
            else:
                ok.append(line)
            if re.search(r",\s", kw) or kw.startswith(" ") or kw.endswith(" "):
                errors.append("keywords: remove spaces around commas (they count as bytes)")
            terms = [t.strip().lower() for t in kw.split(",") if t.strip()]
            dupes = sorted({t for t in terms if terms.count(t) > 1})
            if dupes:
                errors.append(f"keywords: duplicate entries: {', '.join(dupes)}")
            kw_words = set()
            for t in terms:
                kw_words |= words(t)
            in_listing = kw_words & (words(args.title) | words(args.subtitle))
            in_listing -= FILLER
            if in_listing:
                errors.append(
                    "keywords: words already in the title/subtitle (Apple combines them): "
                    + ", ".join(sorted(in_listing))
                )
            filler = kw_words & FILLER
            if filler:
                warnings.append(f"keywords: filler words waste space: {', '.join(sorted(filler))}")
            plural = sorted(w for w in kw_words if w.endswith("s") and w[:-1] in kw_words)
            if plural:
                warnings.append(f"keywords: singular and plural both present: {', '.join(plural)}")
    else:
        if args.short is not None:
            length("short", args.short, limits["short"])

    full = None
    if args.full_file:
        with open(args.full_file, encoding="utf-8") as f:
            full = f.read()
    elif args.full is not None:
        full = args.full
    if full is not None:
        n = len(full)
        line = f"description: {n}/{limits['full']} characters"
        (errors if n > limits["full"] else ok).append(line if n <= limits["full"] else f"{line} - over by {n - limits['full']}")

    return errors, warnings, ok


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--store", choices=["apple", "play"], required=True)
    p.add_argument("--title")
    p.add_argument("--subtitle", help="Apple subtitle")
    p.add_argument("--keywords", help="Apple keyword field, comma separated")
    p.add_argument("--short", help="Play short description")
    p.add_argument("--full", help="Full description text")
    p.add_argument("--full-file", help="File with the full description")
    args = p.parse_args(argv)

    errors, warnings, ok = check(args)
    for line in ok:
        print(f"OK    {line}")
    for line in warnings:
        print(f"WARN  {line}")
    for line in errors:
        print(f"ERROR {line}")
    print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
