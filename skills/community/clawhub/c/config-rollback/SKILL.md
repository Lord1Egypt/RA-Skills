---
name: config-rollback
description: Auto-rollback protection for config changes. Backs up before edit, sets a 5-minute system timer to restore if things go wrong. Works with any service config, not just OpenClaw.
---

# Config Rollback — 改配置再也不怕炸

## Story

凌晨两点，你改了一行 nginx 配置，reload，网站挂了。SSH 连不上——因为你也改了 sshd_config。

你盯着黑屏，后悔没备份。

**这个 skill 就是你的后悔药。**

改配置前，它先备份，然后设一个 5 分钟的系统级定时炸弹。如果 5 分钟内你没说"没问题"——它自动把配置还原，重启服务。就算你把 SSH 搞断了，定时任务照样跑，因为它用的是 `at` 命令，不依赖你的连接。

## How It Works

```
You: "自动回滚"

Agent:
1. cp config → config.bak
2. echo "restore" | at now + 5 minutes  (system-level, survives disconnect)
3. Returns job ID

You: [make changes, test]

Happy? → atrm <job-id>     (cancel the bomb)
Broken? → wait 5 min       (auto-restores)
```

## Usage

Say "auto rollback" or "自动回滚" before editing any config:

```bash
# Backup + set 5-min restore timer
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
echo "cp /etc/nginx/nginx.conf.bak /etc/nginx/nginx.conf && systemctl reload nginx" | at now + 5 minutes

# Make your changes...
vim /etc/nginx/nginx.conf
systemctl reload nginx

# If everything works, cancel the timer:
atrm <job-id>
```

## When to use

- Editing nginx, sshd, firewall, or any service config
- Changing API gateway routing rules
- Updating DNS or proxy settings
- Any change that could lock you out of a remote server

## Key Principle

The restore timer is a **system-level** scheduled task (`at` / `crontab`). It does NOT depend on your shell session, SSH connection, or any application. Even if you brick the service, the timer still fires.
