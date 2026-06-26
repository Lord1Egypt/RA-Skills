#!/usr/bin/env bash
# ==============================================================================
# FeatureLint - Feature Flag Hygiene Analyzer
# Core Analysis Engine
# ==============================================================================
set -euo pipefail

FEATURELINT_VERSION="1.0.0"
FEATURELINT_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source pattern definitions
# shellcheck source=patterns.sh
source "${FEATURELINT_SCRIPT_DIR}/patterns.sh"

# ==============================================================================
# Color and formatting constants
# ==============================================================================
FEATURELINT_COLOR_RED='\033[0;31m'
FEATURELINT_COLOR_YELLOW='\033[0;33m'
FEATURELINT_COLOR_GREEN='\033[0;32m'
FEATURELINT_COLOR_BLUE='\033[0;34m'
FEATURELINT_COLOR_MAGENTA='\033[0;35m'
FEATURELINT_COLOR_CYAN='\033[0;36m'
FEATURELINT_COLOR_GRAY='\033[0;90m'
FEATURELINT_COLOR_BOLD='\033[1m'
FEATURELINT_COLOR_RESET='\033[0m'
FEATURELINT_ACCENT='#e84393'

# ==============================================================================
# Default configuration
# ==============================================================================
FEATURELINT_TARGET_DIR="."
FEATURELINT_OUTPUT_FORMAT="text"
FEATURELINT_REPORT_FILE=""
FEATURELINT_SEVERITY_FILTER="all"
FEATURELINT_CATEGORY_FILTER="all"
FEATURELINT_INCLUDE_PATTERN=""
FEATURELINT_EXCLUDE_PATTERN=""
FEATURELINT_MAX_FILE_SIZE=1048576
FEATURELINT_PARALLEL_JOBS=4
FEATURELINT_VERBOSE=0
FEATURELINT_QUIET=0
FEATURELINT_EXIT_CODE_ON_ERROR=1
FEATURELINT_EXIT_CODE_ON_WARNING=0
FEATURELINT_TIER="free"
FEATURELINT_SCAN_HIDDEN=0
FEATURELINT_CONTEXT_LINES=2
FEATURELINT_TEMPLATE_DIR="${FEATURELINT_SCRIPT_DIR}/../templates"

# ==============================================================================
# Counters and state
# ==============================================================================
FEATURELINT_TOTAL_FILES=0
FEATURELINT_SCANNED_FILES=0
FEATURELINT_SKIPPED_FILES=0
FEATURELINT_TOTAL_FINDINGS=0
FEATURELINT_ERROR_COUNT=0
FEATURELINT_WARNING_COUNT=0
FEATURELINT_INFO_COUNT=0
FEATURELINT_START_TIME=0
FEATURELINT_TEMP_DIR=""

# ==============================================================================
# File extension mapping for supported languages
# ==============================================================================
FEATURELINT_FILE_EXTENSIONS=(
    "js" "jsx" "ts" "tsx" "mjs" "cjs"
    "py" "pyw"
    "rb" "rake"
    "java" "kt" "kts" "scala"
    "go"
    "rs"
    "cs" "fs"
    "php"
    "swift"
    "dart"
    "vue" "svelte"
    "ex" "exs"
    "clj" "cljs"
    "lua"
    "r" "R"
    "yaml" "yml"
    "json" "jsonc"
    "toml"
    "xml"
    "tf" "hcl"
    "sh" "bash" "zsh"
)

# ==============================================================================
# Logging utilities
# ==============================================================================
featurelint_log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

    case "$level" in
        ERROR)
            echo -e "${FEATURELINT_COLOR_RED}[${timestamp}] ERROR: ${message}${FEATURELINT_COLOR_RESET}" >&2
            ;;
        WARN)
            if [[ "$FEATURELINT_QUIET" -eq 0 ]]; then
                echo -e "${FEATURELINT_COLOR_YELLOW}[${timestamp}] WARN: ${message}${FEATURELINT_COLOR_RESET}" >&2
            fi
            ;;
        INFO)
            if [[ "$FEATURELINT_QUIET" -eq 0 ]]; then
                echo -e "${FEATURELINT_COLOR_CYAN}[${timestamp}] INFO: ${message}${FEATURELINT_COLOR_RESET}" >&2
            fi
            ;;
        DEBUG)
            if [[ "$FEATURELINT_VERBOSE" -ge 1 ]]; then
                echo -e "${FEATURELINT_COLOR_GRAY}[${timestamp}] DEBUG: ${message}${FEATURELINT_COLOR_RESET}" >&2
            fi
            ;;
        TRACE)
            if [[ "$FEATURELINT_VERBOSE" -ge 2 ]]; then
                echo -e "${FEATURELINT_COLOR_GRAY}[${timestamp}] TRACE: ${message}${FEATURELINT_COLOR_RESET}" >&2
            fi
            ;;
    esac
}

# ==============================================================================
# Initialization and cleanup
# ==============================================================================
featurelint_init() {
    FEATURELINT_START_TIME=$(date +%s)
    FEATURELINT_TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/featurelint.XXXXXX")"
    FEATURELINT_TOTAL_FILES=0
    FEATURELINT_SCANNED_FILES=0
    FEATURELINT_SKIPPED_FILES=0
    FEATURELINT_TOTAL_FINDINGS=0
    FEATURELINT_ERROR_COUNT=0
    FEATURELINT_WARNING_COUNT=0
    FEATURELINT_INFO_COUNT=0

    # Create temp subdirectories
    mkdir -p "${FEATURELINT_TEMP_DIR}/findings"
    mkdir -p "${FEATURELINT_TEMP_DIR}/work"

    featurelint_log DEBUG "Initialized temp directory: ${FEATURELINT_TEMP_DIR}"
    featurelint_log DEBUG "FeatureLint v${FEATURELINT_VERSION} starting analysis"
    featurelint_log DEBUG "Tier: ${FEATURELINT_TIER}"
    featurelint_log DEBUG "Target: ${FEATURELINT_TARGET_DIR}"
}

