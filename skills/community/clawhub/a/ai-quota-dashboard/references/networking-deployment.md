# Networking & Deployment Guide: Domain, External IP, or Strictly Local LAN

This guide provides step-by-step configurations for accessing your AI Quota Dashboard across three distinct deployment environments: strictly local network, remote access without a domain, and production deployment under a custom domain with HTTPS and access control.

---

## 1. Scenario A: Strictly Local LAN (Maximum Privacy, Zero Internet Exposure)

Ideal for home servers, Raspberry Pi, or local workstations where telemetry should never leave your private Wi-Fi/LAN.

### 1. Bind to Local Network
In the server script or systemd unit, bind to `0.0.0.0` (all interfaces) or your machine's private LAN IP (e.g., `192.168.1.229`):
```bash
python3 -m http.server 8885 --bind 0.0.0.0 --directory /path/to/templates
```

### 2. Restrict Firewall to Subnet Only
Prevent unauthorized external connections while allowing local devices:
```bash
# Allow connections strictly from your home subnet (e.g., 192.168.1.0/24)
sudo ufw allow from 192.168.1.0/24 to any port 8885 proto tcp
sudo ufw status
```

### 3. Access
Open on any smartphone, tablet, or PC connected to the same Wi-Fi:
`http://192.168.1.229:8885`

---

## 2. Scenario B: Remote Access WITHOUT a Custom Domain

When you need mobile access on cellular networks without purchasing or configuring a public domain.

### Option B1: WireGuard / Tailscale Mesh VPN (Recommended)
Zero open ports on your router, full end-to-end encryption.
1. Install Tailscale on the dashboard host:
   ```bash
   # Install Tailscale via your distribution package manager (e.g. apt install tailscale)
   sudo tailscale up
   ```
2. Install Tailscale on your iPhone or Android phone.
3. Access the dashboard via your host's 100.x.y.z Tailscale IP from anywhere in the world:
   `http://100.x.y.z:8885`

### Option B2: Direct External IP (Router Port Forwarding)
If your ISP provides a public static IP:
1. In your home router settings, navigate to **Port Forwarding / Virtual Servers**.
2. Forward External Port `8885` (or a random high port like `28885`) -> Internal IP `192.168.1.229:8885` (TCP).
3. Access via `http://<YOUR_EXTERNAL_IP>:8885`.
*Security Warning:* Never leave an unprotected dashboard exposed to the raw internet without Basic Auth or IP whitelisting.

### Option B3: Free Cloudflare Tunnel (Works behind CGNAT / Gray IP)
1. Install `cloudflared`:
   ```bash
   curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
   sudo dpkg -i cloudflared.deb
   ```
2. Run an instant ad-hoc tunnel:
   ```bash
   cloudflared tunnel --url http://127.0.0.1:8885
   ```
   Provides a free, secure `https://random-name.trycloudflare.com` URL with SSL included.

---

## 3. Scenario C: Custom Domain with HTTPS & Password Protection

Best for permanent, clean URLs (e.g., `https://quota.mydomain.com`) with automated SSL certificates.

### Step 1: Nginx Reverse Proxy Configuration
Create `/etc/nginx/sites-available/quota-dashboard`:
```nginx
server {
    server_name quota.mydomain.com;

    location / {
        proxy_pass http://127.0.0.1:8885;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Mandatory Protection: Basic Auth (so bots cannot view your quotas)
        auth_basic "Restricted AI Dashboard";
        auth_basic_user_file /etc/nginx/.htpasswd_quota;
    }
}
```

### Step 2: Create Password Credentials
```bash
# Generate htpasswd file:
htpasswd -c /etc/nginx/.htpasswd_quota admin
sudo chmod 640 /etc/nginx/.htpasswd_quota
```

### Step 3: Enable Site & Issue Free SSL via Certbot
```bash
sudo ln -s /etc/nginx/sites-available/quota-dashboard /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d quota.mydomain.com
```

Done! Your dashboard is now securely reachable at `https://quota.mydomain.com` with automated Let's Encrypt HTTPS.
