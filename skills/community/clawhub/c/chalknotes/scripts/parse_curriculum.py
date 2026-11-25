#!/usr/bin/env python3
"""Parse an expanded Udemy curriculum text block into structured JSON.

Usage:
  python parse_curriculum.py raw.txt -o curriculum.json [--name COURSE] [--url URL]

Input: visible text of the expanded curriculum (first section title through
the last lecture). Section header = title line followed by 'N lectures • ...'.
Numbering = sequential over all non-quiz items (quizzes unnumbered; coding
exercises and resource downloads consume numbers). Stdlib only.
"""
import argparse, json, re, sys

DUR = re.compile(r'^\d+:\d{2}$')
HDR = re.compile(r'^(\d+) lectures? • (.+)$')


def parse(lines):
    lines = [l.strip() for l in lines if l.strip()]

    def is_header(i):
        return i + 1 < len(lines) and bool(HDR.match(lines[i + 1]))

    sections, i, num = [], 0, 0
    while i < len(lines):
        if not is_header(i):
            i += 1
            continue
        m = HDR.match(lines[i + 1])
        sec = {"section": len(sections) + 1, "title": lines[i],
               "declared_videos": int(m.group(1)), "length": m.group(2),
               "items": []}
        i += 2
        while i < len(lines) and not is_header(i):
            t = lines[i]
            if t == "Quiz":
                sec["items"].append({"title": "Quiz", "type": "quiz"})
                i += 1
                continue
            j = i + 1
            preview = False
            if j < len(lines) and lines[j] == "Preview":
                preview = True
                j += 1
            if j < len(lines) and DUR.match(lines[j]):
                num += 1
                it = {"n": num, "title": t, "type": "video",
                      "duration": lines[j]}
                if preview:
                    it["preview"] = True
                sec["items"].append(it)
                i = j + 1
            else:
                num += 1
                sec["items"].append({"n": num, "title": t,
                                     "type": "exercise"})
                i += 1
        sections.append(sec)
    return sections, num


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("-o", "--out", default="curriculum.json")
    ap.add_argument("--name", default="")
    ap.add_argument("--url", default="")
    a = ap.parse_args()
    text = open(a.raw, encoding="utf-8").read()
    sections, num = parse(text.split("\n"))
    if not sections:
        print("ERROR: no section headers found — is the text the expanded "
              "curriculum block?", file=sys.stderr)
        sys.exit(1)
    videos = sum(1 for s in sections for it in s["items"] if it["type"] == "video")
    exercises = sum(1 for s in sections for it in s["items"] if it["type"] == "exercise")
    quizzes = sum(1 for s in sections for it in s["items"] if it["type"] == "quiz")
    doc = {"course": a.name, "url": a.url, "sections": sections}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"sections={len(sections)} numbered={num} videos={videos} "
          f"exercises={exercises} quizzes={quizzes}")
    print("Validate these ranges against the course player:")
    for s in sections:
        ns = [it["n"] for it in s["items"] if "n" in it]
        rng = f"{ns[0]}-{ns[-1]}" if ns else "-"
        print(f"  {s['section']:2d}. {s['title']}  [{rng}] "
              f"(declared {s['declared_videos']} videos)")
    print(f"saved {a.out}")


if __name__ == "__main__":
    main()
