#!/bin/bash
# ==============================================================================
# CAD Viewer Skill - Environment Auto-Configuration Script
# Installs Python dependencies, ODA File Converter, QCAD, and xvfb virtual display
# 
# Usage: bash setup.sh [--skip-oda] [--skip-qcad] [--oda-rpm /path/to/oda.rpm]
#
# This script requires root permissions (for installing system packages)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSETS_DIR="$SKILL_DIR/assets"
mkdir -p "$ASSETS_DIR"
MARKER_FILE="$ASSETS_DIR/.setup_done"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_err()   { echo -e "${RED}[ERROR]${NC} $1"; }

# ========================== Parameter Parsing ==========================
SKIP_ODA=false
SKIP_QCAD=false
ODA_RPM_PATH=""
QCAD_TAR_PATH=""
CONFIRM=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --confirm)    CONFIRM=true; shift ;;
        --skip-oda)   SKIP_ODA=true; shift ;;
        --skip-qcad)  SKIP_QCAD=true; shift ;;
        --oda-rpm)    ODA_RPM_PATH="$2"; shift 2 ;;
        --qcad-tar)   QCAD_TAR_PATH="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: bash setup.sh [options]"
            echo ""
            echo "Options:"
            echo "  --confirm            Explicitly confirm to run setup (required)"
            echo "  --skip-oda           Skip ODA File Converter installation"
            echo "  --skip-qcad          Skip QCAD installation"
            echo "  --oda-rpm PATH       Specify local ODA RPM package path"
            echo "  --qcad-tar PATH      Specify local QCAD tar.gz package path"
            echo "  -h, --help           Show help message"
            echo ""
            echo "SECURITY NOTICE:"
            echo "  This script downloads binaries from opendesign.com and qcad.org,"
            echo "  and uses sudo for system packages. Use --confirm to proceed."
            exit 0
            ;;
        *) log_err "Unknown parameter: $1"; exit 1 ;;
    esac
done

# Require explicit confirmation
if [ "$CONFIRM" != true ] && [ -z "$ODA_RPM_PATH" ] && [ -z "$QCAD_TAR_PATH" ]; then
    log_err "Setup requires explicit confirmation."
    log_info "Run with --confirm to proceed with automatic setup."
    log_info "Or use --oda-rpm and --qcad-tar with local packages."
    log_warn "This script downloads from opendesign.com and qcad.org,"
    log_warn "and uses sudo for system package installation."
    exit 1
fi

# ========================== System Detection ==========================
log_info "Detecting system environment..."

ARCH=$(uname -m)
if [ "$ARCH" != "x86_64" ]; then
    log_err "Currently only x86_64 architecture is supported, detected: $ARCH"
    exit 1
fi

# Detect package manager
PKG_MANAGER=""
if command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
elif command -v yum &>/dev/null; then
    PKG_MANAGER="yum"
elif command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt-get"
else
    log_err "No supported package manager detected (dnf/yum/apt-get)"
    exit 1
fi
log_ok "Package manager: $PKG_MANAGER | Architecture: $ARCH"

# Detect Python3
if ! command -v python3 &>/dev/null; then
    log_err "python3 not detected, please install Python 3.8+ first"
    exit 1
fi
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
log_ok "Python version: $PYTHON_VERSION"

# ========================== 1. Python Dependencies ==========================
log_info "========== [1/4] Installing Python Dependencies =========="

install_python_pkg() {
    local pkg=$1
    if python3 -c "import $pkg" 2>/dev/null; then
        log_ok "$pkg already installed"
    else
        log_info "Installing $pkg ..."
        pip3 install "$pkg" -q && log_ok "$pkg installed successfully" || log_err "$pkg installation failed"
    fi
}

install_python_pkg ezdxf
install_python_pkg matplotlib

# ========================== 2. xvfb Virtual Display ==========================
log_info "========== [2/4] Installing xvfb Virtual Display =========="

if command -v xvfb-run &>/dev/null; then
    log_ok "xvfb-run already installed"
else
    log_info "Installing xvfb ..."
    if [ "$PKG_MANAGER" = "apt-get" ]; then
        sudo apt-get update -qq && sudo apt-get install -y -qq xvfb
    else
        sudo $PKG_MANAGER install -y xorg-x11-server-Xvfb 2>/dev/null || \
        sudo $PKG_MANAGER install -y Xvfb 2>/dev/null || \
        sudo $PKG_MANAGER install -y xvfb 2>/dev/null || \
        log_warn "xvfb installation failed, ODA and QCAD graphics rendering may be unavailable"
    fi
    if command -v xvfb-run &>/dev/null; then
        log_ok "xvfb installed successfully"
    fi
fi

# ========================== 3. ODA File Converter ==========================
log_info "========== [3/4] Configuring ODA File Converter =========="

ODA_INSTALLED=false

if command -v ODAFileConverter &>/dev/null || [ -f /usr/local/bin/ODAFileConverter ]; then
    log_ok "ODA File Converter already installed"
    ODA_INSTALLED=true
