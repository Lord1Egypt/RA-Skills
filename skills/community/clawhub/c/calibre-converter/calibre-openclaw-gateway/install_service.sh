#!/bin/bash

# Calibre OpenClaw Server - Systemd Service Installer
# This script installs and manages the Calibre OpenClaw Server as a systemd service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="calibre-openclaw-server"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
NIGHTLY_SERVICE_NAME="${SERVICE_NAME}-nightly-embeddings"
NIGHTLY_SERVICE_FILE="/etc/systemd/system/${NIGHTLY_SERVICE_NAME}.service"
NIGHTLY_TIMER_FILE="/etc/systemd/system/${NIGHTLY_SERVICE_NAME}.timer"
NIGHTLY_SERVICE_CREATED=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "ℹ $1"
}

env_value() {
    local key="$1"
    local file="${2:-$ENV_FILE}"
    local line value
    if [[ -z "$file" || ! -f "$file" ]]; then
        printf ''
        return
    fi
    line="$(grep -E "^${key}=" "$file" | tail -n 1 || true)"
    value="${line#*=}"
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"
    printf '%s' "$value"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root. It will use sudo when needed."
        exit 1
    fi
}

# Check if .env file exists
check_env() {
    ENV_FILE=""
    CALL_DIR="$(pwd)"
    PARENT_DIR="$(dirname "$SCRIPT_DIR")"

    # Check in order: script dir, call dir, parent dir
    for dir in "$SCRIPT_DIR" "$CALL_DIR" "$PARENT_DIR"; do
        if [[ -f "$dir/.env" ]]; then
            ENV_FILE="$dir/.env"
            print_success ".env file found at $ENV_FILE"
            chmod 600 "$ENV_FILE" 2>/dev/null || print_warning "Could not set $ENV_FILE permissions to 600"
            break
        fi
    done

    if [[ -z "$ENV_FILE" ]]; then
        print_error ".env file not found!"
        print_info "Searched in:"
        print_info "  - $SCRIPT_DIR/.env"
        print_info "  - $CALL_DIR/.env"
        print_info "  - $PARENT_DIR/.env"
        print_info ""
        print_info "Please create a .env file in one of these locations or specify the path:"
        print_info "  cp .env.example /path/to/.env"
        print_info "  Then edit it with your configuration."
        exit 1
    fi
}

# Check and create virtual environment
check_venv() {
    VENV_DIR="$SCRIPT_DIR/.venv"
    VENV_PYTHON="$VENV_DIR/bin/python"
    VENV_PIP="$VENV_DIR/bin/pip"

    if [[ ! -d "$VENV_DIR" ]]; then
        print_warning "Virtual environment not found. Creating..."
        python3 -m venv "$VENV_DIR"
        if [[ $? -eq 0 ]]; then
            print_success "Virtual environment created at $VENV_DIR"
            # Upgrade pip
            print_info "Upgrading pip in new virtual environment..."
            "$VENV_DIR/bin/python" -m pip install --upgrade pip --no-cache-dir 2>/dev/null
            if [[ $? -ne 0 ]]; then
                print_warning "pip upgrade failed; continuing with the bundled pip"
            fi
            print_success "pip upgraded: $($VENV_DIR/bin/pip --version)"
        else
            print_error "Failed to create virtual environment"
            exit 1
        fi
    else
        print_success "Virtual environment found at $VENV_DIR"
        # Check and upgrade pip if needed
        pip_version=$($VENV_PIP --version | awk '{print $2}')
        pip_major=$(echo $pip_version | cut -d. -f1)
        if [[ "$pip_major" -lt 25 ]]; then
            print_warning "pip version $pip_version is old, upgrading..."
            "$VENV_PYTHON" -m pip install --upgrade pip --no-cache-dir || print_warning "pip upgrade failed; continuing with $pip_version"
        else
            print_success "pip version $pip_version is up to date"
        fi
    fi
}

# Check if requirements.txt exists
check_requirements() {
    if [[ ! -f "${SCRIPT_DIR}/requirements.txt" ]]; then
        print_error "requirements.txt not found!"
        exit 1
    fi
    print_success "requirements.txt found"
}

