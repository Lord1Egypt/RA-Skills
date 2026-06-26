#!/usr/bin/env bash
# plan-trip.sh — Orchestrate flyai API calls for a Grand Slam trip
#
# Usage:
#   bash scripts/plan-trip.sh \
#     --slam "australian-open" \
#     --origin "上海" \
#     --arrive "2026-01-18" \
#     --leave "2026-02-02" \
#     --budget 1500
#
# This script runs all four flyai searches in sequence and saves
# raw JSON results to a temporary directory for the AI to assemble.

set -euo pipefail

# --- Defaults ---
SLAM=""
ORIGIN=""
ARRIVE_DATE=""
LEAVE_DATE=""
BUDGET=""
OUTPUT_DIR="/tmp/slam-trip-results"

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --slam)       SLAM="$2";        shift 2 ;;
    --origin)     ORIGIN="$2";      shift 2 ;;
    --arrive)     ARRIVE_DATE="$2"; shift 2 ;;
    --leave)      LEAVE_DATE="$2";  shift 2 ;;
    --budget)     BUDGET="$2";      shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# --- Validate required args ---
if [[ -z "$SLAM" || -z "$ORIGIN" || -z "$ARRIVE_DATE" || -z "$LEAVE_DATE" ]]; then
  echo "Error: --slam, --origin, --arrive, --leave are all required."
  exit 1
fi

# --- Map slam to city and venue ---
case "$SLAM" in
  australian-open)
    CITY="墨尔本"; VENUE="Melbourne Park"; SLAM_NAME="澳网"; COUNTRY="澳大利亚" ;;
  french-open)
    CITY="巴黎"; VENUE="Roland Garros"; SLAM_NAME="法网"; COUNTRY="法国" ;;
  wimbledon)
    CITY="伦敦"; VENUE="Wimbledon"; SLAM_NAME="温网"; COUNTRY="英国" ;;
  us-open)
    CITY="纽约"; VENUE="Flushing Meadows"; SLAM_NAME="美网"; COUNTRY="美国" ;;
  *)
    echo "Error: --slam must be one of: australian-open, french-open, wimbledon, us-open"
    exit 1 ;;
esac

# --- Prepare output directory ---
mkdir -p "$OUTPUT_DIR"
echo "=== Grand Slam Trip Planner ==="
echo "Tournament: $SLAM_NAME ($SLAM)"
echo "From: $ORIGIN → $CITY"
echo "Dates: $ARRIVE_DATE to $LEAVE_DATE"
echo "Budget cap: ${BUDGET:-"no limit"} CNY/night"
echo "Results will be saved to: $OUTPUT_DIR"
echo ""

# --- Step 1: Search flights ---
echo "[1/4] Searching flights..."
if flyai search-flight --origin "$ORIGIN" --destination "$CITY" --dep-date "$ARRIVE_DATE" --back-date "$LEAVE_DATE" --sort-type 3 > "$OUTPUT_DIR/flights.json" 2>&1; then
  echo "  ✓ Flight results saved."
else
  echo "  ✗ Flight search failed. Check error in $OUTPUT_DIR/flights.json"
fi

# --- Step 2: Search hotels ---
echo "[2/4] Searching hotels near $VENUE..."
if [[ -n "$BUDGET" ]]; then
  if flyai search-hotel --dest-name "$CITY" --poi-name "$VENUE" --check-in-date "$ARRIVE_DATE" --check-out-date "$LEAVE_DATE" --sort distance_asc --max-price "$BUDGET" > "$OUTPUT_DIR/hotels.json" 2>&1; then
    echo "  ✓ Hotel results saved."
  else
    echo "  ✗ Hotel search failed. Check error in $OUTPUT_DIR/hotels.json"
  fi
else
  if flyai search-hotel --dest-name "$CITY" --poi-name "$VENUE" --check-in-date "$ARRIVE_DATE" --check-out-date "$LEAVE_DATE" --sort distance_asc > "$OUTPUT_DIR/hotels.json" 2>&1; then
    echo "  ✓ Hotel results saved."
  else
    echo "  ✗ Hotel search failed. Check error in $OUTPUT_DIR/hotels.json"
  fi
fi

# --- Step 3: Search tickets and experiences ---
echo "[3/4] Searching tickets and experiences..."
YEAR=$(echo "$ARRIVE_DATE" | cut -d'-' -f1)
flyai keyword-search --query "${SLAM_NAME}门票 ${YEAR}" > "$OUTPUT_DIR/tickets.json" 2>&1 || true
flyai keyword-search --query "${CITY} 网球体验" > "$OUTPUT_DIR/experiences.json" 2>&1 || true
flyai keyword-search --query "${COUNTRY}签证" > "$OUTPUT_DIR/visa.json" 2>&1 || true
echo "  ✓ Ticket, experience, and visa results saved."

# --- Step 4: Search nearby attractions ---
echo "[4/4] Searching attractions in $CITY..."
flyai search-poi --city-name "$CITY" --category "城市观光" > "$OUTPUT_DIR/poi_urban.json" 2>&1 || true
flyai search-poi --city-name "$CITY" --category "博物馆" > "$OUTPUT_DIR/poi_museum.json" 2>&1 || true
flyai search-poi --city-name "$CITY" --category "人文古迹" > "$OUTPUT_DIR/poi_culture.json" 2>&1 || true
echo "  ✓ Attraction results saved."

echo ""
echo "=== All searches complete ==="
echo "Result files:"
ls -la "$OUTPUT_DIR"/*.json 2>/dev/null
echo ""
echo "AI agent: read these JSON files to assemble the itinerary using assets/itinerary-template.md"
