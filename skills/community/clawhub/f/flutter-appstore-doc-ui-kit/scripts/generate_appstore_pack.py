#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import struct
import zlib


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def make_spec(app_name: str, locales: list[str], primary: str) -> str:
    locale_text = ", ".join(locales)
    return f"""# {app_name} — App Feature Document (v1)

## 1. Product Positioning

{app_name} is an offline-first personal sorting and retrieval utility app focused on **real-world object/photo organization**. The app helps users capture items quickly and group them into actionable collections so they can find things later without cloud dependency.

This direction is selected to avoid over-saturated generic categories while keeping value clear and App Store-safe.

## 2. Technical Constraints

- Framework: Flutter (managed by FVM)
- Required version: **Flutter 3.35.1**
- Target platforms: iOS first
- Architecture: local-first, no backend server
- Local storage only: on-device database/files

## 3. Core v1 Features

1. Create collections (e.g., pantry, tools, cables, documents).
2. Add item records by camera capture or photo library import.
3. Attach notes, tags, and last-seen location text.
4. Smart local search by title/tag/notes.
5. Filter by collection, tag, and recent updates.
6. Batch move/delete items.
7. Optional pin/favorite collections.
8. Export a local backup file and import it back.

No future roadmap features are included in this document. v1 scope is complete and production-focused.

## 4. Permission Usage

### Camera Permission
- Used only when user taps “Take Photo”.
- Purpose: capture item images for records.
- No continuous/background camera usage.

### Photo Library Permission
- Used only when user taps “Import from Photos”.
- Purpose: attach existing images to item records.
- No automatic scanning of entire library.

## 5. Data & Privacy Model

- No account system.
- No remote server.
- No third-party tracking SDK required for v1.
- User content remains on device.
- User can delete any item/collection permanently.
- User can reset all local data from settings.

## 6. Information Architecture (Pages)

1. Onboarding (permission rationale + local-first promise)
2. Home Dashboard (collections overview)
3. Collection Detail (item grid/list)
4. Add Item (camera/import entry)
5. Item Detail/Edit
6. Search & Filters
7. Backup & Restore
8. Settings (language, theme, accessibility)

## 7. UI/UX Guidelines (Apple-style)

- Visual style: clean hierarchy, large whitespace, subtle separators.
- Typography: SF-style sans serif hierarchy.
- Motion: minimal, context-preserving transitions.
- Dark mode: first-class support.
- Dynamic type and VoiceOver labels included.
- Primary accent color: `{primary}`

## 8. Localization & Theming

- Built-in locales: {locale_text}
- Light and dark themes fully supported.
- Date/time and copy localized by selected language.

## 9. Offline Architecture

- Repository pattern with local persistence.
- Image files saved in app sandbox.
- Metadata saved in local DB.
- Search index built on device.

## 10. App Store Submission Notes

- Permission descriptions must match in-app behavior.
- Marketing copy avoids exaggerated or unverifiable claims.
- App functionality is fully usable without signup.
- No placeholder or temporary data is shipped.
"""


def ui_svg(title: str, subtitle: str, blocks: list[str], primary: str) -> str:
    cards = ""
    y = 210
    for i, b in enumerate(blocks):
        cards += f'''<rect x="70" y="{y}" rx="16" ry="16" width="990" height="92" fill="#FFFFFF"/>
<text x="96" y="{y+55}" font-size="30" fill="#1C1C1E" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif">{b}</text>\n'''
        y += 112

    return f'''<svg width="1170" height="2532" viewBox="0 0 1170 2532" xmlns="http://www.w3.org/2000/svg">
  <rect width="1170" height="2532" fill="#F2F2F7"/>
  <rect x="0" y="0" width="1170" height="150" fill="#F2F2F7"/>
  <text x="90" y="230" font-size="56" font-weight="700" fill="#000000" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif">{title}</text>
  <text x="90" y="285" font-size="30" fill="#636366" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif">{subtitle}</text>
  <rect x="70" y="340" rx="22" ry="22" width="1030" height="130" fill="{primary}" opacity="0.92"/>
  <text x="96" y="420" font-size="34" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif">Primary action</text>
  {cards}
  <rect x="0" y="2380" width="1170" height="152" fill="#FFFFFF"/>
  <rect x="70" y="2418" width="180" height="8" rx="4" fill="#8E8E93"/>
  <rect x="320" y="2418" width="180" height="8" rx="4" fill="#8E8E93"/>
  <rect x="570" y="2418" width="180" height="8" rx="4" fill="#8E8E93"/>
  <rect x="820" y="2418" width="180" height="8" rx="4" fill="#8E8E93"/>
</svg>'''


