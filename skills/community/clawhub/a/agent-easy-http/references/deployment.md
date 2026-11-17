# agent-easy-http 部署指南

## 1. 适用场景

把 OpenClaw Agent 的执行能力通过 **HTTP(S) + 网络 IP** 暴露给其它系统调用：

```
其它系统
   │ POST http://<your-server-ip>:7720/agent/run
   │ Header: X-API-Key: <key>
   ▼
agent-easy-http（你的 OpenClaw 容器/主机）
   │ POST → OpenClaw 原生 /hooks/agent（毫秒级触发）
   ▼
每请求独立 hook:<uuid> session → agent 后台执行
   │
   ▼
客户端用 run_id 轮询 GET /result/<run_id> 拿输出
```

> 📐 架构说明：v3.0 起本 skill 是**轻代理层**，不再自己跑 agent，而是转发到 OpenClaw
> 原生 `/hooks/agent`。因此 v2.0 时代的 `/jobs`、`/async`、callback HMAC 等接口已移除，
> 改用「触发返回 run_id → 轮询 /result」的模型。

---

## 2. 快速开始（5 分钟）

```bash
cd <your-workspace>/skills/agent-easy-http

# 1. 安装依赖
pip install fastapi uvicorn pydantic httpx

# 2. 跑初始化向导（会引导启用 OpenClaw hooks + 生成 API Key，默认 HTTP 模式）
python3 scripts/server.py init

# 3. 启动服务（默认 http://0.0.0.0:7720）
python3 scripts/server.py start
```

启动后会打印：
- 服务地址（含本机探测到的 IP）
- Hook 端点（自动从 openclaw.json 推导）
- 已暴露 / 被禁的 skill 数量
- Watchdog 自愈守护状态

> 默认 **HTTP 模式**（零门槛）。跨主机或不太信任的网络段建议切 HTTPS，见 §4。

---

## 3. 客户端调用示例

> 💡 **服务端路径备注**：密钥/证书放在 `<workspace>/.http/`（跟 PVC 持久化）。
> 跑 `python3 scripts/server.py paths` 查看本机真实路径。下面示例假设已把证书/key
> 拷到客户端机器的 `~/.http/`（HTTP 模式无需证书）。

### 3.1 curl（HTTP 模式）

```bash
API_KEY=$(cat <workspace>/.http/secrets/api-keys/agent-easy-http.key)
BASE=http://<your-server-ip>:7720

# 健康检查（无需鉴权）
curl $BASE/health

# 列出可用 skill
curl -H "X-API-Key: $API_KEY" $BASE/skills

# 通用入口：让 agent 自己决定怎么干
RESP=$(curl -s -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
       -d '{"message":"帮我生成本周工作总结"}' \
       $BASE/agent/run)
RUN_ID=$(echo "$RESP" | jq -r .run_id)

# 轮询结果（建议 4s 后首次查询，之后每 1.5s 一次）
sleep 4
while true; do
  R=$(curl -s -H "X-API-Key: $API_KEY" "$BASE/result/$RUN_ID")
  STATUS=$(echo "$R" | jq -r .status)
  [ "$STATUS" = "done" ] && { echo "$R" | jq -r .output; break; }
  [ "$STATUS" = "not_found" ] && { echo "session 还没建好，再等等"; }
  sleep 1.5
done
```

### 3.2 Python requests

```python
import time
import requests

API_KEY = open("~/.http/secrets/api-keys/agent-easy-http.key").read().strip()
BASE = "http://<your-server-ip>:7720"
HEADERS = {"X-API-Key": API_KEY}

# 触发
resp = requests.post(
    f"{BASE}/agent/run",
    headers=HEADERS,
    json={"message": "帮我生成本周工作总结"},
    timeout=30,
)
run_id = resp.json()["run_id"]

# 轮询
time.sleep(4)
while True:
    r = requests.get(f"{BASE}/result/{run_id}", headers=HEADERS, timeout=10).json()
    if r["status"] == "done":
        print(r["output"])
        break
    time.sleep(1.5)
```

### 3.3 Node.js / JavaScript

```javascript
const axios = require('axios');
const fs = require('fs');

const apiKey = fs.readFileSync(
  process.env.HOME + '/.http/secrets/api-keys/agent-easy-http.key', 'utf-8'
).trim();
const BASE = 'http://<your-server-ip>:7720';
const headers = { 'X-API-Key': apiKey };

(async () => {
  const { data } = await axios.post(`${BASE}/agent/run`,
    { message: '帮我生成本周工作总结' }, { headers });
  const runId = data.run_id;

  await new Promise(r => setTimeout(r, 4000));
  while (true) {
    const { data: res } = await axios.get(`${BASE}/result/${runId}`, { headers });
    if (res.status === 'done') { console.log(res.output); break; }
    await new Promise(r => setTimeout(r, 1500));
  }
})();
```

---

## 4. 切到 HTTPS（按需）

跨主机调用或暴露在不太信任的网络段时建议启用 TLS：

```bash
# 1. 生成自签 SAN 证书（自动嗅探本机 IP 写入 SAN）
python3 scripts/gen_cert.py --san auto

# 2. 编辑 <workspace>/.agent-easy-http/config.json 把 tls_enabled 改 true

# 3. 重启
python3 scripts/server.py restart
```

