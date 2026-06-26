# Auto-Start Configuration

## macOS (LaunchAgent)

```bash
cat > ~/Library/LaunchAgents/com.openclaw.ccproxy.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.ccproxy</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/Users/YOU/.openclaw/workspace/ccproxy-ensure.js</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>30</integer>
    <key>EnvironmentVariables</key>
    <dict>
        <key>ANTHROPIC_API_KEY</key>
        <string></string>
    </dict>
</dict>
</plist>
EOF

# Replace /Users/YOU with your actual home path
# Load it:
launchctl load ~/Library/LaunchAgents/com.openclaw.ccproxy.plist
```

## Linux (systemd)

```bash
cat > ~/.config/systemd/user/ccproxy.service << 'EOF'
[Unit]
Description=Claude CLI Proxy for OpenClaw
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/node /home/YOU/.openclaw/workspace/ccproxy-ensure.js
Restart=always
RestartSec=30
Environment=ANTHROPIC_API_KEY=

[Install]
WantedBy=default.target
EOF

systemctl --user enable ccproxy
systemctl --user start ccproxy
```

## Docker / VPS

Add to HEARTBEAT.md so the proxy is checked every heartbeat cycle:

```markdown
## CCProxy Health Check
node /path/to/workspace/ccproxy-ensure.js
```
