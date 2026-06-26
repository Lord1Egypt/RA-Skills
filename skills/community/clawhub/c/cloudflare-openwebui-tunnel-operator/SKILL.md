---
name: cloudflare-openwebui-tunnel-operator
description: Create and maintain a Cloudflare Tunnel for Open WebUI using a 1Password-managed API token, Docker runtime, and optional systemd persistence. 使用 1Password 管理的 API token、Docker 运行时和可选 systemd 持久化，为 Open WebUI 创建并维护 Cloudflare Tunnel。
homepage: https://docs.openclaw.ai/tools/clawhub
---

# Cloudflare Open WebUI Tunnel Operator

Use this skill when Open WebUI should be exposed through a Cloudflare Tunnel and the Cloudflare API token is stored in 1Password.
当需要通过 Cloudflare Tunnel 暴露 Open WebUI，且 Cloudflare API token 保存在 1Password 中时，使用这个 skill。

## Read First | 先读这些

- `{baseDir}/README.md`
- `{baseDir}/WORKFLOW.md`
- `{baseDir}/FAQ.md`
- `{baseDir}/CHANGELOG.md`

## Primary Rule | 核心原则

Treat 1Password as the secret source, `knowledge/` as the canonical documentation source, and ClawHub only as the distribution layer.
把 1Password 当作密钥来源，把 `knowledge/` 当作规范文档来源，把 ClawHub 仅当作分发层。

## Workflow | 执行流程

1. confirm local Open WebUI health
   确认本地 Open WebUI 健康
2. confirm `op` can read the Cloudflare token
   确认 `op` 能读取 Cloudflare token
3. create or update the remote-managed tunnel and DNS
   创建或更新 remote-managed tunnel 与 DNS
4. write the runtime tunnel token to a local env file
   把运行态 tunnel token 写入本地 env 文件
5. start `cloudflared` with Docker
   用 Docker 启动 `cloudflared`
6. persist the tunnel with `systemd` if reboots must survive
   如果需要跨重启持久化，用 `systemd`
7. verify both local and public URLs
   验证本地与公网 URL
8. backfill `account_id` in 1Password if it was inferred
   如果 `account_id` 是推断得到的，回填到 1Password

## Strong Heuristics | 强判断规则

- if the local Open WebUI is down, do not debug Cloudflare first
- if the 1Password item lacks `account_id`, derive it once and write it back
- if `systemd` cannot authenticate to 1Password, check whether it is calling the wrong `op` binary
- if the public URL returns `502`, check origin readiness before changing tunnel config
- use a hostname derived from project meaning, not the machine hostname

中文解释：

- 本地 Open WebUI 没起来，就不要先查 Cloudflare。
- 1Password 缺 `account_id` 时，可先推断一次，再回填。
- `systemd` 认证不到 1Password 时，优先检查它是否调用了错误的 `op`。
- 公网返回 `502` 时，先检查 origin 是否就绪，不要先改 tunnel 配置。
- 域名应按项目语义命名，不要按机器名命名。

## Safe Commands | 安全命令

```bash
op whoami
docker compose ps
curl -I http://localhost:3301
curl -I https://your-hostname.example.com
systemctl status --no-pager your-tunnel.service
```

## Response Format | 输出格式

Always return:
始终返回：

1. current workflow status
2. missing artifacts
3. next single best action
4. verification after that

## Constraints | 约束

- do not reveal secret values from 1Password, `.env`, or runtime env files
- do not publish machine-specific tokens or raw transcripts
- prefer self-contained docs and package content
- keep the hostname and service mapping explicit

中文约束：

- 不要泄露 1Password、`.env` 或运行态 env 文件中的密钥值。
- 不要发布机器专属 token 或原始聊天记录。
- 优先保持文档和 skill 包自包含。
- 明确写清楚 hostname 和 origin service 的映射关系。