featurelint_cleanup() {
    if [[ -n "${FEATURELINT_TEMP_DIR}" && -d "${FEATURELINT_TEMP_DIR}" ]]; then
        rm -rf "${FEATURELINT_TEMP_DIR}"
        featurelint_log DEBUG "Cleaned up temp directory"
    fi
}

trap featurelint_cleanup EXIT

# ==============================================================================
# File discovery
# ==============================================================================
featurelint_build_extension_filter() {
    local filter=""
    for ext in "${FEATURELINT_FILE_EXTENSIONS[@]}"; do
        if [[ -n "$filter" ]]; then
            filter="${filter}|"
        fi
        filter="${filter}\.${ext}$"
    done
    echo "$filter"
}

featurelint_discover_files() {
    local target_dir="$1"
    local file_list="${FEATURELINT_TEMP_DIR}/file_list.txt"
    local ext_filter
    ext_filter="$(featurelint_build_extension_filter)"

    featurelint_log INFO "Discovering files in: ${target_dir}"

    local find_args=()
    find_args+=("${target_dir}")

    # Exclude hidden directories unless configured
    if [[ "$FEATURELINT_SCAN_HIDDEN" -eq 0 ]]; then
        find_args+=(-not -path '*/\.*')
    fi

    # Common excluded directories
    find_args+=(-not -path '*/node_modules/*')
    find_args+=(-not -path '*/vendor/*')
    find_args+=(-not -path '*/.git/*')
    find_args+=(-not -path '*/dist/*')
    find_args+=(-not -path '*/build/*')
    find_args+=(-not -path '*/coverage/*')
    find_args+=(-not -path '*/__pycache__/*')
    find_args+=(-not -path '*/.next/*')
    find_args+=(-not -path '*/.nuxt/*')
    find_args+=(-not -path '*/target/*')
    find_args+=(-not -path '*/bin/*')
    find_args+=(-not -path '*/obj/*')
    find_args+=(-not -path '*/.venv/*')
    find_args+=(-not -path '*/venv/*')

    find_args+=(-type f)

    # Apply include pattern if set
    if [[ -n "${FEATURELINT_INCLUDE_PATTERN}" ]]; then
        find_args+=(-name "${FEATURELINT_INCLUDE_PATTERN}")
    fi

    # Execute find and filter by extension
    find "${find_args[@]}" 2>/dev/null | grep -E "${ext_filter}" | while read -r file; do
        # Check file size
        local file_size
        file_size=$(wc -c < "$file" 2>/dev/null || echo "0")
        if [[ "$file_size" -le "$FEATURELINT_MAX_FILE_SIZE" ]]; then
            # Apply exclude pattern
            if [[ -n "${FEATURELINT_EXCLUDE_PATTERN}" ]]; then
                if echo "$file" | grep -qE "${FEATURELINT_EXCLUDE_PATTERN}"; then
                    continue
                fi
            fi
            echo "$file"
        else
            featurelint_log DEBUG "Skipping large file (${file_size} bytes): ${file}"
            FEATURELINT_SKIPPED_FILES=$((FEATURELINT_SKIPPED_FILES + 1))
        fi
    done > "${file_list}"

    FEATURELINT_TOTAL_FILES=$(wc -l < "${file_list}" 2>/dev/null || echo "0")
    FEATURELINT_TOTAL_FILES="${FEATURELINT_TOTAL_FILES// /}"
    featurelint_log INFO "Discovered ${FEATURELINT_TOTAL_FILES} files to analyze"

    echo "${file_list}"
}

# ==============================================================================
# Pattern matching engine
# ==============================================================================
featurelint_parse_pattern() {
    local pattern_entry="$1"
    local field="$2"

    # The format is: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
    # The regex field may contain | characters, so we extract from the end.
    # The last 4 fields (severity, check_id, description, recommendation)
    # are guaranteed not to contain | characters.
    case "$field" in
        regex)
            # Everything except the last 4 pipe-delimited fields
            echo "$pattern_entry" | awk -F'|' '{
                n = NF;
                result = $1;
                for (i = 2; i <= n - 4; i++) result = result "|" $i;
                print result;
            }'
            ;;
        severity)       echo "$pattern_entry" | awk -F'|' '{print $(NF-3)}' ;;
        check_id)       echo "$pattern_entry" | awk -F'|' '{print $(NF-2)}' ;;
        description)    echo "$pattern_entry" | awk -F'|' '{print $(NF-1)}' ;;
        recommendation) echo "$pattern_entry" | awk -F'|' '{print $NF}' ;;
    esac
}

featurelint_severity_to_number() {
    local severity="$1"
    case "$severity" in
        error)   echo 3 ;;
        warning) echo 2 ;;
        info)    echo 1 ;;
        *)       echo 0 ;;
    esac
}

featurelint_severity_icon() {
    local severity="$1"
    case "$severity" in
        error)   echo -e "${FEATURELINT_COLOR_RED}[ERROR]${FEATURELINT_COLOR_RESET}" ;;
        warning) echo -e "${FEATURELINT_COLOR_YELLOW}[WARN]${FEATURELINT_COLOR_RESET}" ;;
        info)    echo -e "${FEATURELINT_COLOR_BLUE}[INFO]${FEATURELINT_COLOR_RESET}" ;;
        *)       echo "[???]" ;;
    esac
}

featurelint_should_check_severity() {
    local severity="$1"
    local filter="${FEATURELINT_SEVERITY_FILTER}"

    if [[ "$filter" == "all" ]]; then
        return 0
    fi

    local severity_num
    severity_num=$(featurelint_severity_to_number "$severity")
    local filter_num
    filter_num=$(featurelint_severity_to_number "$filter")

    [[ "$severity_num" -ge "$filter_num" ]]
}

featurelint_should_check_category() {
    local check_id="$1"
    local filter="${FEATURELINT_CATEGORY_FILTER}"

    if [[ "$filter" == "all" ]]; then
        return 0
    fi

    local category_prefix="${check_id%%-*}"
    echo "$filter" | grep -qi "$category_prefix"
}