客户端需信任自签证书：

```bash
# curl：临时用 --cacert
curl --cacert ~/.http/certs/server.crt -H "X-API-Key: $API_KEY" \
     https://<your-server-ip>:7720/health

# 或导入系统信任库（Linux）
sudo cp ~/.http/certs/server.crt /usr/local/share/ca-certificates/agent-easy-http.crt
sudo update-ca-certificates
```

浏览器信任自签证书：
- **macOS**：`sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/.http/certs/server.crt`
- **Linux**：拷到 `/usr/local/share/ca-certificates/` 后 `update-ca-certificates`
- **Windows**：双击 `server.crt` → 安装到「受信任的根证书颁发机构」

---

## 5. 安全加固清单

| 项 | 默认 | 内部网络部署建议 | 公网部署建议 |
|---|---|---|---|
| HTTPS | HTTP（默认）| ✅ 跨主机建议开 | ✅ 必开（Let's Encrypt） |
| API Key | ✅ 强制 | ✅ 32 位随机 | ✅ 64 位随机 + 定期轮换 |
| listen 0.0.0.0 | ✅ | ✅ + 防火墙限来源 IP | ❌ 改 127.0.0.1 走反代 |
| deny_skills | 推荐配 | ✅ 拒有副作用 / 会对外发消息的 skill | ✅ 严格收敛白名单 |
| allowed_agent_ids | `[]`（禁指定）| 按需白名单 | ✅ 固定白名单，不用 `["*"]` |
| 反向代理 | ❌ | 可选 Nginx | ✅ 必加 |

---

## 6. systemd 后台运行模板

`/etc/systemd/system/agent-easy-http.service`：

```ini
[Unit]
Description=agent-easy-http
After=network.target

[Service]
Type=simple
WorkingDirectory=<your-workspace>/skills/agent-easy-http
ExecStart=/usr/bin/python3 scripts/server.py start
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

启用：
```bash
sudo systemctl daemon-reload
sudo systemctl enable agent-easy-http
sudo systemctl start agent-easy-http
sudo journalctl -u agent-easy-http -f
```

> 💡 本 skill 自带 watchdog 自愈（每 30s 自检，挂了自动重启），systemd 与 watchdog
> 可二选一或叠加。容器场景推荐直接 `bash scripts/watchdog.sh run` 前台守护。

---

## 7. Nginx 反代示例（真实域名 + Let's Encrypt）

```nginx
server {
    listen 443 ssl http2;
    server_name agent-api.example.com;

    ssl_certificate     /etc/letsencrypt/live/agent-api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/agent-api.example.com/privkey.pem;

    location / {
        proxy_pass         http://127.0.0.1:7720;   # 后端跑 HTTP，Nginx 做 TLS 卸载
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_read_timeout 300;
    }
}
```

⚠️ 反代场景推荐：agent-easy-http 跑 HTTP（`tls_enabled=false`）+ 绑 `127.0.0.1`，Nginx 做 TLS。

---

## 8. 常见问题

### Q1：客户端报「证书不受信任」
A：把 `~/.http/certs/server.crt` 加到客户端 CA 信任链，或临时用 `curl -k` 跳过校验（仅调试）。

### Q2：服务起不来，提示「api_key 不能为空」或「hook_url 无法解析」
A：跑一遍向导：`python3 scripts/server.py init`（会启用 OpenClaw hooks + 生成 API Key）。

### Q3：`/result/<run_id>` 一直返回 `not_found`
A：多为 OpenClaw hooks 缺 `allowRequestSessionKey` / `allowedSessionKeyPrefixes` 配置。
   跑 `python3 scripts/server.py setup-hooks` 修复（或等 watchdog 30s 内自动修）。
   另外 agent 刚触发时 session 文件还没建好，建议触发后 4s 再首次查询。

### Q4：调用返回 403 Skill is in deny list
A：该 skill 在 `deny_skills` 黑名单里。编辑 `<workspace>/.agent-easy-http/config.json`
   移除该项 → 调 `POST /admin/reload` 热重载。

### Q5：调用返回 403 agent_id not in allowed list
A：调用方传的 `agent_id` 不在 `allowed_agent_ids` 白名单。要允许全部设 `["*"]`，
   或把目标 agent 加进白名单。

### Q6：API Key 忘了在哪？
A：跑 `python3 scripts/server.py paths` 看真实路径并 cat 文件。

### Q7：容器重启后服务起不来 / 密钥不见了？
A：数据默认放在 `<workspace>/.http/` 和 `<workspace>/.agent-easy-http/`，跟 PVC 一起持久化。
   如果你用 `OPENCLAW_HTTP_ROOT` / `AGENT_EASY_HTTP_DATA_ROOT` 改到了非持久化目录，
   容器重建可能丢。建议保持默认（workspace 内）。

### Q8：怎么在 Docker / K8s 里跑？
A：用环境变量覆盖配置：
```bash
docker run -e AGENT_EASY_HTTP_PORT=8080 \
           -e AGENT_EASY_HTTP_API_KEY=xxx \
           -v /your-pvc:<workspace> \
           your-image python3 scripts/server.py start
```
完整环境变量列表见 SKILL.md。
