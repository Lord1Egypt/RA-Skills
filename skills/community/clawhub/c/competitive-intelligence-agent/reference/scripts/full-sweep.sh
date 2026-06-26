#!/bin/bash
# Full Competitive Intelligence Sweep
# Usage: ./full-sweep.sh [--target "Competitor Name"] [--source pricing|social|reviews|product|all]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/output"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
TARGET="${2:-all}"
SOURCE="${4:-all}"

echo "=== Competitive Intelligence Full Sweep ==="
echo "Started: $(date)"
echo "Target: $TARGET"
echo "Source: $SOURCE"
echo "Output: $OUTPUT_DIR/sweep_$TIMESTAMP"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR/data" "$OUTPUT_DIR/reports" "$OUTPUT_DIR/screenshots"

# 1. Pricing Collection
if [ "$SOURCE" = "all" ] || [ "$SOURCE" = "pricing" ]; then
    echo "[1/6] Collecting pricing data..."
    python3 "$PROJECT_DIR/collectors/pricing.py" \
        --config "$PROJECT_DIR/config" \
        --target "$TARGET" \
        --output "$OUTPUT_DIR/data/pricing_$TIMESTAMP.json" \
        --screenshot-dir "$OUTPUT_DIR/screenshots/$TIMESTAMP"
    echo "      ✓ Pricing collected"
fi

# 2. Social Media Collection
if [ "$SOURCE" = "all" ] || [ "$SOURCE" = "social" ]; then
    echo "[2/6] Collecting social media data..."
    python3 "$PROJECT_DIR/collectors/social.py" \
        --config "$PROJECT_DIR/config" \
        --target "$TARGET" \
        --output "$OUTPUT_DIR/data/social_$TIMESTAMP.json"
    echo "      ✓ Social data collected"
fi

# 3. Review Collection
if [ "$SOURCE" = "all" ] || [ "$SOURCE" = "reviews" ]; then
    echo "[3/6] Collecting review data..."
    python3 "$PROJECT_DIR/collectors/reviews.py" \
        --config "$PROJECT_DIR/config" \
        --target "$TARGET" \
        --output "$OUTPUT_DIR/data/reviews_$TIMESTAMP.json"
    echo "      ✓ Reviews collected"
fi

# 4. Product Change Detection
if [ "$SOURCE" = "all" ] || [ "$SOURCE" = "product" ]; then
    echo "[4/6] Checking product/website changes..."
    python3 "$PROJECT_DIR/collectors/product_changes.py" \
        --config "$PROJECT_DIR/config" \
        --target "$TARGET" \
        --output "$OUTPUT_DIR/data/product_$TIMESTAMP.json"
    echo "      ✓ Product changes checked"
fi

# 5. News Monitoring
if [ "$SOURCE" = "all" ] || [ "$SOURCE" = "news" ]; then
    echo "[5/6] Monitoring news and hiring..."
    python3 "$PROJECT_DIR/collectors/news.py" \
        --config "$PROJECT_DIR/config" \
        --target "$TARGET" \
        --output "$OUTPUT_DIR/data/news_$TIMESTAMP.json"
    echo "      ✓ News checked"
fi

# 6. Generate Comparison Report
if [ "$SOURCE" = "all" ]; then
    echo "[6/6] Generating analysis..."
    python3 "$PROJECT_DIR/analyzers/pricing_comparison.py" \
        --pricing "$OUTPUT_DIR/data/pricing_$TIMESTAMP.json" \
        --config "$PROJECT_DIR/config" \
        --output "$OUTPUT_DIR/reports/comparison_$TIMESTAMP.md"
    
    python3 "$PROJECT_DIR/analyzers/sentiment.py" \
        --reviews "$OUTPUT_DIR/data/reviews_$TIMESTAMP.json" \
        --social "$OUTPUT_DIR/data/social_$TIMESTAMP.json" \
        --config "$PROJECT_DIR/config" \
        --output "$OUTPUT_DIR/reports/sentiment_$TIMESTAMP.md"
    echo "      ✓ Analysis generated"
fi

echo ""
echo "=== Sweep Complete ==="
echo "Data: $OUTPUT_DIR/data/"
echo "Reports: $OUTPUT_DIR/reports/"
echo "Screenshots: $OUTPUT_DIR/screenshots/$TIMESTAMP/"
echo "Finished: $(date)"
