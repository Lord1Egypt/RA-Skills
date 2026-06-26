# 🛡️ ClawGuard Guardian

运行时守护者，提供行为监控、拦截、回放、应急冻结功能。

## 通过 Agent 使用（推荐）

### 触发方式

当用户说以下内容时，Agent 会自动读取本 SKILL.md 并执行相应操作：

```
"启动守护"
"开启监控"
"查看状态"
"回放操作"
"冻结会话"
"停止监控"
"查看日志"
```

### 示例对话

```
用户: 帮我开启守护模式

Agent: 🛡️ Guardian 启动中...
      ↓
📝 会话 ID: session-xxx
🕐 开始时间: 2026-03-21 10:00:00

✅ Guardian 已启动，监听模式已启用


用户: 查看状态

Agent:
╔═══════════════════════════════════════════════════════════════╗
║  🛡️ Guardian 状态                                    ║
╠═══════════════════════════════════════════════════════════════╣
║  状态: 🟢 运行中                                    ║
║  会话数: 3                                           ║
║  操作数: 128                                         ║
║  拦截数: 2                                           ║
╚═══════════════════════════════════════════════════════════════╝


用户: 冻结当前会话

Agent: 🛡️ 会话已冻结: session-xxx
       冻结时间: 2026-03-21 10:30:00
       待处理操作: 3

       如需继续执行，请先解除冻结
```

---

## 通过命令行使用

### 基本命令

```bash
# 进入目录
cd guardian-skill && node cli.js

# 启动守护
node cli.js start
# 或
node cli.js monitor

# 查看状态
node cli.js status

# 回放最近会话
node cli.js replay

# 回放指定会话
node cli.js replay session-xxx

# 冻结会话
node cli.js freeze
node cli.js freeze session-xxx  # 冻结指定会话

# 解冻会话
node cli.js unfreeze
node cli.js unfreeze session-xxx  # 解冻指定会话

# 查看日志
node cli.js logs
node cli.js logs 100  # 查看最近 100 条
```

### 启动守护示例

```bash
$ node cli.js start

🛡️ Guardian 启动中...

📝 会话 ID: session-1711001234567-abc123
🕐 开始时间: 2026-03-21 10:00:00

✅ Guardian 已启动，共 0 个历史会话

监听模式已启用，等待操作...
```

### 回放会话示例

```bash
$ node cli.js replay

📺 会话回放:
────────────────────────────────────────
✅ [10:30:01] 执行命令: ls -la
✅ [10:30:05] 读取文件: /tmp/test.txt
🚫 [10:30:10] 尝试删除: /etc/passwd (已拦截)
✅ [10:30:15] 执行命令: cat /var/log/access.log
────────────────────────────────────────
```

---

## 拦截规则

### 路径规则

**禁止访问**：
```
/etc/*          # 系统配置
/root/*         # root 目录
/.ssh/*         # SSH 密钥
/.aws/*         # AWS 凭证
/.kube/*        # Kubernetes 配置
```

**需要确认**：
```
/etc/            # 系统目录
/var/           # 日志目录
```

### 命令规则

**禁止执行**：
```
rm -rf /         # 危险删除
rm -rf /home     # 删除用户目录
:(){ :|:& };:    # Fork 炸弹
dd if=* of=/dev/ # 磁盘写入
```

**需要确认**：
```
rm -rf           # 大范围删除
chmod 777        # 权限过宽
killall          # 批量终止
shutdown         # 系统关机
```

---

## 审计日志

日志位置：`~/.clawguard/logs/`

日志格式：
```json
{
  "timestamp": "2026-03-21T10:30:00.000Z",
  "sessionId": "session-xxx",
  "type": "operation",
  "action": "读取文件",
  "target": "/etc/passwd",
  "result": "BLOCKED",
  "riskLevel": "CRITICAL"
}
```

---

## 相关模块

- **Detect** - 威胁检测（触发 Guardian 联动）
- **Shield** - 提示词注入防护
- **Auditor** - Skill 安装前审计
- **Checker** - 配置安全检查

---

*版本: v3.0.0*