elif [ "$SKIP_ODA" = true ]; then
    log_warn "Skipping ODA installation (--skip-oda), DWG file reading will be unavailable"
else
    if [ -n "$ODA_RPM_PATH" ] && [ -f "$ODA_RPM_PATH" ]; then
        # User provided local RPM package
        log_info "Installing ODA using local RPM package: $ODA_RPM_PATH"
        EXT="${ODA_RPM_PATH##*.}"
        if [ "$EXT" = "rpm" ]; then
            sudo rpm -i --replacefiles --nodeps "$ODA_RPM_PATH" 2>/dev/null || \
            sudo $PKG_MANAGER localinstall --skip-broken -y "$ODA_RPM_PATH" 2>/dev/null
        elif [ "$EXT" = "deb" ]; then
            sudo dpkg -i "$ODA_RPM_PATH" 2>/dev/null || sudo apt-get install -f -y 2>/dev/null
        fi
    else
        # Attempt automatic download
        log_info "Attempting to automatically download ODA File Converter..."

        # ODA official site requires registration, here we provide common download URL patterns
        ODA_URLS=(
            "https://download.opendesign.com/guestfiles/ODAFileConverter/ODAFileConverter_QT6_lnxX64_8.3dll_25.3.rpm"
            "https://download.opendesign.com/guestfiles/ODAFileConverter/ODAFileConverter_QT6_lnxX64_8.3dll_25.3.deb"
        )

        ODA_DOWNLOADED=false
        TMP_DIR=$(mktemp -d)

        for url in "${ODA_URLS[@]}"; do
            FILENAME=$(basename "$url")
            log_info "Attempting download: $FILENAME"
            if wget -q --timeout=30 -O "$TMP_DIR/$FILENAME" "$url" 2>/dev/null || \
               curl -sL --connect-timeout 30 -o "$TMP_DIR/$FILENAME" "$url" 2>/dev/null; then
                if [ -s "$TMP_DIR/$FILENAME" ]; then
                    EXT="${FILENAME##*.}"
                    if [ "$EXT" = "rpm" ]; then
                        sudo rpm -i --replacefiles --nodeps "$TMP_DIR/$FILENAME" 2>/dev/null && ODA_DOWNLOADED=true
                    elif [ "$EXT" = "deb" ]; then
                        sudo dpkg -i "$TMP_DIR/$FILENAME" 2>/dev/null && ODA_DOWNLOADED=true
                    fi
                    if [ "$ODA_DOWNLOADED" = true ]; then
                        log_ok "ODA File Converter installed successfully"
                        break
                    fi
                fi
            fi
        done

        rm -rf "$TMP_DIR"

        if [ "$ODA_DOWNLOADED" = false ]; then
            log_warn "Automatic ODA download failed. Please download manually:"
            log_warn "  1. Visit https://www.opendesign.com/guestfiles/oda_file_converter"
            log_warn "  2. Register a free account and download Linux x86_64 RPM/DEB package"
            log_warn "  3. Re-run: bash setup.sh --oda-rpm /path/to/ODAFileConverter_xxx.rpm"
        fi
    fi

    # Verify installation result
    if command -v ODAFileConverter &>/dev/null || [ -f /usr/local/bin/ODAFileConverter ]; then
        ODA_INSTALLED=true
        log_ok "ODA File Converter installed successfully"
    fi
fi

# Configure oda_wrapper.sh
if [ "$ODA_INSTALLED" = true ]; then
    ODA_BIN=$(command -v ODAFileConverter 2>/dev/null || echo "/usr/local/bin/ODAFileConverter")
    cat > "$ASSETS_DIR/oda_wrapper.sh" << WRAPPER_EOF
#!/bin/bash
# Auto-start real ODA converter in virtual display
xvfb-run -a $ODA_BIN "\$@"
WRAPPER_EOF
    chmod +x "$ASSETS_DIR/oda_wrapper.sh"
    log_ok "oda_wrapper.sh generated: $ASSETS_DIR/oda_wrapper.sh"
fi

# ========================== 4. QCAD (dwg2bmp) ==========================
log_info "========== [4/4] Configuring QCAD (dwg2bmp) =========="

QCAD_INSTALL_DIR="$ASSETS_DIR/qcad"
QCAD_INSTALLED=false

# Check if already installed
if [ -f "$QCAD_INSTALL_DIR/dwg2bmp" ]; then
    log_ok "QCAD dwg2bmp already installed (skill built-in): $QCAD_INSTALL_DIR/dwg2bmp"
    QCAD_INSTALLED=true
elif command -v dwg2bmp &>/dev/null; then
    log_ok "QCAD dwg2bmp already installed (system): $(command -v dwg2bmp)"
    QCAD_INSTALLED=true
elif [ "$SKIP_QCAD" = true ]; then
    log_warn "Skipping QCAD installation (--skip-qcad), screenshot will use matplotlib fallback"
