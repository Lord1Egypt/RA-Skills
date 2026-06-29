---
name: en-tencent-novnc-chromium-cdp
description: "One-click deploy remote visual browser — Linux noVNC + Chromium + CDP for headless servers, Windows direct Edge/Chrome CDP takeover. AI Agent and user share the same browser, manual CAPTCHA/QR-code/login fallback, never get stuck on automation walls."
version: 1.0.45
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [novnc, chromium, cdp, xvfb, x11vnc, remote-browser, windows, edge]
---

## 📖 Tutorial

**Two steps, no manual work required.**

**Step 1: Install this skill**

Copy the prompt below and send it to your AI Agent to install automatically:

```
Please check if the clawhub.ai store is already installed. If not, install the clawhub CLI first (npm i -g clawhub or visit https://clawhub.ai), then install the en-tencent-novnc-chromium-cdp skill. If already installed, install en-tencent-novnc-chromium-cdp directly.
```

**Step 2: Use**

Send the following prompt to the AI Agent:

```
Use the en-tencent-novnc-chromium-cdp skill
```

Once the AI Agent receives it, it will fully automate: detect the system environment → install dependencies → start the Chromium remote browser → configure auto-start on boot → first send the noVNC address and password along with other core info → finally confirm with a screenshot. No manual commands needed at any point.

> 💡 After deployment, for login/CAPTCHA/slider verification, manually complete them in the noVNC page, then tell the AI to continue.

# noVNC + Chromium + CDP Remote Visual Controllable Browser (Linux / Windows Dual Platform)

## Skill Overview

This skill supports both Linux and Windows, covering cloud servers and local environments: deploy noVNC + Chromium remote visual browser on Linux servers, or directly take over Edge/Chrome on Windows via CDP remote debugging.

It solves the most common pain point of traditional headless browser automation: when encountering login, QR code scanning, sliders, CAPTCHAs, or security verification, the AI can pause and let the user manually complete the verification in the noVNC page, then resume AI control afterward.

Suitable for: TikTok Creator Center, Instagram, Facebook, YouTube, various backend management systems, and other web scenarios requiring "AI automation + manual verification collaboration."

## Core Capabilities

- **Visual Browser**: Chromium runs on an Xvfb virtual display; users can view the screen in real time through the noVNC web page.
- **AI Controllable**: The Agent connects via CDP to `127.0.0.1:9223`, supporting webpage navigation, clicking, input, page reading, screenshots, etc.
- **Human-AI Collaboration**: When encountering login, QR codes, sliders, or CAPTCHAs, users can handle them manually in noVNC, then the AI continues execution.
- **Permission Pre-check**: Confirms root/sudo permissions before installation; proactively notifies users how to grant permissions if insufficient, avoiding a half-installed state.
- **Security Boundaries**: Only noVNC's `6080/tcp` is recommended for exposure by default; the CDP debug port `9223/tcp` should not be exposed to the public internet.
- **Completion Feedback**: After deployment, the Agent must proactively send the noVNC access address, access password, auto-start status, and port reminders first; screenshots are sent last as supplementary confirmation. Screenshot failure must not block the core information from being delivered.
- **Windows Native Mode**: The Agent automatically starts Edge/Chrome with a remote debugging port, takes over via CDP, with the screen visible locally in real time. Screenshots capture the current page as feedback. No additional components needed.

After deployment, the Agent controls the browser via CDP (see "VII. Controlling the Browser via CDP").

> ⚠️ **Hard Rule (Highest Priority)**: After this skill is deployed, whenever the user asks the AI Agent to "open the browser / view a webpage / take a screenshot / click / log in" or any other browser operation, **it must use the CDP browser deployed by this skill** (`127.0.0.1:9223`). On Linux, this is the Chromium on `:99` inside noVNC; on Windows, it is the Edge/Chrome on the user's local screen. **The Agent must not use its built-in headless browser or start another instance**, otherwise the user and Agent will see different screens. See "XI. Important Principles" for complete rules.

## Server Requirements & Port Reminders

### Remind the user before deployment

This skill requires installing system dependencies, downloading noVNC, starting the Chromium graphical browser, and the VNC forwarding service — many steps. Before executing the installation, the Agent should send a brief reminder letting the user know the deployment will take some time.

Recommended reminder text (choose based on detected environment type):

**CLOUD (Cloud Server) environment:**
```text
Starting deployment of noVNC + Chromium + CDP remote visual controllable browser.

Important: Server should have at least 2C4G.
Port reminder: You must allow 6080/tcp in the cloud server security group; 5900/tcp is for advanced use — optional, restrict source IP if opened. 9223/tcp (CDP debug port) is for Agent local use only and should not be exposed to the public internet.
Estimated time: Usually about 5-15 minutes; if the server has lower specs, slow network, or many dependencies to install, it may take 20-30 minutes. Please be patient and do not interrupt the deployment process.
Token reminder: Smooth deployment is estimated to consume about 20K-50K tokens; if the network is slow, dependency installation fails, or auto-repair/re-tries are needed, it may consume 50K-100K+ tokens. The actual amount depends on the execution process. Before starting, please confirm that your current session/plan has enough remaining tokens — at least 100K+ tokens is recommended to avoid deployment interruption due to insufficient tokens.
Progress reminder: During installation, I will check progress and service status every 30 seconds. Common issues will be auto-repaired first. I will report deployment progress every minute until successful.
```

