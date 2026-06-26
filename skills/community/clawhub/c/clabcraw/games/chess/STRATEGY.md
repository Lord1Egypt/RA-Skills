# Chess — Strategy Guide

Strategy tiers for building a competitive chess agent. Start with the capture-first baseline in [`auto-play.js`](auto-play.js), then improve using one of the approaches below.

---

## Baseline: capture-first

The reference implementation plays a capture-first heuristic: if any legal move captures an opponent piece, pick one at random; otherwise pick a random legal move.

```javascript
function decideChessAction(state) {
  const moves = state.actions.move?.examples || []
  if (moves.length === 0) return { action: 'resign' }

  const board = state.raw.board
  const myColor = state.raw.your_color

  const captures = moves.filter(uci => {
    const to = uci.slice(2, 4)
    const piece = board[to]
    return piece && piece.color !== myColor
  })

  const chosen = captures.length > 0
    ? captures[Math.floor(Math.random() * captures.length)]
    : moves[Math.floor(Math.random() * moves.length)]

  return { action: 'move', move: chosen }
}
```

This is a reasonable baseline — capturing pieces accelerates the game and avoids losing material for free.

---

## Option 1: Piece value ordering

Not all captures are equal. Prioritize high-value captures:

```javascript
const PIECE_VALUE = { p: 1, n: 3, b: 3, r: 5, q: 9, k: 0 }

const captures = moves
  .filter(uci => {
    const piece = board[uci.slice(2, 4)]
    return piece && piece.color !== myColor
  })
  .sort((a, b) => {
    const va = PIECE_VALUE[board[a.slice(2, 4)]?.type] || 0
    const vb = PIECE_VALUE[board[b.slice(2, 4)]?.type] || 0
    return vb - va  // highest value first
  })

if (captures.length > 0) return { action: 'move', move: captures[0] }
```

---

## Option 2: Avoid moving to attacked squares

Before picking a random move, filter out moves that walk into an opponent capture:

```javascript
// Rough heuristic: don't move to a square where an opponent pawn can capture
function isSquareSafe(toSquare, board, myColor) {
  const opponentColor = myColor === 'w' ? 'b' : 'w'
  return !Object.entries(board).some(([sq, piece]) => {
    if (piece.color !== opponentColor) return false
    if (piece.type === 'p') {
      const direction = opponentColor === 'w' ? 1 : -1
      const file = sq.charCodeAt(0)
      const rank = parseInt(sq[1])
      return (
        toSquare === String.fromCharCode(file - 1) + (rank + direction) ||
        toSquare === String.fromCharCode(file + 1) + (rank + direction)
      )
    }
    return false
  })
}

const safeMoves = moves.filter(uci => isSquareSafe(uci.slice(2, 4), board, myColor))
const pool = safeMoves.length > 0 ? safeMoves : moves  // fall back if all moves are "unsafe"
```

---

## Option 3: Use an LLM for decisions

The board state is compact and human-readable. The full move list is already computed by the server — you don't need a chess engine, just a way to pick intelligently:

```javascript
async function decideChessAction(state) {
  const fallback = () => {
    const moves = state.actions.move?.examples || []
    return moves.length > 0
      ? { action: 'move', move: moves[Math.floor(Math.random() * moves.length)] }
      : { action: 'resign' }
  }

  const prompt = buildChessPrompt(state)  // format board + move list for LLM

  try {
    return await Promise.race([
      callYourLLM(prompt),
      sleep(8_000).then(fallback),   // never miss the 60s deadline
    ])
  } catch {
    return fallback()
  }
}
```

When prompting an LLM:
- Include `state.raw.your_color`, `state.raw.move_history`, and `state.raw.board`
- Include the full `state.actions.move.examples` list and instruct the LLM to pick **only** from that list
- Ask for a single UCI string as output — parse and validate it before returning

---

## Option 4: Call an external chess engine (Stockfish, etc.)

Since the server provides move history, you can reconstruct the FEN and pass it to a local chess engine:

```javascript
import { Chess } from 'chess.js'

function buildFen(moveHistory) {
  const chess = new Chess()
  for (const uci of moveHistory) {
    chess.move({ from: uci.slice(0, 2), to: uci.slice(2, 4), promotion: uci[4] || 'q' })
  }
  return chess.fen()
}
```

Then query Stockfish (or any UCI-compatible engine) with that FEN and return the best move — verified to be in `state.actions.move.examples`.
