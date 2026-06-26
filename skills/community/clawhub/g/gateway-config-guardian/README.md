# Gateway Guardian

<p align="center">中文丨<a href="https://github.com/Dios-Man/gateway-guardian/blob/main/README.en.md">English</a></p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/platform-Linux-blue.svg" alt="Platform: Linux">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-brightgreen.svg" alt="OpenClaw Skill">
</p>

> 一个给 OpenClaw 用户的网关防护 Skill。  
> 配置写坏了自动回滚，网关崩溃了自动重启，出事第一时间通知你。

---

## 它解决什么问题？

OpenClaw 的 AI 能力完全依赖网关（Gateway）。网关一旦挂掉，你就联系不上 AI 了。

常见的"网关挂掉"原因有两种：

**1. 配置文件被写坏**  
AI 在修改配置（比如添加 API Key、切换模型）时，可能因为格式错误或字段缺失，让 `openclaw.json` 变成无效文件。下次网关重启时直接起不来。

**2. 网关进程意外崩溃**  
内存问题、系统资源紧张、偶发性 bug，都可能让网关在运行中突然挂掉。

Gateway Guardian 会自动处理这两种情况，并在第一时间通知你。

---

## 工作方式

### 配置守护（实时）

每次 `openclaw.json` 发生变化，Guardian 会在毫秒内完成三关验证：

1. JSON 语法是否正确
2. 关键字段是否存在（`gateway.port` 必须有）
3. OpenClaw 自身的 schema 校验

验证失败时立刻回滚到最近一个合法备份。整个过程自动完成，无需你介入。

### 崩溃恢复（OnFailure）

如果网关在 60 秒内连续崩溃 3 次，Guardian 接管：
1. 检查配置是否有问题（有则先回滚）
2. 重启网关
3. 等待最多 30 秒确认端口可用
4. 成功则通知你，失败则发紧急告警

### 通知

无论是自动修复还是需要人工处理，都会推送通知到你的消息渠道（飞书 / Telegram / Discord 等）。

---

## 通知示例

**配置自动修复（无需操作）：**

```
✅ OpenClaw 网关守护

⏰ 时间：2026-03-09 22:10
📋 事件：配置文件损坏，已自动回滚并恢复
🔧 回滚至：openclaw.json.20260309-221005
📝 关键日志：
[22:10:03] ❌ Config invalid: missing gateway.port
[22:10:04] ✅ Rolled back to timestamp backup
[22:10:04] ✅ Gateway is running

💬 如果此次告警是由我的操作引起的，请将这条消息直接转发给我，
无需添加任何说明，我会自动了解情况并继续处理。
```

**网关崩溃恢复（无需操作）：**

```
✅ OpenClaw 网关守护 - 网关已恢复

⏰ 时间：2026-03-09 22:10
📋 事件：网关崩溃（配置正常），已自动重启
🔧 处置：重置失败记录 + 重启网关
✅ 结果：网关已恢复正常运行

💬 如果此次告警是由我的操作引起的，请将这条消息直接转发给我，
无需添加任何说明，我会自动了解情况并继续处理。
```

**需要人工处理：**

```
🚨 OpenClaw 网关守护 - 需要人工处理

⏰ 时间：2026-03-09 22:10
📋 事件：网关崩溃，自动恢复失败
❌ 原因：多次重启后网关仍无响应
📝 关键日志：
[22:10:03] Gateway failed repeatedly — starting recovery
[22:10:36] ❌ Gateway still unresponsive after 30s
🔍 网关日志：
Mar 09 22:10:06 node[xxx]: Error: EADDRINUSE: port 18789 already in use

请登录服务器手动处理。
```

**网关主动重启时（两条）：**

```
⚙️ 网关正在重启中，请稍候...
```
```
✅ 已恢复，请发消息继续对话。
```

> **关于"请将消息转发给我"：**  
> 网关重启会中断正在进行的任务。如果是 AI 在帮你做某件事时发生了重启，直接把这条通知转发给 AI，它就能立刻了解情况并继续。不转发也没关系，直接告诉 AI"刚才网关重启了"效果一样。

---

## 安装

