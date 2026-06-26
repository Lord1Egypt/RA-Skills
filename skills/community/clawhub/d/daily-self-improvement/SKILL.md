---
name: daily-self-improvement
slug: daily-self-improvement
version: 1.0.0
description: 每日自动总结问题、搜索改进、做自我反思，持续提升 AI 能力。每天晚上运行，收集当天的错误和问题，分析模式，搜索 ClawHub 上的改进方案，生成报告并推送到 Discord。
author: sunnyhot
license: MIT
homepage: https://github.com/sunnyhot/daily-self-improvement
keywords:
  - self-improvement
  - learning
  - automation
  - daily-report
  - reflection
  - failure-analysis
  - openclaw
  - skill
metadata:
  clawdbot:
    emoji: 📊
    requires:
      bins: ["node"]
    optionalBins: ["clawhub"]
    os: ["linux", "darwin", "win32"]
    configPaths:
      - config/settings.json
---

# Daily Self-Improvement

**每日自动总结问题、搜索改进、做自我反思，持续提升 AI 能力**

---

## 🎯 核心功能

### 1. 收集问题数据
- ✅ 从 `failure-monitor-log.json` 读取失败记录
- ✅ 从 daily notes 提取问题标记
- ✅ 从 `corrections.md` 读取用户纠正

### 2. 分析问题模式
- ✅ 分类问题类型
- ✅ 统计出现频率
- ✅ 识别重复模式

### 3. 搜索改进方案
- ✅ 去 ClawHub 搜索相关技能
- ✅ 生成安装建议

### 4. 自我反思
- ✅ 提取经验教训
- ✅ 更新 memory 文件
- ✅ 记录到 daily note

### 5. 生成报告
- ✅ 保存 Markdown 报告
- ✅ 推送到 Discord 线程

---

## 📅 使用方法

### 手动运行

```bash
cd ~/.openclaw/workspace/skills/daily-self-improvement/scripts
node run.cjs
```

### 设置定时任务（推荐）

```bash
openclaw cron add \
  --name "daily-self-improvement" \
  --cron "0 22 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --message "运行 daily-self-improvement: 总结今天遇到的问题，搜索改进方案，做自我反思，生成报告。"
```

**运行时间**: 每天晚上 10 点（一天结束时）

---

## 📋 工作流程

```
触发 (22:00)
    │
    ▼
收集问题数据
├── failure-monitor-log.json
├── daily notes
└── corrections.md
    │
    ▼
分析问题模式
├── 分类
├── 统计
└── 识别重复
    │
    ▼
搜索改进方案
└── ClawHub 搜索
    │
    ▼
自我反思
├── 提取经验
├── 更新 memory
└── 记录 daily note
    │
    ▼
生成报告
├── Markdown 文件
└── Discord 推送
```

---

## 📊 报告格式

```markdown
# 📊 每日自我改进报告

**日期**: 2026-03-14

## ❌ 今日问题

| 问题类型 | 数量 | 严重程度 |
|---------|------|---------|
| failure | 3 | 🔴 high |
| daily-note | 2 | 🟡 medium |

## 💡 改进建议

1. **self-improving** - 自我反思和学习
   `clawhub install self-improving`

2. **failure-monitor** - 监控失败和自动修复
   `clawhub install failure-monitor`

## 📝 下一步行动

- [ ] 检查 failure-monitor 配置
- [ ] 更新相关技能
- [ ] 记录经验到 MEMORY.md

---
*自动生成 by daily-self-improvement*
```

---

## ⚙️ 配置

编辑 `config/settings.json`:

```json
{
  "reportTime": "22:00",
  "timezone": "Asia/Shanghai",
  "discordChannel": "YOUR_DISCORD_CHANNEL_ID",
  "dataSources": {
    "failureMonitor": "memory/failure-monitor-log.json",
    "corrections": "~/self-improving/corrections.md",
    "dailyNotes": "memory/"
  },
  "clawhubSearch": {
    "enabled": true,
    "keywords": ["discord", "automation", "monitoring"]
  },
  "notifications": {
    "discord": true,
    "email": false
  }
}
```

---

## 🔗 相关技能

| 技能 | 功能 | 安装命令 |
|------|------|---------|
| **self-improving** | 自我反思和学习 | `clawhub install self-improving` |
| **failure-monitor** | 监控失败和自动修复 | `clawhub install failure-monitor` |
| **find-skills** | 搜索和发现技能 | `clawhub install find-skills` |

---

## 📁 文件结构

```
daily-self-improvement/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档
├── package.json          # 包信息
├── LICENSE               # MIT 许可证
├── .gitignore            # Git 忽略文件
├── scripts/
│   └── run.cjs           # 主脚本
└── config/
    └── settings.json     # 配置文件
```

---

## 🚀 安装

### 从 ClawHub 安装

```bash
clawhub install daily-self-improvement
```

### 从 GitHub 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/sunnyhot/daily-self-improvement
```

---

## 💡 核心价值

- **持续学习** - 每天自动总结问题
- **主动改进** - 搜索更好的解决方案
- **避免重复** - 记录经验教训
- **透明报告** - 让用户知道 AI 的进步

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 支持收集问题数据
- ✅ 支持分析问题模式
- ✅ 支持 ClawHub 搜索
- ✅ 支持 Discord 推送

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/sunnyhot/daily-self-improvement

---

## 📄 许可证

MIT License
