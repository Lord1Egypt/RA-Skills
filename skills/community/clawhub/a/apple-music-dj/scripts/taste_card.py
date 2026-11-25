#!/usr/bin/env python3
"""
taste_card.py — Generate a shareable Taste DNA Card (SVG).

Reads a taste profile JSON and produces a visual summary card with:
  - Listener archetype label
  - Top genres with bar chart
  - Top artists
  - Era breakdown
  - Stats: variety, mainstream, energy, velocity

Usage:
  python3 taste_card.py <profile.json> [--output card.svg]
  python3 taste_card.py <profile.json> --format text
  python3 taste_card.py <profile.json> --mode drift --data drift.json   (drift.json from taste_drift.py)

Requires: A taste profile JSON (from taste_profiler.py).
"""

import sys
if sys.version_info < (3, 11):
    sys.exit(
        f"ERROR: Python 3.11+ is required (you have "
        f"{sys.version_info.major}.{sys.version_info.minor}). Please upgrade."
    )

import argparse
import json
import textwrap

from _common import load_profile, write_private

# ── Archetype Detection ──────────────────────────────────────────

ARCHETYPES = [
    # (label, condition_fn, description)
    ("Deep Catalog Digger", lambda p: p["variety_score"] > 0.7 and p["mainstream_score"] < 0.3,
     "You live in the deep end — album tracks, B-sides, and artists most people haven't heard of."),
    ("Genre Drifter", lambda p: p["variety_score"] > 0.6 and len(p["genre_distribution"]) >= 6,
     "Your taste refuses to stay in one lane. Every genre is fair game."),
    ("Comfort Zone Commander", lambda p: p["variety_score"] < 0.3 and len(p["genre_distribution"]) <= 3,
     "You know what you like and you stick to it. Deep loyalty to a tight rotation."),
    ("Nostalgia Keeper", lambda p: _top_era(p).startswith(("19", "200")) and _top_era_weight(p) > 0.5,
     "Your heart lives in a different decade. The classics never get old."),
    ("Trend Surfer", lambda p: p["mainstream_score"] > 0.6,
     "You ride the wave — if it's on the charts, you've heard it."),
    ("Indie Purist", lambda p: p["mainstream_score"] < 0.2 and p["energy_profile"] != "high-energy",
     "Mainstream? Never heard of it. Your taste is curated, intentional, and defiantly independent."),
    ("Energy Chaser", lambda p: p["energy_profile"] == "high-energy" and p["mainstream_score"] > 0.3,
     "Volume up, tempo high. You need music that matches your intensity."),
    ("Chill Architect", lambda p: p["energy_profile"] == "chill",
     "Low tempo, warm tones, ambient vibes. You build soundscapes, not playlists."),
    ("Balanced Explorer", lambda p: True,
     "A well-rounded listener who keeps one foot in the familiar and one in the unknown."),
]


def _top_era(profile: dict) -> str:
    eras = profile.get("era_distribution", [])
    return eras[0]["decade"] if eras else "2020s"


def _top_era_weight(profile: dict) -> float:
    eras = profile.get("era_distribution", [])
    return eras[0]["weight"] if eras else 0.0


def detect_archetype(profile: dict) -> tuple[str, str]:
    """Return (archetype_label, description)."""
    for label, condition, desc in ARCHETYPES:
        try:
            if condition(profile):
                return label, desc
        except (KeyError, IndexError, TypeError):
            continue
    return "Balanced Explorer", "A well-rounded listener."


# ── SVG Card Generator ──────────────────────────────────────────

