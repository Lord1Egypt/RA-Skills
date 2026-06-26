# frp-tunnel 從零建置指南

以 Hetzner Cloud + Cloudflare DNS 為例，從開 VPS 到第一條 tunnel 通。

---

## 概覽

完成後你會有：
- 一台 Hetzner VPS 跑 frps + Caddy
- `*.your-domain.com` wildcard 子域名，自動 HTTPS
- 本地 `frpc` 隨時開 tunnel，不用再動 VPS

預計時間：30-60 分鐘（含等 DNS 生效）

---

## Step 1：註冊 Hetzner Cloud

1. 前往 https://www.hetzner.com/cloud/
2. 註冊帳號（需信用卡或 PayPal）
3. 建立一個 Project（例如 `tunnel`）

### 選機型

| 項目 | 建議 |
|------|------|
| 地區 | 離你最近的（Singapore / Ashburn / Falkenstein） |
| 機型 | **CPX12**（2 vCPU, 2 GB RAM, 40 GB SSD, ~$7.59/月） |
| OS | **Ubuntu 24.04** |
| IPv4 | ✅ 勾選（需要公網 IP） |

> CPX12 是 ARM 架構（Ampere），性價比最高。如果你需要 x86 選 CX22。

---

## Step 2：SSH Key 設定

### 方案 A：讓 AI 幫你操作 VPS（推薦）

讓 AI（OpenClaw / Claude Code）能 SSH 進 VPS 執行指令。

**在你的 Mac 上生成 SSH key：**

```bash
# 生成專用 key（不設 passphrase，AI 才能自動連線）
ssh-keygen -t ed25519 -f ~/.ssh/frp-vps -N "" -C "openclaw-frp-tunnel"
```

**在 Hetzner Console 加入 public key：**

1. 進 Hetzner Cloud Console → Security → SSH Keys
2. 點 Add SSH Key
3. 貼上 `~/.ssh/frp-vps.pub` 的內容
4. 命名為 `openclaw`

**建 VPS 時選這把 key。**

建好後測試：

```bash
ssh -i ~/.ssh/frp-vps root@<VPS_IP>
```

**設定 SSH config 簡化連線（可選但推薦）：**

```bash
cat >> ~/.ssh/config << 'EOF'

Host frp-vps
    HostName <VPS_IP>
    User root
    IdentityFile ~/.ssh/frp-vps
EOF
```

之後 `ssh frp-vps` 就能連。

### 方案 B：自己操作 VPS

如果你不想給 AI SSH 存取，可以自己 SSH 進去，把下面每一步的指令手動貼進去跑。

---

## Step 3：VPS 基礎設定

SSH 進 VPS 後：

```bash
# 更新系統
apt update && apt upgrade -y

# 設定防火牆
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP (Let's Encrypt + redirect)
ufw allow 443/tcp   # HTTPS (Caddy)
ufw allow 7000/tcp  # frp client 連線
ufw allow 7500/tcp  # frp Dashboard（可選，不需要可不開）
ufw --force enable
ufw status
```

---

## Step 4：安裝 frps（frp server）

```bash
# 查最新版本：https://github.com/fatedier/frp/releases
FRP_VERSION="0.62.1"

# 判斷架構
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ]; then
    FRP_ARCH="arm64"
elif [ "$ARCH" = "x86_64" ]; then
    FRP_ARCH="amd64"
fi

# 下載並安裝
cd /tmp
wget https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_${FRP_ARCH}.tar.gz
tar xzf frp_${FRP_VERSION}_linux_${FRP_ARCH}.tar.gz
cp frp_${FRP_VERSION}_linux_${FRP_ARCH}/frps /usr/bin/frps
chmod +x /usr/bin/frps
```

### 建立 frps 設定檔

```bash
mkdir -p /etc/frp

cat > /etc/frp/frps.toml << 'EOF'
bindPort = 7000
vhostHTTPPort = 8080

# Dashboard（可選）
webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "設定你自己的密碼"
EOF
```

> `vhostHTTPPort = 8080`：frps 在 8080 接收所有 HTTP 流量，Caddy 會把 HTTPS 流量反向代理到這裡。

### 建立 systemd service

```bash
cat > /etc/systemd/system/frps.service << 'EOF'
[Unit]
Description=frps server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/frps -c /etc/frp/frps.toml
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable frps
systemctl start frps
systemctl status frps
```

---

## Step 5：設定 DNS（Cloudflare）

1. 登入 Cloudflare Dashboard → 選你的域名
2. DNS → Add Record：

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | `*.tunnel` | `<VPS_IP>` | ❌ DNS only（灰雲） |

> **必須關 Proxy（灰雲）**，不然 Caddy 的 HTTPS 會跟 Cloudflare 的衝突。

3. 等 DNS 生效（通常 1-5 分鐘）：

```bash
dig +short anything.tunnel.your-domain.com
# 應該回傳你的 VPS IP
```

