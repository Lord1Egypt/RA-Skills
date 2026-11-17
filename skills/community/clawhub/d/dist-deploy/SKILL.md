---
name: dist-deploy
description: >-
  Deploy static build output (dist / build / any folder) to any SSH-reachable server: tar, scp, then atomic
  directory swap on the remote host, with automatic backup of the previous release, backup rotation,
  ownership fixup and a post-deploy hook. Nothing is hardcoded — server, port, path, key are all parameters.
  ｜ 通用前端/静态构建产物远程部署，支持任意服务器地址与端口、旧版本备份与回滚。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - ssh
        - scp
        - tar
    emoji: "\U0001F680"
---

# dist-deploy — deploy build artifacts over SSH

Pack a local folder, upload it, and swap it into place on the remote server **atomically**, keeping the
previous release around for rollback. No server address, port, or path is baked in — everything is passed
as arguments, so the skill works for any host.

Two equivalent implementations:

| Platform | Script |
| -------- | ------ |
| Windows (PowerShell 7+) | `scripts/deploy-dist.ps1` |
| macOS / Linux | `scripts/deploy-dist.sh` |

`<SKILL_DIR>` below means the folder containing this file.

## Quick start

PowerShell:

```powershell
pwsh <SKILL_DIR>\scripts\deploy-dist.ps1 `
  -Source .\dist -Server root@192.0.2.10 -Port 22 -Target /var/www/app/dist
```

Bash:

```bash
bash <SKILL_DIR>/scripts/deploy-dist.sh -s ./dist -H root@192.0.2.10 -p 22 -t /var/www/app/dist
```

With key, ownership and a reload hook:

```powershell
pwsh <SKILL_DIR>\scripts\deploy-dist.ps1 -Source .\dist -Server deploy@host -Port 2222 `
  -Key $HOME\.ssh\id_ed25519 -Target /opt/app/dist -Owner www-data:www-data `
  -PostCommand "nginx -t && systemctl reload nginx"
```

```bash
bash <SKILL_DIR>/scripts/deploy-dist.sh -s ./dist -H deploy@host -p 2222 \
  -k ~/.ssh/id_ed25519 -t /opt/app/dist -o www-data:www-data \
  -c "nginx -t && systemctl reload nginx"
```

## Parameters

| PowerShell | Bash | Required | Meaning |
| ---------- | ---- | -------- | ------- |
| `-Source` | `-s` | yes | Local folder to deploy, e.g. `.\dist`. Its *contents* land at the target root (no extra folder level). |
| `-Server` | `-H` | yes | `user@host`, or `host` to use the ssh default user. |
| `-Target` | `-t` | yes | Remote absolute path, e.g. `/var/www/app/dist`. |
| `-Port` | `-p` | no | SSH port, default 22. |
| `-Key` | `-k` | no | Private key path; defaults to ssh-agent / `~/.ssh/config`. |
| `-Owner` | `-o` | no | `chown -R` owner after extraction, e.g. `www-data:www-data`. |
| `-PostCommand` | `-c` | no | Command run on the server after a successful swap (reload nginx, restart container…). |
| `-KeepBackups` | `-n` | no | Number of `<target>.bak.*` releases to keep, default 3. |
| `-Fresh` | `-f` | no | Delete the target instead of backing it up (no rollback). |
| `-DryRun` | `-d` | no | Print what would run, change nothing. |

## How it works

1. `tar -czf` the source folder locally.
2. `scp` the archive to `/tmp/dist-deploy-<id>.tgz`.
3. On the server: extract into `<parent>/.deploy-tmp-<pid>`, optionally `chown -R`, rename the old target
   to `<target>.bak.<timestamp>`, then `mv` the new folder into place.
4. Remove stale backups beyond `KeepBackups`, delete the remote archive and local temp files.
5. Run `PostCommand` last, so a failing reload is visible after files are already live.

Because the old directory is renamed before the new one is moved in, there is no window where the web root
serves a half-extracted release.

## Rollback

The script prints `backup: /opt/app/dist.bak.20261102153000`. Restore it with:

```bash
ssh -p 22 user@host 'rm -rf /opt/app/dist && mv /opt/app/dist.bak.20261102153000 /opt/app/dist'
```

Then reload whatever serves it:

```bash
ssh -p 22 user@host 'nginx -t && systemctl reload nginx'
```

## Manual equivalent (no script)

```bash
tar -czf /tmp/dist.tgz -C ./dist .
scp -P 2222 /tmp/dist.tgz root@host:/tmp/dist.tgz
ssh -p 2222 root@host 'set -e; rm -rf /opt/app/.deploy-tmp && mkdir -p /opt/app/.deploy-tmp && \
  tar -xzf /tmp/dist.tgz -C /opt/app/.deploy-tmp && \
  rm -rf /opt/app/dist.bak.prev && mv /opt/app/dist /opt/app/dist.bak.prev 2>/dev/null || true; \
  mv /opt/app/.deploy-tmp /opt/app/dist && rm -f /tmp/dist.tgz'
```

## Notes

- Needs `ssh`, `scp` and `tar` locally (Windows 10+ ships OpenSSH and bsdtar).
- First connection prompts for a host key. For unattended runs, pre-seed with `ssh-keyscan` or set
  `StrictHostKeyChecking accept-new` in `~/.ssh/config`.
- Without a key the script waits for an interactive password; do not use it in a non-interactive pipeline.
- If the target is a mounted volume (container bind mount, NFS), `mv` may fail or move across filesystems —
  in that case deploy to a sibling directory and switch a symlink instead.
- `-Fresh` / `-f` is not rollback-able; use it only when the old release is disposable.
- Overwriting a live directory is destructive: sanity-check `-Target` first (a dry run is cheap).

## 中文摘要

把本地构建目录（默认 `dist`）打包上传到任意 SSH 可达服务器并原子替换线上目录，旧版本自动备份为
`<target>.bak.<时间戳>`、自动保留最近 N 份、支持属主修正与部署后钩子命令。服务器地址、端口、路径全部走参数，
不写死任何环境。`-Fresh`/`-f` 为「先删后传」模式，不回滚。
