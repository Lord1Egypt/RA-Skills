#!/usr/bin/env python3
"""
Import a local icon pack (a folder of SVGs you downloaded) INTO this skill:
copies the chosen SVGs into assets/icons/<provider>/ and merges entries into
references/icon-index.json so find_icon.py and build_diagram.py can use them
offline.

It auto-detects the two common layouts:
  * AWS Architecture Icons   ("Arch_<Name>_48.svg", "Res_..._48.svg",
                              "Arch-Category_<Name>_48.svg", group "<Name>_32.svg")
  * Azure / Microsoft official ("<digits>-icon-service-<Name>.svg")
...and falls back to a generic "<Name>.svg" reading for anything else.

When several sizes exist it keeps ONE (prefers 48, then 64, 32, 16). For themed
variants it prefers no-theme, then Light, then Dark.

Usage:
    # AWS pack
    python add_icon_pack.py --source /tmp/awspkg --provider aws
    # Azure official pack
    python add_icon_pack.py --source /tmp/azpkg --provider azure

Re-running for the same provider replaces that provider's entries (idempotent).
The msicons.com web icons (provider "microsoft") are left untouched.
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
INDEX = SKILL_ROOT / "references" / "icon-index.json"
ICONS_DIR = SKILL_ROOT / "assets" / "icons"

SIZE_PREF = {"48": 0, "64": 1, "32": 2, "16": 3}
THEME_PREF = {"": 0, "Light": 1, "Dark": 2}

# Short-name aliases appended to the search text for AWS services whose official
# name is the long form (so "S3" finds "Amazon Simple Storage Service").
AWS_ALIASES = {
    "simple storage service": "s3",
    "simple notification service": "sns",
    "simple queue service": "sqs",
    "virtual private cloud": "vpc",
    "identity and access management": "iam",
    "elastic load balancing": "elb alb nlb",
    "elastic compute cloud": "ec2",
    "elastic kubernetes service": "eks",
    "elastic container service": "ecs",
    "elastic container registry": "ecr",
    "relational database service": "rds",
    "elastic block store": "ebs",
    "elastic file system": "efs",
    "key management service": "kms",
    "simple email service": "ses",
}

# Google Cloud short-name aliases.
GCP_ALIASES = {
    "compute engine": "gce",
    "cloud storage": "gcs",
    "google kubernetes engine": "gke",
    "big query": "bq bigquery",
    "cloud sql": "cloudsql",
    "cloud run": "cloudrun",
    "vertex ai": "vertexai",
}


def parse_name(filename: str, keep_variants: bool = False) -> tuple[str, str, str]:
    """Return (clean_name, size, theme) parsed from an icon filename.
    Handles AWS ('Arch_<Name>_48.svg'), Azure ('<digits>-icon-service-<Name>'),
    and Google ('<Name>-512-color-rgb.svg') naming.

    With keep_variants=True, NO size/theme/color stripping is done — the full
    filename (snake/kebab -> spaces) becomes the name. Use this for packs like
    Microsoft Fabric where every size and variant is a distinct icon to keep
    (e.g. 'data_warehouse_24_color' stays 'data warehouse 24 color')."""
    stem = re.sub(r"\.svg$", "", filename, flags=re.I)
    if keep_variants:
        stem = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem)
        name = re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", stem)).strip()
        return name, "", ""
    theme = ""
    m = re.search(r"_(Light|Dark)$", stem)        # AWS theme variants
    if m:
        theme = m.group(1)
        stem = stem[: m.start()]
    size = ""
    m = re.search(r"_(\d{2,3})$", stem)           # AWS size suffix (_48 etc.)
    if m:
        size = m.group(1)
        stem = stem[: m.start()]
    # strip known AWS / Azure prefixes
    stem = re.sub(r"^Arch-Category_", "", stem)
    stem = re.sub(r"^Arch_", "", stem)
    stem = re.sub(r"^Res_", "", stem)
    stem = re.sub(r"^\d+[-_ ]*icon[-_ ]*service[-_ ]*", "", stem, flags=re.I)
    # Google-style qualifiers: "-512-color-rgb", "-color", "-mono". Only fires
    # when a color/rgb/mono keyword is present, so AWS "Route-53" is untouched.
    m = re.search(r"[-_](?:\d{2,4}[-_])?(?:color|rgb|mono)", stem, re.I)
    if m:
        theme = theme or "color"
        stem = stem[: m.start()]
    # split CamelCase ("ComputeEngine" -> "Compute Engine")
    stem = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem)
    name = re.sub(r"[_\-]+", " ", stem)
    name = re.sub(r"\s+", " ", name).strip()
    return name, size, theme


def search_tokens(name: str, category: str, provider: str) -> str:
    base = re.sub(r"[^a-z0-9 ]", " ", f"{name} {category}".lower())
    collapsed = base.replace(" ", "")
    extra = ""
    if provider == "aws":
        low = name.lower()
        for phrase, alias in AWS_ALIASES.items():
            if phrase in low:
                extra += " " + alias
    elif provider == "gcp":
        low = name.lower()
        for phrase, alias in GCP_ALIASES.items():
            if phrase in low:
                extra += " " + alias
    return f"{base} {collapsed}{extra}".strip()


def better(a: dict, b: dict) -> dict:
    """Pick the preferred file between two candidates for the same name."""
    ka = (SIZE_PREF.get(a["size"], 9), THEME_PREF.get(a["theme"], 9))
    kb = (SIZE_PREF.get(b["size"], 9), THEME_PREF.get(b["theme"], 9))
    return a if ka <= kb else b


def collect(source: Path, provider: str, keep_variants: bool = False) -> dict:
    """Map clean_name -> chosen candidate dict."""
    chosen: dict[str, dict] = {}
    for svg in source.rglob("*.svg"):
        if "__MACOSX" in svg.parts:
            continue
        name, size, theme = parse_name(svg.name, keep_variants)
        if not name:
            continue
        category = svg.parent.name
        cand = {"src": svg, "name": name, "size": size, "theme": theme,
                "category": category}
        key = name.lower()
        chosen[key] = better(chosen[key], cand) if key in chosen else cand
    return chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--provider", required=True,
                    help="short id, e.g. 'aws' or 'azure'")
    ap.add_argument("--all-variants", action="store_true",
                    help="keep every size/variant as a distinct icon (no "
                         "size/color de-duplication) — e.g. for Microsoft Fabric")
    args = ap.parse_args()

    source = Path(args.source)
    if not source.exists():
        sys.exit(f"source not found: {source}")

    dest = ICONS_DIR / args.provider
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    chosen = collect(source, args.provider, args.all_variants)
    entries = []
    for key, c in sorted(chosen.items()):
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", c["src"].name)
        shutil.copyfile(c["src"], dest / safe)
        rel = (dest / safe).relative_to(SKILL_ROOT).as_posix()
        entries.append({
            "provider": args.provider,
            "name": c["name"],
            "category": c["category"],
            "file": rel,
            "search": search_tokens(c["name"], c["category"], args.provider),
        })

    # merge into the index, replacing any prior entries for this provider
    index = json.loads(INDEX.read_text("utf-8")) if INDEX.exists() else []
    for e in index:
        e.setdefault("provider", "microsoft")  # msicons web entries
    index = [e for e in index if e.get("provider") != args.provider]
    index.extend(entries)
    INDEX.write_text(json.dumps(index, ensure_ascii=False))

    print(f"Imported {len(entries)} '{args.provider}' icons -> {dest}")
    print(f"Index now holds {len(index)} icons across providers: "
          + ", ".join(sorted({e['provider'] for e in index})))


if __name__ == "__main__":
    main()
