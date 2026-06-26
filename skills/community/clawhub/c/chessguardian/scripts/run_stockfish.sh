#!/bin/bash
# Run Stockfish autoplay bot against ChessGuardian
# Usage: ./run_stockfish.sh [game_id|new] [depth] [delay]
#
# Examples:
#   ./run_stockfish.sh new          # Start new game, depth 20, delay 5s
#   ./run_stockfish.sh new 15 3     # Start new game, depth 15, delay 3s
#   ./run_stockfish.sh AbCdEfGh     # Join existing game
#   ./run_stockfish.sh AbCdEfGh 20 10  # Join game, depth 20, delay 10s

GAME_ID="${1:-new}"
DEPTH="${2:-20}"
DELAY="${3:-5}"

echo "🐟 Stockfish Autoplay Bot"
echo "   Game: $GAME_ID | Depth: $DEPTH | Delay: ${DELAY}s"
echo ""

python3 -u "$(dirname "$0")/autoplay_stockfish.py" "$GAME_ID" --depth "$DEPTH" --delay "$DELAY"
