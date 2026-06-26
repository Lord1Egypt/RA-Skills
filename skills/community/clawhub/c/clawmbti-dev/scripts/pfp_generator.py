# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""MBTI lobster PFP generator — ASCII art + real image URL.

Base lobster skeleton + per-type accessories (hat, eye decoration, left/right claw items),
generating 16 distinct lobster PFP ASCII arts. Also provides real PFP image URL lookup.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# ============================================================
# Component construction helpers
# ============================================================


def _hat(s: str) -> str:
    """Generate a hat line, centered around ~column 17 (antenna convergence point)."""
    col = 17 - len(s) // 2
    return " " * col + s


def _lc(top: str = " . ", bot: str = " . ") -> tuple[str, str, str, str]:
    """Build left claw (4 rows × 8 chars), with 3-char-wide claw item."""
    return (" ,---.  ", f" |{top}|==", f" |{bot}|  ", " '---'==")


def _rc(top: str = " . ", bot: str = " . ") -> tuple[str, str, str, str]:
    """Build right claw (4 rows × 8 chars), with 3-char-wide claw item."""
    return ("  ,---. ", f"==|{top}| ", f"  |{bot}| ", "=='---' ")


# ============================================================
# Per-type accessory definitions
# ============================================================


@dataclass(frozen=True)
class TypeParts:
    """Lobster accessory combination for a single MBTI type."""

    hat: str = ""
    eyes: str = "(o)    (o)"
    left_claw: tuple[str, str, str, str] = (
        " ,---.  ",
        " | . |==",
        " | . |  ",
        " '---'==",
    )
    right_claw: tuple[str, str, str, str] = (
        "  ,---. ",
        "==| . | ",
        "  | . | ",
        "=='---' ",
    )


TYPE_PARTS: dict[str, TypeParts] = {
    # ---- Analysts ----
    "INTJ": TypeParts(  # Architect: monocle + chessboard
        eyes="(O)    (o)",
        left_claw=_lc("#_#", "_#_"),
    ),
    "INTP": TypeParts(  # Logician: round glasses + formula board
        eyes="{o}    {o}",
        left_claw=_lc("E=m", "c^2"),
    ),
    "ENTJ": TypeParts(  # Commander: helmet + scepter
        hat=_hat(".===."),
        left_claw=_lc(" * ", " | "),
    ),
    "ENTP": TypeParts(  # Debater: pointing claw + gesturing claw
        left_claw=_lc(" | ", " / "),
        right_claw=_rc(" | ", " \\ "),
    ),
    # ---- Diplomats ----
    "INFJ": TypeParts(  # Advocate: hood + crystal ball
        hat=_hat("/^^\\"),
        left_claw=_lc("( )", "(_)"),
    ),
    "INFP": TypeParts(  # Mediator: quill pen + starlight decoration
        left_claw=_lc(" ) ", " )|"),
    ),
    "ENFJ": TypeParts(  # Protagonist: flower crown + open claws
        hat=_hat("*~*~*"),
    ),
    "ENFP": TypeParts(  # Campaigner: colorful claws
        left_claw=_lc("~*~", "*~*"),
        right_claw=_rc("~*~", "*~*"),
    ),
    # ---- Sentinels ----
    "ISTJ": TypeParts(  # Logistician: military cap + checklist
        hat=_hat("[___]"),
        left_claw=_lc("[v]", "[v]"),
    ),
    "ISFJ": TypeParts(  # Defender: first-aid kit
        left_claw=_lc(" + ", "+_+"),
    ),
    "ESTJ": TypeParts(  # Executive: briefcase
        left_claw=_lc("===", "   "),
    ),
    "ESFJ": TypeParts(  # Consul: cake
        left_claw=_lc("^v^", "___"),
    ),
    # ---- Explorers ----
    "ISTP": TypeParts(  # Craftsman: wrench + circuit board
        left_claw=_lc("-Y-", " | "),
        right_claw=_rc("[=]", "[_]"),
    ),
    "ISFP": TypeParts(  # Adventurer: beret + paintbrush
        hat=_hat(".'`."),
        left_claw=_lc(" / ", "/  "),
    ),
    "ESTP": TypeParts(  # Entrepreneur: sunglasses + dice
        eyes="[-]    [-]",
        left_claw=_lc("o o", " o "),
    ),
    "ESFP": TypeParts(  # Entertainer: party hat + microphone
        hat=_hat("/|\\"),
        left_claw=_lc(" O ", " | "),
    ),
}


# ============================================================
# ASCII art composition
# ============================================================

_types_cache: dict[str, Any] | None = None


def _load_types_json() -> dict[str, Any]:
    """Load resources/mbti_types.json (with cache)."""
    global _types_cache
    if _types_cache is None:
        p = Path(__file__).resolve().parent.parent / "resources" / "mbti_types.json"
        _types_cache = json.loads(p.read_text("utf-8")) if p.exists() else {}
    return _types_cache