featurelint_scan_file() {
    local file="$1"
    local findings_file="${FEATURELINT_TEMP_DIR}/findings/$(echo "$file" | tr '/' '_').findings"
    local file_findings=0

    featurelint_log TRACE "Scanning: ${file}"

    # Get active categories for current tier
    local categories
    categories="$(featurelint_get_tier_patterns "${FEATURELINT_TIER}")"

    for category in $categories; do
        local array_name
        array_name="$(featurelint_get_pattern_array "$category")"
        if [[ -z "$array_name" ]]; then
            continue
        fi

        local -n patterns_ref="$array_name"

        for pattern_entry in "${patterns_ref[@]}"; do
            local regex severity check_id description recommendation
            regex="$(featurelint_parse_pattern "$pattern_entry" "regex")"
            severity="$(featurelint_parse_pattern "$pattern_entry" "severity")"
            check_id="$(featurelint_parse_pattern "$pattern_entry" "check_id")"
            description="$(featurelint_parse_pattern "$pattern_entry" "description")"
            recommendation="$(featurelint_parse_pattern "$pattern_entry" "recommendation")"

            # Apply severity filter
            if ! featurelint_should_check_severity "$severity"; then
                continue
            fi

            # Apply category filter
            if ! featurelint_should_check_category "$check_id"; then
                continue
            fi

            # Search for pattern matches
            local line_matches
            line_matches=$(grep -nE "$regex" "$file" 2>/dev/null || true)

            if [[ -n "$line_matches" ]]; then
                while IFS= read -r match_line; do
                    local line_num="${match_line%%:*}"
                    local line_content="${match_line#*:}"
                    # Trim leading/trailing whitespace
                    line_content="$(echo "$line_content" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

                    # Write finding record
                    echo "${file}|${line_num}|${severity}|${check_id}|${description}|${recommendation}|${line_content}" >> "$findings_file"
                    file_findings=$((file_findings + 1))

                    # Update counters
                    case "$severity" in
                        error)   echo "error" >> "${FEATURELINT_TEMP_DIR}/work/errors.count" ;;
                        warning) echo "warning" >> "${FEATURELINT_TEMP_DIR}/work/warnings.count" ;;
                        info)    echo "info" >> "${FEATURELINT_TEMP_DIR}/work/infos.count" ;;
                    esac

                done <<< "$line_matches"
            fi
        done
    done

    if [[ "$file_findings" -gt 0 ]]; then
        featurelint_log DEBUG "Found ${file_findings} issues in: ${file}"
    fi

    return 0
}