def _bar(value: float, max_width: int = 180) -> int:
    return max(4, int(value * max_width))


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_svg(profile: dict) -> str:
    archetype, arch_desc = detect_archetype(profile)
    top_genres = profile.get("genre_distribution", [])[:6]
    top_artists = profile.get("top_artists", [])[:8]
    eras = profile.get("era_distribution", [])[:5]
    energy = profile.get("energy_profile", "balanced")
    variety = profile.get("variety_score", 0.5)
    mainstream = profile.get("mainstream_score", 0.5)
    velocity = profile.get("listening_velocity", "moderate")

    # Colors
    bg = "#1a1a2e"
    card_bg = "#16213e"
    accent = "#e94560"
    text = "#eaeaea"
    muted = "#a0a0b0"
    bar_color = "#e94560"
    bar_bg = "#2a2a4a"

    w, h = 480, 720
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    lines.append(f'<rect width="{w}" height="{h}" rx="16" fill="{bg}"/>')
    lines.append(f'<rect x="16" y="16" width="{w-32}" height="{h-32}" rx="12" fill="{card_bg}"/>')

    # Header
    lines.append(f'<text x="240" y="52" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="13" fill="{muted}" letter-spacing="3">TASTE DNA</text>')
    lines.append(f'<text x="240" y="84" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="22" font-weight="700" fill="{accent}">{_escape(archetype)}</text>')
    lines.append(f'<text x="240" y="106" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}">{_escape(arch_desc[:70])}</text>')

    # Divider
    lines.append(f'<line x1="40" y1="122" x2="440" y2="122" stroke="{bar_bg}" stroke-width="1"/>')

    # Top Genres
    y = 148
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">TOP GENRES</text>')
    y += 6
    for g in top_genres:
        y += 22
        bw = _bar(g["weight"])
        lines.append(f'<rect x="140" y="{y-10}" width="180" height="12" rx="3" fill="{bar_bg}"/>')
        lines.append(f'<rect x="140" y="{y-10}" width="{bw}" height="12" rx="3" fill="{bar_color}"/>')
        lines.append(f'<text x="136" y="{y}" text-anchor="end" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{text}">{_escape(g["genre"])}</text>')
        pct = int(g["weight"] * 100)
        lines.append(f'<text x="326" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="10" fill="{muted}">{pct}%</text>')

    # Divider
    y += 18
    lines.append(f'<line x1="40" y1="{y}" x2="440" y2="{y}" stroke="{bar_bg}" stroke-width="1"/>')

    # Top Artists
    y += 22
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">TOP ARTISTS</text>')
    y += 4
    for i, a in enumerate(top_artists):
        y += 20
        rank = f"{i+1}."
        lines.append(f'<text x="50" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{muted}">{rank}</text>')
        lines.append(f'<text x="68" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="12" fill="{text}">{_escape(a["name"])}</text>')

    # Divider
    y += 18
    lines.append(f'<line x1="40" y1="{y}" x2="440" y2="{y}" stroke="{bar_bg}" stroke-width="1"/>')

    # Stats row
    y += 26
    stats = [
        ("Energy", energy.replace("-", " ").title()),
        ("Variety", f"{int(variety * 100)}%"),
        ("Mainstream", f"{int(mainstream * 100)}%"),
        ("Velocity", velocity.title()),
    ]
    col_w = 100
    for i, (label, val) in enumerate(stats):
        cx = 40 + i * col_w + col_w // 2
        lines.append(f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="system-ui,sans-serif" '
                     f'font-size="10" fill="{muted}">{label}</text>')
        lines.append(f'<text x="{cx}" y="{y+18}" text-anchor="middle" font-family="system-ui,sans-serif" '
                     f'font-size="14" font-weight="600" fill="{text}">{val}</text>')

    # Era badges
    y += 42
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">ERA MIX</text>')
    y += 8
    ex = 40
    for era in eras:
        label = era["decade"]
        tw = len(label) * 8 + 16
        lines.append(f'<rect x="{ex}" y="{y}" width="{tw}" height="22" rx="11" '
                     f'fill="{bar_bg}" stroke="{accent}" stroke-width="1"/>')
        lines.append(f'<text x="{ex + tw//2}" y="{y+15}" text-anchor="middle" '
                     f'font-family="system-ui,sans-serif" font-size="10" fill="{text}">{label}</text>')
        ex += tw + 8

    # Footer
    lines.append(f'<text x="240" y="{h-28}" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="9" fill="{muted}">Generated by Apple Music DJ · openclaw</text>')

    lines.append('</svg>')
    return '\n'.join(lines)