# Check if virtual environment Python is available
check_venv_python() {
    VENV_DIR="$SCRIPT_DIR/.venv"
    VENV_PYTHON="$VENV_DIR/bin/python"

    if [[ ! -f "$VENV_PYTHON" ]]; then
        print_error "Virtual environment Python not found at $VENV_PYTHON"
        exit 1
    fi
    print_success "Virtual environment Python found: $($VENV_PYTHON --version)"
}

# Check if virtual environment pip is available
check_venv_pip() {
    VENV_DIR="$SCRIPT_DIR/.venv"
    VENV_PIP="$VENV_DIR/bin/pip"

    if [[ ! -f "$VENV_PIP" ]]; then
        print_error "Virtual environment pip not found at $VENV_PIP"
        exit 1
    fi
    print_success "Virtual environment pip found"
}

# Check if a package is installed in venv
check_package() {
    local package=$1
    VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
    if $VENV_PYTHON -c "import $package" 2>/dev/null; then
        print_success "$package is installed"
        return 0
    else
        print_error "$package is NOT installed"
        return 1
    fi
}

# Check critical packages
check_packages() {
    print_info "Checking required packages..."
    
    missing_packages=0

    # List of packages to check (import names, not pip names)
    declare -a packages=(
        "fastapi"
        "uvicorn"
        "pydantic"
        "psycopg2"
        "fitz"
        "httpx"
    )

    for package in "${packages[@]}"; do
        if ! check_package "$package"; then
            missing_packages=$((missing_packages + 1))
        fi
    done

    # If packages are missing, install them
    if [[ $missing_packages -gt 0 ]]; then
        print_warning "$missing_packages required package(s) are missing"
        print_info "Installing packages from requirements.txt..."
        VENV_PIP="$SCRIPT_DIR/.venv/bin/pip"
        $VENV_PIP install -r "${SCRIPT_DIR}/requirements.txt"
        if [[ $? -eq 0 ]]; then
            print_success "Packages installed successfully"
        else
            print_error "Failed to install packages"
            exit 1
        fi
    else
        print_success "All required packages are installed"
    fi
}

# Check if Ollama is running
check_ollama() {
    print_info "Checking Ollama..."

    if command -v ollama &> /dev/null; then
        print_success "Ollama is installed"
        
        # Check if Ollama is running
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            print_success "Ollama is running"
            
            # Check if model is available
            if curl -s http://localhost:11434/api/tags | grep -q "nomic-embed-text-v2-moe"; then
                print_success "nomic-embed-text-v2-moe model is available"
            else
                print_warning "nomic-embed-text-v2-moe model is not downloaded"
                print_info "  You can download it with: ollama pull nomic-embed-text-v2-moe:latest"
            fi
        else
            print_warning "Ollama is not running"
            print_info "  Start it with: ollama serve"
        fi
    else
        print_warning "Ollama is not installed"
        print_info "  Install it from: https://ollama.ai"
    fi
}

# Check if PostgreSQL is accessible
check_postgresql() {
    print_info "Checking PostgreSQL..."

    PGUSER="$(env_value POSTGRESQL_DB_USER)"
    PGPASSWORD="$(env_value POSTGRESQL_DB_PASSWD)"
    PGDATABASE="$(env_value POSTGRESQL_DB_DATABASE)"
    PGHOST="$(env_value POSTGRESQL_DB_HOST)"
    PGHOST="${PGHOST:-localhost}"
    PGPORT="$(env_value POSTGRESQL_DB_PORT)"
    PGPORT="${PGPORT:-5432}"

    if [[ -z "$PGUSER" || -z "$PGDATABASE" ]]; then
        print_error "POSTGRESQL_DB_USER and POSTGRESQL_DB_DATABASE must be configured in $ENV_FILE"
        exit 1
    fi

    if PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1" > /dev/null 2>&1; then
        print_success "PostgreSQL is accessible"
    else
        print_warning "PostgreSQL is not accessible"
        print_info "  Make sure PostgreSQL is running and credentials are correct in .env"
    fi
}