**NAS environment:**
```text
Starting deployment of noVNC + Chromium + CDP remote visual controllable browser.

Important: NAS should have at least 2C4G.
Port reminder: After deployment, access via the local network address. For external access, set up port forwarding 6080 TCP → <NAS_IP> on your router. 9223/tcp (CDP debug port) is for Agent local use only and should not be exposed.
Estimated time: Usually about 5-15 minutes; if the NAS has lower performance or slow network, it may take 20-30 minutes. Please be patient and do not interrupt the deployment process.
Token reminder: Smooth deployment is estimated to consume about 20K-50K tokens; actual depends on execution. At least 100K+ tokens is recommended.
Progress reminder: During installation, I will check progress every 30 seconds and report every minute until successful.
```

**LOCAL (Local Linux) environment:**
```text
Starting deployment of noVNC + Chromium + CDP remote visual controllable browser.

Important: Local machine should have at least 2C4G.
Port reminder: After deployment, access via the local network address. For external access, set up port forwarding 6080 TCP → <Local_IP> on your router. 9223/tcp (CDP debug port) is for Agent local use only and should not be exposed.
Estimated time: Usually about 5-15 minutes. Please be patient and do not interrupt the deployment process.
Token reminder: Smooth deployment is estimated to consume about 20K-50K tokens.
Progress reminder: During installation, I will check progress every 30 seconds and report every minute until successful.
```

If the detected server has less than 2C4G, additionally warn the user about potential Chromium lag, white screen, or the browser being killed by the system.

### Installation Progress Monitoring & Auto-repair

When deploying this skill, the Agent must not remain silent for long periods. After installation officially begins, the following progress monitoring rules apply:

1. **Check progress every 30 seconds**: Verify if the current install command is still running, check recent logs, and confirm whether it's stuck on dependency installation, software download, service startup, or port listening.
2. **Check key status every 30 seconds**: Focus on whether `Xvfb`, `chromium`, `x11vnc`, and `websockify/noVNC` have started, and whether `6080/tcp` and `9223/tcp` are listening properly.
3. **Auto-repair common issues first**: For missing dependencies, package manager locks, stale processes, port conflicts, Chromium startup failures, incomplete noVNC downloads, etc., first try cleaning up old processes, reinstalling dependencies, restarting services, or re-downloading components.
4. **Report progress every minute**: Send a brief message to the user indicating the current stage (e.g., "Installing system dependencies," "Starting Chromium," "Checking port 6080," "Preparing completion info," "Taking final screenshot confirmation").
5. **Don't spam**: Keep progress messages brief, once per minute; only send additional alerts when user intervention is needed.
6. **Until success or manual intervention needed**: Continuously monitor and report until the noVNC address is accessible, Chromium has opened the Google page, core completion info has been sent, the final screenshot has been sent, or the screenshot failure reason has been clearly reported. If auto-repair fails, clearly tell the user which step failed, the reason, and what they need to do next.

### Minimum Server Configuration

This skill starts a Chromium graphical browser, virtual display, and VNC forwarding service, which consume more resources than normal command-line scripts. Recommended server configuration:

```text
Minimum recommended: 2 core CPU / 4GB RAM (2C4G)
Recommended OS: Debian 10+ / Ubuntu 20.04+
Disk: At least 5GB free space
```

Servers below 2C4G may still start successfully, but are prone to Chromium lag, white screens, high CPU usage on CAPTCHA pages, and the browser being killed by the system.

### Port Opening Instructions

Must open:

- `6080/tcp`: noVNC web access port. Users access the remote Chromium browser via `http://<Server Public IP>:6080/vnc.html`.

Optional:

- `5900/tcp`: Native VNC port. By default, only used by the local websockify forwarder — generally no public exposure needed. Only open if you need to connect via a VNC client directly, and restrict the source IP.
- `9223/tcp`: Chromium CDP debug port. By default, only used by the Agent on the server itself to control the browser. Only open if remote debugging is explicitly needed, and must restrict the source IP to prevent the browser from being hijacked.

## Use Cases

This skill covers two usage modes:

- **Linux Server Mode**: Start a visual browser on a cloud server; users view and manually operate in real time via the noVNC web page; the AI Agent controls the same instance via CDP.
- **Windows Native Mode**: Directly start Edge/Chrome on the user's local machine with a remote debugging port; the Agent takes over via CDP; users see all operations on their local screen in real time.

Typical scenarios:

- Login-type backends: TikTok Creator Center, Instagram Creator Platform, Facebook, YouTube Studio, etc.
- Security verification: Slider CAPTCHAs, QR code login, SMS verification, image CAPTCHAs, device verification, etc.
- Content publishing: Automatically open the publishing page, fill in titles/body/tags/covers, and let the user handle the final manual verification.
- Web debugging: Scenarios where both the user and AI need to see the same browser screen for troubleshooting.

Unsuitable scenarios:

- Pure API call tasks that don't need a browser screen.
- Production environments with extremely high security requirements that cannot expose any remote desktop entry point.
- Linux mode: Servers that cannot open `6080/tcp` or provide root/sudo permissions. (Windows mode has no such restriction.)

