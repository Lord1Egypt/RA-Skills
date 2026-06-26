# Daily Briefing - 每日晨报

[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

每日晨报生成工具，提供稳定、可复现的数据获取和简报生成能力。

## ✨ 特性

- **🌤️ 天气数据** - 自动获取北京天气（wttr.in API，30分钟缓存）
- **🚗 限行信息** - 代码化计算尾号限行规则（2025.12.29-2026.03.29）
- **📰 新闻抓取** - 三源合并：网易 + 新浪 + 搜狐
- **📊 自动分类** - 国际/国内/科技/财经/社会 五大分类
- **⚡ 快速生成** - 3-10秒完成简报（含缓存）
- **🛡️ 容错设计** - API失败时提供备用数据

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/caoyachao/daily-briefing.git
cd daily-briefing

# 安装依赖
npm install
```

### 使用

```bash
# 生成今日晨报（完整版，含新闻）
node scripts/generate-briefing.mjs

# 生成次日晨报
node scripts/generate-briefing.mjs --tomorrow

# 生成简化版（天气+限行，无新闻）
node scripts/generate-briefing.mjs --simple

# 生成无新闻版本
node scripts/generate-briefing.mjs --no-news

# JSON 格式输出
node scripts/generate-briefing.mjs --json
```

## 📋 输出示例

```
📅 **2026年3月19日星期四 今日简报**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌤️ **北京今日天气**
• 当前气温：**10°C**（体感 10°C）
• 最高气温：**16°C**
• 最低气温：**5°C**
• 天气状况：**晴朗**
• 湿度：**25%**
• 风力：**WNW 6 km/h**
• 日出/日落：**06:20 AM / 06:25 PM**

💡 **穿衣建议**：早晚较凉，建议穿外套+长袖...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚗 **北京尾号限行（3月19日星期四）**
• 今日限行尾号：**1 和 6**
• 限行时间：**07:00-20:00**
• 限行范围：**五环路以内道路（不含五环路）**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📰 **今日要闻精选**

【国际要闻】
1. 伊朗为遇难官兵和官员举行葬礼
...

【国内时政】
1. 全国两会后首"虎"任上落马
...

【科技动态】
1. 小米新一代SU7正式上市
...

【财经市场】
1. 美联储宣布维持利率不变
...

【社会热点】
1. 4月1日起医保新规落地
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **简报统计**
• 天气数据：✅ 实时获取
• 限行信息：✅ 已获取
• 新闻条数：✅ 25条
• 生成时间：2026/3/19 23:31 CST
```

## 🔧 API 使用

```javascript
import { generateBriefing, generateBriefingData } from './scripts/generate-briefing.mjs';

// 生成完整晨报（含新闻）
const briefing = await generateBriefing({
  city: 'Beijing',
  dayOffset: 0,  // 0=今天, 1=明天
  includeNews: true
});

// 生成结构化数据
const data = await generateBriefingData({ dayOffset: 0 });
console.log(data);
// {
//   date: "2026-03-19T00:00:00.000Z",
//   dateStr: "2026年3月19日星期四",
//   weather: { ... },
//   trafficLimit: { ... },
//   news: { ... }
// }
```

## 📁 文件结构

```
daily-briefing/
├── scripts/
│   ├── data-collector.mjs      # 天气+限行数据获取
│   ├── news-collector.mjs      # 新闻抓取与分类
│   └── generate-briefing.mjs   # 简报生成主程序
├── .cache/                      # 数据缓存（30分钟TTL）
├── manifest.yaml               # OpenClaw Skill 配置
├── SKILL.md                    # Skill 文档
└── package.json                # npm 配置
```

## 🌍 数据来源

| 数据类型 | 来源 | 更新频率 | 方式 |
|---------|------|---------|------|
| 天气 | wttr.in API | 实时 | curl |
| 限行 | 本地规则配置 | 按周期更新 | 代码计算 |
| 新闻 | 网易、新浪、搜狐 | 实时 | curl + cheerio |

## 🚗 北京限行规则（2025.12.29-2026.03.29）

| 星期 | 限行尾号 | 时间 | 范围 |
|------|---------|------|------|
| 周一 | 3和8 | 07:00-20:00 | 五环路以内 |
| 周二 | 4和9 | 07:00-20:00 | 五环路以内 |
| 周三 | 5和0 | 07:00-20:00 | 五环路以内 |
| 周四 | 1和6 | 07:00-20:00 | 五环路以内 |
| 周五 | 2和7 | 07:00-20:00 | 五环路以内 |
| 周末 | 不限行 | - | - |

## 🔗 Cron 集成

配合 OpenClaw Cron 使用：

```json
{
  "id": "daily-briefing-morning",
  "agentId": "main",
  "name": "每日晨报-早间（7:15）",
  "schedule": {
    "kind": "cron",
    "expr": "0 15 7 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "生成每日晨报：\n\n执行命令获取完整简报：\n```bash\nnode /root/.openclaw/skills/daily-briefing/scripts/generate-briefing.mjs\n```\n\n此命令会自动获取天气、限行、新闻并生成格式化简报。\n\n**邮件通知**：\n```javascript\nimport { sendEmail } from '/root/.openclaw/skills/email-sender/scripts/email-api.mjs';\nawait sendEmail({\n  to: 'caoyachao@sohu.com',\n  subject: '【定时任务通知】' + new Date().toLocaleDateString('zh-CN'),\n  text: generatedContent\n});\n```"
  }
}
```

## ⚡ 性能对比

| 维度 | 纯AI生成 | 本工具（Skill+脚本） |
|------|---------|---------------------|
| 天气准确性 | 依赖AI调用，可能失败 | ✅ 专用脚本，带缓存和容错 |
| 限行准确性 | AI可能记忆错误 | ✅ 代码化规则，准确计算 |
| 新闻时效性 | AI抓取可能遗漏 | ✅ 脚本+kimi_fetch混合策略 |
| 执行时间 | 不稳定（10-60秒） | ✅ 快速（3-10秒） |
| 随机性 | 高 | ✅ 低（固定代码逻辑） |
| 可维护性 | 低（改提示语） | ✅ 高（改代码即可） |

## 📜 更新日志

### v1.1.0 (2026-03-19)
- ✨ 新增新闻自动抓取功能（网易+新浪+搜狐）
- ✨ 新闻自动分类（5大类别）
- ✨ 新增 `--no-news` 参数
- 🔧 优化缓存机制

### v1.0.0 (2026-03-19)
- 🎉 初始版本
- ✨ 天气数据获取（wttr.in）
- ✨ 限行规则代码化
- ✨ 简报生成功能

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**作者**: Kimi Claw  
**仓库**: https://github.com/caoyachao/daily-briefing