# Check if Calibre metadata.db exists
check_calibre_db() {
    print_info "Checking Calibre database..."

    CALIBRE_DB_PATH="$(env_value CALIBRE_DB_PATH)"
    CALIBRE_DB_PATH="${CALIBRE_DB_PATH:-/mnt/Backup_2/Biblioteca/metadata.db}"

    if [[ -f "$CALIBRE_DB_PATH" ]]; then
        print_success "Calibre metadata.db found at $CALIBRE_DB_PATH"
    else
        print_error "Calibre metadata.db not found at $CALIBRE_DB_PATH"
        print_info "  Please check the CALIBRE_DB_PATH in .env"
        exit 1
    fi
}

# Run all checks
run_all_checks() {
    print_info "Running pre-installation checks..."
    echo ""
    
    check_venv
    check_env
    check_requirements
    check_venv_python
    check_venv_pip
    check_packages
    check_ollama
    check_postgresql
    check_calibre_db
    
    echo ""
    print_success "All checks passed!"
}

# Create systemd service file
create_service_file() {
    print_info "Creating systemd service file..."
    
    CURRENT_USER=$(whoami)
    CURRENT_HOME=$(getent passwd "$CURRENT_USER" | cut -d: -f6)
    SERVICE_ENV_DIR="$(dirname "$ENV_FILE")"
    SERVICE_HOST="$(env_value SERVER_HOST)"
    SERVICE_HOST="${SERVICE_HOST:-127.0.0.1}"
    SERVICE_PORT="$(env_value SERVER_PORT)"
    SERVICE_PORT="${SERVICE_PORT:-6180}"
    
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Calibre OpenClaw Server
After=network.target postgresql.service

[Service]
Type=simple
User=${CURRENT_USER}
Group=${CURRENT_USER}
WorkingDirectory=${SCRIPT_DIR}
Environment="PATH=${SCRIPT_DIR}/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="ENV_DIR=${SERVICE_ENV_DIR}"
EnvironmentFile=${ENV_FILE}
ExecStart=${SCRIPT_DIR}/.venv/bin/python -m uvicorn app.main:app --host ${SERVICE_HOST} --port ${SERVICE_PORT}
ExecStop=/bin/kill -SIGTERM \$MAINPID
Restart=always
RestartSec=10
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
StandardOutput=append:${SCRIPT_DIR}/logs/service.log
StandardError=append:${SCRIPT_DIR}/logs/service_error.log

[Install]
WantedBy=multi-user.target
EOF
    
    print_success "Service file created at $SERVICE_FILE"
}