# ==============================================================================
# Parallel scanning coordinator
# ==============================================================================
featurelint_scan_files_parallel() {
    local file_list="$1"
    local total
    total=$(wc -l < "$file_list" 2>/dev/null || echo "0")
    total="${total// /}"
    local scanned=0
    local batch_size="${FEATURELINT_PARALLEL_JOBS}"

    featurelint_log INFO "Starting parallel scan with ${batch_size} workers..."

    # Process files in batches
    local batch=()
    while IFS= read -r file; do
        batch+=("$file")

        if [[ "${#batch[@]}" -ge "$batch_size" ]]; then
            for f in "${batch[@]}"; do
                featurelint_scan_file "$f" &
            done
            wait

            scanned=$((scanned + ${#batch[@]}))
            if [[ "$FEATURELINT_QUIET" -eq 0 && "$total" -gt 0 ]]; then
                local pct=$((scanned * 100 / total))
                printf "\r  Scanning... %d/%d files (%d%%)" "$scanned" "$total" "$pct" >&2
            fi
            batch=()
        fi
    done < "$file_list"

    # Process remaining files
    if [[ "${#batch[@]}" -gt 0 ]]; then
        for f in "${batch[@]}"; do
            featurelint_scan_file "$f" &
        done
        wait
        scanned=$((scanned + ${#batch[@]}))
    fi

    if [[ "$FEATURELINT_QUIET" -eq 0 ]]; then
        printf "\r  Scanning... %d/%d files (100%%)\n" "$scanned" "$total" >&2
    fi

    FEATURELINT_SCANNED_FILES=$scanned

    # Aggregate counters (ensure files exist before counting)
    touch "${FEATURELINT_TEMP_DIR}/work/errors.count" "${FEATURELINT_TEMP_DIR}/work/warnings.count" "${FEATURELINT_TEMP_DIR}/work/infos.count"
    FEATURELINT_ERROR_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/errors.count")
    FEATURELINT_WARNING_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/warnings.count")
    FEATURELINT_INFO_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/infos.count")
    FEATURELINT_ERROR_COUNT="${FEATURELINT_ERROR_COUNT// /}"
    FEATURELINT_WARNING_COUNT="${FEATURELINT_WARNING_COUNT// /}"
    FEATURELINT_INFO_COUNT="${FEATURELINT_INFO_COUNT// /}"
    FEATURELINT_TOTAL_FINDINGS=$((FEATURELINT_ERROR_COUNT + FEATURELINT_WARNING_COUNT + FEATURELINT_INFO_COUNT))
}

featurelint_scan_files_sequential() {
    local file_list="$1"
    local total
    total=$(wc -l < "$file_list" 2>/dev/null || echo "0")
    total="${total// /}"
    local scanned=0

    featurelint_log INFO "Starting sequential scan..."

    while IFS= read -r file; do
        featurelint_scan_file "$file"
        scanned=$((scanned + 1))

        if [[ "$FEATURELINT_QUIET" -eq 0 && "$total" -gt 0 ]]; then
            local pct=$((scanned * 100 / total))
            printf "\r  Scanning... %d/%d files (%d%%)" "$scanned" "$total" "$pct" >&2
        fi
    done < "$file_list"

    if [[ "$FEATURELINT_QUIET" -eq 0 ]]; then
        printf "\r  Scanning... %d/%d files (100%%)\n" "$scanned" "$total" >&2
    fi

    FEATURELINT_SCANNED_FILES=$scanned

    # Aggregate counters (ensure files exist before counting)
    touch "${FEATURELINT_TEMP_DIR}/work/errors.count" "${FEATURELINT_TEMP_DIR}/work/warnings.count" "${FEATURELINT_TEMP_DIR}/work/infos.count"
    FEATURELINT_ERROR_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/errors.count")
    FEATURELINT_WARNING_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/warnings.count")
    FEATURELINT_INFO_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/infos.count")
    FEATURELINT_ERROR_COUNT="${FEATURELINT_ERROR_COUNT// /}"
    FEATURELINT_WARNING_COUNT="${FEATURELINT_WARNING_COUNT// /}"
    FEATURELINT_INFO_COUNT="${FEATURELINT_INFO_COUNT// /}"
    FEATURELINT_TOTAL_FINDINGS=$((FEATURELINT_ERROR_COUNT + FEATURELINT_WARNING_COUNT + FEATURELINT_INFO_COUNT))
}

# ==============================================================================
# Context extraction for findings
# ==============================================================================
featurelint_extract_context() {
    local file="$1"
    local line_num="$2"
    local context_lines="${FEATURELINT_CONTEXT_LINES}"

    local start_line=$((line_num - context_lines))
    if [[ "$start_line" -lt 1 ]]; then
        start_line=1
    fi
    local end_line=$((line_num + context_lines))

    sed -n "${start_line},${end_line}p" "$file" 2>/dev/null | while IFS= read -r line; do
        if [[ "$start_line" -eq "$line_num" ]]; then
            printf "  > %4d | %s\n" "$start_line" "$line"
        else
            printf "    %4d | %s\n" "$start_line" "$line"
        fi
        start_line=$((start_line + 1))
    done
}

# ==============================================================================
# Finding aggregation and deduplication
# ==============================================================================
featurelint_aggregate_findings() {
    local output_file="${FEATURELINT_TEMP_DIR}/all_findings.txt"

    # Merge all findings files
    cat "${FEATURELINT_TEMP_DIR}/findings/"*.findings 2>/dev/null | sort -t'|' -k3,3r -k1,1 -k2,2n > "$output_file" 2>/dev/null || true

    featurelint_log DEBUG "Aggregated findings to: ${output_file}"
    echo "$output_file"
}

featurelint_deduplicate_findings() {
    local input_file="$1"
    local output_file="${FEATURELINT_TEMP_DIR}/deduped_findings.txt"

    # Deduplicate by file + line + check_id
    awk -F'|' '!seen[$1 "|" $2 "|" $4]++' "$input_file" > "$output_file"

    local before after
    before=$(wc -l < "$input_file" 2>/dev/null || echo "0")
    after=$(wc -l < "$output_file" 2>/dev/null || echo "0")
    before="${before// /}"
    after="${after// /}"

    if [[ "$before" -ne "$after" ]]; then
        featurelint_log DEBUG "Deduplicated findings: ${before} -> ${after}"
    fi

    # Update counts after deduplication
    FEATURELINT_ERROR_COUNT=$(grep -c '|error|' "$output_file" 2>/dev/null) || FEATURELINT_ERROR_COUNT=0
    FEATURELINT_WARNING_COUNT=$(grep -c '|warning|' "$output_file" 2>/dev/null) || FEATURELINT_WARNING_COUNT=0
    FEATURELINT_INFO_COUNT=$(grep -c '|info|' "$output_file" 2>/dev/null) || FEATURELINT_INFO_COUNT=0
    FEATURELINT_ERROR_COUNT="${FEATURELINT_ERROR_COUNT// /}"
    FEATURELINT_WARNING_COUNT="${FEATURELINT_WARNING_COUNT// /}"
    FEATURELINT_INFO_COUNT="${FEATURELINT_INFO_COUNT// /}"
    FEATURELINT_TOTAL_FINDINGS=$((FEATURELINT_ERROR_COUNT + FEATURELINT_WARNING_COUNT + FEATURELINT_INFO_COUNT))

    echo "$output_file"
}

# ==============================================================================
# Output formatters
# ==============================================================================
featurelint_format_text() {
    local findings_file="$1"

    echo ""
    echo -e "${FEATURELINT_COLOR_MAGENTA}${FEATURELINT_COLOR_BOLD}  FeatureLint v${FEATURELINT_VERSION} - Feature Flag Hygiene Report${FEATURELINT_COLOR_RESET}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}$(date '+%Y-%m-%d %H:%M:%S') | Tier: ${FEATURELINT_TIER}${FEATURELINT_COLOR_RESET}"
    echo ""

    if [[ ! -s "$findings_file" ]]; then
        echo -e "  ${FEATURELINT_COLOR_GREEN}No feature flag issues found. Your codebase is clean!${FEATURELINT_COLOR_RESET}"
        echo ""
        featurelint_format_summary
        return 0
    fi

    local current_file=""
    while IFS='|' read -r file line_num severity check_id description recommendation line_content; do
        # Print file header when file changes
        if [[ "$file" != "$current_file" ]]; then
            echo ""
            echo -e "  ${FEATURELINT_COLOR_BOLD}${file}${FEATURELINT_COLOR_RESET}"
            current_file="$file"
        fi

        # Format the finding
        local icon
        icon="$(featurelint_severity_icon "$severity")"
        echo -e "    ${icon} ${FEATURELINT_COLOR_BOLD}${check_id}${FEATURELINT_COLOR_RESET} (line ${line_num}): ${description}"
        echo -e "      ${FEATURELINT_COLOR_GRAY}Code: ${line_content}${FEATURELINT_COLOR_RESET}"
        echo -e "      ${FEATURELINT_COLOR_CYAN}Fix: ${recommendation}${FEATURELINT_COLOR_RESET}"

        # Show context if verbose
        if [[ "$FEATURELINT_VERBOSE" -ge 1 ]]; then
            echo ""
            featurelint_extract_context "$file" "$line_num"
            echo ""
        fi
    done < "$findings_file"

    echo ""
    featurelint_format_summary
}

featurelint_format_json() {
    local findings_file="$1"

    echo "{"
    echo "  \"tool\": \"featurelint\","
    echo "  \"version\": \"${FEATURELINT_VERSION}\","
    echo "  \"tier\": \"${FEATURELINT_TIER}\","
    echo "  \"timestamp\": \"$(date -u '+%Y-%m-%dT%H:%M:%SZ')\","
    echo "  \"target\": \"${FEATURELINT_TARGET_DIR}\","
    echo "  \"summary\": {"
    echo "    \"total_files\": ${FEATURELINT_TOTAL_FILES},"
    echo "    \"scanned_files\": ${FEATURELINT_SCANNED_FILES},"
    echo "    \"skipped_files\": ${FEATURELINT_SKIPPED_FILES},"
    echo "    \"total_findings\": ${FEATURELINT_TOTAL_FINDINGS},"
    echo "    \"errors\": ${FEATURELINT_ERROR_COUNT},"
    echo "    \"warnings\": ${FEATURELINT_WARNING_COUNT},"
    echo "    \"info\": ${FEATURELINT_INFO_COUNT}"
    echo "  },"
    echo "  \"findings\": ["

    local first=true
    while IFS='|' read -r file line_num severity check_id description recommendation line_content; do
        if [[ "$first" == "true" ]]; then
            first=false
        else
            echo ","
        fi

        # Escape JSON strings
        line_content=$(echo "$line_content" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g')
        description=$(echo "$description" | sed 's/\\/\\\\/g; s/"/\\"/g')
        recommendation=$(echo "$recommendation" | sed 's/\\/\\\\/g; s/"/\\"/g')

        printf '    {\n'
        printf '      "file": "%s",\n' "$file"
        printf '      "line": %s,\n' "$line_num"
        printf '      "severity": "%s",\n' "$severity"
        printf '      "check_id": "%s",\n' "$check_id"
        printf '      "description": "%s",\n' "$description"
        printf '      "recommendation": "%s",\n' "$recommendation"
        printf '      "code": "%s"\n' "$line_content"
        printf '    }'
    done < "$findings_file"

    echo ""
    echo "  ]"
    echo "}"
}

featurelint_format_csv() {
    local findings_file="$1"

    echo "file,line,severity,check_id,description,recommendation,code"
    while IFS='|' read -r file line_num severity check_id description recommendation line_content; do
        # Escape CSV fields
        description=$(echo "$description" | sed 's/"/""/g')
        recommendation=$(echo "$recommendation" | sed 's/"/""/g')
        line_content=$(echo "$line_content" | sed 's/"/""/g')

        printf '"%s",%s,"%s","%s","%s","%s","%s"\n' \
            "$file" "$line_num" "$severity" "$check_id" \
            "$description" "$recommendation" "$line_content"
    done < "$findings_file"
}

featurelint_format_markdown() {
    local findings_file="$1"
    local template="${FEATURELINT_TEMPLATE_DIR}/report.md.tmpl"

    if [[ -f "$template" ]]; then
        featurelint_render_template "$template" "$findings_file"
    else
        # Fallback inline markdown
        echo "# FeatureLint Report"
        echo ""
        echo "**Version:** ${FEATURELINT_VERSION} | **Tier:** ${FEATURELINT_TIER} | **Date:** $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "## Summary"
        echo ""
        echo "| Metric | Count |"
        echo "|--------|-------|"
        echo "| Files Scanned | ${FEATURELINT_SCANNED_FILES} |"
        echo "| Total Findings | ${FEATURELINT_TOTAL_FINDINGS} |"
        echo "| Errors | ${FEATURELINT_ERROR_COUNT} |"
        echo "| Warnings | ${FEATURELINT_WARNING_COUNT} |"
        echo "| Info | ${FEATURELINT_INFO_COUNT} |"
        echo ""
        echo "## Findings"
        echo ""
        echo "| File | Line | Severity | Check | Description |"
        echo "|------|------|----------|-------|-------------|"

        while IFS='|' read -r file line_num severity check_id description recommendation line_content; do
            echo "| \`${file}\` | ${line_num} | ${severity} | ${check_id} | ${description} |"
        done < "$findings_file"
    fi
}

featurelint_render_template() {
    local template="$1"
    local findings_file="$2"
    local duration=$(($(date +%s) - FEATURELINT_START_TIME))

    # Generate findings rows for template
    local findings_rows=""
    while IFS='|' read -r file line_num severity check_id description recommendation line_content; do
        findings_rows="${findings_rows}| \`${file}\` | ${line_num} | ${severity} | ${check_id} | ${description} | ${recommendation} |\n"
    done < "$findings_file"

    # Substitute template variables
    sed -e "s|{{VERSION}}|${FEATURELINT_VERSION}|g" \
        -e "s|{{TIER}}|${FEATURELINT_TIER}|g" \
        -e "s|{{DATE}}|$(date '+%Y-%m-%d %H:%M:%S')|g" \
        -e "s|{{TARGET}}|${FEATURELINT_TARGET_DIR}|g" \
        -e "s|{{TOTAL_FILES}}|${FEATURELINT_TOTAL_FILES}|g" \
        -e "s|{{SCANNED_FILES}}|${FEATURELINT_SCANNED_FILES}|g" \
        -e "s|{{SKIPPED_FILES}}|${FEATURELINT_SKIPPED_FILES}|g" \
        -e "s|{{TOTAL_FINDINGS}}|${FEATURELINT_TOTAL_FINDINGS}|g" \
        -e "s|{{ERROR_COUNT}}|${FEATURELINT_ERROR_COUNT}|g" \
        -e "s|{{WARNING_COUNT}}|${FEATURELINT_WARNING_COUNT}|g" \
        -e "s|{{INFO_COUNT}}|${FEATURELINT_INFO_COUNT}|g" \
        -e "s|{{DURATION}}|${duration}s|g" \
        -e "s|{{ACCENT}}|${FEATURELINT_ACCENT}|g" \
        "$template"

    # Append findings table rows
    if [[ -n "$findings_rows" ]]; then
        printf '%b' "$findings_rows"
    fi
}

featurelint_format_summary() {
    local duration=$(($(date +%s) - FEATURELINT_START_TIME))

    echo -e "  ${FEATURELINT_COLOR_BOLD}Summary${FEATURELINT_COLOR_RESET}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
    echo -e "  Files scanned:    ${FEATURELINT_SCANNED_FILES} / ${FEATURELINT_TOTAL_FILES}"
    echo -e "  Files skipped:    ${FEATURELINT_SKIPPED_FILES}"
    echo -e "  Total findings:   ${FEATURELINT_TOTAL_FINDINGS}"

    if [[ "$FEATURELINT_ERROR_COUNT" -gt 0 ]]; then
        echo -e "  ${FEATURELINT_COLOR_RED}Errors:           ${FEATURELINT_ERROR_COUNT}${FEATURELINT_COLOR_RESET}"
    else
        echo -e "  Errors:           0"
    fi

    if [[ "$FEATURELINT_WARNING_COUNT" -gt 0 ]]; then
        echo -e "  ${FEATURELINT_COLOR_YELLOW}Warnings:         ${FEATURELINT_WARNING_COUNT}${FEATURELINT_COLOR_RESET}"
    else
        echo -e "  Warnings:         0"
    fi

    echo -e "  Info:             ${FEATURELINT_INFO_COUNT}"
    echo -e "  Duration:         ${duration}s"
    echo -e "  Tier:             ${FEATURELINT_TIER}"

    local pattern_count
    pattern_count="$(featurelint_count_tier_patterns "${FEATURELINT_TIER}")"
    echo -e "  Patterns active:  ${pattern_count}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
    echo ""

    if [[ "${FEATURELINT_TIER}" == "free" ]]; then
        echo -e "  ${FEATURELINT_COLOR_MAGENTA}Upgrade to Pro for Flag Safety & SDK Misuse checks (60 patterns)${FEATURELINT_COLOR_RESET}"
        echo -e "  ${FEATURELINT_COLOR_GRAY}https://featurelint.pages.dev${FEATURELINT_COLOR_RESET}"
        echo ""
    elif [[ "${FEATURELINT_TIER}" == "pro" ]]; then
        echo -e "  ${FEATURELINT_COLOR_MAGENTA}Upgrade to Team for Lifecycle & Architecture checks (90 patterns)${FEATURELINT_COLOR_RESET}"
        echo -e "  ${FEATURELINT_COLOR_GRAY}https://featurelint.pages.dev${FEATURELINT_COLOR_RESET}"
        echo ""
    fi
}

# ==============================================================================
# Category summary breakdown
# ==============================================================================
featurelint_category_breakdown() {
    local findings_file="$1"

    echo -e "\n  ${FEATURELINT_COLOR_BOLD}Category Breakdown${FEATURELINT_COLOR_RESET}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"

    local categories
    categories="$(featurelint_get_tier_patterns "${FEATURELINT_TIER}")"

    for cat in $categories; do
        local cat_name
        case "$cat" in
            SF) cat_name="Stale Flags" ;;
            FC) cat_name="Flag Complexity" ;;
            FS) cat_name="Flag Safety" ;;
            SM) cat_name="SDK Misuse" ;;
            FL) cat_name="Flag Lifecycle" ;;
            FA) cat_name="Flag Architecture" ;;
        esac

        local count
        count=$(grep -c "|${cat}-" "$findings_file" 2>/dev/null) || count=0
        if [[ "$count" -gt 0 ]]; then
            printf "  %-22s %s\n" "${cat} - ${cat_name}:" "${count} issues"
        else
            printf "  ${FEATURELINT_COLOR_GRAY}%-22s %s${FEATURELINT_COLOR_RESET}\n" "${cat} - ${cat_name}:" "0 issues"
        fi
    done

    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
    echo ""
}

# ==============================================================================
# Top offending files
# ==============================================================================
featurelint_top_files() {
    local findings_file="$1"
    local top_n="${2:-10}"

    if [[ ! -s "$findings_file" ]]; then
        return 0
    fi

    echo -e "\n  ${FEATURELINT_COLOR_BOLD}Top ${top_n} Files by Finding Count${FEATURELINT_COLOR_RESET}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"

    cut -d'|' -f1 "$findings_file" | sort | uniq -c | sort -rn | head -n "$top_n" | while read -r count file; do
        printf "  %4d  %s\n" "$count" "$file"
    done

    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
    echo ""
}

# ==============================================================================
# Main analysis pipeline
# ==============================================================================
featurelint_analyze() {
    local target_dir="${1:-$FEATURELINT_TARGET_DIR}"

    # Resolve to absolute path
    target_dir="$(cd "$target_dir" 2>/dev/null && pwd)"
    FEATURELINT_TARGET_DIR="$target_dir"

    # Validate target
    if [[ ! -d "$target_dir" ]]; then
        featurelint_log ERROR "Target directory does not exist: ${target_dir}"
        return 1
    fi

    # Initialize
    featurelint_init

    # Print banner
    if [[ "$FEATURELINT_QUIET" -eq 0 && "$FEATURELINT_OUTPUT_FORMAT" == "text" ]]; then
        echo ""
        echo -e "  ${FEATURELINT_COLOR_MAGENTA}${FEATURELINT_COLOR_BOLD}FeatureLint${FEATURELINT_COLOR_RESET} v${FEATURELINT_VERSION}"
        echo -e "  ${FEATURELINT_COLOR_GRAY}Feature flag hygiene analyzer${FEATURELINT_COLOR_RESET}"
        echo ""
    fi

    # Discover files
    local file_list
    file_list="$(featurelint_discover_files "$target_dir")"

    # Re-read total from file list (subshell variable doesn't propagate)
    if [[ -f "$file_list" ]]; then
        FEATURELINT_TOTAL_FILES=$(wc -l < "$file_list" 2>/dev/null || echo "0")
        FEATURELINT_TOTAL_FILES="${FEATURELINT_TOTAL_FILES// /}"
    fi

    if [[ "$FEATURELINT_TOTAL_FILES" -eq 0 ]]; then
        featurelint_log WARN "No files found to analyze in: ${target_dir}"
        return 0
    fi

    # Scan files
    if [[ "$FEATURELINT_PARALLEL_JOBS" -gt 1 ]]; then
        featurelint_scan_files_parallel "$file_list"
    else
        featurelint_scan_files_sequential "$file_list"
    fi

    # Aggregate and deduplicate
    local aggregated
    aggregated="$(featurelint_aggregate_findings)"
    local deduped
    deduped="$(featurelint_deduplicate_findings "$aggregated")"

    # Output results
    case "$FEATURELINT_OUTPUT_FORMAT" in
        text)
            featurelint_format_text "$deduped"
            featurelint_category_breakdown "$deduped"
            featurelint_top_files "$deduped"
            ;;
        json)
            featurelint_format_json "$deduped"
            ;;
        csv)
            featurelint_format_csv "$deduped"
            ;;
        markdown)
            featurelint_format_markdown "$deduped"
            ;;
        *)
            featurelint_log ERROR "Unknown output format: ${FEATURELINT_OUTPUT_FORMAT}"
            return 1
            ;;
    esac

    # Write to report file if specified
    if [[ -n "$FEATURELINT_REPORT_FILE" ]]; then
        case "$FEATURELINT_OUTPUT_FORMAT" in
            text)     featurelint_format_text "$deduped" > "$FEATURELINT_REPORT_FILE" ;;
            json)     featurelint_format_json "$deduped" > "$FEATURELINT_REPORT_FILE" ;;
            csv)      featurelint_format_csv "$deduped" > "$FEATURELINT_REPORT_FILE" ;;
            markdown) featurelint_format_markdown "$deduped" > "$FEATURELINT_REPORT_FILE" ;;
        esac
        featurelint_log INFO "Report written to: ${FEATURELINT_REPORT_FILE}"
    fi

    # Determine exit code
    local exit_code=0
    if [[ "$FEATURELINT_ERROR_COUNT" -gt 0 && "$FEATURELINT_EXIT_CODE_ON_ERROR" -eq 1 ]]; then
        exit_code=1
    elif [[ "$FEATURELINT_WARNING_COUNT" -gt 0 && "$FEATURELINT_EXIT_CODE_ON_WARNING" -eq 1 ]]; then
        exit_code=1
    fi

    return "$exit_code"
}

