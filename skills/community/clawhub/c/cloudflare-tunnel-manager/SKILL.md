---
name: cloudflare-tunnel
description: Create and manage secure Cloudflare Tunnels using cloudflared. Expose local services to the internet safely, configure DNS routing, set up zero-trust access controls, and manage tunnel authentication without opening firewall ports.
---

# Cloudflare Tunnel

Create secure tunnels to expose local services through Cloudflare's network without opening inbound firewall ports. Supports HTTP/HTTPS services, TCP tunnels, and zero-trust access controls.

## Prerequisites

- Cloudflare account with a domain
- `cloudflared` CLI installed
- Domain DNS managed by Cloudflare
- Local services running (web servers, APIs, etc.)

## Installation

### macOS (Homebrew)
```bash
brew install cloudflare/cloudflare/cloudflared
```

### Linux
```bash
# Download latest release
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

### Windows
```powershell
# Using winget
winget install --id Cloudflare.cloudflared

# Or download from GitHub releases
```

## Usage

### Authentication

**Login to Cloudflare:**
```bash
# Login (opens browser for OAuth)
cloudflared tunnel login

# Verify authentication
cloudflared tunnel list
```

### Basic Tunnel Setup

**Create and run a tunnel:**
```bash
# Create named tunnel
cloudflared tunnel create mytunnel

# Run tunnel for HTTP service
cloudflared tunnel --url http://localhost:3000

# Run tunnel with custom hostname
cloudflared tunnel --url http://localhost:3000 --hostname app.yourdomain.com

# Quick temporary tunnel (random subdomain)
cloudflared tunnel --url http://localhost:8080
```

### Persistent Tunnel Configuration

**Create tunnel and configure DNS:**
```bash
# Create tunnel
cloudflared tunnel create production-app
# Note the tunnel ID from output

# Create DNS record
cloudflared tunnel route dns production-app app.yourdomain.com

# Create config file
mkdir -p ~/.cloudflared
```

**Configuration file (`~/.cloudflared/config.yml`):**
```yaml
tunnel: production-app
credentials-file: /Users/username/.cloudflared/TUNNEL_ID.json

ingress:
  # Main app
  - hostname: app.yourdomain.com
    service: http://localhost:3000
  
  # API service
  - hostname: api.yourdomain.com
    service: http://localhost:4000
    
  # Static files
  - hostname: static.yourdomain.com
    service: http://localhost:8080
    
  # WebSocket service
  - hostname: ws.yourdomain.com
    service: ws://localhost:5000
    
  # SSH access (requires Cloudflare for Teams)
  - hostname: ssh.yourdomain.com
    service: ssh://localhost:22
    
  # Default rule (required)
  - service: http_status:404
```

**Run configured tunnel:**
```bash
# Run with config file
cloudflared tunnel run production-app

# Run in background
cloudflared tunnel run production-app &

# Check tunnel status
cloudflared tunnel info production-app
```

### Advanced Configuration

**Multiple services configuration:**
```yaml
tunnel: multi-service-tunnel
credentials-file: /Users/username/.cloudflared/TUNNEL_ID.json

ingress:
  # Main website
  - hostname: yourdomain.com
    service: http://localhost:3000
    
  # Admin panel with authentication
  - hostname: admin.yourdomain.com
    service: http://localhost:3001
    originRequest:
      noTLSVerify: true
      
  # Development API
  - hostname: dev-api.yourdomain.com
    service: http://localhost:4000
    originRequest:
      httpHostHeader: localhost:4000
      
  # Load balancer for multiple instances
  - hostname: lb.yourdomain.com
    service: http://localhost:3000
    originRequest:
      bastionMode: true
      
  # File server with custom headers
  - hostname: files.yourdomain.com
    service: http://localhost:8000
    originRequest:
      httpHostHeader: files.local
      originServerName: files.local
      
  # Default catch-all
  - service: http_status:404
```

**Advanced origin request options:**
```yaml
originRequest:
  # Disable TLS verification (for self-signed certs)
  noTLSVerify: true
  
  # Custom HTTP headers
  httpHostHeader: internal.service.local
  
  # Connection timeout
  connectTimeout: 30s
  
  # Keep alive settings
  keepAliveConnections: 100
  keepAliveTimeout: 90s
  
  # Proxy settings
  proxyAddress: http://proxy:8080
  proxyPort: 8080
  
  # Bastion mode for kubectl/ssh
  bastionMode: true
```

### Service Management

**Tunnel management commands:**
```bash
# List all tunnels
cloudflared tunnel list

# Get tunnel info
cloudflared tunnel info TUNNEL_NAME

