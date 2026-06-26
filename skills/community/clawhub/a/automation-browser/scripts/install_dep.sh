# ensure system sbin directories are in PATH (required by dpkg, ldconfig, etc.)
export PATH="/usr/local/sbin:/usr/sbin:/sbin:$PATH"

BASE_URL="https://dldir1v6.qq.com/invc/tt/QB/Public/ubuntu_qb"
QB_DEB="qqbrowser-browser-stable-19.1.1.102-1-20260310.amd64.deb"
QB_RPM="qqbrowser-browser-stable-19.1.1.102-1-20260310.x86_64.rpm"
X5USE_WHL="x5use-0.1.3-py3-none-any.whl"

# create temp directory for downloads and ensure cleanup on exit
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID="$ID"
else
    OS_ID="unknown"
fi

# install qb (skip if already installed)
if which qqbrowser-browser-stable > /dev/null 2>&1; then
    echo "✅ QQ Browser already installed: $(which qqbrowser-browser-stable), skipping..."
else
    if [ "$OS_ID" = "ubuntu" ] || [ "$OS_ID" = "debian" ]; then
        echo "📦 Detected Ubuntu/Debian, using .deb package..."
        curl -fSL -o "$TMP_DIR/$QB_DEB" "${BASE_URL}/${QB_DEB}"
        dpkg -i "$TMP_DIR/$QB_DEB" || apt-get install -f -y
    else
        echo "📦 Detected RPM-based system, using .rpm package..."
        curl -fSL -o "$TMP_DIR/$QB_RPM" "${BASE_URL}/${QB_RPM}"
        yum install -y "$TMP_DIR/$QB_RPM"
    fi

    # Verify QQ Browser installation
    if ! which qqbrowser-browser-stable > /dev/null 2>&1; then
        echo "❌ QQ Browser installation failed: 'qqbrowser-browser-stable' not found in PATH."
        exit 1
    fi
    echo "✅ QQ Browser installed successfully: $(which qqbrowser-browser-stable)"
fi

# install pip3 if not available
if ! which pip3 > /dev/null 2>&1; then
    echo "📦 pip3 not found, installing..."
    if [ "$OS_ID" = "ubuntu" ] || [ "$OS_ID" = "debian" ]; then
        apt-get install -y python3-pip
    else
        yum install -y python3-pip
    fi
fi

# install x5-use-mcp (skip if already installed)
if which x5use-linux-mcp > /dev/null 2>&1; then
    echo "✅ x5use already installed: $(which x5use-linux-mcp), skipping..."
else
    curl -fSL -o "$TMP_DIR/$X5USE_WHL" "${BASE_URL}/${X5USE_WHL}"
    pip3 install --break-system-packages --ignore-installed "$TMP_DIR/$X5USE_WHL"

    # Verify x5use installation
    if ! which x5use-linux-mcp > /dev/null 2>&1; then
        echo "❌ x5use installation failed: 'x5use-linux-mcp' command not found in PATH."
        exit 1
    fi
    echo "✅ x5use installed successfully: $(which x5use-linux-mcp)"
fi