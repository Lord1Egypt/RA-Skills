#!/bin/bash
# Daily Literature Search Skill - Installation Script
# Usage: ./install.sh [--dry-run] [--uninstall]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"

# Default values
DRY_RUN=false
UNINSTALL=false
CRON_TIME="30 6"  # 6:30 AM daily

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --uninstall)
            UNINSTALL=true
            shift
            ;;
        --cron-time)
            CRON_TIME="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dry-run] [--uninstall] [--cron-time 'HH MM']"
            exit 1
            ;;
    esac
done

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

run_or_dry() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} Would execute: $1"
    else
        eval "$1"
    fi
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not installed."
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        log_warning "pip3 not found. Please install Python pip."
    fi
    
    # Check cron
    if ! command -v crontab &> /dev/null; then
        log_warning "crontab not found. Scheduled searches won't work automatically."
    fi
    
    log_success "Prerequisites check completed."
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    if [ -f "${SCRIPT_DIR}/requirements.txt" ]; then
        run_or_dry "pip3 install -r ${SCRIPT_DIR}/requirements.txt"
        log_success "Dependencies installed."
    else
        log_warning "requirements.txt not found. Skipping dependency installation."
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."
    
    # Read config or use defaults
    if [ -f "$CONFIG_FILE" ]; then
        PAPERS_DIR=$(grep "^papers_dir:" "$CONFIG_FILE" | cut -d':' -f2- | tr -d ' ' | sed 's/\${HOME}/'$HOME'/g')
    else
        PAPERS_DIR="${HOME}/.openclaw/workspace/papers"
    fi
    
    # Create category directories
    for dir in "B-ALL/raw" "MM/raw" "OTHER/raw"; do
        run_or_dry "mkdir -p ${PAPERS_DIR}/${dir}"
    done
    
    # Create log directory
    run_or_dry "mkdir -p ${PAPERS_DIR}/daily_search_logs"
    
    # Create upload directory
    run_or_dry "mkdir -p ${PAPERS_DIR}/upload_temp/incoming"
    
    log_success "Directory structure created."
}

# Setup configuration
setup_config() {
    log_info "Setting up configuration..."
    
    if [ ! -f "$CONFIG_FILE" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo -e "${YELLOW}[DRY-RUN]${NC} Would copy config.example.yaml to config.yaml"
        else
            cp "${SCRIPT_DIR}/config.example.yaml" "$CONFIG_FILE"
            log_success "Configuration file created: $CONFIG_FILE"
            log_info "Please edit $CONFIG_FILE to customize your settings."
        fi
    else
        log_warning "Configuration file already exists: $CONFIG_FILE"
    fi
}

# Setup cron job
setup_cron() {
    log_info "Setting up cron job..."
    
    if ! command -v crontab &> /dev/null; then
        log_warning "crontab not available. Skipping cron setup."
        log_info "You can manually add the following line to your crontab:"
        echo "  ${CRON_TIME} * * * python3 ${SCRIPT_DIR}/scripts/daily_literature_search.py >> ${SCRIPT_DIR}/logs/cron.log 2>&1"
        return
    fi
    
    # Create cron entry
    CRON_ENTRY="${CRON_TIME} * * * python3 ${SCRIPT_DIR}/scripts/daily_literature_search.py >> ${SCRIPT_DIR}/logs/cron.log 2>&1"
    
    if [ "$UNINSTALL" = true ]; then
        # Remove existing cron entry
        (crontab -l 2>/dev/null | grep -v "daily_literature_search.py") | crontab -
        log_success "Cron job removed."
    else
        # Add cron entry (avoid duplicates)
        TEMP_CRON=$(mktemp)
        crontab -l 2>/dev/null | grep -v "daily_literature_search.py" > "$TEMP_CRON" || true
        echo "$CRON_ENTRY" >> "$TEMP_CRON"
        run_or_dry "crontab $TEMP_CRON"
        rm -f "$TEMP_CRON"
        log_success "Cron job installed: Daily search at ${CRON_TIME// /:}"
    fi
}

# Set environment variables
setup_env() {
    log_info "Setting up environment variables..."
    
    ENV_FILE="${SCRIPT_DIR}/.env"
    
    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << EOF
# Daily Literature Search - Environment Variables
# Edit this file and run: source .env

# Email for API access (required for OpenAlex/Crossref polite pool)
USER_EMAIL="your@email.com"

# Optional API keys for higher rate limits
SEMANTIC_SCHOLAR_API_KEY=""
OPENALEX_API_KEY=""

# Notification settings (optional)
EMAIL_USERNAME=""
EMAIL_PASSWORD=""
NOTIFICATION_WEBHOOK=""
DINGTALK_WEBHOOK=""
EOF
        log_success "Environment file created: $ENV_FILE"
        log_info "Please edit $ENV_FILE and run: source $ENV_FILE"
    else
        log_warning "Environment file already exists: $ENV_FILE"
    fi
}

# Uninstall
uninstall() {
    log_info "Uninstalling Daily Literature Search Skill..."
    
    # Remove cron job
    setup_cron
    
    # Optionally remove data (commented out for safety)
    # log_warning "Removing data directories..."
    # run_or_dry "rm -rf ${PAPERS_DIR}/daily_search_logs"
    
    log_success "Uninstallation completed."
}

# Main installation
main() {
    echo "========================================"
    echo "📚 Daily Literature Search Skill"
    echo "   Installation Script"
    echo "========================================"
    echo ""
    
    if [ "$UNINSTALL" = true ]; then
        uninstall
        exit 0
    fi
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}=== DRY RUN MODE ===${NC}"
        echo "No changes will be made."
        echo ""
    fi
    
    check_prerequisites
    echo ""
    
    create_directories
    echo ""
    
    setup_config
    echo ""
    
    setup_env
    echo ""
    
    install_dependencies
    echo ""
    
    setup_cron
    echo ""
    
    echo "========================================"
    echo "✅ Installation Complete!"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "1. Edit config/config.yaml to customize settings"
    echo "2. Edit .env file and run: source .env"
    echo "3. Test run: python3 scripts/daily_literature_search.py"
    echo "4. Check logs: tail -f logs/cron.log"
    echo ""
    echo "For help, see: README.md"
    echo ""
}

# Run main function
main
