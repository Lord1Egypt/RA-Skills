#!/bin/bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="${AMAZON_SCRAPE_DIR:-$HOME/scrapes}"

# Dockerfile.sh is the source of truth; Dockerfile is generated and gitignored.
# (clawhub only bundles files with known text extensions, so the real one needs .sh)
# Always overwrite: the old `if [ ! -f Dockerfile ]` guard meant edits to
# Dockerfile.sh were silently ignored whenever a stale Dockerfile already existed.
cp "$SKILL_DIR/Dockerfile.sh" "$SKILL_DIR/Dockerfile"

echo "Building Docker image 'amazon-scraper'..."
docker build -t amazon-scraper "$SKILL_DIR"

mkdir -p "$OUT_DIR"

cat <<EOF

Image 'amazon-scraper' is ready. Output directory: $OUT_DIR

Credentials are NOT baked into the image. Supply a proxy at run time, either way:

  export AMAZON_PROXIES="http://USER:PASS@HOST:PORT"        # comma-separate for several
  docker run --rm -e AMAZON_PROXIES amazon-scraper \\
    node assets/amazon_handler.js "https://www.amazon.com/gp/bestsellers/electronics"

  # or mount a file based on config/proxies.example.json
  docker run --rm -v "$SKILL_DIR/config/proxies.json:/app/config/proxies.json:ro" \\
    amazon-scraper node assets/amazon_handler.js "URL"

Verify the exit IP before touching Amazon:

  curl -s -x "\$AMAZON_PROXIES" http://api.ipify.org

Save results to the host (--output is a path inside the container's /data):

  docker run --rm -e AMAZON_PROXIES -v "$OUT_DIR:/data" amazon-scraper \\
    node assets/amazon_handler.js "URL" --output result.json

Notes:
  - Do not pass -t. A TTY merges stderr into stdout and corrupts the JSON on stdout.
  - Exit code 0 = SUCCESS, 3 = PARTIAL (some pages blocked), 2 = ERROR. Check it;
    "status" in the JSON says the same thing.
  - --concurrency is capped at the number of proxy exits. More workers than exits
    just gets the IP blocked.
  - BSR URLs use /gp/bestsellers/ (not /zgbs/).
EOF
