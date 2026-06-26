#!/usr/bin/env bash
set -euo pipefail

# Email Sequence Creator
# Creates automated email sequences via ConvertKit or Mailchimp

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/convertkit-api.sh" 2>/dev/null || true

# Defaults
PLATFORM="convertkit"
SEQUENCE_TYPE=""
PRODUCT_NAME=""
EMAIL_COUNT=3
DELAY_DAYS="0,3,7"
LAUNCH_DATE=""
OUTPUT_FILE=""

usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Create an automated email sequence.

OPTIONS:
  --type TYPE           Sequence type: welcome, launch, nurture
  --product NAME        Product name
  --emails COUNT        Number of emails (default: 3)
  --delay-days DAYS     Comma-separated day delays (default: 0,3,7)
  --launch-date DATE    Launch date for launch sequences (YYYY-MM-DD)
  --platform PLATFORM   convertkit or mailchimp (default: convertkit)
  --output FILE         Output JSON file path
  --help                Show this help

EXAMPLES:
  # Welcome sequence
  $0 --type welcome --product "AI Tax Optimizer" --emails 3

  # Launch sequence
  $0 --type launch --product "AI Tax Optimizer" \\
     --launch-date "2026-04-01" --emails 5

  # Nurture sequence
  $0 --type nurture --product "Einstein Research" --emails 7
EOF
  exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --type) SEQUENCE_TYPE="$2"; shift 2 ;;
    --product) PRODUCT_NAME="$2"; shift 2 ;;
    --emails) EMAIL_COUNT="$2"; shift 2 ;;
    --delay-days) DELAY_DAYS="$2"; shift 2 ;;
    --launch-date) LAUNCH_DATE="$2"; shift 2 ;;
    --platform) PLATFORM="$2"; shift 2 ;;
    --output) OUTPUT_FILE="$2"; shift 2 ;;
    --help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# Validate required args
if [[ -z "$SEQUENCE_TYPE" ]] || [[ -z "$PRODUCT_NAME" ]]; then
  echo "Error: --type and --product are required"
  usage
fi

# Validate sequence type
if [[ ! "$SEQUENCE_TYPE" =~ ^(welcome|launch|nurture)$ ]]; then
  echo "Error: --type must be one of: welcome, launch, nurture"
  exit 1
fi

# Convert delay days to array
IFS=',' read -ra DELAYS <<< "$DELAY_DAYS"

# Generate sequence name
SEQUENCE_TYPE_CAPITALIZED="$(echo "${SEQUENCE_TYPE}" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')"
SEQUENCE_NAME="${PRODUCT_NAME} - ${SEQUENCE_TYPE_CAPITALIZED} Sequence"

# Output file default
if [[ -z "$OUTPUT_FILE" ]]; then
  SAFE_NAME=$(echo "$PRODUCT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  OUTPUT_FILE="$SCRIPT_DIR/sequences/${SAFE_NAME}-${SEQUENCE_TYPE}.json"
fi

# Create sequences directory
mkdir -p "$SCRIPT_DIR/sequences"

# Build email list
EMAILS=()
for i in $(seq 1 "$EMAIL_COUNT"); do
  DELAY_DAYS_VAL="${DELAYS[$((i-1))]:-0}"
  
  # Select template based on type and email number
  TEMPLATE="$SCRIPT_DIR/templates/${SEQUENCE_TYPE}-email-${i}.md"
  
  # Fallback to generic if specific doesn't exist
  if [[ ! -f "$TEMPLATE" ]]; then
    TEMPLATE="$SCRIPT_DIR/templates/${SEQUENCE_TYPE}-email-generic.md"
  fi
  
  # Build email object
  EMAIL_JSON=$(cat <<EOF
{
  "emailNumber": $i,
  "delayDays": $DELAY_DAYS_VAL,
  "template": "$TEMPLATE",
  "subject": "Email $i subject (to be filled from template)",
  "status": "draft"
}
EOF
)
  EMAILS+=("$EMAIL_JSON")
done

# Build sequence JSON
SEQUENCE_JSON=$(cat <<EOF
{
  "sequenceName": "$SEQUENCE_NAME",
  "type": "$SEQUENCE_TYPE",
  "product": "$PRODUCT_NAME",
  "platform": "$PLATFORM",
  "status": "draft",
  "createdAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "emails": [
    $(IFS=,; echo "${EMAILS[*]}")
  ],
  "metadata": {
    "emailCount": $EMAIL_COUNT,
    "launchDate": "${LAUNCH_DATE:-null}"
  }
}
EOF
)

# Write to file
echo "$SEQUENCE_JSON" | jq '.' > "$OUTPUT_FILE"

echo "✓ Sequence created: $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "  1. Fill in email content using templates"
echo "  2. Review with Editorial QA"
echo "  3. Deploy with: ./deploy-sequence.sh --sequence $OUTPUT_FILE"
