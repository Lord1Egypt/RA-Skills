---
name: frp-tunnel
description: Share local development servers via self-hosted frp tunnel with custom domains and auto HTTPS. Use when you need to share localhost with others, demo to clients, or test on mobile. Replaces ngrok/localhost.run with a stable, unlimited, self-hosted solution.
---

# frp-tunnel — 自建內網穿透

用自建的 frp + Caddy + Hetzner VPS 分享本地開發中的網站。自訂域名、自動 HTTPS、無限 tunnel。

> 替代方案（無 VPS 時）：見 `old-share-local-site` skill（ngrok/localhost.run）

## ⚙️ Config（自訂區塊）

使用此 skill 前，請將以下值替換成你自己的環境：

| 變數 | 目前的值 | 說明 |
|------|---------|------|
| VPS IP | `5.223.75.160` | 你的 VPS 公網 IP |
| 域名 | `*.tunnel.fud.city` | 你的 wildcard 子域名 |
| DNS Provider | Cloudflare (`fud.city`) | 管理你域名 DNS 的服務 |
| GitHub 備份 | `https://github.com/darwin7381/frp-tunnel` | 你的 private repo（可選） |

> **Dashboard 密碼**：不記在這裡。在 VPS 的 `frps.toml` 裡設定你自己的密碼。

## 基礎資訊

| 項目 | 值 |
|------|-----|
| VPS IP | 5.223.75.160 |
| VPS Provider | Hetzner Cloud, Singapore, CPX12 |
| 域名 | *.tunnel.fud.city |
| DNS | Cloudflare (fud.city) |
| HTTPS 方式 | **Wildcard cert** (DNS-01 challenge via Cloudflare API) |
| frp Dashboard | http://5.223.75.160:7500 |
| GitHub 備份 | https://github.com/darwin7381/frp-tunnel (private) |
| 本地 config | ~/.frp/frpc.toml |
| 本地 tmux session | `frpc` |
| VPS services | frps (systemd) + caddy (systemd) |

## 目前的 Tunnels

| 名稱 | 本地 Port | URL |
|------|----------|-----|
| news-dashboard | 5173 | https://news.tunnel.fud.city |
| oldweb | 8080 | https://oldweb.tunnel.fud.city |
| api | 8000 | https://api.tunnel.fud.city |
| fin-terminal | 5177 | https://terminal.tunnel.fud.city |
| fin-terminal-api | 3002 | https://terminal-api.tunnel.fud.city |

## HTTPS 方式：Wildcard vs Per-Domain

VPS 上的 Caddy 有兩種方式為 tunnel 提供 HTTPS。**目前使用 Wildcard（推薦）。**

### 方式 A：Wildcard Certificate（目前使用 ✅）

**原理**：一張 `*.tunnel.fud.city` wildcard cert 涵蓋所有子域名。使用 DNS-01 challenge — Caddy 透過 Cloudflare API 自動加 TXT record 驗證。

**Caddyfile：**
```caddyfile
*.tunnel.fud.city {
    tls {
        dns cloudflare {env.CF_API_TOKEN}
    }
    reverse_proxy localhost:8080
}
```

**需要：**
- Caddy with Cloudflare DNS plugin（標準版沒有，需重新編譯或下載）
- Cloudflare API Token（Zone:DNS:Edit 權限，只限 fud.city）
- Token 設定在 `/etc/systemd/system/caddy.service.d/override.conf`

**新增 tunnel 只需改本地 frpc.toml，不用動 VPS。**

**安裝步驟（已完成，僅供紀錄）：**
```bash
# 1. 下載帶 cloudflare plugin 的 Caddy
curl -s "https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fcaddy-dns%2Fcloudflare" -o /usr/bin/caddy
chmod +x /usr/bin/caddy

# 2. 驗證 module 存在
caddy list-modules | grep cloudflare

# 3. 設定 CF token
mkdir -p /etc/systemd/system/caddy.service.d
cat > /etc/systemd/system/caddy.service.d/override.conf << EOF
[Service]
Environment="CF_API_TOKEN=你的token"
EOF

# 4. 更新 Caddyfile
cat > /etc/caddy/Caddyfile << EOF
*.tunnel.fud.city {
    tls {
        dns cloudflare {env.CF_API_TOKEN}
    }
    reverse_proxy localhost:8080
}
EOF

# 5. 重啟
systemctl daemon-reload
systemctl restart caddy
```

### 方式 B：Per-Domain Certificate（備用）

**原理**：每個子域名獨立簽一張 cert。使用 HTTP-01 challenge — Let's Encrypt 訪問 `http://xxx/.well-known/acme-challenge/` 驗證。

**Caddyfile：**
```caddyfile
news.tunnel.fud.city {
    reverse_proxy localhost:8080
}

terminal.tunnel.fud.city {
    reverse_proxy localhost:8080
}

# 每加一個 tunnel 就加一段
```

**需要**：標準版 Caddy 即可，不需要 API token。

**缺點**：每次加 tunnel 都要 SSH 進 VPS 改 Caddyfile 再 reload Caddy。

**適合場景**：
- 不想給 Cloudflare API token
- 需要不同子域名指向不同 upstream（不只是 frp）
- 臨時測試

### 如何切換