# ==============================================================================
# Single file analysis (for git hooks)
# ==============================================================================
featurelint_analyze_file() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        featurelint_log ERROR "File not found: ${file}"
        return 1
    fi

    featurelint_init
    FEATURELINT_TOTAL_FILES=1

    featurelint_scan_file "$file"

    FEATURELINT_SCANNED_FILES=1
    touch "${FEATURELINT_TEMP_DIR}/work/errors.count" "${FEATURELINT_TEMP_DIR}/work/warnings.count" "${FEATURELINT_TEMP_DIR}/work/infos.count"
    FEATURELINT_ERROR_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/errors.count")
    FEATURELINT_WARNING_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/warnings.count")
    FEATURELINT_INFO_COUNT=$(wc -l < "${FEATURELINT_TEMP_DIR}/work/infos.count")
    FEATURELINT_ERROR_COUNT="${FEATURELINT_ERROR_COUNT// /}"
    FEATURELINT_WARNING_COUNT="${FEATURELINT_WARNING_COUNT// /}"
    FEATURELINT_INFO_COUNT="${FEATURELINT_INFO_COUNT// /}"
    FEATURELINT_TOTAL_FINDINGS=$((FEATURELINT_ERROR_COUNT + FEATURELINT_WARNING_COUNT + FEATURELINT_INFO_COUNT))

    local aggregated
    aggregated="$(featurelint_aggregate_findings)"
    local deduped
    deduped="$(featurelint_deduplicate_findings "$aggregated")"

    case "$FEATURELINT_OUTPUT_FORMAT" in
        text) featurelint_format_text "$deduped" ;;
        json) featurelint_format_json "$deduped" ;;
        csv)  featurelint_format_csv "$deduped" ;;
        markdown) featurelint_format_markdown "$deduped" ;;
    esac

    local exit_code=0
    if [[ "$FEATURELINT_ERROR_COUNT" -gt 0 ]]; then
        exit_code=1
    fi
    return "$exit_code"
}

