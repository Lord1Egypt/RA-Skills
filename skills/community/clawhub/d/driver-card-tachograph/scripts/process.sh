#!/bin/bash
#
# driver-card-tachograph Workflow
# Takes .ddd file from inbox/, parses, imports, archives
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BIN_DIR="$PROJECT_DIR/bin"
DATA_DIR="$PROJECT_DIR/data"

INBOX="$DATA_DIR/inbox"
PARSED="$DATA_DIR/parsed"
JSON_QUEUE="$DATA_DIR/json"
ARCHIVE="$DATA_DIR/archive"

LOG_FILE="$PROJECT_DIR/process.log"
SUMMARY_DIR="$PROJECT_DIR/summaries"
SUMMARY_FILE="$SUMMARY_DIR/processing-summary-$(date +%Y%m%d-%H%M%S).json"
HEALTH_REPORT="$SUMMARY_DIR/health-report-$(date +%Y%m%d-%H%M%S).json"

# Create summaries directory
mkdir -p "$SUMMARY_DIR"

# Logging function with level
log() {
    local level="$1"
    shift
    local msg="$*"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_step() { log "STEP" "$@"; }

# Counter variables for summary
PARSER_WARNINGS=0
PARSER_CHR_MISMATCH=0
PARSER_CERT_ERRORS=0
PARSER_ASN1_ERRORS=0
IMPORT_STATUS="pending"

# Colors for output (if terminal)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Batch processing: Process all .ddd files in inbox
BATCH_MODE=false
PROCESSED_COUNT=0
FAILED_COUNT=0
TOTAL_COUNT=0

# Check for single file input
if [ $# -gt 0 ]; then
    INPUT_FILE="$1"
    if [ ! -f "$INPUT_FILE" ]; then
        log_error "Input file does not exist: $INPUT_FILE"
        echo -e "${RED}✗ File not found: $INPUT_FILE${NC}"
        exit 1
    fi
    FILES_TO_PROCESS="$INPUT_FILE"
    TOTAL_COUNT=1
else
    # Find ALL .ddd files in inbox (case-insensitive)
    FILES_TO_PROCESS=$(find "$INBOX" -maxdepth 1 -type f \( -iname "*.ddd" -o -iname "*.DDD" \) 2>/dev/null)
    TOTAL_COUNT=$(echo "$FILES_TO_PROCESS" | grep -c . 2>/dev/null || echo "0")
    
    if [ "$TOTAL_COUNT" -eq 0 ]; then
        log_error "No .ddd files found in inbox/"
        echo -e "${RED}✗ No input files found${NC}"
        exit 1
    fi
    
    if [ "$TOTAL_COUNT" -gt 1 ]; then
        BATCH_MODE=true
        log_info "Batch mode: $TOTAL_COUNT files to process"
        echo "Batch processing: $TOTAL_COUNT files"
    fi
fi

# Function to process a single file
process_single_file() {
    local INPUT_FILE="$1"
    
    if [ ! -f "$INPUT_FILE" ]; then
        log_error "File does not exist: $INPUT_FILE"
        return 1
    fi
    
    # Input validation
    local INPUT_SIZE=$(stat -c%s "$INPUT_FILE" 2>/dev/null || stat -f%z "$INPUT_FILE" 2>/dev/null)
    if [ "$INPUT_SIZE" -lt 1024 ]; then
        log_error "File too small (<1KB): $INPUT_FILE ($INPUT_SIZE bytes)"
        return 1
    fi
    
    local BASENAME=$(basename "$INPUT_FILE" .ddd)
    log_info "=== Processing: $BASENAME ==="
    log_info "Input file size: $INPUT_SIZE bytes"

    # Step 1: Parse .ddd to JSON
    log_step "1/3 Parsing .ddd → JSON..."
    JSON_OUTPUT="$PARSED/$BASENAME.json"
    PARSE_LOG=$(mktemp)

    "$BIN_DIR/dddparser" -card -format -input "$INPUT_FILE" -output "$JSON_OUTPUT" >> "$PARSE_LOG" 2>&1
    PARSE_EXIT=$?

    PARSER_WARNINGS=$(grep -c -i "warn\|error" "$PARSE_LOG" 2>/dev/null || echo "0")
    PARSER_CHR_MISMATCH=$(grep -c -i "CHR mismatch" "$PARSE_LOG" 2>/dev/null || echo "0")
    PARSER_CERT_ERRORS=$(grep -c -i "certificate\|ca pk\|could not find" "$PARSE_LOG" 2>/dev/null || echo "0")
    PARSER_ASN1_ERRORS=$(grep -c -i "asn1\|decode\|sequence truncated" "$PARSE_LOG" 2>/dev/null || echo "0")
    cat "$PARSE_LOG" >> "$LOG_FILE"
    rm -f "$PARSE_LOG"

    if [ ! -f "$JSON_OUTPUT" ]; then
        log_error "Parsing failed - no JSON output created"
        echo -e "${RED}✗ No JSON output${NC}"
        return 1
    fi

    JSON_SIZE=$(stat -c%s "$JSON_OUTPUT" 2>/dev/null || stat -f%z "$JSON_OUTPUT" 2>/dev/null)

    if ! python3 -c "import json; json.load(open('$JSON_OUTPUT'))" 2>/dev/null; then
        log_error "JSON validation failed - output is not valid JSON"
        echo -e "${RED}✗ Invalid JSON output${NC}"
        return 1
    fi

    log_info "Parsed: $JSON_OUTPUT (${JSON_SIZE} bytes)"
    log_info "Parser warnings: $PARSER_WARNINGS total (CHR=$PARSER_CHR_MISMATCH, CERT=$PARSER_CERT_ERRORS, ASN1=$PARSER_ASN1_ERRORS)"
    echo -e "${GREEN}✓${NC} Parsed (${JSON_SIZE} bytes, $PARSER_WARNINGS warnings)"

    # Alerting bei kritischen ASN1-Errors (optional, konfigurierbar)
    if [ "$PARSER_ASN1_ERRORS" -gt 0 ]; then
        log_error "ALERT: ASN1 errors detected ($PARSER_ASN1_ERRORS) - data quality may be compromised"
        echo -e "${YELLOW}⚠ ALERT: ASN1 errors detected ($PARSER_ASN1_ERRORS)${NC}"
        # Optional: Mail-Alert senden (wenn MAIL_TO konfiguriert ist)
        if [ -n "${MAIL_TO:-}" ]; then
            echo "CRITICAL: ASN1 errors detected in tachograph processing of $BASENAME" | \
                mail -s "Tachograph Alert: ASN1 Errors" "$MAIL_TO" 2>/dev/null || true
            log_info "Alert email sent to $MAIL_TO"
        fi
    fi

    # Step 2: Import JSON to SQLite
    log_step "2/3 Importing JSON → SQLite..."
    IMPORT_STATUS="running"

    DB_PATH="$PROJECT_DIR/data/tachograph.db"
    IMPORT_OUTPUT=$(mktemp)
    if ! python3 "$SCRIPT_DIR/import.py" "$JSON_OUTPUT" > "$IMPORT_OUTPUT" 2>&1; then
        IMPORT_STATUS="failed"
        cat "$IMPORT_OUTPUT" >> "$LOG_FILE"
        log_error "Import failed"
        echo -e "${RED}✗ Import failed${NC}"
        rm -f "$IMPORT_OUTPUT"
        return 1
    fi
    IMPORT_STATUS="success"
    cat "$IMPORT_OUTPUT" >> "$LOG_FILE"
    rm -f "$IMPORT_OUTPUT"

    ROW_COUNT=$(python3 -c "import sqlite3; c=sqlite3.connect('$DB_PATH').cursor(); c.execute('SELECT COUNT(*) FROM driver_cards'); print(c.fetchone()[0])")
    DAILY_COUNT=$(python3 -c "import sqlite3; c=sqlite3.connect('$DB_PATH').cursor(); c.execute('SELECT COUNT(*) FROM daily_activities'); print(c.fetchone()[0])")
    log_info "Database now contains $ROW_COUNT driver cards, $DAILY_COUNT daily activities"
    echo -e "${GREEN}✓${NC} Imported ($ROW_COUNT cards, $DAILY_COUNT activities total)"

    # DB Health Check
    log_step "Health Check..."
    if python3 "$SCRIPT_DIR/health_check.py" >> "$LOG_FILE" 2>&1; then
        HEALTH_STATUS="healthy"
        log_info "DB Health Check: OK"
        if [ -f "$PROJECT_DIR/health-report.json" ]; then
            mv "$PROJECT_DIR/health-report.json" "$HEALTH_REPORT"
        fi
    else
        HEALTH_STATUS="unhealthy"
        log_warn "DB Health Check: FAILED"
        if [ -f "$PROJECT_DIR/health-report.json" ]; then
            mv "$PROJECT_DIR/health-report.json" "$HEALTH_REPORT"
        fi
    fi

    # Step 3: Archive original .ddd
    log_step "3/3 Archiving .ddd file..."
    ARCHIVE_NAME="$BASENAME-$(date +%Y%m%d-%H%M%S).ddd"
    mv "$INPUT_FILE" "$ARCHIVE/$ARCHIVE_NAME"
    log_info "Archived: $ARCHIVE/$ARCHIVE_NAME"
    echo -e "${GREEN}✓${NC} Archived"

    # Summary JSON
    cat > "$SUMMARY_FILE" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "input_file": "$INPUT_FILE",
  "input_size": $INPUT_SIZE,
  "basename": "$BASENAME",
  "parse_status": "success",
  "parse_warnings": {
    "total": $PARSER_WARNINGS,
    "chr_mismatch": $PARSER_CHR_MISMATCH,
    "certificate_errors": $PARSER_CERT_ERRORS,
    "asn1_errors": $PARSER_ASN1_ERRORS
  },
  "json_size": $JSON_SIZE,
  "import_status": "$IMPORT_STATUS",
  "driver_cards_total": $ROW_COUNT,
  "daily_activities_total": $DAILY_COUNT,
  "archive_file": "$ARCHIVE/$ARCHIVE_NAME",
  "health_status": "$HEALTH_STATUS",
  "health_report": "$HEALTH_REPORT"
}
EOF
    log_info "Summary written to $SUMMARY_FILE"

    log_info "=== Complete: $BASENAME ==="
    echo -e "${GREEN}✓ Processing complete: $BASENAME${NC}"
    return 0
}

# Single file mode
if [ "$BATCH_MODE" = false ]; then
    if process_single_file "$FILES_TO_PROCESS"; then
        PROCESSED_COUNT=1
    else
        FAILED_COUNT=1
    fi
else
    # Batch mode: process all files
    echo ""
    echo "========================================"
    echo "Batch Processing $TOTAL_COUNT files"
    echo "========================================"
    echo ""
    
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        ((PROCESSED_COUNT++)) || true
        echo ""
        echo "========================================"
        echo "File $PROCESSED_COUNT of $TOTAL_COUNT"
        echo "========================================"
        
        if process_single_file "$file"; then
            ((FAILED_COUNT++)) || true
        fi
    done <<< "$FILES_TO_PROCESS"
    
    echo ""
    echo "========================================"
    echo "Batch Processing Complete"
    echo "========================================"
    echo "Total files: $TOTAL_COUNT"
    echo "Processed: $PROCESSED_COUNT"
    echo "Failed: $((TOTAL_COUNT - PROCESSED_COUNT))"
    echo "========================================"
fi

# Exit with error if any failed
if [ "$FAILED_COUNT" -gt 0 ] || [ "$PROCESSED_COUNT" -eq 0 ]; then
    exit 1
fi
exit 0