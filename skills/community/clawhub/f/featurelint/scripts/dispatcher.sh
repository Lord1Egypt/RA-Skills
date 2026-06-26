#!/usr/bin/env bash
# ==============================================================================
# FeatureLint - Feature Flag Hygiene Analyzer
# CLI Dispatcher (Entry Point)
# ==============================================================================
set -euo pipefail

FEATURELINT_DISPATCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source core modules
# shellcheck source=license.sh
source "${FEATURELINT_DISPATCHER_DIR}/license.sh"
# shellcheck source=analyzer.sh
source "${FEATURELINT_DISPATCHER_DIR}/analyzer.sh"

# ==============================================================================
# Usage and help
# ==============================================================================
featurelint_usage() {
    cat <<'USAGE'

  FeatureLint - Feature Flag Hygiene Analyzer

  USAGE
    featurelint <command> [options] [target]

  COMMANDS
    scan              Analyze a directory for feature flag issues (default)
    file <path>       Analyze a single file
    staged            Analyze git staged files (pre-commit hook)
    baseline          Create a baseline snapshot of current findings
    compare           Compare current findings against the baseline
    health            Run a self-diagnostic health check
    version           Print version information
    help              Show this help message

  OPTIONS
    -f, --format <fmt>       Output format: text, json, csv, markdown (default: text)
    -o, --output <file>      Write report to file
    -s, --severity <level>   Minimum severity: error, warning, info, all (default: all)
    -c, --category <cat>     Filter by category: SF, FC, FS, SM, FL, FA, all (default: all)
    -t, --tier <tier>        License tier: free, pro, team (default: free)
    -j, --jobs <n>           Parallel scan jobs (default: 4)
    -i, --include <pattern>  Include only files matching glob pattern
    -e, --exclude <pattern>  Exclude files matching regex pattern
    -C, --context <n>        Context lines around findings (default: 2)
        --max-size <bytes>   Maximum file size in bytes (default: 1048576)
        --scan-hidden        Include hidden files and directories
        --warn-exit          Exit with code 1 on warnings (default: errors only)
    -v, --verbose            Increase verbosity (use -vv for trace)
    -q, --quiet              Suppress non-essential output
    -V, --version            Print version
    -h, --help               Show this help

  ENVIRONMENT VARIABLES
    FEATURELINT_LICENSE_KEY   License key for Pro/Team tier activation
    FEATURELINT_TIER          Override tier (free, pro, team)
    FEATURELINT_FORMAT        Default output format
    FEATURELINT_SEVERITY      Default severity filter
    FEATURELINT_JOBS          Default parallel job count

  EXAMPLES
    featurelint scan ./src
    featurelint scan --format json --output report.json ./src
    featurelint file ./src/flags.ts
    featurelint staged --severity error
    featurelint scan --category SF --tier pro ./src
    featurelint baseline ./src
    featurelint compare ./src
    featurelint health

  TIER INFORMATION
    Free    30 patterns  Stale Flags + Flag Complexity
    Pro     60 patterns  + Flag Safety + SDK Misuse
    Team    90 patterns  + Flag Lifecycle + Flag Architecture

  Learn more: https://featurelint.pages.dev

USAGE
}

featurelint_version_info() {
    echo "featurelint v${FEATURELINT_VERSION}"
}