# ── Text Card (terminal-friendly) ───────────────────────────────

def generate_text(profile: dict) -> str:
    archetype, arch_desc = detect_archetype(profile)
    top_genres = profile.get("genre_distribution", [])[:6]
    top_artists = profile.get("top_artists", [])[:8]
    eras = profile.get("era_distribution", [])[:5]
    energy = profile.get("energy_profile", "balanced")
    variety = profile.get("variety_score", 0.5)
    mainstream = profile.get("mainstream_score", 0.5)
    velocity = profile.get("listening_velocity", "moderate")

    bar_full = "█"
    bar_empty = "░"

    lines = []
    lines.append("╔══════════════════════════════════════╗")
    lines.append("║          🎧  TASTE DNA CARD          ║")
    lines.append("╠══════════════════════════════════════╣")
    lines.append(f"  Archetype: {archetype}")
    lines.append(f"  {arch_desc}")
    lines.append("")
    lines.append("  ── TOP GENRES ──")
    for g in top_genres:
        pct = int(g["weight"] * 100)
        filled = int(g["weight"] * 20)
        bar = bar_full * filled + bar_empty * (20 - filled)
        lines.append(f"  {g['genre']:.<20s} {bar} {pct}%")
    lines.append("")
    lines.append("  ── TOP ARTISTS ──")
    for i, a in enumerate(top_artists):
        lines.append(f"  {i+1:>2}. {a['name']}")
    lines.append("")
    lines.append("  ── STATS ──")
    lines.append(f"  Energy:     {energy.replace('-', ' ').title()}")
    lines.append(f"  Variety:    {int(variety * 100)}%")
    lines.append(f"  Mainstream: {int(mainstream * 100)}%")
    lines.append(f"  Velocity:   {velocity.title()}")
    lines.append("")
    lines.append("  ── ERA MIX ──")
    era_str = "  " + " · ".join(e["decade"] for e in eras) if eras else "  N/A"
    lines.append(era_str)
    lines.append("")
    lines.append("╚══════════════════════════════════════╝")
    lines.append("  Generated by Apple Music DJ · openclaw")
    return "\n".join(lines)


# ── Compatibility Card ───────────────────────────────────────────

