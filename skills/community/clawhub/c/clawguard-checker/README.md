# 🔧 ClawGuard Checker

OpenClaw 配置安全检查器，支持智能加固建议。

## 通过 Agent 使用（推荐）

### 触发方式

当用户说以下内容时，Agent 会自动读取本 SKILL.md 并执行检查：

```
"检查配置安全"
"安全体检"
"加固配置"
"如何让配置更安全"
"配置有什么风险"
```

### 示例对话

```
用户: 帮我检查一下 OpenClaw 的配置安全

Agent: 正在检查配置...
      (读取 openclaw.json，按指南检测)
      ↓
📋 发现的问题:
   1. 🔴 Gateway 绑定到 0.0.0.0
      修复: 将 bind 改为 "127.0.0.1"
   2. 🔴 命令执行模式为 full
      修复: 改为 "allowlist" 模式
   3. 🟠 沙箱未启用
      修复: 设置 sandbox.enabled = true

建议运行: node cli.js --fix 生成加固配置
```

---

## 通过命令行使用

### 基本用法

```bash
# 进入目录
cd checker-skill && node cli.js

# 检查默认配置（自动查找 ~/.openclaw/openclaw.json）
node cli.js

# 检查指定配置
node cli.js ~/.openclaw/openclaw.json

# 深度检查
node cli.js --deep

# 生成加固配置
node cli.js --fix

# 指定配置文件并生成加固
node cli.js ~/.openclaw/openclaw.json --fix

# 输出报告
node cli.js --output report.json
```

### 加固配置示例

```bash
# 生成加固配置
node cli.js ~/.openclaw/openclaw.json --fix

# 输出: openclaw.json.hardened.json
# 手动应用:
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
cp ~/.openclaw/openclaw.json.hardened.json ~/.openclaw/openclaw.json
```

### 输出示例

```
🔧 ClawGuard v3 Checker - 配置检查中...

╔═══════════════════════════════════════════════════════════════╗
║              🔧 配置安全检查报告                             ║
╠═══════════════════════════════════════════════════════════════╣
║  配置文件: ~/.openclaw/openclaw.json                       ║
║  风险评分: 45/100                                       ║
║  最高风险: 🟠 高危                                      ║
║  发现问题: 3 项                                         ║
╚═══════════════════════════════════════════════════════════════╝

⚠️  发现问题:

1. 🔴 [Gateway 绑定地址]
   问题: Gateway 绑定到 0.0.0.0，暴露公网
   修复: 将 bind 改为 "127.0.0.1"

2. 🔴 [命令执行模式]
   问题: tools.exec.security = "full"
   修复: 改为 "allowlist" 模式

🛡️ 加固配置已生成: openclaw.json.hardened.json
```

---

## 检测项目

| 检测项 | 风险 | 说明 |
|--------|------|------|
| Gateway 绑定 0.0.0.0 | 🔴 | 暴露公网 |
| 未启用认证 | 🔴 | 无访问控制 |
| security: "full" | 🔴 | 允许任意命令 |
| TLS 未启用 | 🟠 | 通信未加密 |
| 沙箱未启用 | 🟠 | 无隔离 |

---

## 相关模块

- **Auditor** - Skill 安装前审计
- **Shield** - 提示词注入检测
- **Guardian** - 运行时守护

---

*版本: v3.0.0*
