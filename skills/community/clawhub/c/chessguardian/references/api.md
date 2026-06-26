# ChessGuardian API Reference

## Game Modes
- `ai` — Play against Stockfish (server plays White, user plays Black)
- `pvp` — Player vs Player (two humans, no AI)

## Game Status Values
- `active` — Game in progress
- `checkmate` — Game ended by checkmate
- `draw` — Game drawn (stalemate, insufficient material, etc.)
- `resigned` — A player resigned

## Result Values
- `1-0` — White wins
- `0-1` — Black wins
- `1/2-1/2` — Draw

## Move Format
Moves can be in SAN (Standard Algebraic Notation) or UCI format:
- SAN: `e4`, `Nf3`, `O-O`, `Qxd5`, `exd5`
- UCI: `e2e4`, `g1f3`, `e1g1`

## Analysis Response
When making a move against AI, the response includes:
```json
{
  "analysis": {
    "bestMove": "Knight from g8 to f6 (Nf6)",
    "evaluation": "Position is equal",
    "explanation": "Why this move is recommended",
    "winChance": 50
  },
  "stockfishMove": "Nf3",
  "fen": "...",
  "history": ["e4", "e5", "Nf3"],
  "gameOver": false,
  "status": "active"
}
```

## Win Chance
- `winChance` — 0-100, percentage chance White wins
- 50 = equal, >50 = White advantage, <50 = Black advantage
- Computed from material balance using sigmoid function

## Turn Indicator
- Derived from FEN (board.turn), not history length
- `turn: "white"` or `turn: "black"`
