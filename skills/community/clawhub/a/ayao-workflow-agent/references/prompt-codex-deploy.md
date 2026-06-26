# Codex Deploy Prompt Template

用于全部任务完成后派发给 `codex-deploy` agent。
目标：拉最新代码 → 构建 → 部署到本地 Nginx → 通知。**不写业务代码。**

## 调用命令格式

```bash
codex exec --dangerously-bypass-approvals-and-sandbox 'PROMPT'
```

## 部署架构（Mac Mini 本地）

```
Next.js build → /opt/homebrew/var/www/[project]/ → Nginx → Cloudflare Tunnel → 外网 URL
```

- Nginx config: `/opt/homebrew/etc/nginx/servers/[project].conf`
- Web root: `/opt/homebrew/var/www/[project]/`
- 外网 URL: https://polygo.doai.run（Cloudflare Tunnel → polygo-macmini）

## 模板

```
## Project
[Project name] — [one-line description]
Working directory: [absolute path]

## 你的任务
这是一个部署任务，不要修改业务代码。请按以下步骤执行：

### Step 1: 拉最新代码
cd [project_dir]
git pull origin main
git log --oneline -5  # 确认最新 commit

### Step 2: 构建
cd [project_dir]/[web-subdir]   # 例如 polygo-web-admin
npm ci                           # 确保依赖最新
npm run build                    # Next.js: next build

如果构建失败，输出错误信息并停止，不要继续部署。

### Step 3: 部署到 Nginx web root
WEB_ROOT="/opt/homebrew/var/www/[project]"
mkdir -p "$WEB_ROOT"
# Next.js static export（如已配置 output: 'export'）:
rsync -av --delete out/ "$WEB_ROOT/"
# 或 Next.js standalone（如已配置 output: 'standalone'）:
# rsync -av --delete .next/standalone/ "$WEB_ROOT/"

### Step 4: 重载 Nginx
/opt/homebrew/bin/nginx -t && /opt/homebrew/bin/nginx -s reload

### Step 5: 验证部署
curl -s -o /dev/null -w "%{http_code}" http://localhost:[port]/
# 期望: 200

### Step 6: 汇报结果
输出格式：
✅ 构建成功（commit: [hash]）
✅ 部署到 /opt/homebrew/var/www/[project]/
✅ Nginx 已重载
✅ 本地访问: http://localhost:[port]
✅ 外网访问: https://polygo.doai.run

## Reference
- Nginx 配置位置: /opt/homebrew/etc/nginx/servers/
- Cloudflare Tunnel config: ~/.cloudflared/config.yml
- 查看 tunnel 域名: cloudflared tunnel info [tunnel-name]

## Do NOT
- 修改任何业务代码
- 修改 Nginx 全局配置（/opt/homebrew/etc/nginx/nginx.conf）
- 停止 Nginx（只 reload）
- push 任何代码（这是只读部署）

## Done When
- 构建产物已复制到 web root
- Nginx reload 成功（nginx -t 无错误）
- curl localhost 返回 200
- 汇报本地和外网访问 URL
```

## Nginx 配置参考（首次部署时由 install-nginx.sh 生成）

```nginx
server {
    listen 3100;
    server_name localhost;
    root /opt/homebrew/var/www/polygo;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Next.js API routes（如果是 standalone 模式需要反代 Node.js）
    # location /api/ {
    #     proxy_pass http://localhost:3000;
    # }
}
```

## 常见错误与预防

| 错误 | 原因 | 预防 |
|------|------|------|
| 构建失败 | 依赖不一致 | npm ci 而不是 npm install |
| Nginx reload 失败 | 配置语法错误 | nginx -t 先检查，失败直接汇报 |
| 外网访问 404 | Cloudflare Tunnel 未运行 | 检查 cloudflared tunnel list 状态 |
| 页面空白 | Next.js output 模式不匹配 | 确认 next.config.js 的 output 配置 |
