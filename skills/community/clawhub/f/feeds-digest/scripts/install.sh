#!/bin/bash
# feeds-digest install script
# Legt Config-Verzeichnis an und kopiert Beispiel-Config

set -e

CONFIG_DIR="${HOME}/.config/feeds-digest"
CACHE_DIR="${HOME}/.cache/feeds-digest"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📁 Erstelle Config-Verzeichnis: $CONFIG_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CACHE_DIR"

if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
    cp "$SKILL_ROOT/config/config.example.yaml" "$CONFIG_DIR/config.yaml"
    echo "✅ Config kopiert nach $CONFIG_DIR/config.yaml"
    echo "   → Bitte anpassen (YouTube Channel-IDs eintragen)"
else
    echo "⏭️  Config existiert bereits: $CONFIG_DIR/config.yaml"
fi

echo ""
echo "📦 Installiere Python-Dependencies..."
pip3 install --quiet --user -r "$SKILL_ROOT/requirements.txt" 2>&1 | tail -5

echo ""
echo "✅ Installation abgeschlossen."
echo ""
echo "Nächste Schritte:"
echo "  1. Config anpassen:  $CONFIG_DIR/config.yaml"
echo "  2. Test:             python3 $SCRIPT_DIR/feeds-digest.py --test"
echo "  3. Erstes Digest:    python3 $SCRIPT_DIR/feeds-digest.py --since 7d"
echo "  4. Optional Cron:    Siehe README.md"
