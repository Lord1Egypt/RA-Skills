#!/usr/bin/env bash
# agent-memory-tools setup — installs Ollama models and validates the environment.
# Usage: bash setup.sh [--minimal]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MINIMAL=false
[[ "${1:-}" == "--minimal" ]] && MINIMAL=true

green()  { printf "\033[32m%s\033[0m\n" "$1"; }
yellow() { printf "\033[33m%s\033[0m\n" "$1"; }
red()    { printf "\033[31m%s\033[0m\n" "$1"; }

echo "🧠 agent-memory-tools setup"
echo "=========================="
echo ""

# ── 1. Python ──
echo "1/4  Checking Python..."
if command -v python3 &>/dev/null; then
  PY_VER=$(python3 --version 2>&1)
  green "  ✅ $PY_VER"
else
  red "  ❌ Python 3 not found. Install Python 3.9+ from https://python.org"
  exit 1
fi

# ── 2. Ollama ──
echo "2/4  Checking Ollama..."
if command -v ollama &>/dev/null; then
  green "  ✅ Ollama installed"
else
  yellow "  ⚠ Ollama not found. Installing..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  → Download from https://ollama.com/download/mac"
    echo "  → Or: brew install ollama"
  elif [[ "$OSTYPE" == "linux"* ]]; then
    echo "  → Running: curl -fsSL https://ollama.com/install.sh | sh"
    curl -fsSL https://ollama.com/install.sh | sh
  else
    echo "  → Download from https://ollama.com/download"
  fi

  if ! command -v ollama &>/dev/null; then
    red "  ❌ Ollama still not found. Please install manually and re-run."
    exit 1
  fi
fi

# Check Ollama is running
if ! ollama list &>/dev/null 2>&1; then
  yellow "  ⚠ Ollama not running. Starting..."
  if [[ "$OSTYPE" == "darwin"* ]]; then
    open -a Ollama 2>/dev/null || ollama serve &>/dev/null &
  else
    ollama serve &>/dev/null &
  fi
  sleep 3
  if ! ollama list &>/dev/null 2>&1; then
    red "  ❌ Cannot start Ollama. Please start it manually and re-run."
    exit 1
  fi
fi
green "  ✅ Ollama running"

# ── 3. Models ──
echo "3/4  Pulling models..."

pull_if_missing() {
  local model="$1"
  if ollama list 2>/dev/null | grep -q "$model"; then
    green "  ✅ $model (already installed)"
  else
    yellow "  ⏳ Pulling $model..."
    ollama pull "$model"
    green "  ✅ $model installed"
  fi
}

# Core models (required)
pull_if_missing "gemma3:4b"
pull_if_missing "nomic-embed-text-v2-moe"

# Extended models (optional, skip with --minimal)
if [[ "$MINIMAL" == false ]]; then
  echo ""
  echo "  Optional models (skip with --minimal):"
  # Only pull if 16GB+ RAM available
  TOTAL_RAM_GB=0
  if [[ "$OSTYPE" == "darwin"* ]]; then
    TOTAL_RAM_GB=$(( $(sysctl -n hw.memsize) / 1073741824 ))
  elif [[ -f /proc/meminfo ]]; then
    TOTAL_RAM_GB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1048576 ))
  fi

  if (( TOTAL_RAM_GB >= 16 )); then
    yellow "  RAM: ${TOTAL_RAM_GB}GB — pulling extended models"
    pull_if_missing "qwen3.5:27b"
  else
    yellow "  RAM: ${TOTAL_RAM_GB}GB — skipping large models (need 16GB+)"
  fi
fi

# ── 4. Validate ──
echo "4/4  Running self-test..."
echo ""

cd "$SCRIPT_DIR"
if python3 scripts/selftest.py; then
  echo ""
  green "🎉 Setup complete! agent-memory-tools is ready."
  echo ""
  echo "Quick start:"
  echo "  python3 scripts/unified_recall.py \"What happened last week?\""
  echo "  python3 scripts/extract_facts.py \"Some text\" --store"
  echo "  python3 scripts/auto_ingest.py --scan"
  echo ""
  echo "Run tests:  python3 scripts/tests.py"
  echo "Full docs:  cat SKILL.md"
else
  echo ""
  red "⚠ Self-test had issues. Check the output above."
  echo "Common fixes:"
  echo "  - Make sure Ollama is running: ollama serve"
  echo "  - Pull missing models: ollama pull gemma3:4b"
  echo "  - Check scripts/config.json for custom settings"
fi