def generate_compatibility_svg(result: dict) -> str:
    """Generate a shareable SVG card for a compatibility comparison."""
    score = result.get("overall_score", 0)
    verdict = result.get("verdict", "Unknown")
    shared = result.get("shared_artists", [])[:6]
    genre_overlap = result.get("genre_overlap", [])[:6]
    user_a = result.get("user_a", "You")
    user_b = result.get("user_b", "Friend")
    unique_a = result.get("unique_to_a", [])[:4]
    unique_b = result.get("unique_to_b", [])[:4]

    bg = "#1a1a2e"
    card_bg = "#16213e"
    accent = "#e94560"
    text = "#eaeaea"
    muted = "#a0a0b0"
    bar_bg = "#2a2a4a"
    green = "#4ecca3"

    w, h = 480, 600
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    lines.append(f'<rect width="{w}" height="{h}" rx="16" fill="{bg}"/>')
    lines.append(f'<rect x="16" y="16" width="{w-32}" height="{h-32}" rx="12" fill="{card_bg}"/>')

    # Header
    lines.append(f'<text x="240" y="52" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="13" fill="{muted}" letter-spacing="3">TASTE COMPATIBILITY</text>')

    # Score circle
    lines.append(f'<circle cx="240" cy="110" r="40" fill="none" stroke="{bar_bg}" stroke-width="6"/>')
    arc_color = green if score >= 60 else accent
    # SVG arc approximation via stroke-dasharray
    circumference = 251  # 2 * pi * 40
    filled = int(circumference * score / 100)
    lines.append(f'<circle cx="240" cy="110" r="40" fill="none" stroke="{arc_color}" '
                 f'stroke-width="6" stroke-dasharray="{filled} {circumference}" '
                 f'transform="rotate(-90 240 110)"/>')
    lines.append(f'<text x="240" y="117" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="28" font-weight="700" fill="{text}">{score}%</text>')

    # Verdict
    lines.append(f'<text x="240" y="170" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="14" font-weight="600" fill="{accent}">{_escape(verdict)}</text>')

    # Users
    lines.append(f'<text x="120" y="196" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="12" fill="{muted}">{_escape(user_a)}</text>')
    lines.append(f'<text x="360" y="196" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="12" fill="{muted}">{_escape(user_b)}</text>')
    lines.append(f'<text x="240" y="196" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="12" fill="{green}">×</text>')

    # Shared artists
    y = 218
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">SHARED ARTISTS</text>')
    for a in shared:
        y += 20
        name = a if isinstance(a, str) else a.get("name", "")
        lines.append(f'<text x="50" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="12" fill="{text}">♫ {_escape(name)}</text>')

    # Genre overlap
    y += 24
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">SHARED GENRES</text>')
    ex = 40
    y += 8
    for g in genre_overlap:
        label = g if isinstance(g, str) else g.get("genre", "")
        tw = len(label) * 7 + 16
        lines.append(f'<rect x="{ex}" y="{y}" width="{tw}" height="22" rx="11" '
                     f'fill="{bar_bg}" stroke="{green}" stroke-width="1"/>')
        lines.append(f'<text x="{ex + tw//2}" y="{y+15}" text-anchor="middle" '
                     f'font-family="system-ui,sans-serif" font-size="10" fill="{text}">{_escape(label)}</text>')
        ex += tw + 8
        if ex > 400:  # wrap
            ex = 40
            y += 28

    # Unique to each
    y += 32
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">UNIQUE TO EACH</text>')
    y += 6
    for a_item, b_item in zip(unique_a, unique_b, strict=False):
        y += 20
        a_name = a_item if isinstance(a_item, str) else a_item.get("name", "")
        b_name = b_item if isinstance(b_item, str) else b_item.get("name", "")
        lines.append(f'<text x="50" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{text}">{_escape(a_name)}</text>')
        lines.append(f'<text x="280" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{text}">{_escape(b_name)}</text>')

    # Footer
    lines.append(f'<text x="240" y="{h-28}" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="9" fill="{muted}">Generated by Apple Music DJ · openclaw</text>')
    lines.append('</svg>')
    return '\n'.join(lines)


def generate_compatibility_text(result: dict) -> str:
    """Generate a terminal-friendly compatibility card."""
    score = result.get("overall_score", 0)
    verdict = result.get("verdict", "Unknown")
    shared = result.get("shared_artists", [])[:6]
    genre_overlap = result.get("genre_overlap", [])[:6]
    user_a = result.get("user_a", "You")
    user_b = result.get("user_b", "Friend")

    bar_full = "█"
    bar_empty = "░"
    filled = int(score / 5)
    bar = bar_full * filled + bar_empty * (20 - filled)

    lines = []
    lines.append("╔══════════════════════════════════════╗")
    lines.append("║      🎧  TASTE COMPATIBILITY         ║")
    lines.append("╠══════════════════════════════════════╣")
    lines.append(f"  {user_a}  ×  {user_b}")
    lines.append(f"  Score: {bar} {score}%")
    lines.append(f"  Verdict: {verdict}")
    lines.append("")
    if shared:
        lines.append("  ── SHARED ARTISTS ──")
        for a in shared:
            name = a if isinstance(a, str) else a.get("name", "")
            lines.append(f"    ♫ {name}")
        lines.append("")
    if genre_overlap:
        lines.append("  ── SHARED GENRES ──")
        genre_names = [g if isinstance(g, str) else g.get("genre", "") for g in genre_overlap]
        lines.append(f"    {' · '.join(genre_names)}")
        lines.append("")
    lines.append("╚══════════════════════════════════════╝")
    lines.append("  Generated by Apple Music DJ · openclaw")
    return "\n".join(lines)


