<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.agent-bridge</string>

    <key>ProgramArguments</key>
    <array>
        <!-- Update this path to match your actual venv location -->
        <string>/Users/YOUR_USERNAME/.openclaw/agent-bridge-mcp/.venv/bin/python</string>
        <string>/Users/YOUR_USERNAME/.openclaw/agent-bridge-mcp/server.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/.openclaw/agent-bridge-mcp</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/.openclaw/agent-bridge-mcp/bridge.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/.openclaw/agent-bridge-mcp/bridge.log</string>
</dict>
</plist>
