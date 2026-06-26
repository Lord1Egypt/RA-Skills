#!/usr/bin/env bash
# Cognitive Enhancement Engine - One-click Setup
# Platforms: Linux / macOS / Windows (Git Bash / WSL)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_PY="$DIR/engine.py"

echo "=== Cognitive Enhancement Engine Setup ==="

# 1. Check Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "[ERROR] Python not found. Please install Python 3.8+"
    exit 1
fi

echo "[1/3] Python version: $($PYTHON --version 2>&1)"

# 2. Verify engine
echo "[2/3] Verifying engine..."
cd "$DIR"
$PYTHON -c "
import sys
sys.path.insert(0, '.')
from engine import CognitiveEnhancer
brain = CognitiveEnhancer()
brain.memorize('Installation test', importance=1.0)
brain.perceive('verification')
status = brain.get_status()
assert status['long_term_memories'] == 1, 'Memory not working'
print('Engine verified OK')
print(f'  Memories: {status[\"long_term_memories\"]}')
print(f'  Working:  {status[\"working_memories\"]}')
"

# 3. Create shell alias (optional)
echo "[3/3] Creating shell alias (optional)..."
SHELL_RC="$HOME/.bashrc"
[ -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.zshrc"

ALIAS_CMD="alias cognitive-enhance='cd $DIR && $PYTHON -c \"import sys; sys.path.insert(0, \\\"$DIR\\\"); from engine import CognitiveEnhancer; b = CognitiveEnhancer(); print(\\\"Cognitive Enhancement Engine loaded. Use b.perceive(), b.memorize(), b.recall() etc.\\\"); import code; code.interact(local=dict(b=b))\"'"

if ! grep -q "cognitive-enhance" "$SHELL_RC" 2>/dev/null; then
    echo "$ALIAS_CMD" >> "$SHELL_RC"
    echo "  Alias 'cognitive-enhance' added to $SHELL_RC"
    echo "  Run: source $SHELL_RC && cognitive-enhance"
else
    echo "  Alias 'cognitive-enhance' already exists"
fi

echo ""
echo "=== Setup Complete ==="
echo "Quick start:  python \"$ENGINE_PY\""
echo "API mode:     from engine import CognitiveEnhancer"
