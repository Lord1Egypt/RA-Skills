---
name: chess-buddy
description: "Stockfish-backed chess buddy for analyzing FEN positions and board images."
version: 0.1.1
licenseAccepted: MIT-0
metadata:
  openclaw:
    requires:
      bins: ["python3", "stockfish"]
    homepage: https://github.com/TommyClawd/chess-buddy-skill
---

# Chess Buddy

Use when the user wants chess help: board pictures, FEN validation, best moves, candidate lines, blunder review, or a training explanation.

## License note

This ClawHub package is **MIT-0** because ClawHub requires MIT-0 for all published skills. It is intentionally small: it treats Stockfish as an external executable dependency, does not bundle Stockfish, and does not import GPL Python libraries such as `python-chess`.

The richer GitHub source package is **GPL-3.0-or-later** because it imports `python-chess` and provides fuller FEN/PGN/SAN tooling: <https://github.com/TommyClawd/chess-buddy-skill>.

## Guardrails

- Do not assist cheating in active human games or rated online play. If the user is currently playing, offer post-game analysis or general principles only.
- Image recognition is uncertain. Always verify side to move, board orientation, castling rights, en passant, and move number before treating an image-derived FEN as authoritative.
- Image annotations are semantic, not self-explanatory. Do not assume an arrow/highlight is the played move; classify whether it is played move, engine recommendation, candidate line, last move, or mistake marker before explaining.
- Engine output is evidence, not prose. Explain candidate moves in human terms and flag tactical vs strategic reasons.

## Workflow

1. Identify input type: image, FEN, PGN, or natural-language position.
2. For images, follow `references/image-to-fen.md`; produce a candidate FEN, classify arrows/highlights, and verify the FEN before analysis.
3. Run `scripts/stockfish_fen.py engine-check` once if the environment is new or engine availability is uncertain.
4. Use `scripts/stockfish_fen.py analyze --fen ... --multipv 3 --depth 12` for real engine analysis.
5. Return concise analysis: position summary, top move(s), key line(s), plan, and uncertainty/verification notes.

## Helper commands

```bash
python3 chess-buddy/scripts/stockfish_fen.py engine-check
python3 chess-buddy/scripts/stockfish_fen.py analyze --fen "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" --multipv 3 --depth 12
```

If Stockfish is missing, report the missing dependency. Do not present non-engine commentary as chess analysis; call it notation validation, position description, or general coaching only.
