# Cloudflare Open WebUI Tunnel Operator

This skill helps expose Open WebUI through a Cloudflare Tunnel using a Cloudflare API token managed in 1Password.
这个 skill 用来通过 Cloudflare Tunnel 暴露 Open WebUI，并使用保存在 1Password 中的 Cloudflare API token。

## What This Skill Is For | 适用场景

Use it when:
适用于：

- Open WebUI already runs locally and you need a public HTTPS hostname
- you want the Cloudflare API token to stay in 1Password
- you want the tunnel and DNS to be created or updated by API
- you want `cloudflared` to run under Docker
- you want a `systemd` path for reboot persistence

## What It Produces | 产出物

The workflow aims to produce:
这个流程目标产出：

- a stable public hostname for Open WebUI
- a repeatable tunnel creation workflow
- a local runtime env file for `cloudflared`
- an optional `systemd` unit
- a reusable, self-contained skill package

## Included Files | 包含文件

- `SKILL.md`
- `README.md`
- `WORKFLOW.md`
- `FAQ.md`
- `CHANGELOG.md`

## Important Decision Rules | 关键判断规则

- keep 1Password as the secret source of truth
- keep canonical docs in `knowledge/`
- treat ClawHub as distribution, not canonical storage
- use project-meaningful hostnames such as `knowledge-stack.xiannai.me`

## Local Use | 本地使用

Place this folder under one of these locations:
把这个目录放到以下任一位置：

- `<workspace>/skills/`
- `~/.openclaw/skills/`

Then start a new OpenClaw session or refresh skills.
然后重新开始一个 OpenClaw 会话，或刷新 skills。

## ClawHub Publish Shape | ClawHub 发布方式

This folder is self-contained so it can be published as a single bundle.
这个目录是自包含的，可以直接作为单个 skill 包发布。

Example publish command:
发布示例命令：

```bash
clawhub publish ./skills/shared/cloudflare-openwebui-tunnel-operator \
  --slug cloudflare-openwebui-tunnel-operator \
  --name "Cloudflare Open WebUI Tunnel Operator" \
  --version 1.0.0 \
  --tags latest,cloudflare,tunnel,open-webui,1password,systemd
```