**前置条件：**
- Linux 系统，`systemd --user` 可用
- OpenClaw Gateway 正在运行
- `inotify-tools`（安装时自动检测并安装，或手动：`sudo apt-get install -y inotify-tools`）

满足条件后，将以下链接发给你的 OpenClaw，并说"帮我安装"：

```
https://raw.githubusercontent.com/Dios-Man/gateway-guardian/main/SKILL.md
```

OpenClaw 会自动检测你的消息渠道和用户 ID，完成全部配置，并根据你的对话语言设置通知语言。

**安装过程：**
1. 备份当前配置（安装前快照）
2. 从 GitHub 拉取脚本文件
3. 注册 `openclaw-config-watcher` 服务（常驻监听配置文件）
4. 注册 `openclaw-recovery` 服务（网关崩溃时 OnFailure 触发）
5. 为网关服务添加 `ExecStopPost` 钩子（停止前发送通知）
6. 生成 `guardian.conf`（保存通知渠道兜底配置）

---

## 卸载

告诉 OpenClaw："卸载 gateway-guardian"

或者手动执行：

```bash
systemctl --user stop openclaw-config-watcher.service
systemctl --user disable openclaw-config-watcher.service
rm -f ~/.config/systemd/user/openclaw-config-watcher.service
rm -f ~/.config/systemd/user/openclaw-recovery.service
rm -f ~/.config/systemd/user/openclaw-gateway.service.d/recovery.conf
systemctl --user daemon-reload
systemctl --user reset-failed openclaw-gateway.service 2>/dev/null
```

卸载不会删除已有的配置备份（`~/.openclaw/config-backups/`），需要的话手动删除：

```bash
rm -rf ~/.openclaw/config-backups/
```

---

## 日志

```bash
tail -f /tmp/config-watcher.log    # 配置监听 + 通知日志
tail -f /tmp/gateway-recovery.log  # 崩溃恢复日志
ls -lt ~/.openclaw/config-backups/ # 时间戳备份列表
```

---

## 常见问题

**Q：Guardian 会影响 OpenClaw 的正常运行吗？**  
不会。config-watcher 使用 inotifywait 事件驱动，平时接近零 CPU 占用，只在配置发生变化时短暂运行。

**Q：通知发不出去怎么办？**  
检查 `guardian.conf` 里的 `FALLBACK_CHANNEL` 和 `FALLBACK_TARGET` 是否正确，或重新安装让 OpenClaw 重新检测。

**Q：通知发到哪里？**  
每次发通知前，Guardian 会查询最近活跃的对话 session，优先发私信。检测失败时兜底使用 `guardian.conf` 中的配置。

**Q：我手动改了配置，Guardian 会把我的改动回滚掉吗？**  
不会。只要改动合法（JSON 格式正确且包含必要字段），Guardian 会将其保存为新备份。只有无效配置才会被回滚。

**Q：`guardian.conf` 里的内容安全吗？**  
`guardian.conf` 只保存消息渠道和用户 ID（兜底配置），不含 API Key 或密码，且不会被上传到 GitHub。

---

## 技术架构

```
config-watcher 服务启动
    ↓
启动检查：验证当前配置
    ├─ 验证通过 → 保存备份
    └─ 验证失败 → 回滚 → 通知用户

openclaw.json 发生变化
    ↓
config-watcher（inotifywait 常驻）
    ├─ 验证通过 → 保存时间戳备份
    └─ 验证失败 → 回滚 → 通知用户

网关进程崩溃
    ↓
systemd 自动重启
    ↓
重启失败超过 3 次/60s → OnFailure 触发
    ↓
gateway-recovery
    ├─ 检查配置（有问题先回滚）
    ├─ 重启网关
    ├─ 等待 30s 确认端口可用
    ├─ 恢复成功 → 通知用户
    └─ 恢复失败 → 紧急通知（含错误日志）

网关主动重启
    ↓
ExecStopPost（pre-stop.sh）→ 发送"重启中"通知
    ↓
config-watcher 后台监测（每 5s 探测）
    └─ 检测到恢复 → 发送"已恢复"通知
```

---

## License

MIT
