# Claw Seatbelt 🛡️ (OpenClaw 安全带)

这是一款为你修改 `openclaw.json` 准备的“安全带”。它不像普通插件那样全天候运行，而是只在你需要修改配置并备份时，提供 10 秒的自动回滚保护。

## 特色功能
- **按需保护**：仅在运行备份脚本时触发，不浪费系统资源。
- **10秒无敌险**：修改配置后若 Gateway 无法在 10 秒内恢复，自动回退到最新备份并重启。
- **极简设计**：无需复杂配置，即装即用。

## Usage
The skill primarily runs as a background watchdog.

### Manual Check
```bash
./bin/watchdog.sh
```

## How it works
1. Probes the local Gateway status.
2. If down, captures the current "broken" config for debugging.
3. Locates the most recent timestamped backup in `~/.openclaw/backups/`.
4. Restores and restarts the Gateway service.