# Create systemd nightly embeddings service and timer files
create_nightly_service_files() {
    print_info "Creating nightly embeddings systemd service and timer files..."

    CURRENT_USER=$(whoami)
    CURRENT_HOME=$(getent passwd "$CURRENT_USER" | cut -d: -f6)
    SERVICE_ENV_DIR="$(dirname "$ENV_FILE")"
    RAG_STOP_AT_LOCAL="$(env_value RAG_STOP_AT_LOCAL)"
    RAG_IDLE_SLEEP_SECONDS="$(env_value RAG_IDLE_SLEEP_SECONDS)"
    RAG_IDLE_SLEEP_SECONDS="${RAG_IDLE_SLEEP_SECONDS:-60}"
    RAG_RUNTIME_MAX_SEC="$(env_value RAG_RUNTIME_MAX_SEC)"
    RAG_TIMER_ON_CALENDAR="$(env_value RAG_TIMER_ON_CALENDAR)"
    RAG_SERVICE_CONTINUOUS="$(env_value RAG_SERVICE_CONTINUOUS)"
    RAG_SERVICE_CONTINUOUS="${RAG_SERVICE_CONTINUOUS:-true}"
    RAG_PREFETCH_RANDOM_BOOKS="$(env_value RAG_PREFETCH_RANDOM_BOOKS)"
    RAG_RECONCILE_ON_START="$(env_value RAG_RECONCILE_ON_START)"
    INSTALL_NIGHTLY_EMBEDDINGS="$(env_value INSTALL_NIGHTLY_EMBEDDINGS)"

    if [[ ! "$INSTALL_NIGHTLY_EMBEDDINGS" =~ ^(1|true|yes|s|sim)$ ]]; then
        print_info "Nightly embeddings service disabled. Set INSTALL_NIGHTLY_EMBEDDINGS=true to install it."
        return
    fi

    if [[ -z "$RAG_TIMER_ON_CALENDAR" ]]; then
        print_error "RAG_TIMER_ON_CALENDAR must be configured in $ENV_FILE"
        exit 1
    fi

    NIGHTLY_ARGS=""
    RUNTIME_MAX_LINE=""
    if [[ "$RAG_SERVICE_CONTINUOUS" =~ ^(1|true|yes|s|sim)$ ]]; then
        NIGHTLY_ARGS="${NIGHTLY_ARGS} --continuous"
    fi
    NIGHTLY_ARGS="${NIGHTLY_ARGS} --idle-sleep ${RAG_IDLE_SLEEP_SECONDS}"
    if [[ -n "$RAG_STOP_AT_LOCAL" ]]; then
        NIGHTLY_ARGS="${NIGHTLY_ARGS} --stop-at-local ${RAG_STOP_AT_LOCAL}"
    fi
    if [[ "$RAG_PREFETCH_RANDOM_BOOKS" =~ ^(1|true|yes|s|sim)$ ]]; then
        NIGHTLY_ARGS="${NIGHTLY_ARGS} --prefetch-random"
    fi
    if [[ "$RAG_RECONCILE_ON_START" =~ ^(1|true|yes|s|sim)$ ]]; then
        NIGHTLY_ARGS="${NIGHTLY_ARGS} --reconcile-embedding-version"
    fi
    if [[ -n "$RAG_RUNTIME_MAX_SEC" ]]; then
        RUNTIME_MAX_LINE="RuntimeMaxSec=${RAG_RUNTIME_MAX_SEC}"
    fi

    sudo tee "$NIGHTLY_SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Calibre OpenClaw Nightly Embedding Prefetch
After=network.target postgresql.service ollama.service
Wants=network-online.target

[Service]
Type=oneshot
User=${CURRENT_USER}
Group=${CURRENT_USER}
WorkingDirectory=${SCRIPT_DIR}
Environment="PATH=${SCRIPT_DIR}/.venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="HOME=${CURRENT_HOME}"
Environment="ENV_DIR=${SERVICE_ENV_DIR}"
EnvironmentFile=${ENV_FILE}
ExecStart=${SCRIPT_DIR}/.venv/bin/python -m app.nightly_embeddings${NIGHTLY_ARGS}
${RUNTIME_MAX_LINE}
TimeoutStopSec=2min
KillSignal=SIGTERM
FinalKillSignal=SIGKILL
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
StandardOutput=append:${SCRIPT_DIR}/logs/nightly_embeddings.log
StandardError=append:${SCRIPT_DIR}/logs/nightly_embeddings_error.log

[Install]
WantedBy=multi-user.target
EOF

    sudo tee "$NIGHTLY_TIMER_FILE" > /dev/null <<EOF
[Unit]
Description=Run Calibre OpenClaw embedding prefetch

[Timer]
OnCalendar=${RAG_TIMER_ON_CALENDAR}
RandomizedDelaySec=0
Persistent=false
Unit=${NIGHTLY_SERVICE_NAME}.service

[Install]
WantedBy=timers.target
EOF

    print_success "Nightly service file created at $NIGHTLY_SERVICE_FILE"
    print_success "Nightly timer file created at $NIGHTLY_TIMER_FILE"
    NIGHTLY_SERVICE_CREATED=true
}

