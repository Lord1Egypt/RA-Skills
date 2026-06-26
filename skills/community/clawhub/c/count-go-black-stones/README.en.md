# Count Go Black Stones and Estimate Chinese-Area Score

[中文 README](README.md)

This Codex skill detects a 19x19 Go board from a source board photo, counts visible black stones, estimates black Chinese-area scoring, and can render a clean static result board image. Circles show actual stones; small squares show computed territory; the footer shows a result such as `黑 197 子 胜`.

## Use Cases

- A user uploads an original Go board photo and asks how many black stones are visible.
- A user asks for `黑多少子`, area scoring, or position assessment.
- A user wants a clean result-board image instead of a scoring-app screenshot.
- The task needs to distinguish actual stones from surrounded empty territory.

## Install Dependencies

Install only when dependencies are missing:

```bash
python3 -m pip install -r scripts/requirements.txt
```

## Basic Usage

Generate JSON, a verification overlay, and a clean result board:

```bash
python3 scripts/count_go_black_stones.py /path/to/board.jpg \
  --json \
  --overlay /tmp/go-count-overlay.jpg \
  --result-image /tmp/go-result-board.jpg
```

Print a human-readable result only:

```bash
python3 scripts/count_go_black_stones.py /path/to/board.jpg
```

If automatic board detection is wrong, pass the four board corners in clockwise order from top-left:

```bash
python3 scripts/count_go_black_stones.py /path/to/board.jpg \
  --corners "74,76 1100,53 1118,1031 72,1034" \
  --overlay /tmp/go-count-overlay.jpg \
  --result-image /tmp/go-result-board.jpg
```

If the supplied corners are the four outer grid intersections rather than the wooden board corners, add:

```bash
--grid-corners
```

## Output Fields

- `black_stones`: visible black stones on the board.
- `white_stones`: visible white stones on the board.
- `black_territory`: empty intersections surrounded only by black stones.
- `white_territory`: empty intersections surrounded only by white stones.
- `black_area_chinese`: black stones plus black territory.
- `white_area_chinese`: white stones plus white territory.
- `black_result_chinese`: estimated black result, `胜` or `负`, under Chinese-area scoring.
- `area_total_ok`: whether black and white area sum to the total board intersections.
- `warnings`: confidence, scoring-overlay, dame, or area-check warnings.

## Interpretation

- Report `black_stones` when the user literally asks how many black stones are visible.
- Report `black_area_chinese` when the user asks for `黑多少子`, counting, scoring, or position assessment.
- On a 19x19 board, black wins at `185` or more under Chinese rules after the standard 3.75-stone komi.
- `board_ascii` contains only stones: `X` for black and `O` for white.
- `result_ascii` separates stones and territory: `X/O` for stones, `x/o` for territory, and `.` for neutral empty points.
- If `area_total_ok` is `false`, or the board is blurry, cropped, obstructed, or contains unsettled dead stones, state that manual review is needed.

## Publishing

When publishing this skill or agent configuration, the default listing should be Chinese: Chinese display name, Chinese description, and Chinese default prompt. Link English-language documentation to this README:

[https://github.com/imcaptor/count-go-black-stones/blob/main/README.en.md](https://github.com/imcaptor/count-go-black-stones/blob/main/README.en.md)
