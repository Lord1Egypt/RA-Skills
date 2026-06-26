#!/bin/bash
#
# Claw Gatekeeper - Conversation Sanitizer
# Removes sensitive patterns from text before processing
#
# Usage:
#   ./sanitizer.sh --file <input_file> [> output_file]
#   ./sanitizer.sh --text "sensitive text to sanitize"
#   ./sanitizer.sh --stdin < input.txt > output.txt
#
# This script is optional and can be used to pre-process content
# before Guardian analyzes it, ensuring no sensitive data is exposed.

set -e

VERSION="0.1.1"

# Sensitive patterns to redact
# Format: description|regex_pattern
SENSITIVE_PATTERNS=(
    # Credentials & Secrets
    "Password|password[:\\s=]+\\S+"
    "Passphrase|passphrase[:\\s=]+\\S+"
    "API Key|api[_-]?key[:\\s=]+\\S+"
    "Secret Key|secret[_-]?key[:\\s=]+\\S+"
    "Auth Token|auth[_-]?token[:\\s=]+\\S+"
    "Access Token|access[_-]?token[:\\s=]+\\S+"
    "Bearer Token|bearer\\s+\\S+"
    "Private Key|private[_-]?key[:\\s=]+\\S+"
    "Secret|secret[:\\s=]+\\S+"
    "Credential|credential[:\\s=]+\\S+"
    
    # Cloud Provider Keys
    "AWS Access Key|AKIA[0-9A-Z]{16}"
    "AWS Secret Key|[0-9a-zA-Z/+=]{40}"
    "GitHub Token|gh[pousr]_[A-Za-z0-9_]{36}"
    "GitLab Token|glpat-[0-9a-zA-Z\\-]{20}"
    "OpenAI API Key|sk-[a-zA-Z0-9]{48}"
    "Anthropic API Key|sk-ant-[a-zA-Z0-9]{32,}"
    "Google API Key|AIza[0-9A-Za-z_-]{35}"
    "Stripe Key|sk_live_[0-9a-zA-Z]{24,}"
    "Slack Token|xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*"
    "Discord Token|[MN][A-Za-zd]{23}\\.[A-Za-zd]{6}\\.[A-Za-zd_]{27}"
    "Telegram Token|[0-9]{9}:[a-zA-Z0-9_-]{35}"
    "Twilio Key|SK[0-9a-fA-F]{32}"
    "SendGrid Key|SG\\.[0-9a-zA-Z_-]{22}\\.[0-9a-zA-Z_-]{43}"
    "Mailgun Key|key-[0-9a-f]{32}"
    
    # Database Connection Strings
    "MongoDB URI|mongodb(\+srv)?://[^\\s\"']+"
    "PostgreSQL URI|postgresql://[^\\s\"']+"
    "MySQL URI|mysql://[^\\s\"']+"
    "Redis URI|redis://[^\\s\"']+"
    "Connection String|connection[_-]?string[:\\s=]+[^\\s\"']+"
    
    # Personal Information
    "Email Address|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
    "Credit Card|[0-9]{4}[\\s-]?[0-9]{4}[\\s-]?[0-9]{4}[\\s-]?[0-9]{4}"
    "SSN|\\b[0-9]{3}-[0-9]{2}-[0-9]{4}\\b"
    "Phone Number|\\b[0-9]{3}-[0-9]{3}-[0-9]{4}\\b"
    "IP Address|\\b[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\b"
    "MAC Address|([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    
    # Cryptocurrency
    "Bitcoin Address|\\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\\b"
    "Ethereum Address|\\b0x[a-fA-F0-9]{40}\\b"
    "Private Key|\\b5[HJK][1-9A-Za-z][^OIl]{48}\\b"
    
    # Tokens & Certificates
    "JWT Token|eyJ[a-zA-Z0-9_-]*\\.eyJ[a-zA-Z0-9_-]*\\.[a-zA-Z0-9_-]*"
    "Certificate|-----BEGIN CERTIFICATE-----[^-]*-----END CERTIFICATE-----"
    "RSA Private Key|-----BEGIN RSA PRIVATE KEY-----[^-]*-----END RSA PRIVATE KEY-----"
    "SSH Private Key|-----BEGIN OPENSSH PRIVATE KEY-----[^-]*-----END OPENSSH PRIVATE KEY-----"
    "PGP Private Key|-----BEGIN PGP PRIVATE KEY BLOCK-----[^-]*-----END PGP PRIVATE KEY BLOCK-----"
    
    # Shell History Patterns
    "History Command|history[-_]?command[:\\s=]+\\S+"
    "Shell Command|bash[-_]?command[:\\s=]+\\S+"
)

# Redaction marker
REDACTION_MARKER="[REDACTED]"

# Colors (disable if not tty)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    GRAY='\033[0;90m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    GRAY=''
    NC=''
fi

