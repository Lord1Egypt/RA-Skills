#!/usr/bin/env python3
"""
Example 2: Multi-Canvas Output

Generate the same deck in 3 different aspect ratios:
- 16:9 (widescreen, for desktop/TV)
- 9:16 (vertical, for mobile/social — TikTok, Reels, Stories)
- 1:1 (square, for Instagram feed)
- A4 (for printing)

The DeckEngine automatically adapts all 20+ layout methods to the chosen canvas.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import DeckEngine

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Content shared across all canvases
SLIDES = {
    "cover": dict(
        title="Product Launch 2026",
        subtitle="Now available worldwide",
        author="Brand Team",
        date="Q3 2026",
    ),
    "toc": dict(items=[
        ("01", "What's New", "Three big features"),
        ("02", "Pricing", "Plans for every team"),
        ("03", "Get Started", "How to upgrade"),
    ]),
    "content": dict(
        title="What's New",
        bullets=[
            "AI-powered insights dashboard",
            "Real-time collaboration with 50+ teammates",
            "Enterprise-grade security (SOC 2 Type II)",
        ],
        key_point="Built for teams that move fast and ship more.",
    ),
    "summary": dict(
        title="Takeaways",
        key_points=[
            "Three new features, zero price increase",
            "Free 30-day trial for all paid plans",
        ],
        conclusion="Visit example.com/launch for the full reveal",
    ),
    "closing": dict(title="Thank You", message="Try it free today"),
}


def build_deck(theme: str, canvas: str) -> str:
    """Build a deck and return the output path."""
    eng = DeckEngine(theme_name=theme, canvas=canvas)
    eng.cover(**SLIDES["cover"])
    eng.toc(**SLIDES["toc"])
    eng.content(**SLIDES["content"])
    eng.summary(**SLIDES["summary"])
    eng.closing(**SLIDES["closing"])

    out_path = os.path.join(OUT_DIR, "output", f"02_multi_{canvas.replace(':', 'x')}.pptx")
    eng.save(out_path)
    return out_path, eng._slide_count, eng.prs.slide_width / 914400, eng.prs.slide_height / 914400


if __name__ == "__main__":
    print("=" * 60)
    print("Multi-Canvas Deck Generation")
    print("=" * 60)

    for theme, canvas in [
        ("business", "16:9"),    # Desktop / widescreen
        ("creative", "9:16"),    # Mobile vertical (TikTok/Reels/Stories)
        ("minimal", "1:1"),      # Instagram square
        ("elegant", "A4"),       # Print landscape
    ]:
        path, slides, w, h = build_deck(theme, canvas)
        print(f"  {theme:10s} × {canvas:5s} → {slides} slides, {w:.1f}\" × {h:.1f}\"")
        print(f"     {path}")

    print()
    print("✓ All canvases generated. Check output with PowerPoint or LibreOffice.")
