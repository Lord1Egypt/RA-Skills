#!/usr/bin/env bash
set -euo pipefail

echo "=== Token Reduction Engine Setup ==="
echo ""

# Check Python 3.9+
PYVER=$(python3 --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
if [ -z "$PYVER" ]; then
    echo "ERROR: Python 3.9+ required. Install from https://python.org"
    exit 1
fi

MAJOR=$(echo "$PYVER" | cut -d. -f1)
MINOR=$(echo "$PYVER" | cut -d. -f2)
if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]); then
    echo "ERROR: Python 3.9+ required. Found: $PYVER"
    exit 1
fi

echo "✓ Python $PYVER"

# Setup directory
INSTALL_DIR="${TRE_HOME:-$HOME/.tre}"
mkdir -p "$INSTALL_DIR"

# Copy core modules from skill bundle
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 Installing Token Reduction Engine..."

# Copy core modules
if [ -f "$SCRIPT_DIR/tre.py" ]; then
    cp "$SCRIPT_DIR/tre.py" "$INSTALL_DIR/tre.py"
    echo "  ✓ tre.py (core cache engine)"
fi

if [ -f "$SCRIPT_DIR/hallucination_detector.py" ]; then
    cp "$SCRIPT_DIR/hallucination_detector.py" "$INSTALL_DIR/hallucination_detector.py"
    echo "  ✓ hallucination_detector.py (guard module)"
fi

# Create __init__.py for import
cat > "$INSTALL_DIR/__init__.py" << 'EOF'
"""Token Reduction Engine — Cut AI token costs with intelligent caching."""
from .tre import (
    cache_answer, get_cached_answer, get_metrics,
    clear_cache, reduce_tokens, configure
)

__all__ = [
    "cache_answer", "get_cached_answer", "get_metrics",
    "clear_cache", "reduce_tokens", "configure"
]
EOF
echo "  ✓ __init__.py (package init)"

# Create example script
cat > "$INSTALL_DIR/example.py" << 'EOF'
#!/usr/bin/env python3
"""Quick example: Cache LLM responses to save tokens."""

from tre import cache_answer, get_cached_answer, get_metrics

# 1. Simulate an LLM call (expensive)
query = "What is our refund policy?"
llm_answer = "30 days, no questions asked. Full refund to original payment method."

# 2. Cache the answer (free after first time)
result = cache_answer(query, llm_answer)
print(f"Cached: {result['cached']} | Flagged: {result['flagged']}")

# 3. Next time — zero tokens, instant response
cached = get_cached_answer(query)
if cached:
    answer, tokens = cached
    print(f"Cache hit! Saved {tokens} tokens. Answer: {answer}")

# 4. Check your savings
print(f"\nMetrics: {get_metrics()}")
EOF
chmod +x "$INSTALL_DIR/example.py"
echo "  ✓ example.py (quick start)"

echo ""
echo "✅ Token Reduction Engine installed!"
echo ""
echo "Location: $INSTALL_DIR"
echo "Cache: SQLite-backed, automatic persistence"
echo ""
echo "Quick start:"
echo "  cd $INSTALL_DIR"
echo "  python3 example.py"
echo ""
echo "Python API:"
echo "  from tre import cache_answer, get_cached_answer, get_metrics"
echo ""
echo "Integration with Company Brain:"
echo "  clawhub install company-brain-os certainlogic-tre"
echo ""
echo "Documentation:"
echo "  - Configuration: references/CONFIGURATION.md"
echo "  - API Reference: references/API.md"
echo ""