# ── Year In Review Card ─────────────────────────────────────────

def generate_year_review_svg(review: dict) -> str:
    """Generate a shareable SVG card for a year-in-review summary."""
    year = review.get("year", "")
    total_minutes = review.get("total_minutes")
    top_genre = review.get("top_genre") or "Unknown"
    top_artist = review.get("top_artist") or "Unknown"
    top_songs = review.get("top_songs", [])[:5]
    milestones = review.get("milestones", [])[:4]
    insights = review.get("insights", [])[:3]
    hours = f"{total_minutes // 60:,}" if total_minutes else "—"  # unknown without Replay
    # Without that year's Replay, artist and genre are today's taste (listening_insights falls back).
    now = "" if review.get("replay_available", True) else " (now)"

    bg = "#1a1a2e"
    card_bg = "#16213e"
    text = "#eaeaea"
    muted = "#a0a0b0"
    bar_bg = "#2a2a4a"
    gold = "#ffd700"

    w, h = 480, 680
    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    lines.append(f'<rect width="{w}" height="{h}" rx="16" fill="{bg}"/>')
    lines.append(f'<rect x="16" y="16" width="{w-32}" height="{h-32}" rx="12" fill="{card_bg}"/>')

    # Header
    lines.append(f'<text x="240" y="52" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="13" fill="{muted}" letter-spacing="3">YEAR IN REVIEW</text>')
    lines.append(f'<text x="240" y="86" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="32" font-weight="700" fill="{gold}">{_escape(str(year))}</text>')

    # Big stats
    y = 118
    stats = [
        (hours, "Hours Listened"),
        (_escape(top_genre), "Top Genre" + now),
        (_escape(top_artist), "#1 Artist" + now),
    ]
    col_w = 140
    for i, (val, label) in enumerate(stats):
        cx = 40 + i * col_w + col_w // 2
        lines.append(f'<text x="{cx}" y="{y}" text-anchor="middle" font-family="system-ui,sans-serif" '
                     f'font-size="18" font-weight="700" fill="{text}">{val}</text>')
        lines.append(f'<text x="{cx}" y="{y+18}" text-anchor="middle" font-family="system-ui,sans-serif" '
                     f'font-size="10" fill="{muted}">{label}</text>')

    # Divider
    y += 34
    lines.append(f'<line x1="40" y1="{y}" x2="440" y2="{y}" stroke="{bar_bg}" stroke-width="1"/>')

    # Top songs
    y += 22
    lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                 f'font-size="11" fill="{muted}" letter-spacing="2">TOP SONGS</text>')
    for i, song in enumerate(top_songs):
        y += 22
        name = song if isinstance(song, str) else song.get("name", "")
        artist = "" if isinstance(song, str) else song.get("artist", "")
        display = f"{name} — {artist}" if artist else name
        lines.append(f'<text x="50" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{gold}">{i+1}.</text>')
        lines.append(f'<text x="68" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="12" fill="{text}">{_escape(display[:45])}</text>')

    # Milestones
    if milestones:
        y += 26
        lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{muted}" letter-spacing="2">MILESTONES</text>')
        for ms in milestones:
            y += 20
            ms_text = ms if isinstance(ms, str) else ms.get("text", "")
            lines.append(f'<text x="50" y="{y}" font-family="system-ui,sans-serif" '
                         f'font-size="11" fill="{text}">🏆 {_escape(ms_text[:50])}</text>')

    # Insights
    if insights:
        y += 26
        lines.append(f'<text x="40" y="{y}" font-family="system-ui,sans-serif" '
                     f'font-size="11" fill="{muted}" letter-spacing="2">INSIGHTS</text>')
        for ins in insights:
            y += 20
            ins_text = ins if isinstance(ins, str) else ins.get("text", "")
            lines.append(f'<text x="50" y="{y}" font-family="system-ui,sans-serif" '
                         f'font-size="11" fill="{text}">→ {_escape(ins_text[:50])}</text>')

    # Footer
    lines.append(f'<text x="240" y="{h-28}" text-anchor="middle" font-family="system-ui,sans-serif" '
                 f'font-size="9" fill="{muted}">Generated by Apple Music DJ · openclaw</text>')
    lines.append('</svg>')
    return '\n'.join(lines)


