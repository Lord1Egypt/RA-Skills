# Networking & Deployment Guide: Domain, External IP, or Strictly Local LAN

This guide describes how to access your AI Quota Dashboard across three deployment environments: strictly local network, remote access without a domain, and production deployment under a custom domain with HTTPS and access control.

> **Privileged operations note.** Firewall changes, package installation, nginx site management and certificate issuance require administrator privileges on the host. Perform them through your distribution's standard administrative workflow (a privileged shell or your configuration-management tooling). This guide deliberately describes the required steps instead of prescribing raw privileged command lines; review each change against your own security policy before applying it. The dashboard contains private account telemetry — never expose it without authentication.

---

## 1. Scenario A: Strictly Local LAN (Maximum Privacy, Zero Internet Exposure)

Ideal for home servers, Raspberry Pi, or local workstations where telemetry should never leave your private Wi-Fi/LAN.

### 1. Bind to Local Network
In the server script or systemd unit, bind to `0.0.0.0` (all interfaces) or your machine's private LAN IP:
```bash
python3 -m http.server 8885 --bind 0.0.0.0 --directory /path/to/templates
```

### 2. Restrict Firewall to Subnet Only
Configure the host firewall (e.g. `ufw` or `firewalld`) so that inbound TCP port 8885 is accepted **only from your local subnet** (for example `192.168.1.0/24`) and dropped from every other source. Apply the rule with your firewall administration tooling and verify the active ruleset afterwards.

### 3. Access
Open on any smartphone, tablet, or PC connected to the same Wi-Fi:
`http://<LAN_IP>:8885`

---

## 2. Scenario B: Remote Access WITHOUT a Custom Domain

When you need mobile access on cellular networks without purchasing or configuring a public domain.

### Option B1: WireGuard / Tailscale Mesh VPN (Recommended)
Zero open ports on your router, full end-to-end encryption.
1. Install Tailscale (or WireGuard) on the dashboard host using your distribution's package repository, then bring the tunnel up and authenticate the node.
2. Install the same VPN client on your iPhone or Android phone and join the same tailnet.
3. Access the dashboard via the host's 100.x.y.z Tailscale IP from anywhere in the world:
   `http://100.x.y.z:8885`

### Option B2: Direct External IP (Router Port Forwarding)
If your ISP provides a public static IP:
1. In your home router settings, navigate to **Port Forwarding / Virtual Servers**.
2. Forward an external TCP port (e.g. `28885`) to the dashboard host's LAN IP, port `8885`. Restrict the rule to known source IPs where the router supports it.
3. Access via `http://<YOUR_EXTERNAL_IP>:28885`.

*Security Warning:* Never leave an unprotected dashboard exposed to the raw internet without Basic Auth or IP whitelisting.

### Option B3: Cloudflare Tunnel (Works behind CGNAT / Gray IP)
1. Install `cloudflared` from the official Cloudflare package repository for your distribution (follow the vendor's documented installation instructions; verify the package source before installing).
2. Run an ad-hoc tunnel pointing at the local dashboard:
   ```bash
   cloudflared tunnel --url http://127.0.0.1:8885
   ```
   This provides a `https://random-name.trycloudflare.com` URL with TLS included.

*Security Warning:* A tunnel makes the dashboard reachable from the whole internet. Put Basic Auth or an access policy in front of it first (see Scenario C); an unauthenticated tunnel leaks your account telemetry to anyone who learns the URL.

---

## 3. Scenario C: Custom Domain with HTTPS & Password Protection

Best for permanent, clean URLs (e.g. `https://quota.mydomain.com`) with automated SSL certificates.

### Step 1: Nginx Reverse Proxy Configuration
Create a site configuration (e.g. `/etc/nginx/sites-available/quota-dashboard`):
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
Use the `htpasswd` utility (from your distribution's apache2-utils / httpd-tools package) to create `/etc/nginx/.htpasswd_quota` with a strong password. Restrict the file so only the owner and the nginx group can read it (mode `0640`).

### Step 3: Enable Site & Issue SSL
Through your administrative workflow: enable the site (symlink it into `sites-enabled`), validate the nginx configuration, reload nginx, and issue a Let's Encrypt certificate for the domain with Certbot's nginx plugin.

Done! Your dashboard is now securely reachable at `https://quota.mydomain.com` with automated HTTPS and Basic Auth.
