#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def has(text: str, patterns):
    t = text.lower()
    return any(re.search(p, t) for p in patterns)


def main():
    p = argparse.ArgumentParser(description="Strict consistency checker for legal pages vs feature doc")
    p.add_argument("--feature", required=True, help="Path to app feature markdown/text")
    p.add_argument("--privacy", required=True, help="Path to generated privacy.html")
    p.add_argument("--terms", required=True, help="Path to generated terms.html")
    args = p.parse_args()

    feature = Path(args.feature).read_text(encoding="utf-8").lower()
    privacy = Path(args.privacy).read_text(encoding="utf-8").lower()
    terms = Path(args.terms).read_text(encoding="utf-8").lower()

    errors = []

    # 1) No placeholders ever
    for label, text in [("privacy", privacy), ("terms", terms)]:
        if any(x in text for x in ["todo", "temp", "fixme"]):
            errors.append(f"{label}: contains placeholder token (TODO/TEMP/FIXME)")

    # 2) Offline/no-cloud/no-server claims should not be contradicted
    offline_claim = any(k in feature for k in ["offline", "on your device", "all processing happens offline", "本地完成"]) \
        or ("no cloud" in feature) or ("无云" in feature) or ("无服务器" in feature) or ("no server" in feature)
    if offline_claim:
        bad = [
            r"share data with service providers",
            r"infrastructure, analytics, or support",
            r"processed in regions where our infrastructure",
            r"international transfers",
            r"upload(ed)? to (our )?servers",
        ]
        for pat in bad:
            if re.search(pat, privacy):
                errors.append(f"privacy: contradicts offline/no-cloud posture: /{pat}/")

    # 3) No analytics / no tracking claims
    if ("no analytics" in feature) or ("无分析" in feature):
        # flag positive analytics collection language; allow explicit negatives like "do not use analytics"
        if has(privacy, [r"collect analytics", r"use analytics to", r"analytics events", r"usage trends"]):
            if not has(privacy, [r"do not use analytics", r"no analytics"]):
                errors.append("privacy: contradicts 'No Analytics' claim")

    if ("no tracking" in feature) or ("无追踪" in feature):
        if has(privacy, [r"tracking", r"track users across apps|track users across websites"]):
            # allow explicit negative sentence like "do not track"
            if not has(privacy, [r"do not track", r"not track"]):
                errors.append("privacy: may contradict 'No Tracking' claim")

    # 4) EXIF local-only requirement when EXIF is mentioned in feature doc
    if "exif" in feature:
        if not has(privacy, [r"exif", r"metadata"]):
            errors.append("privacy: feature doc mentions EXIF but privacy page does not")
        if has(privacy, [r"upload", r"share with third parties"]) and not has(privacy, [r"never upload", r"on-device only", r"on your device only"]):
            errors.append("privacy: EXIF mentioned but no clear local-only handling statement")

    # 5) Terms should not force governing law if not provided explicitly in feature
    if not any(k in feature for k in ["governing law", "jurisdiction", "法律", "法域"]):
        if "governing law" in terms:
            errors.append("terms: includes Governing Law though feature doc does not provide jurisdiction")

    if errors:
        print("CONSISTENCY_CHECK_FAILED")
        for e in errors:
            print(f"- {e}")
        raise SystemExit(1)

    print("CONSISTENCY_CHECK_OK")


if __name__ == "__main__":
    main()
