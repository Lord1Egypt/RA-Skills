#!/bin/bash
# context-hawk one-command install script
# Supports: Ubuntu/Debian, Fedora/RHEL/CentOS/Rocky/AlmaLinux, Arch, Alpine, openSUSE, macOS
# Usage:
#   curl -fsSL https://.../install.sh | bash
#   ./install.sh --help
#
set -euo pipefail

# ───────────────────────────────────────────────
# Constants
# ───────────────────────────────────────────────
VERSION="1.0.0"
REPO_URL="https://github.com/relunctance/context-hawk"
HAWK_DIR="${HOME}/.hawk"
SCRIPT_NAME="$(basename "$0")"

# ───────────────────────────────────────────────
# Colors
# ───────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ───────────────────────────────────────────────
# Logging helpers
# ───────────────────────────────────────────────
log()   { printf "${GREEN}[✓]${RESET} %s\n" "$*"; }
warn()  { printf "${YELLOW}[!]${RESET} %s\n" "$*"; }
err()   { printf "${RED}[✗]${RESET} %s\n" "$*"; }
step()  { printf "${CYAN}[→]${RESET} %s\n" "$*"; }
bold()  { printf "${BOLD}%s${RESET}\n" "$*"; }

# ───────────────────────────────────────────────
# Usage
# ───────────────────────────────────────────────
usage() {
    bold "context-hawk v${VERSION} — One-Command Installer"
    echo ""
    echo "Usage: $SCRIPT_NAME [options]"
    echo ""
    echo "Options:"
    echo "  --help         Show this help message"
    echo "  --force        Overwrite existing config and installation"
    echo "  --skip-deps    Skip system dependency installation"
    echo ""
    echo "Supported OS:"
    echo "  Ubuntu / Debian"
    echo "  Fedora / RHEL / CentOS / Rocky / AlmaLinux"
    echo "  Arch Linux"
    echo "  Alpine Linux"
    echo "  openSUSE"
    echo "  macOS"
}

# ───────────────────────────────────────────────
# Parse arguments
# ───────────────────────────────────────────────
FORCE=false
SKIP_DEPS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --force)     FORCE=true; shift ;;
        --skip-deps) SKIP_DEPS=true; shift ;;
        --help|-h)   usage; exit 0 ;;
        *)           err "Unknown option: $1"; usage; exit 1 ;;
    esac
done

# ───────────────────────────────────────────────
# Detect OS
# ───────────────────────────────────────────────
detect_os() {
    if [[ "$(uname)" == "Darwin" ]]; then
        echo "macos"
        return
    fi

    if [[ -f /etc/os-release ]]; then
        source /etc/os-release
        case "${ID}" in
            ubuntu|debian|linuxmint|pop)
                echo "debian" ;;
            fedora|rhel|centos|rocky|almalinux)
                echo "fedora" ;;
            arch|manjaro|endeavouros)
                echo "arch" ;;
            alpine)
                echo "alpine" ;;
            opensuse|opensuse-leap|opensuse-tumbleweed|suse|sles)
                echo "suse" ;;
            *)
                if [[ -n "${ID_LIKE:-}" ]]; then
                    case "$ID_LIKE" in
                        *debian*|*ubuntu*) echo "debian" ;;
                        *rhel*|*fedora*|*centos*) echo "fedora" ;;
                        *suse*) echo "suse" ;;
                        *) echo "unknown" ;;
                    esac
                else
                    echo "unknown"
                fi
                ;;
        esac
    else
        echo "unknown"
    fi
}

OS_TYPE=$(detect_os)

