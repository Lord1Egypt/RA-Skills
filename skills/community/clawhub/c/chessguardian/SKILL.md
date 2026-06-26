---
name: chessguardian
description: >
  Play chess via ChessGuardian API — start games, make moves, watch live games,
  run autoplay bots (Stockfish or Minimax), and get board snapshots. Use when
  the user wants to play chess, start a new chess game, make a chess move, view
  a live chess board, run an AI chess bot, get a QR code for a chess game,
  analyze a chess position, or any chess-related interaction. Requires a running
  ChessGuardian instance.
---

# ChessGuardian Skill

Interact with ChessGuardian — a live chess platform with Stockfish AI.

## Configuration

Set the base URL in the environment or default to:
```
CHESSGUARDIAN_URL=https://chessguardian-production.up.railway.app
```

## API Endpoints

### Start a new game
```
POST /api/live/start
Body: {"mode": "ai"} or {"mode": "pvp"}
Returns: {id, fen, history, lastMove}
```

### Get game state
```
GET /api/live/<game_id>
Returns: {id, fen, history, status, turn, winChance, gameOver}
```

### Make a move
```
POST /api/live/<game_id>/move
Body: {"move": "e5"} (SAN or UCI format)
Returns: {fen, history, stockfishMove, analysis, gameOver, status}
```

### Get QR code
```
GET /api/live/<game_id>/qr
Returns: PNG image
```

## Workflows

### Start a game and send QR code
1. POST `/api/live/start` with `{"mode": "ai"}`
2. GET `/api/live/<id>/qr` → save to outbound media
3. Send QR image + live link to user

### Make a move for the user
1. POST `/api/live/<id>/move` with the move in SAN (e.g. "e5", "Nf6", "O-O")
2. Show the AI analysis and Stockfish's reply
3. Optionally render the board snapshot

### Run autoplay bot
Execute the bundled scripts:
- **Stockfish bot:** `python3 -u scripts/autoplay_stockfish.py <game_id|new> --depth 20 --delay 5`
- **Minimax bot:** `python3 -u scripts/autoplay_minimax.py <game_id|new> --depth 4 --delay 5`

Both scripts support `new` to auto-start a game. Use `-u` for unbuffered output.

### Render board snapshot
1. Generate an HTML file using chessboard.js with the FEN from game state
2. Screenshot with Playwright: `npx playwright screenshot --browser chromium --viewport-size=440,520 board.html output.png`
3. Send the image to user

## Dependencies

- Python 3 with `chess` and `requests` packages
- Stockfish binary (for autoplay_stockfish.py)
- Playwright + Chromium (for board screenshots)
- curl or equivalent for API calls

## Live page

Users can watch games in browser at: `<base_url>/live/<game_id>`