def generate_year_review_text(review: dict) -> str:
    """Generate a terminal-friendly year-in-review card."""
    year = review.get("year", "")
    total_minutes = review.get("total_minutes")
    top_genre = review.get("top_genre") or "Unknown"
    top_artist = review.get("top_artist") or "Unknown"
    top_songs = review.get("top_songs", [])[:5]
    milestones = review.get("milestones", [])[:4]
    insights = review.get("insights", [])[:3]
    hours = f"{total_minutes // 60:,}" if total_minutes else "—"  # unknown without Replay
    # Without that year's Replay, artist and genre are today's taste (listening_insights falls back).
    now = "" if review.get("replay_available", True) else " (now)"

    lines = []
    lines.append("╔══════════════════════════════════════╗")
    lines.append(f"║       🎧  YEAR IN REVIEW {year}        ║")
    lines.append("╠══════════════════════════════════════╣")
    lines.append(f"  Hours Listened:  {hours}")
    if now:
        lines.append(f"  #1 Genre (now):  {top_genre}")
        lines.append(f"  #1 Artist (now): {top_artist}")
    else:
        lines.append(f"  #1 Genre:        {top_genre}")
        lines.append(f"  #1 Artist:       {top_artist}")
    lines.append("")
    if top_songs:
        lines.append("  ── TOP SONGS ──")
        for i, song in enumerate(top_songs):
            name = song if isinstance(song, str) else song.get("name", "")
            artist = "" if isinstance(song, str) else song.get("artist", "")
            display = f"{name} — {artist}" if artist else name
            lines.append(f"  {i+1:>2}. {display}")
        lines.append("")
    if milestones:
        lines.append("  ── MILESTONES ──")
        for ms in milestones:
            ms_text = ms if isinstance(ms, str) else ms.get("text", "")
            lines.append(f"    🏆 {ms_text}")
        lines.append("")
    if insights:
        lines.append("  ── INSIGHTS ──")
        for ins in insights:
            ins_text = ins if isinstance(ins, str) else ins.get("text", "")
            lines.append(f"    → {ins_text}")
        lines.append("")
    lines.append("╚══════════════════════════════════════╝")
    lines.append("  Generated by Apple Music DJ · openclaw")
    return "\n".join(lines)


# ── Taste Drift Card ─────────────────────────────────────────────

def _signed_pct(delta: float) -> str:
    return f"{delta * 100:+.0f}%".replace("-", "−")