# ==============================================================================
# Staged files analysis (for pre-commit hooks)
# ==============================================================================
featurelint_analyze_staged() {
    featurelint_init

    local staged_files
    staged_files="$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)"

    if [[ -z "$staged_files" ]]; then
        featurelint_log INFO "No staged files to analyze"
        return 0
    fi

    local ext_filter
    ext_filter="$(featurelint_build_extension_filter)"

    local filtered_files
    filtered_files="$(echo "$staged_files" | grep -E "$ext_filter" || true)"

    if [[ -z "$filtered_files" ]]; then
        featurelint_log INFO "No supported files in staged changes"
        return 0
    fi

    local file_list="${FEATURELINT_TEMP_DIR}/staged_files.txt"
    echo "$filtered_files" > "$file_list"

    FEATURELINT_TOTAL_FILES=$(wc -l < "$file_list" 2>/dev/null || echo "0")
    FEATURELINT_TOTAL_FILES="${FEATURELINT_TOTAL_FILES// /}"

    featurelint_log INFO "Analyzing ${FEATURELINT_TOTAL_FILES} staged files"

    featurelint_scan_files_sequential "$file_list"

    local aggregated
    aggregated="$(featurelint_aggregate_findings)"
    local deduped
    deduped="$(featurelint_deduplicate_findings "$aggregated")"

    case "$FEATURELINT_OUTPUT_FORMAT" in
        text) featurelint_format_text "$deduped" ;;
        json) featurelint_format_json "$deduped" ;;
        csv)  featurelint_format_csv "$deduped" ;;
        markdown) featurelint_format_markdown "$deduped" ;;
    esac

    local exit_code=0
    if [[ "$FEATURELINT_ERROR_COUNT" -gt 0 && "$FEATURELINT_EXIT_CODE_ON_ERROR" -eq 1 ]]; then
        exit_code=1
    fi
    return "$exit_code"
}

