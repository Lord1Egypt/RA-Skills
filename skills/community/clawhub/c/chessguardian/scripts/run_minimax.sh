#!/bin/bash
# Run Minimax Alpha-Beta Pruning autoplay bot against ChessGuardian
# Usage: ./run_minimax.sh [game_id|new] [depth] [delay]
#
# Examples:
#   ./run_minimax.sh new          # Start new game, depth 4, delay 5s
#   ./run_minimax.sh new 5 3      # Start new game, depth 5, delay 3s
#   ./run_minimax.sh AbCdEfGh     # Join existing game
#   ./run_minimax.sh AbCdEfGh 4 10  # Join game, depth 4, delay 10s

GAME_ID="${1:-new}"
DEPTH="${2:-4}"
DELAY="${3:-5}"

echo "🧠 Minimax Alpha-Beta Autoplay Bot"
echo "   Game: $GAME_ID | Depth: $DEPTH | Delay: ${DELAY}s"
echo ""

python3 -u "$(dirname "$0")/autoplay_minimax.py" "$GAME_ID" --depth "$DEPTH" --delay "$DELAY"
