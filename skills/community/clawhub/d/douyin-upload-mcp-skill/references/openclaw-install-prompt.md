# 发给 OpenClaw 的安装提示词

把下面这段和 `douyin-upload-mcp-skill-*.tar.gz` 附件一起发给目标机器的 OpenClaw。

```text
请帮我把这个附件安装成 OpenClaw skill，并完成自动配置。

要求：
1. 你需要自己完成安装，不要让我执行命令。
2. 先查找我刚发的附件或本机下载目录里的 `douyin-upload-mcp-skill*.tar.gz`。
   常见位置包括：
   - 当前 OpenClaw 会话附件路径
   - ~/Downloads
   - /mnt/c/Users/*/Downloads
   - /tmp
   - ~/.openclaw/workspace
3. 找到压缩包后，执行：
   mkdir -p /tmp/douyin-skill-install
   tar -xzf <压缩包绝对路径> -C /tmp/douyin-skill-install
   cd /tmp/douyin-skill-install
   node scripts/install-openclaw-skill.js --apply
4. 如果 `node` 不存在或版本低于 22，请先帮我安装/切换 Node 22+，再继续。
5. 如果缺浏览器，请安装或配置 Chrome/Edge。
6. 安装器完成后，请继续执行健康检查。若安装器复制到了 `~/.openclaw/skills/douyin-upload-mcp-skill`，进入这个目录；若使用 ClawHub 安装，则进入 `~/.openclaw/workspace/skills/douyin-upload-mcp-skill`：
   cd ~/.openclaw/skills/douyin-upload-mcp-skill || cd ~/.openclaw/workspace/skills/douyin-upload-mcp-skill
   node scripts/preflight.js --online
   node scripts/agent-ready.js
   node scripts/douyin-schedule-manager.js status
7. 最后只告诉我：
   - 是否安装成功
   - 是否已注册 douyin MCP
   - supervisor/daemon 是否正常
   - 定时任务状态
   - 还需要我人工处理什么，比如首次抖音扫码、短信、安全验证、飞书权限

如果你无法直接读取附件，只回复：
“我看不到附件，请把 `douyin-upload-mcp-skill*.tar.gz` 下载到电脑 Downloads 文件夹后告诉我已下载。”
不要要求我手动执行命令。
```

注意：
- 如果目标 OpenClaw 接的是自己的飞书机器人，需要安装后修改 skill 目录里的 `.env.local`，填写 `FEISHU_APP_ID`、`FEISHU_APP_SECRET` 和 `DOUYIN_FEISHU_RECEIVE_ID`。
- 如果使用包里自带的飞书配置，消息会发到包内配置的飞书会话。
- 包不包含抖音登录态，首次使用仍需扫码和可能的短信/安全验证。