# Install the service
install_service() {
    print_info "Installing ${SERVICE_NAME} service..."
    
    check_root
    
    # Run all pre-installation checks
    run_all_checks
    
    # Create logs directory if it doesn't exist
    mkdir -p "${SCRIPT_DIR}/logs"
    
    # Create service file
    create_service_file

    # Create nightly embeddings service and timer files
    create_nightly_service_files
    
    # Reload systemd
    print_info "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    print_success "Systemd daemon reloaded"
    
    # Enable service to start on boot
    print_info "Enabling service to start on boot..."
    sudo systemctl enable "$SERVICE_NAME"
    print_success "Service enabled"

    if [[ "$NIGHTLY_SERVICE_CREATED" == "true" ]]; then
        print_info "Enabling nightly embeddings timer..."
        sudo systemctl enable --now "$NIGHTLY_SERVICE_NAME.timer"
        print_success "Nightly embeddings timer enabled"
    fi
    
    print_success "Service installed successfully!"
    print_info "You can now manage the service using:"
    print_info "  sudo systemctl start ${SERVICE_NAME}"
    print_info "  sudo systemctl stop ${SERVICE_NAME}"
    print_info "  sudo systemctl restart ${SERVICE_NAME}"
    print_info "  sudo systemctl status ${SERVICE_NAME}"
    print_info "  sudo systemctl start ${NIGHTLY_SERVICE_NAME}.service"
    print_info "  sudo systemctl status ${NIGHTLY_SERVICE_NAME}.timer"
    print_info "  systemctl list-timers ${NIGHTLY_SERVICE_NAME}.timer"
    print_info "  systemctl --user start ${SERVICE_NAME}"
    print_info "  systemctl --user stop ${SERVICE_NAME}"
    print_info "  systemctl --user restart ${SERVICE_NAME}"
    print_info "  systemctl --user status ${SERVICE_NAME}"
}

# Uninstall the service
uninstall_service() {
    print_info "Uninstalling ${SERVICE_NAME} service and ${NIGHTLY_SERVICE_NAME} timer..."
    
    # Stop service if running
    if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null || systemctl --user is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
        print_info "Stopping service..."
        sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || systemctl --user stop "$SERVICE_NAME" 2>/dev/null
        print_success "Service stopped"
    fi

    if systemctl is-active --quiet "$NIGHTLY_SERVICE_NAME.timer" 2>/dev/null; then
        print_info "Stopping nightly embeddings timer..."
        sudo systemctl stop "$NIGHTLY_SERVICE_NAME.timer" 2>/dev/null
        print_success "Nightly embeddings timer stopped"
    fi

    if systemctl is-active --quiet "$NIGHTLY_SERVICE_NAME.service" 2>/dev/null; then
        print_info "Stopping nightly embeddings service..."
        sudo systemctl stop "$NIGHTLY_SERVICE_NAME.service" 2>/dev/null
        print_success "Nightly embeddings service stopped"
    fi
    
    # Disable service
    print_info "Disabling service..."
    sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || systemctl --user disable "$SERVICE_NAME" 2>/dev/null
    print_success "Service disabled"

    print_info "Disabling nightly embeddings timer..."
    sudo systemctl disable --now "$NIGHTLY_SERVICE_NAME.timer" 2>/dev/null || true
    print_success "Nightly embeddings timer disabled"
    
    # Remove service file
    if [[ -f "$SERVICE_FILE" ]]; then
        print_info "Removing service file..."
        sudo rm -f "$SERVICE_FILE"
        print_success "Service file removed"
    fi

    if [[ -f "$NIGHTLY_SERVICE_FILE" ]]; then
        print_info "Removing nightly embeddings service file..."
        sudo rm -f "$NIGHTLY_SERVICE_FILE"
        print_success "Nightly embeddings service file removed"
    fi

    if [[ -f "$NIGHTLY_TIMER_FILE" ]]; then
        print_info "Removing nightly embeddings timer file..."
        sudo rm -f "$NIGHTLY_TIMER_FILE"
        print_success "Nightly embeddings timer file removed"
    fi
    
    # Reload systemd
    print_info "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    print_success "Systemd daemon reloaded"
    
    print_success "Service uninstalled successfully!"
}

# Start the service
start_service() {
    print_info "Starting ${SERVICE_NAME} service..."
    
    if [[ -f "$SERVICE_FILE" ]]; then
        sudo systemctl start "$SERVICE_NAME"
    else
        systemctl --user start "$SERVICE_NAME"
    fi
    
    print_success "Service started!"
    print_info "Check status with: $0 status"
}

