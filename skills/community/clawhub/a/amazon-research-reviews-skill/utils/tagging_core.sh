#!/bin/bash

# Tagging Core Module for Review Analyzer
# Handles single and batch review tagging using Claude AI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$(dirname "$SCRIPT_DIR")/prompts"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Progress tracking
declare -a TAGGING_RESULTS=()
TAGGING_SUCCESS=0
TAGGING_FAILED=0

# Function to print progress
progress() {
    echo -e "${BLUE}[PROGRESS]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to format a review for tagging
format_review() {
    local review_json="$1"

    # Extract fields using jq if available, else use grep/sed
    if command -v jq &> /dev/null; then
        echo "$review_json" | jq -r '"[\(.review_id // "unknown")] \(.title // "No title") - \(.body // "")"'
    else
        echo "$review_json"
    fi
}

# Function to create single tagging prompt
create_single_prompt() {
    local review_json="$1"
    local prompt_template="$PROMPTS_DIR/tagging.txt"

    if [[ ! -f "$prompt_template" ]]; then
        error "Prompt template not found: $prompt_template"
        return 1
    fi

    # Extract review data
    local review_id=$(echo "$review_json" | grep -o '"review_id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: "\(.*\)".*/\1/')
    local title=$(echo "$review_json" | grep -o '"title"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: "\(.*\)".*/\1/' | head -1)
    local body=$(echo "$review_json" | grep -o '"body"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: "\(.*\)".*/\1/' | head -1)
    local rating=$(echo "$review_json" | grep -o '"rating"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: "\(.*\)".*/\1/' | head -1)

    # Set defaults
    review_id=${review_id:-"unknown"}
    title=${title:-""}
    body=${body:-""}
    rating=${rating:-"3"}

    # Read and format prompt
    local prompt=$(cat "$prompt_template")
    prompt="${prompt//{review_id}/$review_id}"
    prompt="${prompt//{title}/$title}"
    prompt="${prompt//{body}/$body}"
    prompt="${prompt//{rating}/$rating}"

    echo "$prompt"
}

# Function to create batch tagging prompt
create_batch_prompt() {
    local reviews_json="$1"
    local prompt_template="$PROMPTS_DIR/tagging_batch.txt"
    local batch_size=$(echo "$reviews_json" | jq '. | length' 2>/dev/null || echo "1")

    if [[ ! -f "$prompt_template" ]]; then
        error "Prompt template not found: $prompt_template"
        return 1
    fi

    # Read and format prompt
    local prompt=$(cat "$prompt_template")
    prompt="${prompt//{batch_size}/$batch_size}"
    prompt="${prompt//{reviews_json}/$reviews_json}"

    echo "$prompt"
}

# Function to parse tagging result
parse_tagging_result() {
    local result="$1"
    local review_id="$2"

    # Extract JSON from result (handles markdown code blocks)
    local json_data=$(echo "$result" | sed -n '/```json/,/```/p' | sed '1d;$d' || echo "$result")

    # Validate JSON structure
    if command -v jq &> /dev/null; then
        if ! echo "$json_data" | jq '.' > /dev/null 2>&1; then
            error "Invalid JSON result for review: $review_id"
            return 1
        fi

        # Ensure required fields exist
        local has_review_id=$(echo "$json_data" | jq 'has("review_id")')
        local has_tags=$(echo "$json_data" | jq 'has("tags")')

        if [[ "$has_review_id" != "true" ]] || [[ "$has_tags" != "true" ]]; then
            error "Missing required fields in result for: $review_id"
            return 1
        fi
    fi

    echo "$json_data"
    return 0
}

# Function to tag a single review
tag_single_review() {
    local review_json="$1"

    progress "Tagging review: $(format_review "$review_json")"

    # Create prompt
    local prompt=$(create_single_prompt "$review_json")
    if [[ $? -ne 0 ]]; then
        ((TAGGING_FAILED++))
        return 1
    fi

    # The actual AI call will be done by the main skill
    # This function prepares the prompt and returns it
    echo "$prompt"
}

# Function to tag a batch of reviews
tag_batch_reviews() {
    local reviews_json="$1"
    local batch_size=$(echo "$reviews_json" | jq '. | length' 2>/dev/null || echo "1")

    progress "Tagging batch of $batch_size reviews..."

    # Create prompt
    local prompt=$(create_batch_prompt "$reviews_json")
    if [[ $? -ne 0 ]]; then
        return 1
    fi

    # The actual AI call will be done by the main skill
    echo "$prompt"
}

# Function to split reviews into batches
split_into_batches() {
    local reviews_json="$1"
    local batch_size="${2:-30}"
    local total=$(echo "$reviews_json" | jq '. | length' 2>/dev/null || echo "0")

    if [[ "$total" -le "$batch_size" ]]; then
        echo "$reviews_json"
        return 0
    fi

    # Split into batches
    for ((i=0; i<total; i+=batch_size)); do
        local end=$((i + batch_size - 1))
        if [[ $end -ge $total ]]; then
            end=$((total - 1))
        fi
        echo "$reviews_json" | jq ".[$i:$end]"
    done
}

# Function to merge tagging results
merge_results() {
    local all_results="["

    local first=true
    for result in "${TAGGING_RESULTS[@]}"; do
        if [[ "$first" == "true" ]]; then
            all_results="$all_results$result"
            first=false
        else
            all_results="$all_results,$result"
        fi
    done

    all_results="$all_results]"

    echo "$all_results"
}

# Function to save results to CSV
save_to_csv() {
    local results_json="$1"
    local original_csv="$2"
    local output_csv="$3"

    if ! command -v python3 &> /dev/null; then
        error "Python3 required for CSV output"
        return 1
    fi

    python3 -c "
import csv
import json
import sys

# Load tagging results
with open('$results_json', 'r', encoding='utf-8') as f:
    tagged = json.load(f)

# Create lookup
tagged_lookup = {item['review_id']: item for item in tagged}

# Read original CSV and append tags
with open('$original_csv', 'r', encoding='utf-8', errors='ignore') as infile, \\
     open('$output_csv', 'w', encoding='utf-8', newline='', errors='ignore') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['情感_总体评价', '评论价值打分', '打标时间']

    # Add all tag columns
    all_tags = set()
    for item in tagged:
        for tag_key in item.get('tags', {}).keys():
            all_tags.add(tag_key)
    fieldnames.extend(sorted(all_tags))

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Find review ID
        rid = row.get('review_id') or row.get('id') or row.get('Id') or ''
        tagged_item = tagged_lookup.get(rid)

        if tagged_item:
            row['情感_总体评价'] = tagged_item.get('sentiment', '')
            row['评论价值打分'] = tagged_item.get('info_score', '')
            row['打标时间'] = tagged_item.get('timestamp', '')

            # Add all tags
            for tag_key in all_tags:
                tag_value = tagged_item.get('tags', {}).get(tag_key, '未提及')
                row[tag_key] = tag_value

        writer.writerow(row)

print(f'Saved {len(tagged)} tagged reviews to {output_csv}')
"
}

# Main function
main() {
    local action="$1"
    shift

    case "$action" in
        "single")
            tag_single_review "$@"
            ;;
        "batch")
            tag_batch_reviews "$@"
            ;;
        "split")
            split_into_batches "$@"
            ;;
        "merge")
            merge_results
            ;;
        "csv")
            save_to_csv "$@"
            ;;
        *)
            echo "Usage: $0 {single|batch|split|merge|csv} ..."
            exit 1
            ;;
    esac
}

main "$@"