**Wildcard → Per-Domain：**
```bash
ssh root@5.223.75.160
# 刪除 override.conf（或保留也無妨）
# 把 Caddyfile 改成逐一列出每個域名
systemctl restart caddy
```

**Per-Domain → Wildcard：**
按上面方式 A 的安裝步驟。

## 日常操作

### 啟動 frpc（Mac 重啟後需要）

```bash
SOCK=/tmp/openclaw-tmux/openclaw.sock
tmux -S $SOCK new-session -d -s frpc 'frpc -c ~/.frp/frpc.toml'
```

### 檢查 frpc 狀態

```bash
SOCK=/tmp/openclaw-tmux/openclaw.sock
tmux -S $SOCK capture-pane -t frpc -p -S -10
```

### 加新 tunnel（Wildcard 模式 — 只需改本地）

**Step 1 — 本地 config**

編輯 `~/.frp/frpc.toml`，加一段：
```toml
[[proxies]]
name = "new-project"
type = "http"
localPort = 3000
customDomains = ["new.tunnel.fud.city"]
```

**Step 2 — 重啟本地 frpc**

```bash
SOCK=/tmp/openclaw-tmux/openclaw.sock
tmux -S $SOCK send-keys -t frpc C-c
sleep 2
tmux -S $SOCK send-keys -t frpc 'frpc -c ~/.frp/frpc.toml' Enter
```

**Step 3 — 驗證**（不需要動 VPS！Wildcard cert 自動涵蓋）

```bash
curl -sI https://new.tunnel.fud.city | head -5
```

確認回傳 `HTTP/2 200` 才告訴用戶。

**Step 4 — 同步 GitHub 備份**

```bash
cd ~/Projects/frp-tunnel
cp ~/.frp/frpc.toml ./frpc.toml
git add -A && git commit -m "Add tunnel: new-project" && git push
```

### 加新 tunnel（Per-Domain 模式 — 需改 VPS）

同上 Step 1-2，但在 Step 2 和 3 之間多一步：

```bash
ssh root@5.223.75.160
# 編輯 /etc/caddy/Caddyfile，加：
# new.tunnel.fud.city {
#     reverse_proxy localhost:8080
# }
systemctl reload caddy
# 等 30 秒讓 cert 簽發
```

### 前端 Vite 的 allowedHosts

Vite dev server 預設會拒絕非 localhost 的 Host header。加 tunnel 時前端 `vite.config.ts` 也要加：

```ts
server: {
  allowedHosts: ['xxx.tunnel.fud.city'],
}
```

### 臨時開一條（不改 config）

```bash
frpc http --server-addr 5.223.75.160:7000 --local-port 3000 --custom-domain temp.tunnel.fud.city
```

Wildcard 模式下，臨時 tunnel 也自動有 HTTPS。

## 發送 URL 前必做的檢查（SOP）

**每次**發送 tunnel URL 給用戶前：

1. **確認 frpc 在跑** — `tmux capture-pane -t frpc`
2. **確認 proxy 成功** — 看到 `start proxy success`
4. **確認回傳 200** — 不是 502/404/連線失敗
5. **確認內容正確** — `curl -s https://xxx.tunnel.fud.city | grep "<title>"`，title 必須是預期的網站名稱
6. **確認本地 server 是活的，不是僵屍進程** — `ps aux | grep <port>` 檢查進程啟動時間，如果是幾天前啟動的舊進程，很可能已經僵屍化（佔 port 但不正常服務，偶爾回 200 但頁面空白）。殺掉重啟。
7. **瀏覽器驗證時禁止信任 cache** — 用無痕模式或 `curl --resolve` 強制走 VPS IP，不要用已開過的 tab

### ⚠️ 已知 Failure Mode：僵屍進程（2026-03-04 事故）

本地 dev server（如 Vite）長時間不重啟會變成僵屍：佔著 port、偶爾回 HTTP 200，但實際頁面是空白。
curl 檢查看似正常，瀏覽器有 cache 也看似正常，但外部用戶（包含手機）打開是空白。

**排查步驟**：
1. `ps aux | grep <port>` — 看進程啟動時間，超過 1-2 天就該懷疑
2. 殺掉舊進程，在 tmux 裡重新 `npm run dev`
3. 重啟後再 curl + grep title 確認

## VPS 故障排除

```bash
# SSH 進 VPS
ssh root@5.223.75.160

# 檢查 frps
systemctl status frps
journalctl -u frps --no-pager -n 20

# 檢查 Caddy
systemctl status caddy
journalctl -u caddy --no-pager -n 20

# 檢查 Caddy modules（確認有 cloudflare）
caddy list-modules | grep cloudflare

# 檢查 cert 狀態
caddy cert list 2>/dev/null || journalctl -u caddy | grep "certificate obtained"

# 重啟
systemctl restart frps
systemctl restart caddy
```

## 防火牆規則（VPS ufw）

| Port | 用途 |
|------|------|
| 22 | SSH |
| 80 | HTTP (Caddy + Let's Encrypt) |
| 443 | HTTPS (Caddy) |
| 7000 | frp client 連線 |
| 7500 | frp Web Dashboard |

## 費用

- VPS: $7.59/月（Hetzner CPX12 Singapore + IPv4）
- 域名: 已有 fud.city
- SSL: 免費（Let's Encrypt via Caddy）
- 流量: 0.5 TB/月（實際用量約 10-15 GB/月）
