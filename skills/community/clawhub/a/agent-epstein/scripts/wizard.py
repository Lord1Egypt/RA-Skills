"""wizard.py — interactive setup, so nobody has to remember flags.

Asks what to scrape, from where, how many, and where to put it, then
prints (and optionally runs) the exact commands.

    python wizard.py                        # interactive
    python wizard.py --yes --out ./ds       # non-interactive defaults
    python wizard.py --script-only          # print commands, never run
"""
from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STRICT = ["danbooru", "testbooru", "yandere", "konachan",
          "safebooru", "gelbooru", "e621"]
LOOSE = ["twitter", "pixiv"]
ALL_SOURCES = STRICT + LOOSE

HERE = Path(__file__).resolve().parent
# The interpreter running this wizard, not a bare "python" on PATH. The
# skill's deps (playwright, pillow) live in a venv elsewhere, so a
# PATH-resolved system interpreter would fail to import them.
PY = sys.executable or "python"

# Set False by --yes: ask() then returns defaults without touching stdin.
INTERACTIVE = True


def ask(prompt: str, default: str = "") -> str:
    if not INTERACTIVE:
        return default
    suffix = f" [{default}]" if default else ""
    try:
        got = input(f"{prompt}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise SystemExit(130)
    return got or default


def ask_yes(prompt: str, default: bool = False) -> bool:
    d = "Y/n" if default else "y/N"
    got = ask(f"{prompt} ({d})", "").lower()
    if not got:
        return default
    return got.startswith("y")


def ask_int(prompt: str, default: int) -> int:
    got = ask(prompt, str(default))
    try:
        return int(got)
    except ValueError:
        print(f"  not a number, using {default}")
        return default


def main(argv=None) -> int:
    global INTERACTIVE
    p = argparse.ArgumentParser(description="Interactive harvest setup.")
    p.add_argument("--yes", action="store_true",
                   help="accept defaults, ask nothing")
    p.add_argument("--run", action="store_true",
                   help="run the plan instead of only printing it")
    p.add_argument("--script-only", action="store_true",
                   help="print commands only (with --yes this is implicit)")
    p.add_argument("--out", default="")
    p.add_argument("--cdp", default="http://localhost:9222",
                   help="CDP endpoint for sites needing a real session")
    args = p.parse_args(argv)

    interactive = not args.yes
    INTERACTIVE = interactive
    print("=" * 68)
    print("  AgentEpstein — setup")
    print("=" * 68)

    if interactive:
        print("\nWhich sources?")
        print("  strict tags (search term == content):")
        print("   ", ", ".join(STRICT))
        print("  loose/no tags (content must be verified visually):")
        print("   ", ", ".join(LOOSE))
        print("  'all' for everything.")
    sources = ask("\nSources (comma separated or 'all')", "danbooru,yandere,e621")
    if sources.strip().lower() == "all":
        chosen = ALL_SOURCES
    else:
        chosen = [s.strip() for s in sources.split(",") if s.strip()]
    bad = [s for s in chosen if s not in ALL_SOURCES]
    if bad:
        print(f"unknown source(s): {', '.join(bad)}", file=sys.stderr)
        print(f"available: {', '.join(ALL_SOURCES)}", file=sys.stderr)
        return 1
    has_loose = any(s in LOOSE for s in chosen)

    if interactive:
        print("\nWhat to look for.")
        print("  On strict-tag sites this is a tag, e.g. 'yuri'.")
        print("  On X/Pixiv use the fandom + characters instead, e.g.")
        print("  'wuthering waves' + 'jinhsi,changli,yinlin,camellya'.")
    tags = ask("Tag / query", "yuri")
    fandom = ""
    chars = ""
    if has_loose:
        fandom = ask("Fandom / game name (for X & Pixiv)", "")
        chars = ask("Character names, comma separated (for ship queries)", "")

    limit = ask_int("\nHow many images, total cap", 20)
    if interactive:
        print("\nContent you want. This is a CEILING, so 'sensitive' keeps")
        print("safe and sensitive art together, not only sensitive.")
        print("  general      safe only (default)")
        print("  sensitive    + suggestive")
        print("  questionable + more")
        print("  explicit     everything the site has")
        print("  any          no rating limit at all")
    rating = ask("Rating ceiling", "general")
    if rating not in ("general", "sensitive", "questionable", "explicit", "any"):
        print(f"  '{rating}' is not a rating; using general")
        rating = "general"

    min_likes = 0
    if "twitter" in chosen:
        if interactive:
            print("\nMinimum likes on X.")
            print("  X search returns a lot of reposts, screenshots and")
            print("  chatter. Filtering by engagement server-side is the")
            print("  cheapest way to skip it. 0 disables.")
        min_likes = ask_int("Minimum likes (X only, 0 = off)", 100)

    out = args.out or ask("\nWhere should the dataset go", "./dataset")

    use_gate = False
    if has_loose:
        if interactive:
            print("\nX and Pixiv have no reliable tags, so a search hit is")
            print("NOT evidence the image is what you asked for. Recommended")
            print("flow: collect a big candidate pool, look at every one,")
            print("then download only the ones that pass.")
        use_gate = ask_yes("Use the verify-before-download flow?", True)

    cdp = ""
    if any(s in LOOSE for s in chosen):
        if interactive:
            print("\nX refuses to let an automated browser log in. The fix is")
            print("to drive YOUR browser: run start_browser.py in another")
            print("terminal, log in there, then point at its debug port.")
        if ask_yes(f"Attach to your real browser at {args.cdp}?", True):
            cdp = args.cdp

    # ---- build the plan --------------------------------------------------
    base = [PY, str(HERE / "harvest.py"), "--out", out,
            "--limit", str(limit), "--rating", rating,
            "--show-rating-breakdown"]
    if cdp:
        base += ["--cdp", cdp]
    if min_likes and "twitter" in chosen:
        base += ["--min-likes", str(min_likes)]

    steps: list[list[str]] = []
    if use_gate:
        steps.append([PY, str(HERE / "start_browser.py")] if cdp else [])
        steps.append(base + ["--sources", ",".join(chosen), "--tags", tags,
                             "--fandom", fandom, "--chars", chars,
                             "--pool", str(limit * 4), "--vision-gate"])
        steps.append([PY, str(HERE / "vision_filter.py"),
                      "--dataset", out, "--backend", "worklist"])
        steps.append(["# agent looks at each image in vision_worklist.json,",
                      "then writes verdicts.json"])
        steps.append([PY, str(HERE / "vision_filter.py"), "--dataset", out,
                      "--apply", "verdicts.json", "--drop"])
        steps.append(base + ["--sources", ",".join(chosen),
                             "--download-only"])
    else:
        steps.append(base + ["--sources", ",".join(chosen), "--tags", tags])

    steps.append([PY, str(HERE / "publish.py"), "--dataset", out,
                  "--mode", "local"])

    print("\n" + "=" * 68)
    print("  PLAN")
    print("=" * 68)
    if cdp:
        print("\n# 1. In another terminal: open the browser you'll log into")
        print(f"   {PY} \"{HERE / 'start_browser.py'}\"")
        print("   Log into x.com in the window that opens.")
    for i, cmd in enumerate([s for s in steps if s], 1):
        print(f"\n# {i}.")
        print("   " + " ".join(shlex.quote(c) if " " in c else c for c in cmd))

    print(f"\nDataset will be written to: {Path(out).resolve()}")
    if use_gate:
        print("Nothing is downloaded until the images have been looked at.")

    if not args.run or args.script_only:
        print("\n(not run — add --run to execute, or copy the commands)")
        return 0

    import subprocess
    for cmd in [s for s in steps if s and not s[0].startswith("#")]:
        if cmd[0] == PY and cmd[1].endswith("start_browser.py"):
            print("\nSkipping start_browser (needs its own terminal).")
            continue
        print(f"\n$ {' '.join(cmd)}")
        rc = subprocess.call(cmd)
        if rc != 0:
            print(f"  step exited {rc}; stopping.", file=sys.stderr)
            return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