# ==============================================================================
# Baseline management
# ==============================================================================
featurelint_create_baseline() {
    local target_dir="${1:-$FEATURELINT_TARGET_DIR}"
    local baseline_file="${target_dir}/.featurelint-baseline.json"

    FEATURELINT_OUTPUT_FORMAT="json"
    FEATURELINT_QUIET=1

    local output
    output="$(featurelint_analyze "$target_dir")" || true

    echo "$output" > "$baseline_file"
    featurelint_log INFO "Baseline created: ${baseline_file}"
    echo "Baseline saved with ${FEATURELINT_TOTAL_FINDINGS} findings to ${baseline_file}"
}

featurelint_compare_baseline() {
    local target_dir="${1:-$FEATURELINT_TARGET_DIR}"
    local baseline_file="${target_dir}/.featurelint-baseline.json"

    if [[ ! -f "$baseline_file" ]]; then
        featurelint_log ERROR "No baseline found at: ${baseline_file}"
        featurelint_log ERROR "Run 'featurelint baseline' to create one"
        return 1
    fi

    # Get current findings count
    FEATURELINT_QUIET=1
    featurelint_analyze "$target_dir" || true

    local baseline_count
    baseline_count=$(grep -c '"check_id"' "$baseline_file" 2>/dev/null) || baseline_count=0

    local current_count="$FEATURELINT_TOTAL_FINDINGS"
    local diff=$((current_count - baseline_count))

    echo ""
    echo -e "  ${FEATURELINT_COLOR_BOLD}Baseline Comparison${FEATURELINT_COLOR_RESET}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
    echo "  Baseline findings:  ${baseline_count}"
    echo "  Current findings:   ${current_count}"

    if [[ "$diff" -gt 0 ]]; then
        echo -e "  ${FEATURELINT_COLOR_RED}New findings:       +${diff}${FEATURELINT_COLOR_RESET}"
        echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
        return 1
    elif [[ "$diff" -lt 0 ]]; then
        echo -e "  ${FEATURELINT_COLOR_GREEN}Resolved findings:  ${diff}${FEATURELINT_COLOR_RESET}"
        echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
        return 0
    else
        echo -e "  ${FEATURELINT_COLOR_CYAN}No change from baseline${FEATURELINT_COLOR_RESET}"
        echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
        return 0
    fi
}