# Delete tunnel
cloudflared tunnel delete TUNNEL_NAME

# Clean up unused tunnels
cloudflared tunnel cleanup TUNNEL_NAME

# Update tunnel
cloudflared tunnel route dns TUNNEL_NAME new-subdomain.yourdomain.com
```

**DNS management:**
```bash
# Add DNS route
cloudflared tunnel route dns mytunnel app.yourdomain.com

# List DNS routes
cloudflared tunnel route list

# Delete DNS route
cloudflared tunnel route delete ROUTE_ID
```

### Zero Trust Access Control

**Access policy configuration (via Cloudflare Dashboard):**

1. Go to Cloudflare Zero Trust → Access → Applications
2. Add application:
   - Application type: Self-hosted
   - App domain: admin.yourdomain.com
   - Policy name: Admin Access

3. Create access policy:
   - Allow/Block/Bypass
   - Include: Email domain contains @yourcompany.com
   - Require: Country is in Taiwan

**Service authentication token:**
```bash
# Create service token for API access
# (Done via Cloudflare Dashboard → Zero Trust → Access → Service Tokens)

# Use service token in requests
curl -H "CF-Access-Client-Id: TOKEN_ID" \
     -H "CF-Access-Client-Secret: TOKEN_SECRET" \
     https://api.yourdomain.com/data
```

### System Service Setup

**Linux systemd service:**
```ini
# /etc/systemd/system/cloudflared-tunnel.service
[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=cloudflared
ExecStart=/usr/local/bin/cloudflared tunnel run production-app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cloudflared-tunnel
sudo systemctl start cloudflared-tunnel
sudo systemctl status cloudflared-tunnel
```

**macOS LaunchAgent:**
```xml
<!-- ~/Library/LaunchAgents/com.cloudflare.tunnel.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cloudflare.tunnel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/cloudflared</string>
        <string>tunnel</string>
        <string>run</string>
        <string>production-app</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

```bash
# Load and start LaunchAgent
launchctl load ~/Library/LaunchAgents/com.cloudflare.tunnel.plist
launchctl start com.cloudflare.tunnel
```

### Monitoring and Troubleshooting

**Health checking:**
```bash
# Check tunnel connectivity
curl -H "Host: yourdomain.com" http://localhost:3000

# Test external access
curl https://yourdomain.com

# Check tunnel logs
cloudflared tunnel --loglevel debug run production-app

# Monitor metrics (if enabled)
curl http://localhost:2000/metrics
```

**Common troubleshooting:**
```bash
# Check tunnel status
cloudflared tunnel info production-app

# Validate config file
cloudflared tunnel ingress validate

# Test ingress rules
cloudflared tunnel ingress rule https://app.yourdomain.com

# Debug connection
cloudflared tunnel --loglevel debug run production-app
```

### Production Example Setup

**Complete production deployment:**
```bash
#!/bin/bash
# setup-cloudflare-tunnel.sh

TUNNEL_NAME="propower-production"
DOMAIN="api.pro-power.cc"

echo "Setting up Cloudflare Tunnel: $TUNNEL_NAME"

# Create tunnel
cloudflared tunnel create $TUNNEL_NAME

# Get tunnel ID
TUNNEL_ID=$(cloudflared tunnel list | grep $TUNNEL_NAME | awk '{print $1}')

# Create DNS records
cloudflared tunnel route dns $TUNNEL_NAME $DOMAIN
cloudflared tunnel route dns $TUNNEL_NAME api.$DOMAIN

# Create config file
cat > ~/.cloudflared/config.yml << EOF
tunnel: $TUNNEL_NAME
credentials-file: $HOME/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: $DOMAIN
    service: http://localhost:3000
  - hostname: api.$DOMAIN
    service: http://localhost:4000
  - service: http_status:404

metrics: localhost:2000
EOF

echo "Configuration created. Start tunnel with:"
echo "cloudflared tunnel run $TUNNEL_NAME"
```

### Backup and Migration

**Backup tunnel configuration:**
```bash
# Backup credentials and config
cp ~/.cloudflared/*.json ~/backup/
cp ~/.cloudflared/config.yml ~/backup/

# Export tunnel list
cloudflared tunnel list > ~/backup/tunnel-list.txt
```

**Migration to new server:**
```bash
# Copy credentials to new server
scp ~/.cloudflared/*.json user@newserver:~/.cloudflared/
scp ~/.cloudflared/config.yml user@newserver:~/.cloudflared/

# Test on new server
ssh user@newserver "cloudflared tunnel run production-app --dry-run"
```

This skill enables secure, firewall-friendly exposure of local services through Cloudflare's global network with built-in DDoS protection and zero-trust access controls.