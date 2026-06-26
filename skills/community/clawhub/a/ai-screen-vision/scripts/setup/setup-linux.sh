#!/bin/bash
# Linux setup script for screen-vision skill
# Usage: setup-linux.sh [--headless|--desktop]

set -e

MODE="desktop"
if [ "$1" = "--headless" ]; then
    MODE="headless"
fi

echo "=== Screen-Vision Linux Setup ==="
echo "Mode: $MODE"
echo ""

# Detect package manager
if command -v apt-get &>/dev/null; then
    PKG="apt"
    echo "Package manager: apt"
elif command -v yum &>/dev/null; then
    PKG="yum"
    echo "Package manager: yum"
elif command -v dnf &>/dev/null; then
    PKG="dnf"
    echo "Package manager: dnf"
else
    echo "ERROR: Unsupported package manager"
    exit 1
fi

# Install common tools
echo "[1/6] Installing common tools..."
case "$PKG" in
    apt)  apt-get update -qq && apt-get install -y -qq scrot xdotool python3 python3-pip imagemagick;;
    yum)  yum install -y scrot xdotool python3 python3-pip ImageMagick;;
    dnf)  dnf install -y scrot xdotool python3 python3-pip ImageMagick;;
esac

# Install Python dependencies
echo "[2/6] Installing Python dependencies..."
pip3 install --quiet Pillow numpy 2>/dev/null || pip install --quiet Pillow numpy

# Headless mode: install desktop environment
if [ "$MODE" = "headless" ]; then
    echo "[3/6] Installing XFCE4 desktop environment (headless)..."
    case "$PKG" in
        apt)  apt-get install -y -qq xfce4 xfce4-terminal chromium-browser 2>/dev/null || \
              apt-get install -y -qq xfce4 xfce4-terminal chromium;;
        yum)  yum groupinstall -y "Xfce" && yum install -y chromium;;
        dnf)  dnf groupinstall -y "Xfce" && dnf install -y chromium;;
    esac
    
    echo "[4/6] Installing noVNC and VNC server..."
    case "$PKG" in
        apt)  apt-get install -y -qq novnc tigervnc-standalone-server tigervnc-common python3-websockify;;
        *)    echo "WARN: Auto VNC setup only supported on apt. Manual setup needed.";;
    esac
    
    echo "[5/6] Configuring VNC server..."
    # VNC config
    mkdir -p ~/.vnc
    cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &
EOF
    chmod +x ~/.vnc/xstartup
    
    # Set VNC password (default: screen123)
    echo "screen123" | vncpasswd -f > ~/.vnc/passwd
    chmod 600 ~/.vnc/passwd
    
    echo "[6/6] Creating start/stop scripts..."
    cat > /usr/local/bin/sv-start << 'SCRIPT'
#!/bin/bash
# Start virtual desktop for screen-vision
echo "Starting VNC server on display :1..."
vncserver :1 -geometry 1024x768 -depth 24 -localhost no 2>/dev/null || \
vncserver :1 -geometry 1024x768 -depth 24

echo "Starting noVNC on port 6080..."
websockify --web=/usr/share/novnc/ 6080 localhost:5901 &>/tmp/novnc.log &
NOVNC_PID=$!

echo "Virtual desktop started!"
echo "  VNC:  vnc://localhost:5901"
echo "  noVNC: http://localhost:6080/vnc.html"
echo "  PID:  $NOVNC_PID"
echo $NOVNC_PID > /tmp/sv-novnc.pid
SCRIPT
    chmod +x /usr/local/bin/sv-start
    
    cat > /usr/local/bin/sv-stop << 'SCRIPT'
#!/bin/bash
echo "Stopping screen-vision desktop..."
vncserver -kill :1 2>/dev/null
kill $(cat /tmp/sv-novnc.pid 2>/dev/null) 2>/dev/null
rm -f /tmp/sv-novnc.pid
echo "Stopped."
SCRIPT
    chmod +x /usr/local/bin/sv-stop

else
    echo "[3/6] Desktop mode - skipping desktop environment install"
    echo "[4/6] Desktop mode - skipping VNC install"
    echo "[5/6] Desktop mode - skipping VNC config"
    echo "[6/6] Verifying display..."
    
    if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
        echo "WARN: No DISPLAY detected. Use --headless mode for servers."
    else
        echo "Display: ${DISPLAY:-$WAYLAND_DISPLAY}"
    fi
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Installed tools:"
command -v scrot && echo "  ✅ scrot"
command -v xdotool && echo "  ✅ xdotool"
python3 -c "from PIL import Image; print('  ✅ Pillow')" 2>/dev/null
echo ""
if [ "$MODE" = "headless" ]; then
    echo "To start virtual desktop: sv-start"
    echo "To stop: sv-stop"
    echo "Access noVNC: http://<ip>:6080/vnc.html"
fi
