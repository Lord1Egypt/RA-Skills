# Cloudflare Worker 部署指南

## 前置条件

1. 安装 Wrangler CLI：
   ```bash
   npm install -g wrangler
   ```

2. 登录 Cloudflare：
   ```bash
   wrangler login
   ```

## 部署步骤

### 1. 创建 KV 命名空间

```bash
cd cloudflare-worker
wrangler kv:namespace create "KV"
```

记下输出的 `id`，例如：`{ binding = "KV", id = "xxxx-xxxx-xxxx" }`

### 2. 配置 wrangler.toml

编辑 `wrangler.toml`，取消注释并填入 KV ID：

```toml
[[kv_namespaces]]
binding = "KV"
id = "你的-kv-namespace-id"
```

### 3. 设置密码

编辑 `worker.js`，修改 TOKEN：

```javascript
const TOKEN = 'your-secret-token'; // 改成你的密码
```

### 4. 部署

```bash
wrangler deploy
```

部署成功后会显示 Worker URL，例如：
`https://cryptofolio-api.your-username.workers.dev`

## 配置 OpenClaw

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "cryptofolio": {
        "enabled": true,
        "env": {
          "CRYPTOFOLIO_API_URL": "https://cryptofolio-api.your-username.workers.dev",
          "CRYPTOFOLIO_TOKEN": "your-secret-token"
        }
      }
    }
  }
}
```

## 测试

```bash
# 测试健康检查
curl https://cryptofolio-api.your-username.workers.dev/api/health

# 测试获取数据
curl -H "Authorization: Bearer your-secret-token" \
  https://cryptofolio-api.your-username.workers.dev/api/data
```