# Stop the service
stop_service() {
    print_info "Stopping ${SERVICE_NAME} service..."
    
    if [[ -f "$SERVICE_FILE" ]]; then
        sudo systemctl stop "$SERVICE_NAME"
    else
        systemctl --user stop "$SERVICE_NAME"
    fi
    
    print_success "Service stopped!"
}

# Restart the service
restart_service() {
    print_info "Restarting ${SERVICE_NAME} service..."
    
    if [[ -f "$SERVICE_FILE" ]]; then
        sudo systemctl restart "$SERVICE_NAME"
    else
        systemctl --user restart "$SERVICE_NAME"
    fi
    
    print_success "Service restarted!"
    print_info "Check status with: $0 status"
}

# Show service status
show_status() {
    print_info "${SERVICE_NAME} service status:"
    echo ""
    
    if [[ -f "$SERVICE_FILE" ]]; then
        sudo systemctl status "$SERVICE_NAME"
        echo ""
        print_info "${NIGHTLY_SERVICE_NAME} timer status:"
        sudo systemctl status "$NIGHTLY_SERVICE_NAME.timer" 2>/dev/null || true
        echo ""
        print_info "${NIGHTLY_SERVICE_NAME} next runs:"
        systemctl list-timers "$NIGHTLY_SERVICE_NAME.timer" 2>/dev/null || true
    else
        systemctl --user status "$SERVICE_NAME"
    fi
}

# Enable service to start on boot
enable_service() {
    print_info "Enabling ${SERVICE_NAME} service to start on boot..."
    
    if [[ -f "$SERVICE_FILE" ]]; then
        sudo systemctl enable "$SERVICE_NAME"
        sudo systemctl enable --now "$NIGHTLY_SERVICE_NAME.timer"
    else
        systemctl --user enable "$SERVICE_NAME"
    fi
    
    print_success "Service enabled!"
}

# Disable service from starting on boot
disable_service() {
    print_info "Disabling ${SERVICE_NAME} service from starting on boot..."
    
    if [[ -f "$SERVICE_FILE" ]]; then
        sudo systemctl disable "$SERVICE_NAME"
        sudo systemctl disable --now "$NIGHTLY_SERVICE_NAME.timer"
    else
        systemctl --user disable "$SERVICE_NAME"
    fi
    
    print_success "Service disabled!"
}

# Show usage
show_usage() {
    cat <<EOF
Calibre OpenClaw Server - Service Management Script

Usage: $0 <command>

Commands:
  install     Install the service as a systemd service (requires sudo)
  uninstall   Remove the systemd service and nightly timer (requires sudo)
  start       Start the service
  stop        Stop the service
  restart     Restart the service
  status      Show service status
  enable      Enable service to start on boot
  disable     Disable service from starting on boot
  help        Show this help message

Examples:
  $0 install     # Install the server service and nightly embeddings timer
  $0 start       # Start the service
  $0 status      # Check service status
  $0 stop        # Stop the service
  $0 uninstall   # Remove the service

After installation, you can also use systemctl directly:
  sudo systemctl start ${SERVICE_NAME}
  sudo systemctl stop ${SERVICE_NAME}
  sudo systemctl restart ${SERVICE_NAME}
  sudo systemctl status ${SERVICE_NAME}
  sudo systemctl start ${NIGHTLY_SERVICE_NAME}.service
  sudo systemctl status ${NIGHTLY_SERVICE_NAME}.timer
  systemctl list-timers ${NIGHTLY_SERVICE_NAME}.timer
  
Or with user systemd (if installed as user service):
  systemctl --user start ${SERVICE_NAME}
  systemctl --user stop ${SERVICE_NAME}
  systemctl --user restart ${SERVICE_NAME}
  systemctl --user status ${SERVICE_NAME}
EOF
}

# Main script logic
case "${1:-}" in
    install)
        install_service
        ;;
    uninstall)
        uninstall_service
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        show_status
        ;;
    enable)
        enable_service
        ;;
    disable)
        disable_service
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: ${1:-}"
        echo ""
        show_usage
        exit 1
        ;;
esac