# ==============================================================================
# Configuration validation
# ==============================================================================
featurelint_validate_config() {
    local errors=0

    # Validate target directory
    if [[ ! -d "$FEATURELINT_TARGET_DIR" ]]; then
        featurelint_log ERROR "Target directory does not exist: ${FEATURELINT_TARGET_DIR}"
        errors=$((errors + 1))
    fi

    # Validate output format
    case "$FEATURELINT_OUTPUT_FORMAT" in
        text|json|csv|markdown) ;;
        *) featurelint_log ERROR "Invalid output format: ${FEATURELINT_OUTPUT_FORMAT}"; errors=$((errors + 1)) ;;
    esac

    # Validate severity filter
    case "$FEATURELINT_SEVERITY_FILTER" in
        all|error|warning|info) ;;
        *) featurelint_log ERROR "Invalid severity filter: ${FEATURELINT_SEVERITY_FILTER}"; errors=$((errors + 1)) ;;
    esac

    # Validate tier
    case "$FEATURELINT_TIER" in
        free|pro|team) ;;
        *) featurelint_log ERROR "Invalid tier: ${FEATURELINT_TIER}"; errors=$((errors + 1)) ;;
    esac

    # Validate parallel jobs
    if [[ "$FEATURELINT_PARALLEL_JOBS" -lt 1 || "$FEATURELINT_PARALLEL_JOBS" -gt 32 ]]; then
        featurelint_log ERROR "Invalid parallel jobs: ${FEATURELINT_PARALLEL_JOBS} (must be 1-32)"
        errors=$((errors + 1))
    fi

    return "$errors"
}

# ==============================================================================
# Health check / self-test
# ==============================================================================
featurelint_health_check() {
    echo -e "\n  ${FEATURELINT_COLOR_BOLD}FeatureLint Health Check${FEATURELINT_COLOR_RESET}"
    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"

    # Version
    echo -e "  Version:       ${FEATURELINT_VERSION}"

    # Pattern validation
    local pattern_errors
    featurelint_validate_patterns 2>/dev/null
    pattern_errors=$?
    if [[ "$pattern_errors" -eq 0 ]]; then
        echo -e "  Patterns:      ${FEATURELINT_COLOR_GREEN}OK${FEATURELINT_COLOR_RESET} (all valid)"
    else
        echo -e "  Patterns:      ${FEATURELINT_COLOR_RED}FAIL${FEATURELINT_COLOR_RESET} (${pattern_errors} errors)"
    fi

    # Pattern counts
    echo -e "  Free patterns: $(featurelint_count_tier_patterns free)"
    echo -e "  Pro patterns:  $(featurelint_count_tier_patterns pro)"
    echo -e "  Team patterns: $(featurelint_count_tier_patterns team)"

    # Dependencies
    local deps_ok=true
    for cmd in grep sed awk find sort uniq wc cut mktemp date; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            echo -e "  ${cmd}:           ${FEATURELINT_COLOR_RED}MISSING${FEATURELINT_COLOR_RESET}"
            deps_ok=false
        fi
    done

    if [[ "$deps_ok" == "true" ]]; then
        echo -e "  Dependencies:  ${FEATURELINT_COLOR_GREEN}OK${FEATURELINT_COLOR_RESET}"
    fi

    # Git availability
    if command -v git >/dev/null 2>&1; then
        echo -e "  Git:           ${FEATURELINT_COLOR_GREEN}Available${FEATURELINT_COLOR_RESET}"
    else
        echo -e "  Git:           ${FEATURELINT_COLOR_YELLOW}Not found (staged analysis disabled)${FEATURELINT_COLOR_RESET}"
    fi

    # Tier
    echo -e "  Current tier:  ${FEATURELINT_TIER}"

    echo -e "  ${FEATURELINT_COLOR_GRAY}-------------------------------------------${FEATURELINT_COLOR_RESET}"
    echo ""
}
