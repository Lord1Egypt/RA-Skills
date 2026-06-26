# 📜 每日毛选语录推送

> **解一语录，传一智慧** — 每天清晨，在算法试图麻痹你时，强制进行一次高强度认知重启。

**daily-maoxuan-push** 是一款基于 OpenClaw 的 AI 自动化技能。每天从《毛泽东选集》中选出一条语录，生成 2000+ 字的深度认知解读，配以高清配图和语音播报，推送到你的 Obsidian 笔记库和 Telegram。

---

## ✨ 核心特色

### 🤖 AI 深度解读（七章结构）

每条语录不是简单翻译，而是从 **语义追溯 → 历史张力 → 跨时空映射 → 实证链条 → 当代痛点 → 行动建议** 七个维度深度解构。

### 🎨 智能配图

调用 Seedream API 生成 2K 高清配图，风格与语录主题深度契合。

### 🎤 自然语音播报

Edge-TTS 自然语言合成，20-30秒完整播报，Obsidian 直接播放。

### 📱 多渠道推送

- **Obsidian**：标准 Markdown 文档，兼容双向链接
- **Telegram**：直接推送到聊天，随时可读

### ⏰ 定时自动化

配置一次，每天 9:00 自动执行，无需人工干预。

---

## 🚀 快速开始

### 1. 安装技能

```bash
clawhub install daily-maoxuan-push
```

### 2. 配置环境变量

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
export SEEDREAM_API_KEY="your-key"  # 可选，配图用
```

### 3. 手动测试

```bash
# 生成今日语录并推送
python3 scripts/generate_daily.py

# 仅生成文档
python3 scripts/generate_daily.py --no-send

# 指定日期测试
python3 scripts/generate_daily.py --date 2026-05-01
```

### 4. 配置定时任务

```bash
openclaw cron create \
  --name "每日毛选语录推送" \
  --schedule "0 9 * * *" \
  --agent <your-agent> \
  --task "执行每日毛选语录推送" \
  --timezone "Asia/Shanghai"
```

---

## 📖 深度解读示例

以 *"谦虚使人进步，骄傲使人落后"* 为例：

| 章节 | 内容 |
|------|------|
| **语义追溯** | "谦"字本义为"受人敬服"，谦虚不是压抑，而是主动打开认知输入通道 |
| **历史张力** | 1946年重庆谈判后，党内滋生了什么心态？不写这句话，最惨会怎样？ |
| **跨时空映射** | 2026年的"大厂"里，什么人正在被温水煮青蛙？ |
| **实证链条** | 乔布斯、贝索斯、张一鸣如何用"求知若饥，虚心若愚"塑造企业基因 |
| **当代痛点** | 算法推荐让你越来越确信自己是对的——这正是"聪明人陷阱" |
| **行动建议** | 每天主动寻找一条反对自己观点的信息（第一眼会抗拒，细想极有用） |

---

## 📁 输出示例

```
/tank/obsidian/每日语录/2026-05-14.md
/tank/obsidian/每日语录/assets/2026-05-14.jpg   # 配图
/tank/obsidian/每日语录/assets/2026-05-14.mp3   # 语音
```

文档结构：
```markdown
# 📜 每日毛选语录 | 2026-05-14

> "谦虚使人进步，骄傲使人落后"
> — 毛泽东，《中国共产党第七届中央委员会第二次全体会议上的报告》，1949年3月

## 📍 文章定位与核心命题

...

## 🔍 语义追溯

...
```

---

## 🔧 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | Telegram 推送必填 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Telegram 推送必填 |
| `SEEDREAM_API_KEY` | Seedream API Key | 配图生成可选 |
| `MAOXUAN_OUTPUT_DIR` | Obsidian 输出目录 | 可选 |

---

## 📦 文件结构

```
daily-maoxuan-push/
├── SKILL.md
├── README.md
├── scripts/
│   ├── generate_daily.py    # 主生成脚本
│   ├── push_daily.py        # 推送脚本
│   ├── utils.py             # 工具函数
│   └── deep_gen.py          # AI 深度解读生成
├── references/
│   ├── maoxuan_quotes.json  # 语录数据库
│   └── config.json
└── config/
    └── channels.json
```

---

## 💡 核心理念

> 这个技能不是为了"学历史"。
> **是为了每天强迫你进行一次认知重启——在信息茧房、短视频、算法推荐的围剿中，杀出一条思想的血路。**

如果你发现每天读完后有一种"脑子被重启"的感觉——这就对了。

---

**作者**：imagor  
**版本**：4.0.0  
**许可证**：MIT