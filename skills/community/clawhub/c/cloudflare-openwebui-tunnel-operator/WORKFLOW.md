# Workflow

## Goal | 目标

Expose Open WebUI through a Cloudflare Tunnel using a Cloudflare API token stored in 1Password, then keep the tunnel stable with Docker and optional `systemd`.
把保存在 1Password 中的 Cloudflare API token 用于创建 Cloudflare Tunnel 暴露 Open WebUI，并结合 Docker 与可选 `systemd` 保持隧道稳定运行。

## Canonical Sequence | 标准顺序

1. verify local Open WebUI health
   验证本地 Open WebUI 健康状态
2. verify `op` access to the Cloudflare token item
   验证 `op` 能访问 Cloudflare token 条目
3. resolve the Cloudflare zone and account
   解析 Cloudflare zone 和 account
4. create or reuse a remote-managed tunnel
   创建或复用 remote-managed tunnel
5. apply ingress from the public hostname to the local Open WebUI service
   把公网 hostname 映射到本地 Open WebUI 服务
6. create or update the proxied DNS CNAME
   创建或更新代理 CNAME 记录
7. fetch the tunnel runtime token and write a local env file
   获取 tunnel 运行 token 并写入本地 env 文件
8. start `cloudflared` in Docker
   用 Docker 启动 `cloudflared`
9. enable `systemd` if reboot persistence is required
   如果要求跨重启持久化，启用 `systemd`
10. verify local and public URLs
    验证本地与公网 URL
11. backfill `account_id` into 1Password if it was inferred
    如果 `account_id` 是推断出来的，则回填到 1Password

## Recommended Checks | 推荐检查

```bash
op whoami
docker compose ps
curl -I http://localhost:3301
curl -I https://your-hostname.example.com
docker compose logs --tail=50 cloudflared
systemctl status --no-pager your-tunnel.service
```

## Interpretation Rules | 解释规则

- local `200 OK`, public `502`: the tunnel is up before the origin is ready
- local failure, public failure: fix Open WebUI first
- `systemd` can not read 1Password: it is often using the wrong `op` binary or wrong `PATH`
- missing `account_id`: derive it once, then persist it back into 1Password

## Packaging Rules | 打包规则

- do not ship secrets
- do not ship raw command transcripts
- keep the package self-contained
- keep the hostname, tunnel name, and origin service explicit
- if the audience is mixed, keep the docs bilingual
