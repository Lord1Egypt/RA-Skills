#!/bin/bash
# © 2026 Vortex Group. Alle rettigheder forbeholdt.
# 🎬 CC Video Producer — Kør mig!
# Brug: ./cc_produce.sh [video_nummer]
# Eksempel: ./cc_produce.sh 9  (House of Wisdom)

cd /home/openclaw/.openclaw/workspace/projects/factsage

VIDEO=${1:-9}
echo "🎬 Producerer video #$VIDEO..."
echo ""

# Vælg animationstype
echo "Vælg animationstype:"
echo "1) Manim (guld-blæk tekst + animation) — 0 kr"
echo "2) Ken Burns (billeder zoom) — 0 kr"
read -p "Valg (1/2): " TYPE

if [ "$TYPE" = "2" ]; then
    python3 produce_animated.py $VIDEO
else
    echo ""
    echo "Vælg hastighed:"
    echo "1) Normal kvalitet (langsom)"
    echo "2) Quick (hurtig, lavere kvalitet)"
    read -p "Valg (1/2): " SPEED
    
    if [ "$SPEED" = "2" ]; then
        python3 produce_with_manim.py $VIDEO --quick
    else
        python3 produce_with_manim.py $VIDEO
    fi
fi

echo ""
echo "✅ Færdig! Find din video i: output/"
ls -lh output/cc-*-$VIDEO*.mp4 output/animated-$VIDEO*.mp4 2>/dev/null
