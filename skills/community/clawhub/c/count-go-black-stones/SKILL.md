---
name: count-go-black-stones
description: Count black Go/Weiqi stones from source board photos, estimate black Chinese-area scoring, and render a clean static 19x19 result board image. Use when the user sends an original Go board photo and asks to count black stones, count black's "子", generate a result-board image, or distinguish actual stones from surrounded territory.
---

# Count Go Black Stones

## Workflow

1. Use the source board photo as input. Do not require or depend on a scoring-app result screenshot.
2. Run `scripts/count_go_black_stones.py` on the image to detect the 19x19 grid, classify intersections as black, white, or empty, and compute:
   - `black_stones`: visible black stones on the board.
   - `black_territory`: empty intersections surrounded only by black stones.
   - `black_area_chinese`: black stones plus empty regions bordered only by black stones.
   - `black_result_chinese`: `胜` when `black_area_chinese >= 185` on a 19x19 board, otherwise `负`.
   - `area_total_ok`: sanity check that black area plus white area equals `19*19`.
3. Generate a clean static board with `--result-image` when the user asks for a result image. Actual stones are circles; surrounded territory is marked with small squares; the footer shows the black Chinese-area result, e.g. `黑 197 子 胜`.
4. Compare the script output with the image visually. Correct obvious misses before answering.
5. State uncertainty when the board is blurry, cropped, obstructed, or has unsettled dead stones. Chinese-area scoring assumes dead stones have already been removed or are visually treated as alive.

## Quick Start

Install script dependencies only if they are missing:

```bash
python3 -m pip install -r /path/to/count-go-black-stones/scripts/requirements.txt
```

Run the detector:

```bash
python3 /path/to/count-go-black-stones/scripts/count_go_black_stones.py /path/to/board.jpg \
  --result-image /tmp/go-result-board.jpg \
  --overlay /tmp/go-count-overlay.jpg
```

For JSON-only output:

```bash
python3 /path/to/count-go-black-stones/scripts/count_go_black_stones.py /path/to/board.jpg --json
```

If automatic board detection is wrong, pass the four board corners in image coordinates, ordered clockwise from top-left:

```bash
python3 /path/to/count-go-black-stones/scripts/count_go_black_stones.py board.jpg \
  --corners "74,76 1100,53 1118,1031 72,1034" \
  --result-image /tmp/go-result-board.jpg \
  --overlay /tmp/go-count-overlay.jpg
```

If the supplied corners are the four outer grid intersections rather than the wooden board corners, add `--grid-corners`.

## Interpretation

- Report `black_stones` when the user literally asks how many black stones are visible.
- Report `black_area_chinese` when the user asks for `黑多少子`, `数子`, or `形势`.
- Treat `area_total_ok: false` as a sign that classification or life-and-death status needs review before trusting the result.
- In the generated result image, circles are actual stones from the source photo; small squares are territory markers computed from surrounded empty intersections; the bottom score label uses `black_area_chinese`.
- The result image and JSON use Chinese-area judgement for black: 19x19 black wins at `black_area_chinese >= 185`, after the standard 3.75子 komi.
- In JSON, `board_ascii` contains only stones (`X` black, `O` white), while `result_ascii` separates stones from territory (`X/O` stones, `x/o` territory).
- Treat `black_area_chinese` as a rules-based estimate, not an AI life-and-death judgment. If dead groups remain on the board, tell the user manual confirmation is needed.
- Use the overlay when available to inspect classification mistakes: black stones are marked `B`, white stones `W`, black territory `b`, and white territory `w`.