---

## Step 6：安裝 Caddy（帶 Cloudflare DNS plugin）

標準版 Caddy 不支援 DNS-01 challenge（wildcard cert 需要）。需要帶 Cloudflare plugin 的版本：

```bash
# 下載帶 cloudflare plugin 的 Caddy（自動偵測架構）
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ]; then
    CADDY_ARCH="arm64"
elif [ "$ARCH" = "x86_64" ]; then
    CADDY_ARCH="amd64"
fi

curl -sL "https://caddyserver.com/api/download?os=linux&arch=${CADDY_ARCH}&p=github.com%2Fcaddy-dns%2Fcloudflare" -o /usr/bin/caddy
chmod +x /usr/bin/caddy

# 驗證 cloudflare module 存在
caddy list-modules | grep cloudflare
# 應看到：dns.providers.cloudflare
```

### 建立 Cloudflare API Token

1. Cloudflare Dashboard → My Profile → API Tokens → Create Token
2. 選 **Custom Token**：
   - Permissions: `Zone > DNS > Edit`
   - Zone Resources: `Include > Specific zone > your-domain.com`
3. 建立後複製 token

### 設定 Caddy

```bash
# 設定 Cloudflare API Token
mkdir -p /etc/systemd/system/caddy.service.d
cat > /etc/systemd/system/caddy.service.d/override.conf << EOF
[Service]
Environment="CF_API_TOKEN=貼上你的token"
EOF

# Caddyfile
mkdir -p /etc/caddy
cat > /etc/caddy/Caddyfile << 'EOF'
*.tunnel.your-domain.com {
    tls {
        dns cloudflare {env.CF_API_TOKEN}
    }
    reverse_proxy localhost:8080
}
EOF
```

> 把 `your-domain.com` 換成你的域名。

### 建立 Caddy systemd service

```bash
# 建立 caddy user（如果不存在）
groupadd --system caddy 2>/dev/null
useradd --system --gid caddy --create-home --home-dir /var/lib/caddy --shell /usr/sbin/nologin caddy 2>/dev/null

cat > /etc/systemd/system/caddy.service << 'EOF'
[Unit]
Description=Caddy
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=caddy
Group=caddy
ExecStart=/usr/bin/caddy run --environ --config /etc/caddy/Caddyfile
ExecReload=/usr/bin/caddy reload --config /etc/caddy/Caddyfile
TimeoutStopSec=5s
LimitNOFILE=1048576
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable caddy
systemctl start caddy

# 確認 cert 簽發成功（等 10-30 秒）
journalctl -u caddy --no-pager -n 20 | grep -i "certificate obtained"
```

---

## Step 7：本地安裝 frpc（Mac）

```bash
# macOS (Homebrew)
brew install frp

# 或手動下載
# https://github.com/fatedier/frp/releases → darwin_arm64 (Apple Silicon) / darwin_amd64 (Intel)
```

### 建立本地設定檔

```bash
mkdir -p ~/.frp

cat > ~/.frp/frpc.toml << 'EOF'
serverAddr = "<VPS_IP>"
serverPort = 7000

[[proxies]]
name = "my-first-tunnel"
type = "http"
localPort = 3000
customDomains = ["app.tunnel.your-domain.com"]
EOF
```

> 把 `<VPS_IP>` 和 `your-domain.com` 換成你的。`localPort` 改成你本地 dev server 的 port。

---

## Step 8：啟動並驗證

### 啟動本地 frpc

```bash
# 用 tmux 持久化（推薦）
SOCK=/tmp/openclaw-tmux/openclaw.sock
tmux -S $SOCK new-session -d -s frpc 'frpc -c ~/.frp/frpc.toml'

# 或直接跑（關 terminal 就斷）
frpc -c ~/.frp/frpc.toml
```

### 驗證

```bash
# 1. 確認 frpc 連上 server
tmux -S $SOCK capture-pane -t frpc -p -S -5
# 應看到：start proxy success

# 2. 確認本地 server 在跑（例如 port 3000）
curl -s http://localhost:3000 | head -5

# 3. 確認 tunnel 通
curl -sI https://app.tunnel.your-domain.com | head -5
# 應看到：HTTP/2 200
```

🎉 完成！你現在有一條穩定的 HTTPS tunnel。

---

## 之後加新 tunnel

只需要改本地 `~/.frp/frpc.toml`，加一段 `[[proxies]]`，重啟 frpc。不用動 VPS。

詳見主文件 `SKILL.md` 的「加新 tunnel」段落。

---

## 費用總結

| 項目 | 費用 |
|------|------|
| Hetzner CPX12 | ~$7.59/月 |
| 域名 | 你已有的域名（或 ~$10/年） |
| SSL | 免費（Let's Encrypt via Caddy） |
| Cloudflare DNS | 免費 |
| **合計** | **~$7.59/月** |
