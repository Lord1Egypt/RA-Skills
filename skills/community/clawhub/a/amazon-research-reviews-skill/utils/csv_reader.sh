#!/bin/bash

# CSV Reader Utility for Review Analyzer
# Supports fuzzy column matching, multiple encodings, and proper CSV parsing

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print error message
error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Function to print success message
success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Function to print info message
info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Function to detect file encoding
detect_encoding() {
    local file="$1"

    # Try to detect encoding using file command
    if command -v file &> /dev/null; then
        local encoding=$(file -b --mime-encoding "$file" 2>/dev/null)
        echo "$encoding"
        return 0
    fi

    # Fallback: try common encodings
    for enc in utf-8 gbk gb2312 latin-1; do
        if iconv -f "$enc" -t utf-8 "$file" > /dev/null 2>&1; then
            echo "$enc"
            return 0
        fi
    done

    echo "unknown"
}

# Function to convert file to UTF-8
convert_to_utf8() {
    local file="$1"
    local output="$2"
    local encoding=$(detect_encoding "$file")

    info "Detected encoding: $encoding"

    if [[ "$encoding" == *"utf-8"* ]] || [[ "$encoding" == *"utf8"* ]]; then
        cp "$file" "$output"
        return 0
    fi

    # Try to convert to UTF-8
    if iconv -f "$encoding" -t utf-8 "$file" -o "$output" 2>/dev/null; then
        success "Converted to UTF-8"
        return 0
    else
        # Try common encodings as fallback
        for enc in gbk gb2312 latin-1 iso-8859-1; do
            if iconv -f "$enc" -t utf-8 "$file" -o "$output" 2>/dev/null; then
                success "Converted using fallback encoding: $enc"
                return 0
            fi
        done
    fi

    error "Failed to convert file to UTF-8"
    return 1
}

# Function to detect delimiter
detect_delimiter() {
    local file="$1"
    local first_line=$(head -n 1 "$file")

    # Count delimiters in first line
    local comma_count=$(echo "$first_line" | grep -o ',' | wc -l)
    local semicolon_count=$(echo "$first_line" | grep -o ';' | wc -l)
    local tab_count=$(echo "$first_line" | grep -o $'\t' | wc -l)
    local pipe_count=$(echo "$first_line" | grep -o '|' | wc -l)

    # Return delimiter with most occurrences
    if (( pipe_count > comma_count )) && (( pipe_count > semicolon_count )) && (( pipe_count > tab_count )); then
        echo "|"
    elif (( tab_count > comma_count )) && (( tab_count > semicolon_count )); then
        echo $'\t'
    elif (( semicolon_count > comma_count )); then
        echo ";"
    else
        echo ","
    fi
}

# Function to find column index by fuzzy matching
find_column() {
    local headers="$1"
    local column_name="$2"

    # Convert to lowercase for comparison
    local lower_headers=$(echo "$headers" | tr '[:upper:]' '[:lower:]')
    local lower_name=$(echo "$column_name" | tr '[:upper:]' '[:lower:]')

    # Array of possible column names
    local names=($lower_name)

    # Add synonyms based on column type
    case "$lower_name" in
        "body"|"content"|"review")
            names+=("body" "content" "review" "text" "comment" "内容" "评价" "评论")
            ;;
        "rating"|"score"|"star")
            names+=("rating" "score" "stars" "star" "打分" "评分" "rating_score")
            ;;
        "date"|"time")
            names+=("date" "time" "timestamp" "created_at" "时间" "日期")
            ;;
        "title"|"summary")
            names+=("title" "summary" "subject" "标题")
            ;;
        "user"|"author"|"name")
            names+=("user" "username" "author" "reviewer_name" "用户")
            ;;
        "id")
            names+=("id" "review_id" "reviewid")
            ;;
    esac

    # Try to find matching column
    local index=1
    while IFS= read -r header; do
        local lower_header=$(echo "$header" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')
        for name in "${names[@]}"; do
            local clean_name=$(echo "$name" | tr -d '[:space:]')
            if [[ "$lower_header" == *"$clean_name"* ]]; then
                echo $index
                return 0
            fi
        done
        ((index++))
    done <<< "$headers"

    # Not found
    echo "0"
}

