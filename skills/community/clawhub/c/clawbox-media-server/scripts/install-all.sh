#!/bin/bash
# LAN Media Server + Upload Server - One-click installer
# This script sets up both servers and creates systemd services for auto-start.

# set -e  # Disabled to allow continuation if systemd commands fail in this session

echo "🚀 Setting up LAN Media Server & Upload Server..."

# Create shared media directory if missing
mkdir -p "$HOME/projects/shared-media"
echo "📁 Shared media directory: $HOME/projects/shared-media"

# Check dependencies
if ! command -v node &> /dev/null; then
  echo "❌ Node.js is not installed. Please install Node.js first."
  exit 1
fi
echo "✅ Node.js found"

if ! command -v python3 &> /dev/null; then
  echo "❌ Python3 is not installed. Please install Python 3.8+ first."
  exit 1
fi
echo "✅ Python3 found"

# Copy systemd service files
mkdir -p "$HOME/.config/systemd/user"
cp "$(dirname "$0")/../media-server.service" "$HOME/.config/systemd/user/" 2>/dev/null || true
cp "$(dirname "$0")/../upload-server.service" "$HOME/.config/systemd/user/" 2>/dev/null || true
# Also create them if not present (with correct skill name)

# Create systemd services if not exist
if [ ! -f "$HOME/.config/systemd/user/media-server.service" ]; then
  cat > "$HOME/.config/systemd/user/media-server.service" << 'EOF'
[Unit]
Description=LAN Media Server (file hosting)
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.openclaw/workspace/skills/clawbox-media-server/scripts
Environment=MEDIA_PORT=18801
Environment=BIND_ADDR=0.0.0.0
Environment=MEDIA_ROOT=%h/projects/shared-media
ExecStart=/usr/bin/node server.js
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
fi

if [ ! -f "$HOME/.config/systemd/user/upload-server.service" ]; then
  cat > "$HOME/.config/systemd/user/upload-server.service" << 'EOF'
[Unit]
Description=LAN Upload Server (file receiving)
After=network.target

[Service]
Type=simple
WorkingDirectory=%h/.openclaw/workspace/skills/clawbox-media-server/scripts
Environment=UPLOAD_PORT=18802
Environment=BIND_ADDR=0.0.0.0
Environment=UPLOAD_ROOT=%h/projects/shared-media
ExecStart=/usr/bin/python3 upload-server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
fi

# Reload systemd user daemon (if available)
if command -v systemctl &> /dev/null; then
  systemctl --user daemon-reload 2>/dev/null || echo "⚠️  Could not reload systemd user daemon (no user bus?). Services will be available at next login."
  echo "✅ Systemd service files created"
else
  echo "⚠️  systemctl not found — services not enabled. Start servers manually."
fi

# Start services now
echo "🔄 Starting servers..."

# More targeted kill: use exact pattern with -x to match full command line
MY_SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Use pgrep to find exact PIDs and kill them (more precise than pkill -f)
if pgrep -f "node ${MY_SCRIPT_DIR}/server.js" > /dev/null; then
  pkill -x -f "node ${MY_SCRIPT_DIR}/server.js"
  echo "   Stopped old media server"
fi
if pgrep -f "python3 ${MY_SCRIPT_DIR}/upload-server.py" > /dev/null; then
  pkill -x -f "python3 ${MY_SCRIPT_DIR}/upload-server.py"
  echo "   Stopped old upload server"
fi

# Start media server
MEDIA_BIND_ADDR="${MEDIA_BIND_ADDR:-0.0.0.0}"
echo "🔧 Media server binding to: ${MEDIA_BIND_ADDR}"
MEDIA_PORT="${MEDIA_PORT:-18801}" node "$(dirname "$0")/server.js" > /tmp/media-server.log 2>&1 &
# Save PID for later reference
echo $! > /tmp/media-server.pid
echo "✅ Media server started on port 18801"

# Start upload server
UPLOAD_BIND_ADDR="${UPLOAD_BIND_ADDR:-0.0.0.0}"
echo "🔧 Upload server binding to: ${UPLOAD_BIND_ADDR}"
python3 "$(dirname "$0")/upload-server.py" > /tmp/upload-server.log 2>&1 &
# Save PID for later reference
echo $! > /tmp/upload-server.pid
echo "✅ Upload server started on port 18802"

# Give them a moment
sleep 1

# Check status
if ss -tulpn | grep -q ':18801 '; then
  echo "✅ Media server listening on 18801"
else
  echo "❌ Media server failed to start (check /tmp/media-server.log)"
fi

if ss -tulpn | grep -q ':18802 '; then
  echo "✅ Upload server listening on 18802"
else
  echo "❌ Upload server failed to start (check /tmp/upload-server.log)"
fi

# Get LAN IP
LAN_IP=$(hostname -I | awk '{print $1}')
if [ -z "$LAN_IP" ]; then
  LAN_IP="<your-lan-ip>"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 URLs:"
echo "   Upload page: http://$LAN_IP:18802/"
echo "   File listing: http://$LAN_IP:18801/"
echo ""
echo "🔧 To enable auto-start on boot, run:"
echo "   systemctl --user enable media-server.service upload-server.service"
echo ""
echo "📁 Files are stored in: $HOME/projects/shared-media"
echo ""
echo "You can now drag-and-drop files to http://$LAN_IP:18802/ from any device on your LAN."
