# Image to FEN workflow

Use the vision model to inspect a board image, then validate with deterministic chess tooling.

## Required output from vision

Ask for:
- board orientation: which color is at bottom, and which square is bottom-left
- piece placement by square, e.g. `White: Kg1 Qd1 ...; Black: Kg8 ...`
- side to move if visible; otherwise ask user or infer from context only when clear
- castling rights, en-passant target, halfmove clock, fullmove number; default to `- 0 1` only when unknown and say so
- uncertainty list: obscured pieces, ambiguous colors, cropped squares, highlighted last move squares
- annotation semantics: whether arrows/highlights show the move played, engine recommendation, candidate move, last move, mistake marker, or tactical idea

## Verification checklist

Before engine analysis:
- exactly one white king and one black king
- no side has more than legal maximum pieces without promotion note
- kings are not adjacent
- side-to-move is known or explicitly assumed
- FEN has six fields
- image annotations are classified before explanation: played move vs engine recommendation vs candidate line vs mistake marker. If unclear, state the ambiguity and ask or analyze both interpretations.

## Ambiguous annotation rule

Do not assume an arrow is the move that was played. Chess-app screenshots often show several semantic layers at once: the player's move, the engine's recommended move, colored mistake markers, and last-move highlights. Before explaining why a move is good/bad:

1. Identify the current board state.
2. Identify whose turn it is in that board state.
3. Classify arrows/highlights by context and color if possible.
4. If two interpretations are plausible, run the engine on both and say which assumption you used.
5. Phrase the answer as "if the arrow is X..." unless the annotation semantics are clear.

Regression example: an image showed White queen on b5 after the mistake, while a green arrow indicated the engine recommendation **Bf4xg5**. The correct explanation was not "Bxg5 is bad"; it was "Qb5? is bad because it leaves Black's knight on g5 alive, allowing ...Nf3+; Bxg5 was the recommended prevention."
