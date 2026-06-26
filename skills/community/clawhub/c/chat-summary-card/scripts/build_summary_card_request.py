#!/usr/bin/env python3
"""Build a Mew design request body for a conversation summary image."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

STYLE_PROMPTS = {
    "minimalism": (
        "Minimalist summary card, large white space, disciplined editorial layout, Source Han Sans or PingFang style sans-serif typography, "
        "Morandi gray-blue and light beige accents, structured information blocks, calm professional presentation, highly readable. "
        "Make the minimalist look dominant and unmistakable with very large blank margins, restrained decoration, clean section separation, "
        "thin dividers, low visual density, and almost no ornamental illustration. "
        "Do not make it look like glassmorphism, chat bubbles, a playful illustrated poster, or a glowing technology dashboard."
    ),
    "healing-illustration": (
        "Healing illustration summary board, warm textured paper background, gentle illustration cues such as plants, coffee cups, "
        "or simple characters, soft hand-made atmosphere, note-board composition, warm and emotionally resonant. "
        "Make the healing illustration style obvious through warm paper texture, gentle doodle-like motifs, sticky-note or scrapbook feeling, "
        "hand-made softness, and comforting visual warmth. "
        "Do not make it look like a corporate dashboard, glass UI, minimalist report card, or cold futuristic interface."
    ),
    "glassmorphism": (
        "Glassmorphism summary interface, frosted translucent panels, rounded floating cards, premium gradients, "
        "subtle light and shadow, bright refined icon accents, modern upscale technology aesthetic. "
        "Make the glassmorphism style unmistakable with strong frosted translucent panels, clearly visible background blur through the cards, "
        "floating layered UI depth, bright glass edge highlights, specular reflections, and soft volumetric shadows. "
        "Do not make it look like flat white cards, paper notes, a standard dashboard, plain infographic panels, or a static poster."
    ),
    "chat-bubbles": (
        "Conversation-summary long image styled like beautified instant messaging, polished chat bubbles, pastel or macaron accents, "
        "highlighted quotes, left-right dialogue rhythm, and a final consensus card at the bottom. "
        "Make the conversation feel unmistakable with obvious left-right bubbles, quoted lines, visible send-reply rhythm, and a strong bottom consensus block. "
        "Do not make it look like a generic report card, glass dashboard, sparse editorial poster, or plain bullet list."
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble a design request body for a conversation summary image.",
    )
    parser.add_argument("--title", required=True, help="Main title shown in the image.")
    parser.add_argument("--summary", required=True, help="One-line summary sentence.")
    parser.add_argument(
        "--point",
        action="append",
        default=[],
        help="Repeatable key point line. Use 3 to 5.",
    )
    parser.add_argument(
        "--next-step",
        action="append",
        default=[],
        help="Repeatable next step line.",
    )
    parser.add_argument(
        "--decision",
        action="append",
        default=[],
        help="Repeatable decision line.",
    )
    parser.add_argument(
        "--style",
        choices=sorted(STYLE_PROMPTS),
        default="minimalism",
        help="Visual style.",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(STYLE_PROMPTS),
        help="Deprecated alias for --style.",
    )
    parser.add_argument("--brand-color", help="Optional brand color or palette hint.")
    parser.add_argument("--audience", help="Optional audience hint such as engineers or stakeholders.")
    parser.add_argument("--width", type=int, default=1080, help="Design width in px.")
    parser.add_argument(
        "--height",
        type=int,
        default=-1,
        help="Design height in px or -1 for adaptive height.",
    )
    parser.add_argument(
        "--output",
        help="Write JSON to this file instead of stdout.",
    )
    return parser.parse_args()


def build_user_query(args: argparse.Namespace) -> str:
    style = args.style or args.mode or "minimalism"
    sections = [
        "Create a single conversation-summary image in Chinese unless the provided copy is clearly another language.",
        f"Main title: {args.title}",
        f"Summary sentence: {args.summary}",
    ]

    if args.point:
        sections.append("Key takeaways:\n" + "\n".join(f"- {item}" for item in args.point))
    if args.decision:
        sections.append("Decisions:\n" + "\n".join(f"- {item}" for item in args.decision))
    if args.next_step:
        sections.append("Next steps:\n" + "\n".join(f"- {item}" for item in args.next_step))

    if style == "chat-bubbles":
        sections.append(
            "Present the strongest lines as polished left-right chat bubbles and add a bottom consensus card that summarizes the shared conclusion. Make the chat-bubble style visually obvious with left-right dialogue bubbles, highlighted quotable lines, conversational rhythm, and a bottom consensus block. Avoid generic report-card sections or dashboard cards."
        )
    elif style == "glassmorphism":
        sections.append(
            "Make the glass effect visually obvious with strong frosted translucent floating panels, visible background blur through the cards, bright edge highlights, reflective glass edges, and soft layered shadows. Avoid flat white cards, plain dashboard blocks, paper texture, or static poster composition."
        )
    elif style == "healing-illustration":
        sections.append(
            "Make the healing illustration style visually obvious with warm paper texture, gentle illustrated motifs, sticky-note or scrapbook feeling, and a soft note-board composition. Avoid hard-edged enterprise UI, heavy glass effects, and cold gradients."
        )
    elif style == "minimalism":
        sections.append(
            "Make the minimalist style visually obvious with large white space, restrained Morandi accents, clean card grouping, low visual density, and almost no decorative noise. Avoid glass highlights, cartoon illustration, decorative 3D icons, and dense layout."
        )
    else:
        sections.append(
            "Use clearly separated sections, strong heading hierarchy, concise copy blocks, and keep the final image readable on phone screens."
        )
    sections.append(
        'Add a subtle but readable text watermark "Mew.Design" at the bottom of the image.'
    )
    return "\n\n".join(sections)


def build_design_concept(args: argparse.Namespace) -> str:
    style = args.style or args.mode or "minimalism"
    parts = [STYLE_PROMPTS[style]]
    if args.brand_color:
        parts.append(f"Use brand accents inspired by {args.brand_color}.")
    if args.audience:
        parts.append(f"Tailor tone and labeling for {args.audience}.")
    parts.append(
        "Avoid generic AI art imagery. Focus on editorial information design, cards, dividers, icons, and layout rhythm."
    )
    parts.append(
        'Place the watermark text "Mew.Design" along the bottom edge in a clean, understated, readable way.'
    )
    parts.append(
        "Treat the chosen style as a hard constraint rather than a light mood reference."
    )
    return " ".join(parts)


def main() -> int:
    args = parse_args()
    if not args.style and args.mode:
        args.style = args.mode

    if not args.point:
        raise SystemExit("At least one --point is required.")

    payload = {
        "userQuery": build_user_query(args),
        "designConcept": build_design_concept(args),
        "width": args.width,
        "height": args.height,
    }

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
