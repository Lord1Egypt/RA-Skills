#!/usr/bin/env python3
"""
Build (or refresh) the msicons.com icon index.

msicons.com is a Vite SPA whose main JS bundle inlines the path of every icon
SVG it serves. The icons themselves are plain static files at:

    https://msicons.com/icons/<Category>/<Filename>.svg

This script downloads the current bundle, extracts every "/icons/.../*.svg"
path, derives a human-readable name + search tokens from each filename, and
writes references/icon-index.json.

Run this only when you want to refresh the index (e.g. msicons added new
icons). The skill ships with a pre-built index, so day-to-day use does NOT
need network access for the index itself.

Usage:
    python build_icon_index.py                # fetch bundle, write index
    python build_icon_index.py --bundle x.js  # use a local bundle file
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

SITE = "https://msicons.com"
OUT = Path(__file__).resolve().parent.parent / "references" / "icon-index.json"

# Color/theme suffixes and prefixes that are noise for matching.
NOISE = [
    "_scalable", "_Light", "_Dark", "_Gray", "_Grey", "_Blue", "_blue",
    "dark-blue-", "light-blue-", "blue-", "gray-", "grey-",
]


def fetch_bundle() -> str:
    # Find the hashed bundle name from the index.html, then download it.
    html = urllib.request.urlopen(f"{SITE}/", timeout=30).read().decode("utf-8", "replace")
    m = re.search(r'src="(/assets/index-[^"]+\.js)"', html)
    if not m:
        sys.exit("Could not locate the JS bundle in index.html (site layout changed?)")
    url = SITE + m.group(1)
    return urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "replace")


def humanize(filename: str) -> str:
    """'PowerAutomate_scalable.svg' -> 'Power Automate'.
    '00028-icon-service-Batch-AI.svg' -> 'Batch AI'."""
    name = re.sub(r"\.svg$", "", filename, flags=re.I)
    # Azure official icons are named "<digits>-icon-service-<Name>"
    name = re.sub(r"^\d+[-_ ]*icon[-_ ]*service[-_ ]*", "", name, flags=re.I)
    name = re.sub(r"^\d+[-_ ]+", "", name)  # any other leading numeric id
    for n in NOISE:
        name = name.replace(n, " ")
    # split camelCase / PascalCase (Power-Automate already split below)
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def tokens(name: str, category: str) -> str:
    base = re.sub(r"[^a-z0-9 ]", " ", f"{name} {category}".lower())
    collapsed = base.replace(" ", "")          # 'open ai' -> 'openai'
    return f"{base} {collapsed}".strip()


def build(bundle: str) -> list[dict]:
    paths = sorted(set(re.findall(r'/icons/[^"\']+?\.svg', bundle)))
    out = []
    for p in paths:
        parts = p.split("/")
        category = parts[2] if len(parts) > 3 else ""
        filename = parts[-1]
        name = humanize(filename)
        out.append({
            "provider": "microsoft",
            "path": p,
            "url": SITE + p,
            "category": category,
            "name": name,
            "search": tokens(name, category),
        })
    return out


def bundle_svgs(entries, root):
    """Download each entry's SVG into assets/icons/microsoft/<cat>/ and set
    entry['file'] so the Microsoft set works offline."""
    import urllib.parse
    base = root / "assets" / "icons" / "microsoft"
    ok = 0
    for e in entries:
        cat = re.sub(r"[^A-Za-z0-9._-]", "_", e["category"] or "misc")
        (base / cat).mkdir(parents=True, exist_ok=True)
        fn = re.sub(r"[^A-Za-z0-9._-]", "_", e["url"].split("/")[-1])
        f = base / cat / fn
        e["file"] = f.relative_to(root).as_posix()
        if not (f.exists() and f.stat().st_size):
            try:
                u = urllib.parse.quote(e["url"], safe=":/?#[]@!$&'()*+,;=~")
                f.write_bytes(urllib.request.urlopen(u, timeout=30).read())
            except Exception as ex:
                print(f"  ! {e['url']}: {ex}", file=sys.stderr)
                e.pop("file", None)
                continue
        ok += 1
    print(f"Bundled {ok}/{len(entries)} Microsoft SVGs into {base}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", help="path to a local msicons bundle .js (skip download)")
    ap.add_argument("--offline", action="store_true",
                    help="also download every SVG into assets/icons/microsoft/ so "
                         "the Microsoft set works without network")
    args = ap.parse_args()

    bundle = Path(args.bundle).read_text("utf-8", "replace") if args.bundle else fetch_bundle()
    ms = build(bundle)
    if args.offline:
        bundle_svgs(ms, OUT.parent.parent)

    # Merge into the existing multi-provider index, replacing only 'microsoft'
    # (so aws / azure / gcp entries added by add_icon_pack.py are preserved).
    OUT.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(OUT.read_text("utf-8")) if OUT.exists() else []
    for e in existing:
        e.setdefault("provider", "microsoft")
    merged = [e for e in existing if e.get("provider") != "microsoft"] + ms
    OUT.write_text(json.dumps(merged, ensure_ascii=False))
    provs = sorted({e.get("provider") for e in merged})
    print(f"Wrote {len(ms)} microsoft icons; index now {len(merged)} across {provs} -> {OUT}")


if __name__ == "__main__":
    main()