else
    if [ -n "$QCAD_TAR_PATH" ] && [ -f "$QCAD_TAR_PATH" ]; then
        # User provided local tar.gz package
        log_info "Installing QCAD using local tar.gz package: $QCAD_TAR_PATH"
        mkdir -p "$QCAD_INSTALL_DIR"
        tar -xzf "$QCAD_TAR_PATH" -C "$QCAD_INSTALL_DIR" --strip-components=1 2>/dev/null
    else
        # Auto-download QCAD Trial (includes dwg2bmp)
        log_info "Attempting to automatically download QCAD Professional Trial..."

        QCAD_URLS=(
            "https://www.qcad.org/archives/qcad/qcad-3.32.6-trial-linux-x86_64.tar.gz"
            "https://www.qcad.org/archives/qcad/qcad-3.32.5-trial-linux-x86_64.tar.gz"
            "https://www.qcad.org/archives/qcad/qcad-3.32.4-trial-linux-x86_64.tar.gz"
        )

        TMP_DIR=$(mktemp -d)
        QCAD_DOWNLOADED=false

        for url in "${QCAD_URLS[@]}"; do
            FILENAME=$(basename "$url")
            log_info "Attempting download: $FILENAME"
            if wget -q --timeout=60 -O "$TMP_DIR/$FILENAME" "$url" 2>/dev/null || \
               curl -sL --connect-timeout 60 -o "$TMP_DIR/$FILENAME" "$url" 2>/dev/null; then
                if [ -s "$TMP_DIR/$FILENAME" ]; then
                    mkdir -p "$QCAD_INSTALL_DIR"
                    tar -xzf "$TMP_DIR/$FILENAME" -C "$QCAD_INSTALL_DIR" --strip-components=1 2>/dev/null
                    if [ -f "$QCAD_INSTALL_DIR/dwg2bmp" ]; then
                        QCAD_DOWNLOADED=true
                        log_ok "QCAD extracted successfully"
                        break
                    fi
                fi
            fi
        done

        rm -rf "$TMP_DIR"

        if [ "$QCAD_DOWNLOADED" = false ]; then
            log_warn "Automatic QCAD download failed. Please download manually:"
            log_warn "  1. Visit https://qcad.org/en/download"
            log_warn "  2. Download QCAD Professional Trial (Linux 64-bit) tar.gz"
            log_warn "  3. Re-run: bash setup.sh --qcad-tar /path/to/qcad-xxx-trial-linux-x86_64.tar.gz"
        fi
    fi

    # Verify installation result
    if [ -f "$QCAD_INSTALL_DIR/dwg2bmp" ]; then
        chmod +x "$QCAD_INSTALL_DIR/dwg2bmp"
        QCAD_INSTALLED=true
        log_ok "QCAD dwg2bmp installed successfully: $QCAD_INSTALL_DIR/dwg2bmp"
    fi
fi

# Install QCAD system dependencies (libGL, etc.)
if [ "$QCAD_INSTALLED" = true ]; then
    log_info "Checking QCAD system dependencies..."
    if [ "$PKG_MANAGER" = "apt-get" ]; then
        sudo apt-get install -y -qq libgl1-mesa-glx libglu1-mesa libxcb-xinerama0 2>/dev/null || true
    else
        sudo $PKG_MANAGER install -y mesa-libGL mesa-libGLU libxcb 2>/dev/null || true
    fi
fi

# ========================== Final Verification ==========================
echo ""
log_info "==================== Environment Configuration Results ===================="

# Python dependencies
python3 -c "import ezdxf" 2>/dev/null && log_ok "✅ ezdxf     — Ready" || log_err "❌ ezdxf     — Not installed"
python3 -c "import matplotlib" 2>/dev/null && log_ok "✅ matplotlib — Ready" || log_err "❌ matplotlib — Not installed"

# xvfb
command -v xvfb-run &>/dev/null && log_ok "✅ xvfb-run  — Ready" || log_warn "⚠️  xvfb-run  — Not installed"

# ODA
if [ "$ODA_INSTALLED" = true ]; then
    log_ok "✅ ODA File Converter — Ready (DWG reading supported)"
else
    log_warn "⚠️  ODA File Converter — Not installed (DXF only)"
fi

# QCAD
if [ "$QCAD_INSTALLED" = true ]; then
    log_ok "✅ QCAD dwg2bmp — Ready (High-quality screenshots)"
else
    log_warn "⚠️  QCAD dwg2bmp — Not installed (screenshots will use matplotlib fallback)"
fi

# Write marker file
cat > "$MARKER_FILE" << EOF
setup_completed=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
oda_installed=$ODA_INSTALLED
qcad_installed=$QCAD_INSTALLED
qcad_path=$QCAD_INSTALL_DIR/dwg2bmp
oda_wrapper=$ASSETS_DIR/oda_wrapper.sh
python_version=$PYTHON_VERSION
arch=$ARCH
pkg_manager=$PKG_MANAGER
EOF

echo ""
log_ok "Environment configuration complete! Marker file written to: $MARKER_FILE"
log_info "You can now use cad_tools.py."