Final setup:

**Linux Mode:**
- User access: `http://<Server_IP>:6080/vnc.html`
- Agent control: `http://127.0.0.1:9223/json` / CDP WebSocket
- Browser runs on virtual display `:99`

**Windows Mode:**
- Users see Edge/Chrome on their local screen directly
- Agent control: `http://127.0.0.1:9223/json` / CDP WebSocket
- No additional components needed

> 💡 Unified use of **9223** port to avoid conflict with the AI Agent's built-in Playwright/Chromium on **9222**.

Data flow:

**Linux:** Xvfb → Virtual display `:99` → Chromium (CDP `9223`) → x11vnc → noVNC/websockify → User's browser
**Windows:** Edge/Chrome (CDP `9223`) + Local screen → Agent control, no extra components needed

## 0. System Detection (Step 1, Mandatory)

After loading this skill, the Agent **must first detect the current operating system**:

```bash
# Step 1: Detect operating system
uname -s 2>/dev/null | grep -qi linux && echo "LINUX" || true

# If Linux, further classify the environment type (Cloud Server / NAS / Local Linux)
if [ "$(uname -s)" = "Linux" ]; then
  # Check if it's a cloud server (Tencent Cloud/AliCloud/AWS metadata)
  if curl -s --connect-timeout 2 http://metadata.tencentyun.com/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  elif curl -s --connect-timeout 2 http://100.100.100.200/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  elif curl -s --connect-timeout 2 http://169.254.169.254/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  # Check if it's a NAS (Synology / QNAP)
  elif [ -f /etc/synoinfo.conf ]; then
    echo "ENV_TYPE=NAS"
  elif [ -f /etc/platform.conf ] || [ -f /etc/version ]; then
    echo "ENV_TYPE=NAS"
  else
    echo "ENV_TYPE=LOCAL"
  fi
fi
```

**Branching logic**:

- **Linux detected (CLOUD / NAS / LOCAL)** → Continue with "I. Check System & Server Configuration" and subsequent chapters (noVNC + Chromium remote deployment flow). After completion, send the corresponding address based on environment type:
  - `CLOUD` (Cloud Server) → Send noVNC address with public IP
  - `NAS` (NAS Device) → Send noVNC address with local LAN IP, and remind user to open port 6080 on the NAS control panel
  - `LOCAL` (Local Debian/Ubuntu) → Send noVNC address with local LAN IP, and remind user to allow port 6080 in the system firewall
- **Windows detected** → Skip Linux deployment chapters; jump directly to "XII. Windows System: Remote Debug CDP to Control Edge/Chrome."

> The following chapters "I" through "VI-bis" apply only to Linux systems (including CLOUD / NAS / LOCAL).

> ⚠️ **Hard Rule: System detection is mandatory and cannot be skipped.** After the Agent obtains `ENV_TYPE`, **it must strictly follow the rules below to send the corresponding IP address. No shortcuts or guesswork allowed**:
>
> | ENV_TYPE | Address to Send | Hard Rule |
> |---|---|---|
> | `CLOUD` | **Public IP** | Must use `curl -4 -s https://ifconfig.me` to get the public IP. **Strictly forbidden** to send `192.168.x.x` / `10.x.x.x` / `172.16-31.x.x` private IPs |
> | `NAS` | **LAN IP** | Use `hostname -I` to get the LAN IP. Also remind user to open port 6080 on the NAS control panel |
> | `LOCAL` | **LAN IP** | Use `hostname -I` to get the LAN IP. Also remind user to allow port 6080 in the system firewall |
>
> **Common mistake (prohibited)**: Detecting `CLOUD` but sending a private IP → **Serious error**, the user cannot access from the internet. Detecting `NAS`/`LOCAL` but trying to get a public IP → also wrong, the local environment may not have a public IP at all. The Agent must strictly follow the above mapping and not pick an IP based on "feel."

## I. Check System & Server Configuration

```bash
cat /etc/os-release | head -3
uname -m
nproc
free -h
df -h /
```

Recommended environment: Debian 10+ / Ubuntu 20.04+ / modern Linux distributions.

Configuration requirements: At least **2 core CPU / 4GB RAM (2C4G)** recommended. If memory is below 4GB, the Agent should first warn the user about potential Chromium lag, white screen, or the browser being killed, then proceed with installation.

## II. Permission Pre-check (Mandatory)

Deploying this skill requires installing system packages, writing to `/opt` and `/root/start-remote-browser.sh`, requiring `root` or usable `sudo` privileges.

```bash
if [ "$(id -u)" = "0" ]; then
  echo "PERMISSION_OK: Currently root user"
elif command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
  echo "PERMISSION_OK: Current user has passwordless sudo"
else
  echo "PERMISSION_DENIED: Current user is not root and cannot use passwordless sudo."
fi
```

If output is `PERMISSION_OK`, proceed directly with deployment.

If output is `PERMISSION_DENIED`, handle in the following order of priority:

**First choice: Configure passwordless sudo**