# ───────────────────────────────────────────────
# Install system dependencies
# ───────────────────────────────────────────────
install_system_deps() {
    step "Installing system dependencies (${OS_TYPE})..."

    if [[ "$SKIP_DEPS" == true ]]; then
        warn "Skipping system dependencies (--skip-deps)"
        return
    fi

    case "${OS_TYPE}" in
        debian)
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -qq
            apt-get install -y -qq \
                python3 python3-pip python3-venv \
                git curl \
                build-essential libssl-dev zlib1g-dev \
                > /dev/null 2>&1
            ;;

        fedora)
            dnf install -y -q \
                python3 python3-pip \
                git curl \
                gcc gcc-c++ make \
                openssl-devel zlib-devel \
                > /dev/null 2>&1
            ;;

        arch)
            pacman -Sy --noconfirm \
                python python-pip \
                git curl \
                base-devel \
                > /dev/null 2>&1
            ;;

        alpine)
            apk add --no-cache \
                python3 py3-pip \
                git curl \
                build-base openssl-dev zlib-dev \
                > /dev/null 2>&1
            ;;

        suse)
            zypper install -y -q \
                python3 python3-pip \
                git curl \
                gcc gcc-c++ make \
                libopenssl-devel zlib-devel \
                > /dev/null 2>&1
            ;;

        macos)
            if ! command -v brew &> /dev/null; then
                bold "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
                    > /dev/null 2>&1 || true
                eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || true)"
            fi
            if command -v brew &> /dev/null; then
                brew install python@3.12 git curl 2>/dev/null || true
            fi
            ;;

        unknown)
            warn "Could not detect OS. Attempting generic install..."
            if command -v apt-get &> /dev/null; then
                apt-get update -qq && apt-get install -y -qq \
                    python3 python3-pip git curl build-essential > /dev/null 2>&1 || true
            elif command -v dnf &> /dev/null; then
                dnf install -y -q python3 python3-pip git curl gcc make > /dev/null 2>&1 || true
            elif command -v pacman &> /dev/null; then
                pacman -Sy --noconfirm python python-pip git curl base-devel > /dev/null 2>&1 || true
            fi
            ;;
    esac

    log "System dependencies installed"
}

# ───────────────────────────────────────────────
# Find Python (>=3.10)
# ───────────────────────────────────────────────
find_python() {
    step "Finding Python 3.10+..."

    for py in python3.12 python3.11 python3.10 python3 python; do
        if command -v "$py" &> /dev/null; then
            version=$("$py" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
            major=$(echo "$version" | cut -d. -f1)
            minor=$(echo "$version" | cut -d. -f2)
            if [[ "$major" -eq 3 && "$minor" -ge 10 ]]; then
                log "Using ${py} ${version}"
                echo "$py"
                return
            fi
        fi
    done

    err "Python 3.10+ not found. Please install Python 3.10 or higher."
    exit 1
}

# ───────────────────────────────────────────────
# Ensure pip is available
# ───────────────────────────────────────────────
ensure_pip() {
    PYTHON_CMD="$1"
    step "Ensuring pip is available..."

    if ! "$PYTHON_CMD" -m pip --version &> /dev/null; then
        warn "pip not available, installing..."
        case "${OS_TYPE}" in
            debian)
                apt-get install -y -qq python3-pip > /dev/null 2>&1 || true
                ;;
            fedora)
                dnf install -y -q python3-pip > /dev/null 2>&1 || true
                ;;
            arch)
                pacman -Sy --noconfirm python-pip > /dev/null 2>&1 || true
                ;;
            alpine)
                apk add --no-cache py3-pip > /dev/null 2>&1 || true
                ;;
            suse)
                zypper install -y -q python3-pip > /dev/null 2>&1 || true
                ;;
            macos)
                "$PYTHON_CMD" -m ensurepip --upgrade &> /dev/null || true
                ;;
        esac
    fi

    "$PYTHON_CMD" -m pip install --upgrade pip -q 2>/dev/null || true
    log "pip ready"
}

# ───────────────────────────────────────────────
# Install Python packages
# ───────────────────────────────────────────────
install_python_packages() {
    PYTHON_CMD="$1"
    step "Installing context-hawk and Python dependencies..."

    # Try installing context-hawk from pip first
    if "$PYTHON_CMD" -m pip install context-hawk -q 2>/dev/null; then
        log "Installed context-hawk from PyPI"
    else
        warn "context-hawk not found on PyPI, falling back to git+https install"
        if "$PYTHON_CMD" -m pip install "git+${REPO_URL}.git" -q 2>/dev/null; then
            log "Installed context-hawk from git"
        else
            warn "Could not install context-hawk from pip/git, installing dependencies manually"
            # Fallback: install core dependencies manually
            FALLBACK_PACKAGES=(
                "lancedb>=0.10"
                "rank-bm25>=0.2"
                "openai>=1.0"
                "tiktoken>=0.7"
                "sentence-transformers>=2.0"
                "httpx>=0.25"
            )
            for pkg in "${FALLBACK_PACKAGES[@]}"; do
                if "$PYTHON_CMD" -m pip install "$pkg" -q 2>/dev/null; then
                    log "Installed fallback: $pkg"
                else
                    warn "Could not install: $pkg (optional)"
                fi
            done
        fi
    fi

    log "Python packages ready"
}

