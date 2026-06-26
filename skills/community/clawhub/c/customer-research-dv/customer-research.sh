#!/bin/bash
# Customer Research CLI Wrapper
# Unified interface for all customer research tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"

show_help() {
    cat << EOF
Customer Research & Validation Tool

Pre-pipeline validation for marketing campaigns. Ensures strategy is built on real customer signal.

USAGE:
    customer-research <action> [options]

ACTIONS:
    mine        Mine Reddit for customer insights
    survey      Generate customer survey
    interview   Generate interview script
    validate    Validate persona against data
    scrape      Scrape competitor reviews
    help        Show this help message

EXAMPLES:
    # Mine Reddit for tax software pain points
    customer-research mine \\
        --category "tax software" \\
        --subreddits personalfinance,tax \\
        --output insights.json

    # Generate survey from hypothesis
    customer-research survey \\
        --hypothesis "AI tax optimizer for W-2 employees" \\
        --output survey.json \\
        --markdown survey.md

    # Create interview script
    customer-research interview \\
        --persona tech_pm_high_earner \\
        --output interview.json \\
        --markdown interview.md

    # Validate persona against Reddit data
    customer-research validate \\
        --persona persona.json \\
        --insights reddit-insights.json \\
        --output validated.json \\
        --markdown report.md

    # Scrape competitor reviews
    customer-research scrape \\
        --platform url \\
        --url "https://example.com/reviews" \\
        --output competitor-reviews.json

For detailed options on each action, run:
    customer-research <action> --help

EOF
}

# Check Python dependencies
check_deps() {
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is required but not installed" >&2
        exit 1
    fi
    
    # Check for required packages
    python3 -c "import praw, textblob, bs4, requests" 2>/dev/null || {
        echo "Error: Missing Python dependencies" >&2
        echo "Install with: pip install -r $SCRIPT_DIR/requirements.txt" >&2
        exit 1
    }
}

# Main router
case "${1:-help}" in
    mine)
        check_deps
        shift
        python3 "$SCRIPTS_DIR/reddit-miner.py" "$@"
        ;;
    
    survey)
        check_deps
        shift
        python3 "$SCRIPTS_DIR/survey-gen.py" "$@"
        ;;
    
    interview)
        check_deps
        shift
        python3 "$SCRIPTS_DIR/interview-script.py" "$@"
        ;;
    
    validate)
        check_deps
        shift
        python3 "$SCRIPTS_DIR/persona-validator.py" "$@"
        ;;
    
    scrape)
        check_deps
        shift
        python3 "$SCRIPTS_DIR/competitor-scraper.py" "$@"
        ;;
    
    help|--help|-h)
        show_help
        ;;
    
    *)
        echo "Error: Unknown action '${1}'" >&2
        echo "Run 'customer-research help' for usage" >&2
        exit 1
        ;;
esac