# ============================================================
# Image URL
# ============================================================

_PFP_DIR = Path(__file__).resolve().parent.parent / "resources" / "mbti-pfp"
_CDN_BASE = "https://pub-statics.finchain.global/clawmbti-nft"


def get_image_path(mbti_type: str) -> Path | None:
    """Return the absolute PFP image path for the given MBTI type, or None if not found."""
    mbti_type = mbti_type.upper().strip()
    info = _load_types_json().get(mbti_type, {})
    filename = info.get("image")
    if filename:
        p = _PFP_DIR / filename
        if p.exists():
            return p
    # Fallback: try naming convention
    for ext in ("png", "jpg"):
        p = _PFP_DIR / f"{mbti_type} Lobster NFT PFP.{ext}"
        if p.exists():
            return p
    return None


def get_image_url(mbti_type: str) -> str:
    """Return the CDN image URL for the given MBTI type."""
    return f"{_CDN_BASE}/{mbti_type.upper().strip()}.webp"


def compose(mbti_type: str) -> str:
    """Compose the lobster PFP ASCII art for the given MBTI type."""
    mbti_type = mbti_type.upper().strip()
    if mbti_type not in TYPE_PARTS:
        valid = ", ".join(sorted(TYPE_PARTS))
        raise ValueError(f"Unknown type: {mbti_type}. Valid: {valid}")

    parts = TYPE_PARTS[mbti_type]
    info = _load_types_json().get(mbti_type, {})
    lc, rc = parts.left_claw, parts.right_claw

    lines: list[str] = []

    # Antennae
    lines.append("              ||    ||")
    lines.append("               \\\\  //")

    # Hat (optional)
    if parts.hat:
        lines.append(parts.hat)

    # Head
    lines.append("          .--'    '--.")
    lines.append("         / " + parts.eyes + " \\")
    lines.append("        |    '----'    |")

    # Body + left/right claws (4 rows)
    body = [
        "|              |",
        "|   .------.   |",
        "|   |      |   |",
        "|   '------'   |",
    ]
    for i in range(4):
        lines.append(lc[i] + body[i] + rc[i])

    # Lower body + tail
    lines.append("         \\            /")
    lines.append("          '-..____.-'")
    lines.append("         / ||    || \\")
    lines.append("        /  ||    ||  \\")
    lines.append("           '--  --'")

    # Type label
    lines.append("")
    nickname = info.get("nickname_en", "???")
    lines.append("       [ " + mbti_type + " | " + nickname + " ]")

    return "\n".join(line.rstrip() for line in lines)


# ============================================================
# CLI
# ============================================================


def cmd_generate(args: argparse.Namespace) -> None:
    """Generate the lobster PFP ASCII art for the specified type."""
    mbti_type = args.type.upper().strip()
    if mbti_type not in TYPE_PARTS:
        print(
            json.dumps(
                {"error": f"unknown type: {mbti_type}", "valid": sorted(TYPE_PARTS)}
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    art = compose(mbti_type)

    if args.json:
        info = _load_types_json().get(mbti_type, {})
        image_path = get_image_path(mbti_type)
        result: dict[str, Any] = {
            "type": mbti_type,
            "nickname_en": info.get("nickname_en", ""),
            "art": art,
            "image_path": str(image_path) if image_path else None,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(art)


def cmd_all(_args: argparse.Namespace) -> None:
    """Generate all 16 lobster PFP types (preview)."""
    for i, mbti_type in enumerate(sorted(TYPE_PARTS)):
        if i > 0:
            print("\n" + "=" * 40 + "\n")
        print(compose(mbti_type))


def cmd_image_path(args: argparse.Namespace) -> None:
    """Output the PFP image path and CDN URL for the specified MBTI type."""
    mbti_type = args.type.upper().strip()
    image_path = get_image_path(mbti_type)
    image_url = get_image_url(mbti_type)

    if args.json:
        info = _load_types_json().get(mbti_type, {})
        result: dict[str, Any] = {
            "type": mbti_type,
            "image_url": image_url,
            "image_path": str(image_path) if image_path else None,
            "image_filename": image_path.name if image_path else None,
            "nickname_en": info.get("nickname_en", ""),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(image_url)


def main() -> None:
    parser = argparse.ArgumentParser(description="MBTI lobster PFP generator")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate lobster PFP ASCII art for a type")
    gen.add_argument("--type", required=True, help="MBTI type (e.g. INTJ, ENFP)")
    gen.add_argument("--json", action="store_true", help="Output as JSON")

    sub.add_parser("all", help="Generate all 16 types (preview)")

    img = sub.add_parser("image-path", help="Get PFP image path for a type")
    img.add_argument("--type", required=True, help="MBTI type (e.g. INTJ, ENFP)")
    img.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    commands: dict[str, Any] = {
        "generate": cmd_generate,
        "all": cmd_all,
        "image-path": cmd_image_path,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
