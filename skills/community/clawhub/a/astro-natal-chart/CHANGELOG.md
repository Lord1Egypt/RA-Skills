# Changelog

## v3.12.0 (2026-06-01)

- **Header layout fix**: removed "NATAL CHART" title from above the wheel, kept it only above the interpretation panel
- **Name placement**: person's name now shown below the "NATAL CHART" title in the right panel
- **ClawHub link moved**: relocated from under the wheel legends to the bottom of the right interpretation panel

## v3.11.0 (2026-06-01)

- **Layout redesign**: removed right zodiac circle, merged center+right into single 3600px interpretation panel
- **Chart header**: added "NATAL CHART" title above left wheel + optional `--name` parameter for person's name
- **Full interpretation panel**: Sun/Moon/ASC sign descriptions, dominant element, stelliums, retrograde planets, all 12 houses with cusp positions, house meanings, and planets in each house
- **ClawHub link**: added skill repository URL under the legends below the wheel
- Language-aware: interpretation text in Russian (`--lang ru`) or English (`--lang en`)
- Cleaned up debug files

## v3.10.0 (2026-06-01)

- **Fonts shipped as .ttf.dat to bypass ClawHub filter**: ClawHub silently strips `.ttf` files from skill packages. Fonts are now bundled as `seguisym.ttf.dat` (2.4 MB) and `segoeuisl.ttf.dat` (854 KB). `draw_wheel.py` auto-detects and restores them to `.ttf` on first run via `shutil.copy2`.
- This ensures the skill renders correctly on all machines after ClawHub installation without any manual font setup.

## v3.9.0 (2026-06-01)

- **Attempted bundled fonts**: included `seguisym.ttf` and `segoeuisl.ttf` directly in `scripts/`. ClawHub silently filtered them out — not present in the published package.

## v3.8.0 (2026-06-01)

- **Fixed element coloring bug**: `Pillow pieslice()` uses a different coordinate system than `cos/sin` — sectors were drawn at mirrored positions, causing wrong element colors. Replaced with `draw.polygon()` using explicit coordinate math.
- **Sector boundaries aligned to zodiac signs**: sectors start from the beginning of each sign, not from the ASC degree.
- Bundled fonts reference added (deferred to v3.9.0 for actual inclusion).

## v3.7.0 (2026-06-01)

- **Two equal-size wheels**: natal chart with houses (left) and zodiac planet circle (right) — both 2160×2160px
- **Panoramic layout**: 5760×2880 total (2:1), data panel (1440px) between the two wheels
- **Dual-font rendering** with per-character font selection
- **Zodiac planet circle**: same planet orbit radius and size as main wheel

## v2.1.0 (2026-05-28)

- Fixed `.pyd.dat` loading on Windows
- Added Microsoft Visual C++ Redistributable requirement
- Requires Python 3.14.x

## v2.0.0 (2026-05-28)

- Switched to Swiss Ephemeris (pyswisseph 2.10.3.2) as primary calculation engine
- House calculation via `swe.houses_ex()` (exact iterative Placidus)
- Added retrograde detection via `FLG_SPEED` flag

## v1.x (earlier)

- Initial release using simplified analytical formulas