def generate_drift_text(report: dict) -> str:
    """Terminal-friendly taste-drift card (input: taste_drift.py JSON report)."""
    period = report.get("period", {})
    genres = report.get("genres", {})
    artists = report.get("artists", {})
    arch = report.get("archetype", {})

    lines = []
    lines.append("╔══════════════════════════════════════╗")
    lines.append("║          🎧  TASTE DRIFT              ║")
    lines.append("╠══════════════════════════════════════╣")
    lines.append(f"  {period.get('from', '?')} → {period.get('to', '?')}  ({period.get('days', 0)} days)")
    lines.append("")
    for chunk in textwrap.wrap(report.get("narrative", ""), 40):
        lines.append(f"  {chunk}")
    lines.append("")
    if genres.get("risers"):
        lines.append("  ── RISING ──")
        for g in genres["risers"]:
            lines.append(f"    ▲ {g['genre']}  {_signed_pct(g['delta'])}")
        lines.append("")
    if genres.get("fallers"):
        lines.append("  ── FALLING ──")
        for g in genres["fallers"]:
            lines.append(f"    ▼ {g['genre']}  {_signed_pct(g['delta'])}")
        lines.append("")
    if artists.get("new"):
        lines.append("  ── NEW IN YOUR TOP 20 ──")
        for name in artists["new"][:5]:
            lines.append(f"    + {name}")
        lines.append("")
    if arch.get("from"):
        lines.append(f"  Archetype: {arch['from']}" + (f" → {arch['to']}" if arch.get("changed") else " (unchanged)"))
        lines.append("")
    lines.append("╚══════════════════════════════════════╝")
    lines.append("  Generated by Apple Music DJ · openclaw")
    return "\n".join(lines)


def generate_drift_svg(report: dict) -> str:
    """Shareable SVG taste-drift card (input: taste_drift.py JSON report)."""
    period = report.get("period", {})
    genres = report.get("genres", {})
    artists = report.get("artists", {})
    arch = report.get("archetype", {})
    risers = genres.get("risers", [])[:3]
    fallers = genres.get("fallers", [])[:3]
    new_artists = artists.get("new", [])[:5]
    narrative = textwrap.wrap(report.get("narrative", ""), 48)[:5]

    bg, card_bg, text, muted, bar_bg = "#1a1a2e", "#16213e", "#eaeaea", "#a0a0b0", "#2a2a4a"
    up, down, accent = "#4ecca3", "#e94560", "#ffd700"
    w = 480
    h = 330 + 22 * len(narrative) + 28 * (len(risers) + len(fallers)) + 22 * len(new_artists)
    font = 'font-family="system-ui,sans-serif"'

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<rect width="{w}" height="{h}" rx="16" fill="{bg}"/>',
           f'<rect x="16" y="16" width="{w-32}" height="{h-32}" rx="12" fill="{card_bg}"/>',
           f'<text x="240" y="52" text-anchor="middle" {font} font-size="13" fill="{muted}" letter-spacing="3">TASTE DRIFT</text>',
           f'<text x="240" y="84" text-anchor="middle" {font} font-size="20" font-weight="700" fill="{accent}">'
           f'{_escape(str(period.get("from", "?")))} → {_escape(str(period.get("to", "?")))}</text>',
           f'<text x="240" y="106" text-anchor="middle" {font} font-size="12" fill="{muted}">'
           f'{_escape(str(period.get("days", 0)))} days</text>']

    y = 144
    for chunk in narrative:
        out.append(f'<text x="40" y="{y}" {font} font-size="14" fill="{text}">{_escape(chunk)}</text>')
        y += 22
    y += 14

    def bars(rows: list[dict], color: str, label: str, y: int) -> int:
        if not rows:
            return y
        out.append(f'<text x="40" y="{y}" {font} font-size="11" fill="{muted}" letter-spacing="2">{label}</text>')
        y += 20
        biggest = max(abs(r["delta"]) for r in rows) or 1
        for r in rows:
            width = max(4, int(abs(r["delta"]) / biggest * 140))
            out.append(f'<text x="40" y="{y}" {font} font-size="13" fill="{text}">{_escape(r["genre"])}</text>')
            out.append(f'<rect x="200" y="{y-11}" width="150" height="12" rx="6" fill="{bar_bg}"/>')
            out.append(f'<rect x="200" y="{y-11}" width="{width}" height="12" rx="6" fill="{color}"/>')
            out.append(f'<text x="440" y="{y}" text-anchor="end" {font} font-size="13" fill="{color}">'
                       f'{_signed_pct(r["delta"])}</text>')
            y += 28
        return y + 6

    y = bars(risers, up, "RISING", y)
    y = bars(fallers, down, "FALLING", y)

    if new_artists:
        out.append(f'<text x="40" y="{y}" {font} font-size="11" fill="{muted}" letter-spacing="2">NEW IN YOUR TOP 20</text>')
        y += 22
        for name in new_artists:
            out.append(f'<text x="40" y="{y}" {font} font-size="13" fill="{text}">+ {_escape(name)}</text>')
            y += 22
        y += 6

    if arch.get("from"):
        label = f"{arch['from']} → {arch['to']}" if arch.get("changed") else f"{arch['from']} (unchanged)"
        out.append(f'<text x="240" y="{y + 14}" text-anchor="middle" {font} font-size="14" font-weight="600" '
                   f'fill="{accent}">{_escape(label)}</text>')

    out.append(f'<text x="240" y="{h-28}" text-anchor="middle" {font} font-size="10" fill="{muted}">'
               'Generated by Apple Music DJ · openclaw</text>')
    out.append("</svg>")
    return "\n".join(out)