# ==============================================================================
# Argument parsing
# ==============================================================================
featurelint_parse_args() {
    FEATURELINT_COMMAND="scan"
    local positional_args=()

    # Apply environment variable defaults
    if [[ -n "${FEATURELINT_FORMAT:-}" ]]; then
        FEATURELINT_OUTPUT_FORMAT="$FEATURELINT_FORMAT"
    fi
    if [[ -n "${FEATURELINT_SEVERITY:-}" ]]; then
        FEATURELINT_SEVERITY_FILTER="$FEATURELINT_SEVERITY"
    fi
    if [[ -n "${FEATURELINT_JOBS:-}" ]]; then
        FEATURELINT_PARALLEL_JOBS="$FEATURELINT_JOBS"
    fi
    if [[ -n "${FEATURELINT_TIER:-}" ]]; then
        FEATURELINT_TIER="${FEATURELINT_TIER}"
    fi

    # Check for license key to determine tier
    if [[ -n "${FEATURELINT_LICENSE_KEY:-}" ]]; then
        local validated_tier
        validated_tier="$(featurelint_validate_license "${FEATURELINT_LICENSE_KEY}")"
        if [[ -n "$validated_tier" ]]; then
            FEATURELINT_TIER="$validated_tier"
        fi
    fi

    while [[ $# -gt 0 ]]; do
        case "$1" in
            scan|file|staged|baseline|compare|health|version|help)
                FEATURELINT_COMMAND="$1"
                shift
                ;;
            -f|--format)
                FEATURELINT_OUTPUT_FORMAT="$2"
                shift 2
                ;;
            -o|--output)
                FEATURELINT_REPORT_FILE="$2"
                shift 2
                ;;
            -s|--severity)
                FEATURELINT_SEVERITY_FILTER="$2"
                shift 2
                ;;
            -c|--category)
                FEATURELINT_CATEGORY_FILTER="$2"
                shift 2
                ;;
            -t|--tier)
                FEATURELINT_TIER="$2"
                shift 2
                ;;
            -j|--jobs)
                FEATURELINT_PARALLEL_JOBS="$2"
                shift 2
                ;;
            -i|--include)
                FEATURELINT_INCLUDE_PATTERN="$2"
                shift 2
                ;;
            -e|--exclude)
                FEATURELINT_EXCLUDE_PATTERN="$2"
                shift 2
                ;;
            -C|--context)
                FEATURELINT_CONTEXT_LINES="$2"
                shift 2
                ;;
            --max-size)
                FEATURELINT_MAX_FILE_SIZE="$2"
                shift 2
                ;;
            --scan-hidden)
                FEATURELINT_SCAN_HIDDEN=1
                shift
                ;;
            --warn-exit)
                FEATURELINT_EXIT_CODE_ON_WARNING=1
                shift
                ;;
            -v|--verbose)
                FEATURELINT_VERBOSE=$((FEATURELINT_VERBOSE + 1))
                shift
                ;;
            -vv)
                FEATURELINT_VERBOSE=2
                shift
                ;;
            -q|--quiet)
                FEATURELINT_QUIET=1
                shift
                ;;
            -V|--version)
                FEATURELINT_COMMAND="version"
                shift
                ;;
            -h|--help)
                FEATURELINT_COMMAND="help"
                shift
                ;;
            --)
                shift
                positional_args+=("$@")
                break
                ;;
            -*)
                featurelint_log ERROR "Unknown option: $1"
                featurelint_usage
                return 1
                ;;
            *)
                positional_args+=("$1")
                shift
                ;;
        esac
    done

    # Set target from positional args
    if [[ ${#positional_args[@]} -gt 0 ]]; then
        FEATURELINT_TARGET_DIR="${positional_args[0]}"
    fi
}

# ==============================================================================
# Command dispatch
# ==============================================================================
featurelint_dispatch() {
    local command="$1"

    case "$command" in
        scan)
            featurelint_validate_config || return 1
            featurelint_analyze "${FEATURELINT_TARGET_DIR}"
            ;;
        file)
            if [[ -z "${FEATURELINT_TARGET_DIR}" || ! -f "${FEATURELINT_TARGET_DIR}" ]]; then
                featurelint_log ERROR "Please provide a valid file path"
                featurelint_log ERROR "Usage: featurelint file <path>"
                return 1
            fi
            featurelint_analyze_file "${FEATURELINT_TARGET_DIR}"
            ;;
        staged)
            featurelint_analyze_staged
            ;;
        baseline)
            featurelint_create_baseline "${FEATURELINT_TARGET_DIR}"
            ;;
        compare)
            featurelint_compare_baseline "${FEATURELINT_TARGET_DIR}"
            ;;
        health)
            featurelint_health_check
            ;;
        version)
            featurelint_version_info
            ;;
        help)
            featurelint_usage
            ;;
        *)
            featurelint_log ERROR "Unknown command: ${command}"
            featurelint_usage
            return 1
            ;;
    esac
}

# ==============================================================================
# Pre-flight checks
# ==============================================================================
featurelint_preflight() {
    # Ensure minimum bash version
    if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
        echo "ERROR: featurelint requires bash 4.0 or later (found ${BASH_VERSION})" >&2
        echo "On macOS, install with: brew install bash" >&2
        return 1
    fi

    # Ensure required commands exist
    local required_cmds=(grep sed awk find sort uniq wc cut mktemp date)
    for cmd in "${required_cmds[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            echo "ERROR: Required command not found: ${cmd}" >&2
            return 1
        fi
    done

    return 0
}

# ==============================================================================
# Signal handlers
# ==============================================================================
featurelint_handle_sigint() {
    echo "" >&2
    featurelint_log WARN "Interrupted by user"
    featurelint_cleanup
    exit 130
}

featurelint_handle_sigterm() {
    featurelint_log WARN "Terminated"
    featurelint_cleanup
    exit 143
}

trap featurelint_handle_sigint INT
trap featurelint_handle_sigterm TERM

# ==============================================================================
# Main entry point
# ==============================================================================
featurelint_main() {
    # Pre-flight checks
    featurelint_preflight || exit 1

    # Parse arguments (sets FEATURELINT_COMMAND and other globals directly)
    featurelint_parse_args "$@"

    # Dispatch command
    featurelint_dispatch "${FEATURELINT_COMMAND}"
    local exit_code=$?

    return "$exit_code"
}

# Run if executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    featurelint_main "$@"
    exit $?
fi
