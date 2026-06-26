# Daily Self-Improvement

**每日自动总结问题、搜索改进、做自我反思，持续提升 AI 能力**

---

## 🎯 功能

1. **总结当天问题**
   - 从 failure-monitor 读取失败记录
   - 从 daily notes 提取问题
   - 从 corrections 读取用户纠正

2. **分析问题模式**
   - 分类问题类型
   - 统计频率
   - 识别重复模式

3. **搜索改进方案**
   - 去 ClawHub 搜索相关技能
   - 生成改进建议

4. **自我反思**
   - 提取经验教训
   - 更新 memory 文件
   - 记录到 daily note

5. **生成报告**
   - 保存 Markdown 报告
   - 推送到 Discord 线程

---

## 📅 使用方法

### 手动运行

```bash
cd ~/.openclaw/workspace/skills/daily-self-improvement/scripts
node run.cjs
```

### 设置定时任务

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

## 📊 报告格式

```markdown
# 📊 每日自我改进报告

**日期**: 2026-03-14

## ❌ 今日问题

| 问题类型 | 数量 |
|---------|------|
| failure | 3 |
| daily-note | 2 |

## 💡 改进建议

- **self-improving**: 自我反思和学习
  `clawhub install self-improving`

- **failure-monitor**: 监控失败和自动修复
  `clawhub install failure-monitor`

## 📝 下一步行动

- [ ] 检查 failure-monitor 配置
- [ ] 更新相关技能
- [ ] 记录经验到 MEMORY.md

---
*自动生成 by daily-self-improvement*
```

---

## 🔗 相关技能

- **self-improving** - 自我反思和学习
- **failure-monitor** - 监控失败和自动修复
- **find-skills** - 搜索和发现技能
- **clawhub-skill-installer** - 安装技能

---

## 📁 文件结构

```
daily-self-improvement/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档
├── package.json          # 包信息
├── scripts/
│   └── run.cjs           # 主脚本
└── config/
    └── settings.json     # 配置文件
```

---

## 🚀 安装

```bash
# 从 ClawHub 安装
clawhub install daily-self-improvement

# 或从本地安装
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw-community/daily-self-improvement
```

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

---

## 📄 许可证

MIT License

---

**🎉 让 AI 持续自我提升！**