# ───────────────────────────────────────────────
# Create ~/.hawk/ directory and config
# ───────────────────────────────────────────────
setup_hawk_dir() {
    step "Setting up ~/.hawk/..."

    mkdir -p "${HAWK_DIR}"
    mkdir -p "${HAWK_DIR}/lancedb"

    log "Created ~/.hawk/ and ~/.hawk/lancedb/"
}

# ───────────────────────────────────────────────
# Create config.json
# ───────────────────────────────────────────────
create_config() {
    step "Creating ~/.hawk/config.json..."

    CONFIG_PATH="${HAWK_DIR}/config.json"

    if [[ -f "${CONFIG_PATH}" && "$FORCE" != true ]]; then
        log "config.json already exists, skipping (use --force to overwrite)"
        return
    fi

    if [[ -f "${CONFIG_PATH}" && "$FORCE" == true ]]; then
        cp "${CONFIG_PATH}" "${CONFIG_PATH}.bak.$(date +%s)"
        warn "Backed up existing config.json"
    fi

    cat > "${CONFIG_PATH}" << 'EOF'
{
  "openai_api_key": "",
  "embedding_model": "jina-embeddings-v3",
  "embedding_dimensions": 1024,
  "db_path": "~/.hawk/lancedb",
  "recall_top_k": 5,
  "recall_min_score": 0.6,
  "auto_check_rounds": 10,
  "keep_recent": 5,
  "auto_compress_threshold": 70
}
EOF

    log "Created ~/.hawk/config.json"
}

# ───────────────────────────────────────────────
# Verify installation
# ───────────────────────────────────────────────
verify_installation() {
    PYTHON_CMD="$1"
    step "Verifying installation..."

    if output=$(python3 -c "from hawk.memory import MemoryManager; print('ok')" 2>&1); then
        if [[ "$output" == "ok" ]]; then
            log "Verification passed — MemoryManager imported successfully"
        else
            log "Verification passed"
        fi
    else
        err "Verification failed: could not import from hawk.memory"
        err "Output: $output"
        warn "The package may still be installed correctly — try: python3 -c 'import hawk; print(hawk.__version__)'"
    fi
}

# ───────────────────────────────────────────────
# Print success message
# ───────────────────────────────────────────────
print_success() {
    bold ""
    bold "╔════════════════════════════════════════════════════════╗"
    bold "║     context-hawk v${VERSION} — Installation Complete!         ║"
    bold "╚════════════════════════════════════════════════════════╝"
    echo ""
    log "Config:   ${HOME}/.hawk/config.json"
    log "LanceDB:  ${HOME}/.hawk/lancedb/"
    echo ""

    bold "Next steps:"
    echo ""
    echo "  1. (Optional) Add your API key to ~/.hawk/config.json:"
    echo "     Jina AI (free): https://jina.ai/settings/"
    echo "     Set openai_api_key to jina_xxxx"
    echo ""
    echo "  2. Test the installation:"
    echo "     python3 -c \"from hawk.memory import MemoryManager; print('ok')\""
    echo ""
    echo "  3. Use in Python:"
    echo "     from hawk.memory import MemoryManager"
    echo "     mm = MemoryManager()"
    echo ""
    echo "  4. Install all features (including sentence-transformers):"
    echo "     pip install \"context-hawk[all]\""
    echo ""
}

# ───────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────
main() {
    bold "context-hawk v${VERSION} installer"
    bold "OS: ${OS_TYPE} | Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    if [[ "$EUID" -eq 0 ]]; then
        warn "Running as root. This may cause issues with pip user installs."
        warn "Consider running as a non-root user."
    fi

    install_system_deps
    PYTHON_CMD=$(find_python)
    ensure_pip "$PYTHON_CMD"
    install_python_packages "$PYTHON_CMD"
    setup_hawk_dir
    create_config
    verify_installation "$PYTHON_CMD"
    print_success

    log "Installation finished!"
}

main "$@"