Guide the user to run one command on the server terminal (the password never leaves the user's machine):

```bash
echo "$(whoami) ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/hermes-deploy
```

After completion, the Agent can continue deployment via `sudo`. After deployment is done, run `sudo rm /etc/sudoers.d/hermes-deploy` to revoke the permission.

**Fallback: Provide SSH credentials**

Only use this when the user cannot access the server terminal. The Agent should explain the purpose of the credentials:

```text
Current environment lacks sufficient permissions. Please provide the following SSH information so I can log in to the server and complete the installation:

- Server IP
- SSH port (default 22)
- SSH username
- SSH password

The above credentials will only be used for the following operations, nothing else:
1. Install system dependencies (apt install xvfb x11vnc git python3-pip, etc.)
2. Download noVNC to /opt/noVNC
3. Create the startup script /root/start-remote-browser.sh
4. Configure systemd auto-start (write to /etc/systemd/system/)
5. Open firewall port 6080

After deployment, please change your password immediately.
```

> ⚠️ The Agent must not store or record the credentials and must remind the user to change the password after deployment.

## III. Install Dependencies

Debian / Ubuntu:

```bash
apt update && apt upgrade -y
apt install -y xvfb x11vnc git python3-pip curl wget ca-certificates
```

### Prioritize installing deb-version Chromium/Chrome

This skill controls the browser via CDP. When installing the browser, **prioritize installing the deb-package form of Chromium/Chrome**. If deb installation fails, automatically fall back to other available Chromium/Chrome versions to ensure the deployment flow is uninterrupted.

Installation should first detect the system type, then follow the "deb first, auto-fallback on failure" strategy:

```bash
. /etc/os-release

if [ "$ID" = "debian" ]; then
  apt install -y chromium || apt install -y chromium-browser || true
elif [ "$ID" = "ubuntu" ]; then
  echo "Ubuntu environment: prioritise installing deb-version Chrome as the Chromium/CDP-compatible browser."
  if wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; then
    apt install -y /tmp/google-chrome-stable_current_amd64.deb || true
  fi
  if command -v google-chrome-stable >/dev/null 2>&1; then
    ln -sf /usr/bin/google-chrome-stable /usr/local/bin/chromium
    # Chrome and Chromium share the same CDP debug protocol and user-data-dir.
    # The --disable-session-crashed-bubble / --restore-last-session=false and ExecStartPre in the 「VI-bis」 systemd template also apply to Chrome.
  else
    echo "Deb-version Chrome installation failed, trying system repo Chromium/Chromium Browser."
    apt install -y chromium || apt install -y chromium-browser || true
  fi
else
  apt install -y chromium || apt install -y chromium-browser || true
fi

CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
if [ -z "$CHROME_BIN" ]; then
  echo "ERROR: Chromium/Chrome executable not found"
  exit 1
fi

echo "Browser path: $CHROME_BIN"
```

Install noVNC and websockify:

```bash
cd /opt
if [ ! -d /opt/noVNC ]; then
  git clone https://github.com/novnc/noVNC.git
fi
pip3 install websockify --break-system-packages
```

If the noVNC master version shows ES module errors in Chrome, pin to a stable release:

```bash
cd /opt/noVNC
git fetch --tags
git checkout v1.6.0
```

## IV. Open Ports

Port opening rules vary by environment type. The Agent must select the appropriate firewall commands based on the previously determined environment type (`$ENV_TYPE`):

**CLOUD (Cloud Server):**
```bash
# System firewall allows noVNC
ufw allow 6080/tcp || true
ufw reload || true

# Cloud vendor security group also needs to allow:
# - 6080/tcp: noVNC web access port
# - 9223/tcp: CDP debug port, **not recommended for public exposure**, for Agent local 127.0.0.1 only
```

**NAS:**
```bash
# NAS deployment: direct intranet access, no firewall operation needed.
# For external access: set up port forwarding 6080 TCP → <NAS_IP> on your router
# 9223/tcp CDP port is for local use only, do not forward.
echo "NAS environment: access noVNC via intranet address. For external access, configure port forwarding for 6080 on your router."
```

**LOCAL (Local Linux):**
```bash
# System firewall allows noVNC
ufw allow 6080/tcp || true
ufw reload || true

# For external access: set up port forwarding 6080 TCP → <local_IP> on your router
# 9223/tcp CDP port is for local use only, do not forward.
```

## V. Create One-Click Startup Script

### 1. Generate noVNC Access Password (Mandatory)

To prevent the noVNC port (6080) from being exposed to the public bare, allowing anyone to take over the browser, an **8-character random password** (alphanumeric) must be generated before startup. x11vnc must start with password mode. The Agent must save the plaintext password to a fixed path for easy retrieval after deployment.

```bash
# 8-character random password (alphanumeric mix)
NOVNC_PASS=$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 8)
echo -n "$NOVNC_PASS" > /root/.novnc_password
chmod 600 /root/.novnc_password

# Use x11vnc's own tool to generate the VNC password file
x11vnc -storepasswd "$NOVNC_PASS" /root/.vncpasswd
chmod 600 /root/.vncpasswd

echo "noVNC access password generated: $NOVNC_PASS"
echo "Plaintext stored at: /root/.novnc_password (root-readable only)"
echo "VNC password file: /root/.vncpasswd"
```

> When starting x11vnc later, you must use `-rfbauth /root/.vncpasswd`, **not `-nopw`**.

### 2. Write `/root/start-remote-browser.sh`

Write `/root/start-remote-browser.sh`:

```bash
cat > /root/start-remote-browser.sh <<'SCRIPT_END'
#!/bin/bash
set -e

pkill -9 -f x11vnc 2>/dev/null || true
pkill -9 -f Xvfb 2>/dev/null || true
pkill -9 -f websockify 2>/dev/null || true
pkill -9 -f 'chromium.*remote-debugging-port=9223' 2>/dev/null || true
sleep 2

echo "[1/4] Starting virtual display..."
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1
export DISPLAY=:99

echo "[2/4] Starting Chromium (CDP:9223)..."
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
if [ -z "$CHROME_BIN" ]; then
  echo "ERROR: Chromium/Chrome executable not found"
  exit 1
fi
# CDP is for Agent local control only, listens on 127.0.0.1, not exposed externally.
# ⚠️ Do NOT add --headless or --headless=new, otherwise noVNC screen won't display.
"$CHROME_BIN" \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9223 \
  --remote-debugging-address=127.0.0.1 \
  --remote-allow-origins='*' \
  --window-size=1920,1080 \
  --start-maximized \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir=/root/.chromium-remote \
  --restore-last-session=false \
  https://www.google.com/ &
sleep 3

echo "[3/4] Starting x11vnc..."
x11vnc -display :99 -forever -rfbauth /root/.vncpasswd -quiet -listen 127.0.0.1 &
sleep 1

echo "[4/4] Starting noVNC (port:6080)..."
websockify --web /opt/noVNC 6080 127.0.0.1:5900 &
sleep 1

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "========================================"
echo "  ✅ Remote browser ready"
echo "  User access: http://${IP}:6080/vnc.html"
echo "  CDP: http://127.0.0.1:9223/json (Agent local only)"
echo "========================================"
SCRIPT_END

chmod +x /root/start-remote-browser.sh
```

## VI. Start the Remote Browser

```bash
bash /root/start-remote-browser.sh
```

After starting, user access:

```text
http://<Server_IP>:6080/vnc.html
```

CDP check address:

```bash
curl -s http://127.0.0.1:9223/json/version
curl -s http://127.0.0.1:9223/json
```

**⚠️ At this stage of deployment, the manually started Chromium is still running in the background. Before configuring systemd auto-start, you must kill the manual process first to avoid two Chromium instances contending for the same `--user-data-dir`, causing piled-up tabs.**

```bash
pkill -9 -f "(chromium|chrome).*remote-debugging-port=9223" 2>/dev/null || true
sleep 2
```

> Otherwise: manual script opens Google → systemd auto-start opens another → OOM restart opens another → stacking into three Google pages.

## VI-bis. Configure Auto-Start on Boot (Mandatory)

To ensure that noVNC + Chromium + CDP automatically recover after a server reboot, the entire service must be set up as a **systemd unit**, not just relying on a one-shot `bash /root/start-remote-browser.sh`.

After deployment, the following steps must be executed, using `enable --now` to make the service **take effect immediately + boot auto-start**:

```bash
# 1) Xvfb virtual display
cat > /etc/systemd/system/xvfb.service <<'EOF'
[Unit]
Description=Xvfb virtual display :99
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24 -ac
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 2) x11vnc (must use -rfbauth for password mode)
cat > /etc/systemd/system/x11vnc.service <<'EOF'
[Unit]
Description=x11vnc server on :99 (password protected)
After=xvfb.service
Requires=xvfb.service

[Service]
Type=simple
Environment=DISPLAY=:99
ExecStart=/usr/bin/x11vnc -display :99 -forever -shared -rfbauth /root/.vncpasswd -rfbport 5900 -quiet
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 3) noVNC websockify
cat > /etc/systemd/system/novnc.service <<'EOF'
[Unit]
Description=noVNC websockify on 6080
After=x11vnc.service
Requires=x11vnc.service

[Service]
Type=simple
ExecStart=/usr/local/bin/websockify --web=/opt/noVNC 6080 localhost:5900
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 4) Chromium + CDP (auto-detect available Chromium/Chrome binary)
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable)
cat > /etc/systemd/system/chromium-remote.service <<EOF
[Unit]
Description=Chromium with CDP on :9223, display :99
After=xvfb.service
Requires=xvfb.service
StartLimitBurst=3
StartLimitInterval=120

[Service]
Type=simple
Environment=DISPLAY=:99
# Kill any residual chromium/chrome processes before starting to avoid user-data-dir conflicts causing tab stacking
ExecStartPre=/usr/bin/pkill -9 -f "(chromium|chrome).*remote-debugging-port=9223" || true
ExecStartPre=/bin/sleep 2
# ⚠️ Do NOT add --headless or --headless=new, otherwise noVNC screen won't display.
ExecStart=${CHROME_BIN} --no-sandbox --disable-gpu --disable-dev-shm-usage --disable-session-crashed-bubble --restore-last-session=false --remote-debugging-port=9223 --remote-debugging-address=127.0.0.1 --remote-allow-origins=* --user-data-dir=/root/.chromium-remote --no-first-run --no-default-browser-check --window-size=1920,1080 --start-maximized https://www.google.com/
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now xvfb.service x11vnc.service novnc.service chromium-remote.service
```

Verification (should all show `active`):

```bash
systemctl is-active xvfb x11vnc novnc chromium-remote
ss -tlnp | grep -E ':6080|:5900|:9223'
```

> After the server reboots, neither the Agent nor the user needs to manually run `start-remote-browser.sh` — the entire service comes up automatically.

---

**Deployment and auto-start are fully complete. Now follow these three wrap-up steps in order — cannot be skipped or reordered:**

**Step 1: Open Google to confirm** — Refer to the CDP code in Section VII, change `url` to `'https://www.google.com/'`, only call `Page.enable → Page.navigate → sleep(3)`, remove `Runtime.enable` and `Runtime.evaluate`.

**Step 2: Send core completion info first** — Use the template in Section VIII to send the noVNC address, access password, auto-start status, port reminders, and CAPTCHA handling instructions. **This must be sent first, not waiting for the screenshot to succeed.**

**Step 3: Take and send the screenshot last** — Run `DISPLAY=:99 import -window root /tmp/remote-browser.png`, then send the image as per the screenshot delivery method in Section VIII. The screenshot is the final supplementary confirmation. If screenshot fails, report the failure reason after the core info has been sent and attempt repair/retry. Screenshot failure must never prevent the address and password from being delivered.

---

## VII. Controlling the Browser via CDP (Reference Code — Use When Needing to Open a Webpage)

Control the already-started Chromium using Python:

```bash
python3 - <<'PY'
import json, time, urllib.request
import websocket

url = 'https://example.com'
tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
ws = websocket.create_connection(
    page['webSocketDebuggerUrl'],
    header=['Origin: http://127.0.0.1:9223'],
    timeout=20,
)

msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg

call('Page.enable')
call('Runtime.enable')
call('Page.navigate', {'url': url})
time.sleep(3)
res = call('Runtime.evaluate', {
    'expression': '({title: document.title, url: location.href})',
    'returnByValue': True,
})
print(json.dumps(res['result']['result']['value'], ensure_ascii=False, indent=2))
ws.close()
PY
```

If the websocket package is missing:

```bash
pip3 install websocket-client --break-system-packages
```

## VIII. Reply Template

When wrapping up, the core completion info must be sent first, then the screenshot as the final step. Screenshot generation or delivery failure must not prevent the noVNC address, access password, and other core info from being delivered.

### 1. Pre-send Preparation

Run the script to get the noVNC address:

```bash
# Select IP based on environment type (ENV_TYPE was set in the "0. System Detection" step)
if [ "$ENV_TYPE" = "CLOUD" ]; then
  # Cloud server: prioritise public IP
  PUBLIC_IP=$(curl -4 -s https://ifconfig.me 2>/dev/null || curl -4 -s https://api.ipify.org 2>/dev/null || true)
  if [ -n "$PUBLIC_IP" ]; then
    NOVNC_URL="http://${PUBLIC_IP}:6080/vnc.html"
  else
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    NOVNC_URL="http://${LOCAL_IP}:6080/vnc.html"
  fi
else
  # NAS / Local Linux: use LAN IP directly
  LOCAL_IP=$(hostname -I | awk '{print $1}')
  NOVNC_URL="http://${LOCAL_IP}:6080/vnc.html"
fi
echo "$NOVNC_URL"
echo "ENV_TYPE=$ENV_TYPE"
```

Read the access password:

```bash
cat /root/.novnc_password
```

### 2. Send Order — Hard Rule (Highest Priority)

1. **Send core completion info first**: The noVNC address, access password, browser status, auto-start status, port reminders, and CAPTCHA handling instructions must be sent to the user first.
2. **Screenshot last**: After the core info is sent, take and send the screenshot. The screenshot is just a visual confirmation and must not block the core info.
3. **Screenshot failure handling**: If the screenshot command fails, image copy fails, or the platform fails to send the image, do not suppress the core info. First ensure the user has the access entry point, then explain the screenshot failure reason and attempt repair/retry.
4. **Forbidden to only give a path**: After the screenshot is successfully generated, it must be sent via the current platform's image/file capability. Do not just say "the screenshot is at `/tmp/remote-browser.png`."
5. **Single-message scenario**: If the Agent can only send one final reply, put the text core info at the beginning and the screenshot tag at the end.

### 3. Linux Mode Reply

```text
Remote Chromium browser is ready:

- noVNC address: http://<IP>:6080/vnc.html
- noVNC access password: <read from /root/.novnc_password>
- Browser status: Already opened Google page. Screenshot will be sent as final supplementary confirmation.
- Auto-start: systemd configured, automatically starts on reboot.
- CDP address: For Agent local control only; not recommended for public exposure.
- If you encounter login, CAPTCHA, or slider verification, manually complete them in the noVNC page, then tell me to continue.
```

**Append based on environment type (Agent must strictly use the detected ENV_TYPE):**
- `CLOUD`: Please confirm your cloud server security group has allowed 6080/tcp.
- `NAS`: 🌐 This is the NAS LAN address. Please allow 6080/tcp in the NAS control panel; for router access, set up port forwarding.
- `LOCAL`: 🌐 This is the local LAN address. Please ensure the firewall has allowed 6080/tcp.

**🔴 Environment Misidentification Prohibition (Highest Priority):**
- ❌ For `NAS`/`LOCAL` users, **strictly forbidden** to mention "cloud security group," "cloud server," "Tencent Cloud," or "AliCloud."
- ❌ `NAS`/`LOCAL` environments: **Strictly forbidden** to send a noVNC link with a public IP (the public IP does not belong to the user and won't work).
- ❌ `CLOUD` environments: **Strictly forbidden** to send a private IP address to the user.
- ❌ **Strictly forbidden** to skip the environment detection step and reply assuming a cloud server.

**Port reminder:** `9223/tcp` is the CDP debug port, for Agent local use only; not recommended for public exposure.

#### Final Step: Screenshot Delivery

> ⚠️ **Hard Rule: Screenshot must be taken and sent AFTER the core completion info. For QQ/QQbot channels, screenshots must strictly follow the rules below. Violation equals deployment failure. The following methods have been verified to work on QQ channels. The Agent must follow them exactly, without deviation.**

**Step 1: Generate and copy the screenshot to the QQbot media directory (must execute bash commands, not just describe them)**

```bash
DISPLAY=:99 import -window root /tmp/remote-browser.png
mkdir -p ~/.openclaw/media/qqbot
cp /tmp/remote-browser.png ~/.openclaw/media/qqbot/remote-browser.png
```

**Step 2: Send using the `<qqmedia>` tag (the Agent must output the following tag in its reply, exactly as shown)**

```text
<qqmedia>/root/.openclaw/media/qqbot/remote-browser.png</qqmedia>
```

> 🔴 **Prohibitions (violating any one equals deployment failure)**:
> - 🚫 **Strictly forbidden** to use the `MEDIA:/tmp/remote-browser.png` format to send images (QQ channel does not support it; the user won't see it)
> - 🚫 **Strictly forbidden** to skip the first step's three bash commands: `DISPLAY=:99 import` + `mkdir -p` + `cp` (describing without executing = file doesn't exist = can't send)
> - 🚫 **Strictly forbidden** to write the `<qqmedia>` tag in any variant form (e.g., `<qq-media>`, `<qqmedia>` with missing `/root` prefix, relative paths, etc.)
> - 🚫 **Strictly forbidden** to decide "other methods might also work" — the QQ channel only recognizes `<qqmedia>` + absolute path. No exceptions.
> - 🚫 **Strictly forbidden to send duplicates**: Send the same screenshot **only once**. If you use `<qqmedia>`, do not also add a `MEDIA:` tag, or the user will receive two identical images.
>
> ✅ **Correct example (Agent must follow this pattern)**:
> 1. Terminal: `DISPLAY=:99 import -window root /tmp/remote-browser.png && mkdir -p ~/.openclaw/media/qqbot && cp /tmp/remote-browser.png ~/.openclaw/media/qqbot/remote-browser.png`
> 2. Reply: `<qqmedia>/root/.openclaw/media/qqbot/remote-browser.png</qqmedia>`

**Platform branching hard rule (highest priority):**

- **Only when the current session is explicitly a QQ / QQbot channel is the `<qqmedia>` tag allowed.**
- Telegram / Discord / Email / Terminal / Web UI / Other platforms: **Strictly forbidden** to use `<qqmedia>` — the image will appear as raw text or fail to send.
- Other channels must use the media delivery method supported by that platform. If the Agent supports a universal media tag, `MEDIA:/tmp/remote-browser.png` should be used by default.
- For unknown platforms, do not apply QQ-specific rules. Default to universal `MEDIA:` or the platform's official attachment/image delivery capability.

**Other channels (Telegram / Discord / Email / Terminal / Web UI, etc.):**

```text
MEDIA:/tmp/remote-browser.png
```

### 4. Windows Mode Reply

```text
✅ Browser is fully under AI Agent control.

- Browser: Edge/Chrome (CDP port 9223)
- You can see all operations on your screen and take over manually at any time
- Please do not close this browser window
- If you encounter login, CAPTCHA, or slider verification, just handle it directly and tell me to continue
```

Windows mode must also send the takeover completion message above first, then the screenshot as the final step. Screenshot is taken via CDP `Page.captureScreenshot` (full code in 「XII-3 Screenshot the Current Page」). Screenshot failure must not affect the takeover completion info.

## IX. Verification Checklist

### Linux Mode Verification

```bash
ss -tlnp | grep -E '6080|5900|9223'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:6080/vnc.html
curl -s http://127.0.0.1:9223/json/version
```

Should satisfy:

- `6080` is listening
- `5900` is listening for local VNC
- `9223` is listening for CDP
- `vnc.html` returns `200`
- User can see the remote Chromium screen in their browser

### Windows Mode Verification

```bash
curl -s http://127.0.0.1:9223/json/version
curl -s http://127.0.0.1:9223/json
```

Should satisfy:

- `9223` is listening for CDP
- `json/version` returns browser info
- `json` returns at least one page-type tab
- User can see the Edge/Chrome browser window on their local screen

## X. FAQ

### Linux Mode

### 1. noVNC Opens Blank or Can't Connect

Check processes:

```bash
ps -ef | grep -E 'Xvfb|chromium|x11vnc|websockify' | grep -v grep
ss -tlnp | grep -E '6080|5900|9223'
```

Re-run:

```bash
bash /root/start-remote-browser.sh
```

### 2. Port 6080 Inaccessible from Outside

Need to check both:

- Whether the cloud server security group allows `6080/tcp`
- Whether the system firewall allows `6080/tcp`
- Whether `websockify` is listening on `0.0.0.0:6080`

### 3. CDP WebSocket 403

Chromium startup parameters must include:

```bash
--remote-allow-origins='*'
```

When connecting via Python websocket, include the Origin header:

```python
websocket.create_connection(ws_url, header=['Origin: http://127.0.0.1:9223'])
```

### 4. Browser Screen Freezes

Clean restart:

```bash
pkill -9 -f chromium || true
pkill -9 -f Xvfb || true
pkill -9 -f x11vnc || true
pkill -9 -f websockify || true
bash /root/start-remote-browser.sh
```

### 5. noVNC Frontend JS Errors

If using the noVNC master branch causes browser compatibility issues, pin to a stable version:

```bash
cd /opt/noVNC
git fetch --tags
git checkout v1.6.0
bash /root/start-remote-browser.sh
```

### Windows Mode

### 6. Edge/Chrome Won't Start in CDP Mode

The browser may already be running. Close all Edge/Chrome windows first, then execute:

```powershell
taskkill /F /IM msedge.exe
taskkill /F /IM chrome.exe
start msedge --remote-debugging-port=9223 --remote-allow-origins=*
```

### 7. CDP Port 9223 Occupied

Check port usage and release:

```powershell
netstat -ano | findstr :9223
taskkill /F /PID <PID>
```

Then restart the browser.

### 8. CDP WebSocket 403 / Connection Refused

Make sure startup parameters include `--remote-allow-origins=*`. If still getting 403, try including the Origin header when connecting:

```python
websocket.create_connection(ws_url, header=['Origin: http://127.0.0.1:9223'])
```

## XI. Important Principles

> ⚠️ After deployment, all browser operations by the Agent must control the browser deployed by this skill via CDP (`127.0.0.1:9223`) — on Linux, the Chromium on display `:99` inside noVNC; on Windows, the user's local Edge/Chrome. **Strictly forbidden to add `--headless` or `--headless=new` startup parameters to Chromium** — otherwise the noVNC screen won't display properly. **The Agent must not use its built-in headless browser or other instances** — otherwise the user and Agent see different screens and can't collaborate on CAPTCHAs. The only exception: when the user explicitly requests a different browser.

## XII. Windows System: Remote Debug CDP to Control Edge/Chrome

When "0. System Detection" determines the OS is Windows, follow the flow below. **Windows mode requires no dependency installation — directly use the system's built-in Edge or Chrome browser.**

### Startup Flow

**The Agent must prioritise automatically trying to start the browser.** Only if that fails should the user be asked to do it manually.

#### 1. Auto-start (Agent Executes)

The Agent first tries to start Edge, falling back to Chrome on failure:

```powershell
# Prioritise Edge
start msedge --remote-debugging-port=9223 --remote-allow-origins=*
```

```powershell
# Fall back to Chrome if Edge is unavailable
start chrome --remote-debugging-port=9223 --remote-allow-origins=*
```

If both commands fail (browser not installed, insufficient permissions, etc.), then tell the user to manually execute:

```text
Open PowerShell or CMD as Administrator and execute the following commands:

Edge:
start msedge --remote-debugging-port=9223 --remote-allow-origins=*

Or Chrome:
start chrome --remote-debugging-port=9223 --remote-allow-origins=*
```

#### 2. Verify CDP Connectivity

```bash
curl -s http://127.0.0.1:9223/json/version
```

#### 3. Screenshot the Current Page

After confirming connectivity, take a screenshot of the current default page (new tab or browser homepage) via CDP. **Windows mode does not need to navigate to Google — just capture whatever the browser is currently showing.**

```bash
# Get current pages
curl -s http://127.0.0.1:9223/json
# Capture page screenshot via CDP, save as PNG
python3 - <<'PY'
import json, base64, urllib.request
tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
import websocket
ws = websocket.create_connection(page['webSocketDebuggerUrl'], header=['Origin: http://127.0.0.1:9223'], timeout=20)
msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg
call('Page.enable')
res = call('Page.captureScreenshot', {'format': 'png'})
with open('/tmp/browser_screenshot.png', 'wb') as f:
    f.write(base64.b64decode(res['result']['data']))
print('Screenshot saved: /tmp/browser_screenshot.png')
ws.close()
PY
```

After the screenshot is generated, send it as the final step via MEDIA. If it's a QQ/QQbot channel, use the `<qqmedia>` rules from Section VIII.

#### 4. Completion Reminder

Refer to the Windows reply template in 「VIII-4」 — **send the takeover completion message first**, then execute 「XII-3」 to take a screenshot and send it as the final step. Screenshot failure must not block the takeover completion info.

### Windows Mode: Subsequent Usage

After takeover is complete, all subsequent browser operations by the Agent (opening pages, clicking, inputting, screenshots, etc.) control this browser instance via the CDP interface at `127.0.0.1:9223`. Users can see all operations in real time on their local screen and can manually intervene whenever encountering logins or CAPTCHAs.
