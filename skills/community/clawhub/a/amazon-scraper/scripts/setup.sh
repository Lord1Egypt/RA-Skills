#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Dockerfile.sh is the actual Dockerfile (renamed for clawhub bundling compatibility)
# clawhub only bundles files with known text extensions; Dockerfile has no extension
if [ ! -f "$SCRIPT_DIR/Dockerfile" ]; then
  cp "$SCRIPT_DIR/Dockerfile.sh" "$SCRIPT_DIR/Dockerfile"
fi

echo "🔧 Building Docker image 'amazon-scraper'..."
docker build -t amazon-scraper "$SCRIPT_DIR"

mkdir -p ~/scrapes
echo "✅ Done. Image 'amazon-scraper' is ready."
echo "   Scrape output directory: ~/scrapes"
echo ""
echo "Quick test (proxy pre-configured):"
echo "  docker run -t --rm amazon-scraper node assets/amazon_handler.js \"https://www.amazon.com/gp/bestsellers/electronics\""
echo ""
echo "Save results to file (mapped to ~/scrapes):"
echo "  docker run -t --rm -v ~/scrapes:/data amazon-scraper node assets/amazon_handler.js \"URL\" --output result.json"
echo ""
echo "Multi-page search with output:"
echo "  docker run -t --rm -v ~/scrapes:/data amazon-scraper node assets/amazon_handler.js \"https://www.amazon.com/s?k=phone\" --pages 2 --output phone_search.json"
echo ""
echo "Override built-in proxies with your own:"
echo "  docker run -t --rm -e AMAZON_PROXIES=\"http://user:pass@host:8001,...\" amazon-scraper node assets/amazon_handler.js \"URL\""
echo ""
echo "Tips:"
echo "  - 5 rotating proxies are pre-configured in config/proxies.json"
echo "  - BSR URLs use /gp/bestsellers/ (not /zgbs/) for correct page routing"
echo "  - Output path is relative to /data inside container; map -v ~/scrapes:/data to persist locally"
echo "  - AMAZON_PROXIES env var overrides built-in config; AMAZON_PROXY uses a single proxy"
