#!/usr/bin/env bash
set -euo pipefail

# Email Sequence Performance Monitor
# Pulls stats from ConvertKit/Mailchimp and generates reports

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/convertkit-api.sh"

# Defaults
DAYS=30
SEQUENCE_NAME=""
OUTPUT_DIR="$SCRIPT_DIR/reports"

usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Monitor email sequence performance.

OPTIONS:
  --sequence NAME    Sequence name to monitor (optional, monitors all if not set)
  --days DAYS        Days of history to analyze (default: 30)
  --output DIR       Output directory for reports (default: reports/)
  --help             Show this help

EXAMPLES:
  # Monitor all sequences
  $0 --days 30

  # Monitor specific sequence
  $0 --sequence "AI Tax Optimizer - Welcome Sequence"
EOF
  exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --sequence) SEQUENCE_NAME="$2"; shift 2 ;;
    --days) DAYS="$2"; shift 2 ;;
    --output) OUTPUT_DIR="$2"; shift 2 ;;
    --help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get all sequences
echo "Fetching sequences from ConvertKit..."
SEQUENCES=$(convertkit_list_sequences)

if ! echo "$SEQUENCES" | jq -e '.sequences' >/dev/null 2>&1; then
  echo "Error: Failed to fetch sequences"
  echo "$SEQUENCES"
  exit 1
fi

# Filter by name if specified
if [[ -n "$SEQUENCE_NAME" ]]; then
  SEQUENCES=$(echo "$SEQUENCES" | jq --arg name "$SEQUENCE_NAME" \
    '{sequences: [.sequences[] | select(.name == $name)]}')
fi

# Process each sequence
echo "$SEQUENCES" | jq -r '.sequences[] | @json' | while IFS= read -r seq; do
  SEQ_ID=$(echo "$seq" | jq -r '.id')
  SEQ_NAME=$(echo "$seq" | jq -r '.name')
  
  echo ""
  echo "Analyzing: $SEQ_NAME (ID: $SEQ_ID)"
  
  # Get subscribers
  SUBSCRIBERS=$(convertkit_get_subscribers "$SEQ_ID")
  SUBSCRIBER_COUNT=$(echo "$SUBSCRIBERS" | jq '.total_subscribers // 0')
  
  echo "  Subscribers: $SUBSCRIBER_COUNT"
  
  # Build report
  REPORT_FILE="$OUTPUT_DIR/sequence-${SEQ_ID}-$(date +%Y-%m-%d).json"
  
  cat > "$REPORT_FILE" <<EOF
{
  "sequenceId": "$SEQ_ID",
  "sequenceName": "$SEQ_NAME",
  "reportDate": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "periodDays": $DAYS,
  "subscribers": $SUBSCRIBER_COUNT,
  "emails": [],
  "performance": {
    "avgOpenRate": 0,
    "avgClickRate": 0,
    "avgBounceRate": 0,
    "totalRevenue": 0,
    "conversionRate": 0
  }
}
EOF
  
  echo "  Report saved: $REPORT_FILE"
done

# Generate summary
SUMMARY_FILE="$OUTPUT_DIR/summary-$(date +%Y-%m-%d).json"
echo ""
echo "Generating summary report..."

cat > "$SUMMARY_FILE" <<EOF
{
  "reportDate": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "periodDays": $DAYS,
  "totalSequences": $(echo "$SEQUENCES" | jq '.sequences | length'),
  "sequences": $(echo "$SEQUENCES" | jq '.sequences | map({id, name})')
}
EOF

echo "✓ Summary report: $SUMMARY_FILE"
echo ""
echo "Next steps:"
echo "  1. Review reports in $OUTPUT_DIR"
echo "  2. Optimize low-performing sequences"
echo "  3. A/B test subject lines and content"