show_usage() {
    cat << EOF
OpenClaw Guardian - Conversation Sanitizer v$VERSION

Usage:
    $0 [OPTIONS] <command>

Commands:
    --file <path>       Sanitize contents of a file
    --text "string"     Sanitize a text string
    --stdin             Read from stdin and sanitize
    --check <path>      Check if file contains sensitive data (exit 1 if found)
    --list-patterns     List all configured patterns
    --help              Show this help message

Options:
    --verbose           Show what patterns were matched
    --marker "text"     Custom redaction marker (default: [REDACTED])
    --dry-run           Show what would be redacted without modifying

Examples:
    # Sanitize a file
    $0 --file conversation.txt > sanitized.txt

    # Sanitize stdin
    echo "password: secret123" | $0 --stdin

    # Check for sensitive data
    $0 --check session.json && echo "Clean" || echo "Contains sensitive data"

    # Verbose mode
    $0 --file log.txt --verbose

EOF
}

sanitize_text() {
    local text="$1"
    local verbose="${2:-false}"
    local dry_run="${3:-false}"
    local match_count=0
    
    for pattern_entry in "${SENSITIVE_PATTERNS[@]}"; do
        IFS='|' read -r description pattern <<< "$pattern_entry"
        
        if echo "$text" | grep -qiE "$pattern" 2>/dev/null; then
            match_count=$((match_count + 1))
            
            if [ "$verbose" = "true" ]; then
                echo -e "${YELLOW}[MATCH]${NC} $description pattern found" >&2
            fi
            
            if [ "$dry_run" = "false" ]; then
                # Use perl for better regex compatibility
                if command -v perl &> /dev/null; then
                    text=$(echo "$text" | perl -pe "s/$pattern/$REDACTION_MARKER/g")
                else
                    # Fallback to sed (limited regex support)
                    text=$(echo "$text" | sed -E "s/$pattern/$REDACTION_MARKER/g" 2>/dev/null || echo "$text")
                fi
            fi
        fi
    done
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO]${NC} Total patterns matched: $match_count" >&2
    fi
    
    echo "$text"
}

sanitize_file() {
    local file_path="$1"
    local verbose="${2:-false}"
    local dry_run="${3:-false}"
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}[ERROR]${NC} File not found: $file_path" >&2
        exit 1
    fi
    
    if [ "$verbose" = "true" ]; then
        echo -e "${BLUE}[INFO]${NC} Processing file: $file_path" >&2
    fi
    
    local content
    content=$(cat "$file_path")
    sanitize_text "$content" "$verbose" "$dry_run"
}

check_sensitive() {
    local file_path="$1"
    local verbose="${2:-false}"
    local found=0
    
    if [ ! -f "$file_path" ]; then
        echo -e "${RED}[ERROR]${NC} File not found: $file_path" >&2
        exit 2
    fi
    
    local content
    content=$(cat "$file_path")
    
    for pattern_entry in "${SENSITIVE_PATTERNS[@]}"; do
        IFS='|' read -r description pattern <<< "$pattern_entry"
        
        if echo "$content" | grep -qiE "$pattern" 2>/dev/null; then
            found=1
            if [ "$verbose" = "true" ]; then
                echo -e "${YELLOW}[FOUND]${NC} $description" >&2
            fi
        fi
    done
    
    if [ $found -eq 1 ]; then
        echo -e "${RED}[RESULT]${NC} Sensitive data detected" >&2
        exit 1
    else
        echo -e "${GREEN}[RESULT]${NC} No sensitive data detected" >&2
        exit 0
    fi
}

list_patterns() {
    echo "Configured Sensitive Patterns:"
    echo "=============================="
    echo ""
    
    local i=1
    for pattern_entry in "${SENSITIVE_PATTERNS[@]}"; do
        IFS='|' read -r description pattern <<< "$pattern_entry"
        printf "  %2d. %-30s %s\n" "$i" "$description" "${GRAY}(regex: ${pattern:0:40}...)${NC}"
        i=$((i + 1))
    done
    
    echo ""
    echo "Total patterns: ${#SENSITIVE_PATTERNS[@]}"
}

# Main
case "${1:-}" in
    --file)
        shift
        file_path="$1"
        shift
        verbose="false"
        dry_run="false"
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --verbose) verbose="true" ;;
                --dry-run) dry_run="true" ;;
                --marker) REDACTION_MARKER="$2"; shift ;;
            esac
            shift
        done
        sanitize_file "$file_path" "$verbose" "$dry_run"
        ;;
    
    --text)
        shift
        text="$1"
        shift
        verbose="false"
        dry_run="false"
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --verbose) verbose="true" ;;
                --dry-run) dry_run="true" ;;
                --marker) REDACTION_MARKER="$2"; shift ;;
            esac
            shift
        done
        sanitize_text "$text" "$verbose" "$dry_run"
        ;;
    
    --stdin)
        shift
        verbose="false"
        dry_run="false"
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --verbose) verbose="true" ;;
                --dry-run) dry_run="true" ;;
                --marker) REDACTION_MARKER="$2"; shift ;;
            esac
            shift
        done
        content=$(cat)
        sanitize_text "$content" "$verbose" "$dry_run"
        ;;
    
    --check)
        shift
        file_path="$1"
        shift
        verbose="false"
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --verbose) verbose="true" ;;
            esac
            shift
        done
        check_sensitive "$file_path" "$verbose"
        ;;
    
    --list-patterns)
        list_patterns
        ;;
    
    --help|-h)
        show_usage
        ;;
    
    *)
        show_usage
        exit 1
        ;;
esac
