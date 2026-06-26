# Command Output Display - 命令输出展示技能

## 核心原则

**用户应该能像坐在你旁边看你操作终端一样，看到每一个命令和它的完整输出！**

## 📋 展示规范

### 1. 命令执行前

**格式：**
```bash
$ <command>
```

**说明：**
- 使用 `$` 前缀表示要执行的命令
- 如果是多行命令，完整展示
- 如果有注释，用 `#` 标注

**示例：**
```bash
$ systemctl --user status openclaw-gateway-boss.service --no-pager
```

```bash
$ cat > /tmp/test.json << 'EOF'
{
  "config": "value"
}
EOF
```

### 2. 命令执行后

**格式：**
```bash
# 输出：
<command output here>
```

**说明：**
- 使用 `# 输出：` 标记输出开始
- 完整展示 stdout 和 stderr
- 保持原始格式（包括颜色代码如果有的话）
- 不要截断重要信息

**示例：**
```bash
# 输出：
● openclaw-gateway-boss.service - OpenClaw Gateway - Boss (爪爪机器人)
   Loaded: loaded (/home/admin/.config/systemd/user/openclaw-gateway-boss.service; enabled)
   Active: active (running) since Thu 2026-03-12 16:04:48 CST
 Main PID: 5820 (MainThread)
```

### 3. 错误输出

**格式：**
```bash
# 输出（错误）：
<error output>

# 错误信息：
- 退出码：<exit code>
- 详细说明：<details>
```

**示例：**
```bash
# 输出（错误）：
Job for openclaw-gateway-boss.service failed because the control process exited with error code.

# 错误信息：
- 退出码：1
- 服务状态：failed
- 可能原因：配置文件不存在
```

## 🎯 完整流程示例

### 示例 1: 服务管理

```
📝 目标：检查 boss 网关服务状态

执行命令：
```bash
$ systemctl --user status openclaw-gateway-boss.service --no-pager -n 10
```

# 输出：
● openclaw-gateway-boss.service - OpenClaw Gateway - Boss (爪爪机器人)
   Loaded: loaded (/home/admin/.config/systemd/user/openclaw-gateway-boss.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2026-03-12 16:04:48 CST; 6s ago
 Main PID: 5820 (MainThread)
   CGroup: /user.slice/user-1000.slice/user@1000.service/openclaw-gateway-boss.service
           └─5820 /usr/bin/node /opt/openclaw/dist/index.js gateway

Mar 12 16:04:48 iZbp14orusdl51yeoyqk9yZ systemd[992]: Started OpenClaw Gateway - Boss (爪爪机器人).

✅ 服务运行正常
```

### 示例 2: 文件操作

```
📝 目标：创建配置文件

执行命令：
```bash
$ cat > /home/admin/.openclaw/openclaw-boss.json << 'EOF'
{
  "gateway": {
    "port": 19922,
    "mode": "local"
  }
}
EOF
```

# 输出：
（无输出表示成功）

验证文件：
```bash
$ ls -lh /home/admin/.openclaw/openclaw-boss.json
```

# 输出：
-rw-r--r-- 1 admin admin 6.0K Mar 12 17:50 /home/admin/.openclaw/openclaw-boss.json

✅ 文件创建成功，大小 6KB
```

### 示例 3: 多步骤操作

```
📝 任务：配置新网关

━━━━━━━━━━━━━━━━━━━━━━━━━━━
步骤 1/4: 创建目录
━━━━━━━━━━━━━━━━━━━━━━━━━━━

执行命令：
```bash
$ mkdir -p /home/admin/.openclaw/agents/boss
```

# 输出：
（无输出）

✅ 完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━
步骤 2/4: 复制 agent 配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━

执行命令：
```bash
$ cp -r /home/admin/.openclaw/agents/main/* /home/admin/.openclaw/agents/boss/
```

# 输出：
（无输出）

✅ 完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━
步骤 3/4: 创建配置文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[展示文件内容...]

✅ 配置文件已创建

━━━━━━━━━━━━━━━━━━━━━━━━━━━
步骤 4/4: 验证结构
━━━━━━━━━━━━━━━━━━━━━━━━━━━

执行命令：
```bash
$ tree -L 2 /home/admin/.openclaw/agents/boss/
```

# 输出：
/home/admin/.openclaw/agents/boss/
├── agent
│   └── agent.json
└── sessions
    └── sessions.json

✅ 目录结构正确

━━━━━━━━━━━━━━━━━━━━━━━━━━━
总结：所有步骤完成！
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 示例 4: 调试问题

```
⚠️ 服务启动失败，正在调试...

📝 步骤 1: 查看服务状态

执行命令：
```bash
$ systemctl --user status openclaw-gateway-boss.service --no-pager
```

# 输出：
● openclaw-gateway-boss.service - OpenClaw Gateway - Boss
   Loaded: loaded
   Active: failed (Result: exit-code)
 Main PID: 1234 (code=exited, status=1/FAILURE)

❌ 服务启动失败

---

📝 步骤 2: 查看详细日志

执行命令：
```bash
$ journalctl --user -u openclaw-gateway-boss.service -n 20 --no-pager
```

# 输出：
Mar 12 16:05:14 node[1234]: error: unknown option '--config'
Mar 12 16:05:14 systemd[992]: openclaw-gateway-boss.service: Failed with result 'exit-code'.

🔍 发现问题：命令行参数 `--config` 不被支持

---

📝 步骤 3: 检查正确的参数

执行命令：
```bash
$ node /opt/openclaw/dist/index.js gateway --help
```

# 输出：
Usage: gateway [options]

Options:
  --port <port>    Gateway port (default: 10041)
  --verbose        Enable verbose logging
  --help           Show help

✅ 应该使用 `--port` 而不是 `--config`
```

## 🛠️ 特殊情况处理

### 1. 长输出

如果输出很长（超过 50 行）：
```bash
# 输出（前 50 行）：
[显示前 50 行]

... (共 234 行，需要看完整输出吗？)
```

### 2. 二进制输出

如果命令产生二进制输出或乱码：
```bash
# 输出：
[二进制数据，已跳过]

# 文件信息：
-rwxr-xr-x 1 admin admin 1.2M Mar 12 17:50 binary_file
```

### 3. 交互式命令

如果需要用户交互：
```
⚠️ 这个命令需要交互输入：
```bash
$ openclaw channels login
```

输出：
```
? 选择渠道类型：
❯ WhatsApp
  Telegram
  Discord
```

需要你在终端亲自操作，我没法代劳。要我继续其他步骤吗？
```

### 4. 后台命令

如果命令在后台运行：
```
📝 启动后台服务...

执行命令：
```bash
$ systemctl --user start openclaw-gateway.service &
```

# 输出：
[后台运行中...]

等待 3 秒后检查状态：
```bash
$ systemctl --user is-active openclaw-gateway.service
```

# 输出：
active

✅ 服务已在后台启动
```

## 📊 输出解读

不要只展示输出，还要帮助解读：

```bash
# 输出：
tcp        0      0 0.0.0.0:19922    0.0.0.0:*    LISTEN    5820/openclaw-gatew

# 解读：
- 端口 19922 正在监听
- 进程 ID: 5820
- 绑定地址：0.0.0.0 (所有接口)
✅ 网关已成功启动
```

## ✅ 检查清单

执行命令后，确保：
- [ ] 展示了完整的命令
- [ ] 展示了完整的输出
- [ ] 包含了错误信息（如果有）
- [ ] 提供了解读或总结
- [ ] 格式清晰易读

---

**目标：** 让用户感觉就像坐在你旁边，看着你在终端上操作一样！