def icon_svg(primary: str) -> str:
    return f'''<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0A0A0C"/>
      <stop offset="100%" stop-color="#1C1C22"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="1024" height="1024" fill="url(#g)"/>
  <rect x="182" y="182" width="660" height="660" fill="none" stroke="{primary}" stroke-width="44"/>
  <rect x="300" y="300" width="180" height="180" fill="{primary}"/>
  <rect x="544" y="300" width="180" height="180" fill="#FFFFFF"/>
  <rect x="300" y="544" width="180" height="180" fill="#FFFFFF"/>
  <rect x="544" y="544" width="180" height="180" fill="{primary}"/>
</svg>'''


def parse_hex_color(c: str):
    c = c.lstrip('#')
    if len(c) != 6:
        return (10, 132, 255)
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def write_png_icon(path: Path, primary: str):
    w = h = 1024
    pr, pg, pb = parse_hex_color(primary)

    # RGBA canvas with sharp corners (no rounding)
    raw = bytearray()
    for y in range(h):
        raw.append(0)  # filter type 0
        for x in range(w):
            # dark gradient background
            t = (x + y) / (w + h)
            bg = int(10 + t * 20)
            r = g = b = bg
            a = 255

            # outer square stroke-like frame
            if 182 <= x < 842 and 182 <= y < 842 and (x < 226 or x >= 798 or y < 226 or y >= 798):
                r, g, b = pr, pg, pb

            # 2x2 blocks
            if 300 <= x < 480 and 300 <= y < 480:
                r, g, b = pr, pg, pb
            if 544 <= x < 724 and 300 <= y < 480:
                r, g, b = 255, 255, 255
            if 300 <= x < 480 and 544 <= y < 724:
                r, g, b = 255, 255, 255
            if 544 <= x < 724 and 544 <= y < 724:
                r, g, b = pr, pg, pb

            raw.extend([r, g, b, a])

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack('!I', len(data)) + tag + data + struct.pack('!I', zlib.crc32(tag + data) & 0xffffffff)

    png = bytearray(b'\x89PNG\r\n\x1a\n')
    ihdr = struct.pack('!IIBBBBB', w, h, 8, 6, 0, 0, 0)
    png.extend(chunk(b'IHDR', ihdr))
    png.extend(chunk(b'IDAT', zlib.compress(bytes(raw), level=9)))
    png.extend(chunk(b'IEND', b''))
    path.write_bytes(bytes(png))


def main():
    p = argparse.ArgumentParser(description='Generate App Store-ready app feature markdown + Apple-style UI images + icon')
    p.add_argument('--app-name', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--locales', default='en,zh-Hans')
    p.add_argument('--primary-color', default='#0A84FF')
    args = p.parse_args()

    out = Path(args.out)
    docs = out / 'docs'
    ui = out / 'ui'
    icon = out / 'icon'
    ensure_dir(docs)
    ensure_dir(ui)
    ensure_dir(icon)

    locales = [x.strip() for x in args.locales.split(',') if x.strip()]

    write_text(docs / 'app-feature-spec.md', make_spec(args.app_name, locales, args.primary_color))

    pages = [
        ('Home Dashboard', 'Collections and quick actions', ['Pinned collections', 'Recent captures', 'Storage summary']),
        ('Collection Detail', 'Grid/list of saved items', ['Sort by updated time', 'Filter by tag', 'Batch select']),
        ('Add Item', 'Capture or import images', ['Take photo', 'Import from Photos', 'Add title and tags']),
        ('Item Detail', 'Edit metadata and image', ['Rename item', 'Update notes', 'Delete item']),
        ('Search', 'Local full-text and tags', ['Query suggestions', 'Tag chips', 'Recent searches']),
        ('Backup & Restore', 'Local file export/import', ['Create backup file', 'Restore from file', 'Integrity check']),
        ('Onboarding', 'Permission and privacy intro', ['Camera rationale', 'Photos rationale', 'Offline-first promise']),
        ('Settings', 'Language, theme, accessibility', ['Language selector', 'Dark mode', 'Reset local data']),
    ]

    for i, (title, subtitle, blocks) in enumerate(pages, start=1):
        svg = ui_svg(title, subtitle, blocks, args.primary_color)
        slug = ''.join(ch if ch.isalnum() else '-' for ch in title.lower())
        while '--' in slug:
            slug = slug.replace('--', '-')
        slug = slug.strip('-')
        write_text(ui / f'page-{i:02d}-{slug}.svg', svg)

    write_text(icon / 'app_icon_1024.svg', icon_svg(args.primary_color))
    write_png_icon(icon / 'app_icon_1024.png', args.primary_color)

    print('Generated:')
    print(docs / 'app-feature-spec.md')
    for f in sorted(ui.glob('*.svg')):
        print(f)
    print(icon / 'app_icon_1024.svg')
    print(icon / 'app_icon_1024.png')


if __name__ == '__main__':
    main()
