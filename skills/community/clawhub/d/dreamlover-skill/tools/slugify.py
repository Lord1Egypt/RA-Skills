from __future__ import annotations

import argparse
import hashlib
import re
import unicodedata

MAX_SLUG_LENGTH = 64


def slugify(text: str, prefix: str = "char") -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    slug = re.sub(r"-+", "-", slug)
    if slug:
        return slug[:MAX_SLUG_LENGTH]
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a filesystem-safe slug.")
    parser.add_argument("text", help="Source text to slugify.")
    parser.add_argument("--prefix", default="char", help="Fallback prefix when ASCII slug is empty.")
    args = parser.parse_args()
    print(slugify(args.text, args.prefix))


if __name__ == "__main__":
    main()