# Function to get column value
get_column() {
    local line="$1"
    local col_index="$2"
    local delimiter="$3"

    if [[ "$col_index" -eq 0 ]]; then
        echo ""
        return
    fi

    # Use awk to properly handle CSV quoted fields
    awk -v idx="$col_index" -F"$delimiter" '{
        # Handle quoted fields
        for(i=1; i<=NF; i++) {
            # Remove leading/trailing quotes
            gsub(/^"|"$/, "", $i)
            # Unescape quotes
            gsub(/""/, "\"", $i)
            if(i == idx) {
                print $i
                exit
            }
        }
    }' <<< "$line"
}

# Function to count actual records (not lines, as CSV may have multi-line records)
count_records() {
    local file="$1"
    local delimiter="$2"

    # Use Python if available for accurate CSV parsing
    if command -v python3 &> /dev/null; then
        python3 -c "
import csv
import sys
try:
    with open('$file', 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter='$delimiter')
        count = sum(1 for row in reader)
        print(count - 1)  # Exclude header
except:
    print(0)
" 2>/dev/null
    else
        # Fallback: subtract 1 for header, but this may be inaccurate
        local lines=$(wc -l < "$file")
        echo $((lines - 1))
    fi
}

# Function to extract reviews in JSON format
extract_reviews() {
    local file="$1"
    local delimiter="$2"
    local max_records="${3:-0}"

    # Use Python for accurate CSV parsing if available
    if command -v python3 &> /dev/null; then
        python3 -c "
import csv
import json
import sys

max_records = $max_records

with open('$file', 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f, delimiter='$delimiter')

    # Get headers
    headers = reader.fieldnames
    if not headers:
        sys.exit(1)

    # Find column indices
    body_col = None
    rating_col = None
    title_col = None
    id_col = None
    date_col = None

    for h in headers:
        hl = h.lower().strip()
        if hl in ['body', 'content', 'review', 'text', 'comment', '内容', '评价', '评论']:
            body_col = h
        elif hl in ['rating', 'score', 'stars', 'star', '打分', '评分']:
            rating_col = h
        elif hl in ['title', 'summary', 'subject', '标题']:
            title_col = h
        elif hl in ['id', 'review_id', 'reviewid']:
            id_col = h
        elif hl in ['date', 'time', 'timestamp', 'created_at', '时间', '日期']:
            date_col = h

    # Extract reviews
    reviews = []
    for i, row in enumerate(reader):
        if max_records > 0 and i >= max_records:
            break

        body = row.get(body_col, '').strip() if body_col else ''
        if not body:
            continue

        review = {
            'review_id': row.get(id_col, f'r{i+1}') if id_col else f'r{i+1}',
            'title': row.get(title_col, '').strip() if title_col else '',
            'body': body,
            'rating': row.get(rating_col, '3').strip() if rating_col else '3'
        }

        reviews.append(review)

    print(json.dumps(reviews, ensure_ascii=False, indent=2))
" 2>/dev/null
    else
        error "Python3 not found. Cannot parse CSV accurately."
        return 1
    fi
}

# Main function
main() {
    local file="$1"
    local action="${2:-info}"
    local max_records="${3:-0}"

    if [[ ! -f "$file" ]]; then
        error "File not found: $file"
        exit 1
    fi

    # Create temp file for UTF-8 conversion
    local temp_file=$(mktemp)
    trap "rm -f $temp_file" EXIT

    # Convert to UTF-8
    if ! convert_to_utf8 "$file" "$temp_file"; then
        exit 1
    fi

    # Detect delimiter
    local delimiter=$(detect_delimiter "$temp_file")
    info "Detected delimiter: '${delimiter}'"

    # Get headers
    local headers=$(head -n 1 "$temp_file")
    info "Headers: $headers"

    # Perform action
    case "$action" in
        "count")
            local count=$(count_records "$temp_file" "$delimiter")
            echo "$count"
            ;;
        "extract")
            extract_reviews "$temp_file" "$delimiter" "$max_records"
            ;;
        "info")
            local count=$(count_records "$temp_file" "$delimiter")
            info "Total records: $count"

            # Find key columns
            local body_idx=$(find_column "$headers" "body")
            local rating_idx=$(find_column "$headers" "rating")
            local title_idx=$(find_column "$headers" "title")

            info "Body column index: $body_idx"
            info "Rating column index: $rating_idx"
            info "Title column index: $title_idx"
            ;;
        *)
            error "Unknown action: $action"
            echo "Usage: $0 <file> <action> [max_records]"
            echo "Actions: info, count, extract"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
