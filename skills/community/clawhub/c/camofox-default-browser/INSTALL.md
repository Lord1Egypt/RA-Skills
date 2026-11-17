# Camofox Default Browser — Installation Guide

---

## Overview

Camofox is a Firefox fork with C++-level anti-detection fingerprint spoofing, designed for browser automation that needs to bypass bot detection services like Google reCAPTCHA, Cloudflare Turnstile, WAFs, and commercial scraping protections. This document covers installation on Linux (recommended), Docker deployment, verification, and cleanup.

---

## 1. Prerequisites

### Operating System
- **Recommended:** Ubuntu 22.04 LTS or Debian 12+ (x86_64 / AMD64)
- Also works on: CentOS 8+, Fedora, Arch Linux, Alpine (limited support)
- macOS and Windows require manual binary download from [GitHub releases](https://github.com/jo-inc/camofox-browser/releases)

### Node.js
- **Minimum:** Node.js 18.x (LTS recommended)
- Required for the OpenClaw plugin server (`server.js`)
- Verify with `node --version` — output should be `v18.x.x` or higher
- If not installed: follow official instructions at https://nodejs.org

### Disk Space
- **Minimum:** 500 MB free disk space
  - Camoufox binary (Firefox-based): ~300-400 MB extracted
  - Node.js packages and cache: ~100-150 MB
- Recommended: 1 GB+ if planning to use cookie import features extensively

### RAM
- **Minimum:** 2 GB RAM
- Normal operation: 200-400 MB during active browser sessions
- Idle memory footprint: ~40 MB (daemon only)
- Each tab adds approximately 150-300 MB depending on page complexity
- Recommended: 4 GB+ for multi-tab usage

---

## 2. Step-by-Step Installation

### Step 1: Install System Dependencies

These libraries are required by the Firefox-based Camoufox binary to render pages correctly:

```bash
sudo apt-get update && sudo apt-get install -y \
  libgtk-3-0 \
  libgdk-pixbuf2.0-0 \
  libdbus-glib-1-2 \
  libxt6 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libatk-bridge2.0-0 \
  libdrm2 \
  libgbm1 \
  xvfb
```

> **Note:** On headless servers (no display), `xvfb` provides a virtual framebuffer so the browser can run without a physical monitor.

### Step 2: Download Camoufox Binary

Create the cache directory and download the latest release:

```bash
# Create target directory
mkdir -p /root/.cache/camoufox

# Download latest release (adjust URL for your platform)
# Check https://github.com/jo-inc/camofox-browser/releases for the latest version
CAMOUFOX_VERSION="latest"
curl -L -o /tmp/camoufox.tar.gz \
  "https://github.com/jo-inc/camofox-browser/releases/latest/download/camoufox-linux-amd64.tar.gz"

# Extract
tar xzf /tmp/camoufox.tar.gz -C /root/.cache/camoufox/
chmod +x /root/.cache/camoufox/camoufox

# Cleanup
rm -f /tmp/camoufox.tar.gz
```

If you need a specific version, replace `latest` with e.g. `v0.0.1`.

### Step 3: Set Environment Variables

The OpenClaw plugin needs to know where the Camoufox binary lives:

```bash
# Add to ~/.bashrc for persistence
echo 'export CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox' >> ~/.bashrc
source ~/.bashrc

# Verify it's set
echo $CAMOUFOX_EXECUTABLE
```

Optional but recommended environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `CAMOUFOX_EXECUTABLE` | unset | Path to camoufox binary (required) |
| `CAMOUFOX_API_KEY` | none | API key for authenticated features (cookie import) |
| `CAMOUFOX_CRASH_REPORT_ENABLED` | true | Set `false` to disable anonymized crash telemetry |

### Step 4: Install OpenClaw Plugin

Place the skill in the OpenClaw skills directory:

```bash
# Clone or copy the skill into the workspace
cp -r /path/to/camofox-default-browser ~/.openclaw/workspace/skills/camofox-default-browser/

# The plugin includes a server.js that runs on port 9377
cd ~/.openclaw/workspace/skills/camofox-default-browser/

# Make sure startup script is executable
chmod +x scripts/startup.sh
```

### Step 5: Start the Server

The Camoufox server starts automatically when OpenClaw Gateway loads the plugin. For manual start:

```bash
# Using the provided startup script
bash scripts/startup.sh

# Or manually:
export CAMOUFOX_EXECUTABLE=/root/.cache/camoufox/camoufox
nohup node server.js --port 9377 > /tmp/camofox-daemon.log 2>&1 &
disown
```

Verify it's running:

```bash
curl -sf http://localhost:9377/health && echo "Camoufox server is UP" || echo "Server not responding"
```

Expected response: `{"status":"ok","uptime":...}`

---

## 3. Docker Installation (Alternative)

For environments where you don't want to install system dependencies directly, use Docker.

### Dockerfile

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CAMOUFOX_EXECUTABLE=/opt/camoufox/camoufox

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
    libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libatk-bridge2.0-0 libdrm2 libgbm1 xvfb \
    curl wget ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Camoufox binary
RUN mkdir -p /opt/camoufox \
    && cd /tmp \
    && curl -L -o camoufox.tar.gz \
       "https://github.com/jo-inc/camofox-browser/releases/latest/download/camoufox-linux-amd64.tar.gz" \
    && tar xzf camoufox.tar.gz -C /opt/camoufox/ \
    && chmod +x /opt/camoufox/camoufox \
    && rm camoufox.tar.gz

# Copy skill directory
COPY . /app/skill/
WORKDIR /app

# Expose the server port
EXPOSE 9377

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -sf http://localhost:9377/health || exit 1

CMD ["bash", "-c", "export CAMOUFOX_EXECUTABLE=/opt/camoufox/camoufox && node server.js --port 9377"]
```

### Docker Compose Snippet

```yaml
services:
  camoufox:
    build: ./camofox-default-browser
    container_name: camoufox-browser
    restart: unless-stopped
    ports:
      - "9377:9377"
    environment:
      - CAMOUFOX_EXECUTABLE=/opt/camoufox/camoufox
      - CAMOUFOX_CRASH_REPORT_ENABLED=false
    volumes:
      # Mount cookies for persistent authentication
      - ./data/cookies:/app/cookies
      # Mount logs for debugging
      - ./data/logs:/tmp
      # Reusable cache directory (survives rebuilds)
      - camoufox-cache:/opt/camoufox/cache

volumes:
  camoufox-cache:
```

Usage:

```bash
docker compose up -d --build
docker compose logs -f camoufox
```

---

## 4. Verification

### Quick Health Check

```bash
# Check daemon health endpoint
curl -s http://localhost:9377/health | python3 -m json.tool
```

Expected output:
```json
{
  "status": "ok",
  "uptime": 3600,
  "tabs": 0
}
```

### Test Tab Creation

```bash
# Create a test tab
curl -X POST http://localhost:9377/tab/create \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'

# Should return a tabId like "tab_abc123"

# Then take a snapshot
curl -s http://localhost:9377/tab/<tabId>/snapshot | python3 -m json.tool | head -20
```

### List Tabs

```bash
curl -s http://localhost:9377/tabs/list | python3 -m json.tool
```

### Common Installation Issues

| Problem | Solution |
|---------|----------|
| `error while loading shared libraries: libgtk-3.so.0` | Run `apt-get install libgtk-3-0`; verify with `ldd $(which camoufox)` |
| Server won't start on port 9377 | Check `lsof -i :9377`; another process may be using it |
| Blank pages / missing fonts | Install fonts: `apt-get install fonts-liberation fonts-dejavu-core` |
| Headless rendering fails | Ensure `xvfb` is installed; try launching with DISPLAY=:99 |
| `CAMOUFOX_EXECUTABLE not found` | Double-check the path exists: `ls -la $CAMOUFOX_EXECUTABLE` |
| npm dependency errors | Make sure Node.js >= 18: `nvm install 20 && nvm use 20` |
| Memory OOM kills | Increase swap or add more RAM; reduce concurrent tabs |

---

## 5. Uninstallation

To completely remove Camoufox and all related files:

```bash
# Stop the server
pkill -f "node server.js --port 9377" 2>/dev/null
pkill -f "camoufox" 2>/dev/null

# Remove the binary
rm -rf /root/.cache/camoufox/

# Remove the skill directory
rm -rf ~/.openclaw/workspace/skills/camofox-default-browser/

# Remove environment variable from bashrc
sed -i '/export CAMOUFOX_EXECUTABLE/d' ~/.bashrc
source ~/.bashrc

# Optionally clean up system dependencies (if they were installed solely for Camoufox)
sudo apt-get autoremove -y libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
  libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libatk-bridge2.0-0 libdrm2 libgbm1 xvfb
```

If installed via Docker:

```bash
docker compose down
docker image prune -f  # remove unused images
```

---

## Reference Links

- **Repository:** https://github.com/jo-inc/camofox-browser
- **Releases:** https://github.com/jo-inc/camofox-browser/releases
- **OpenClaw Docs:** https://docs.openclaw.ai
- **Support:** Open an issue on GitHub or contact through OpenClaw community channels