# ── Data-file loading ────────────────────────────────────────────

def load_data_file(path: str) -> dict:
    """Load an extra-data JSON file, reporting a missing or malformed file cleanly."""
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: --data file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in --data file: {path}", file=sys.stderr)
        print(f"  Parse error at line {e.lineno}, column {e.colno}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Cannot read --data file: {path} ({e.strerror})", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):  # e.g. `[]` or `null` from a script that failed part-way
        print(f"ERROR: --data file must hold a JSON object, not {type(data).__name__}: {path}", file=sys.stderr)
        sys.exit(1)
    return data


# ── Main ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate Taste DNA Card")
    parser.add_argument("profile", help="Path to taste profile JSON")
    parser.add_argument("--output", "-o", default=None, help="Output file path (default: stdout)")
    parser.add_argument("--format", choices=["svg", "text"], default="svg",
                        help="Output format (default: svg)")
    parser.add_argument("--mode", choices=["taste", "compatibility", "year-review", "drift"],
                        default="taste",
                        help="Card mode (default: taste)")
    parser.add_argument("--data", default=None,
                        help="Path to extra data JSON (compatibility result, year review or drift report)")
    args = parser.parse_args()

    profile = load_profile(args.profile)

    if args.mode == "taste":
        if args.format == "svg":
            result = generate_svg(profile)
        else:
            result = generate_text(profile)
    elif args.mode == "compatibility":
        if not args.data:
            print("ERROR: --data required for compatibility mode "
                  "(path to compatibility result JSON).", file=sys.stderr)
            sys.exit(1)
        compat_data = load_data_file(args.data)
        if args.format == "svg":
            result = generate_compatibility_svg(compat_data)
        else:
            result = generate_compatibility_text(compat_data)
    elif args.mode == "year-review":
        if not args.data:
            print("ERROR: --data required for year-review mode "
                  "(path to year review JSON).", file=sys.stderr)
            sys.exit(1)
        review_data = load_data_file(args.data)
        if args.format == "svg":
            result = generate_year_review_svg(review_data)
        else:
            result = generate_year_review_text(review_data)
    elif args.mode == "drift":
        if not args.data:
            print("ERROR: --data required for drift mode "
                  "(path to taste_drift.py JSON output).", file=sys.stderr)
            sys.exit(1)
        drift_data = load_data_file(args.data)
        if args.format == "svg":
            result = generate_drift_svg(drift_data)
        else:
            result = generate_drift_text(drift_data)
    else:  # argparse's `choices` makes this unreachable; it keeps `result` provably assigned
        print(f"ERROR: unknown mode '{args.mode}'.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        write_private(args.output, result)
        print(f"✅ Card written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
