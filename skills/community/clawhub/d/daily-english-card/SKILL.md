---
name: daily-english-card
description: |
  每日英语口语学习卡片推送。每天早上8:30自动生成英语场景对话卡片图片并推送到微信。
  支持440个日常场景、11种卡片风格、遗忘曲线复习，自动上传到IMA知识库存档。
  触发词：英语卡片、英语学习、英语口语、口语练习、每日英语、英语推送、English card、口语、学英语、背单词
---

# 每日英语场景对话卡片推送

## 核心原则

- **必须用 python3.9**：Homebrew python@3.14 无 Pillow，路径固定为 `/usr/local/opt/python@3.9/bin/python3.9`
- **只发送图片，不附加文字**：message 工具发图时 media 字段只填图片路径
- **不回复 HEARTBEAT_OK**：定时推送时直接输出确认，不要回复心跳确认
- **IMA 失败不阻塞**：上传失败时卡片仍推送，标记错误但不中断

## Prerequisites

1. Python 环境：`/usr/local/opt/python@3.9/bin/python3.9 -m pip install Pillow`
2. 数据文件：`~/workspace/english_learning.json`（440场景）
3. IMA 凭证：`~/Library/Application Support/QClaw/openclaw/config/skills/ima/get-token.sh`
4. cron job 已配置（见附录）

## 推送流程

### Step 1：生成卡片

```bash
/usr/local/opt/python@3.9/bin/python3.9 ~/workspace/scripts/push_english_daily.py
```

脚本输出 JSON 到 stdout，提取 `image_path` 字段。

**正常输出示例：**
```json
{
  "image_path": "~/workspace/cards/card_2026-04-27.png",
  "style": "lake",
  "title_zh": "餐厅点餐",
  "progress": "12/440",
  "is_weekend": false,
  "tencent_doc_url": ""
}
```

**失败处理：**
- `python3.9: command not found` → 改用 `python3` 重试，并报告路径错误
- PIL 报错 → 确认用的是 `python3.9`，不是系统 python3
- 脚本报错 → 直接报告错误，不继续

### Step 2：发送图片到微信

从 Step 1 输出中提取 `image_path`，使用 message 工具：

- **channel**: `openclaw-weixin`
- **target**: `o9cq800qdEr8F9W0A_BulcOhDiCk@im.wechat`
- **accountId**: `e7aef5bc05d2-im-bot`
- **media**: 图片绝对路径（展开 `~` 为真实路径）

⚠️ **不要附加文字消息**，只发图片。如果发了文字，微信会将图片压缩。

**失败处理：**
- 发送失败 → 报告"图片发送失败，请手动检查"
- 路径不存在 → 用 `ls ~/workspace/cards/` 确认文件是否存在

### Step 3：输出确认

图片发送成功后，输出简短确认：

```
✅ 今日英语卡片已送达
📖 场景：餐厅点餐（进度 12/440）
🎨 风格：清冷湖海
```

## 卡片系统说明

### 学习逻辑

| 时间 | 行为 |
|------|------|
| 工作日 | 学习新场景，`current_index` + 1 |
| 周末 | 按遗忘曲线找复习场景，不推进进度 |
| 遗忘曲线间隔 | `[1, 2, 4, 7, 15]` 天 |

### 11 种风格

风景风格（4种）：`forest` 雾境森林 | `sunrise` 山野晨昏 | `lake` 清冷湖海 | `twilight` 荒原暮色

色卡风格（7种）：`periwinkle` 梦幻薰衣 | `blush` 蜜桃绒纱 | `candy` 糖果彩虹 | `nautical` 海军蓝调 | `lavender` 薰衣草梦 | `ocean` 深海幽蓝 | `warmth` 暖阳绒毯

风格按日期轮换（11天一轮），同一天风格固定。

### 数据文件

- 场景数据：`~/workspace/english_learning.json`（440场景，44主题×10变体）
- 卡片输出：`~/workspace/cards/card_YYYY-MM-DD.png`
- 进度管理：`~/workspace/scripts/learning_manager.py`

## Fallback

| 问题 | 解决方案 |
|------|----------|
| python3.9 找不到 | 改用 `python3`，并报告需修复路径 |
| PIL 报错 | 确认用的是 Homebrew python@3.9，不是系统 Python |
| 脚本输出非 JSON | 直接报告脚本错误，不继续 |
| 图片路径含 `~` 无法发送 | 用 `os.path.expanduser()` 展开为绝对路径 |
| IMA 上传失败 | 卡片仍推送，报告"IMA 存档失败（可忽略）" |
| 微信发送失败 | 报告"发送失败，请手动检查"，不阻塞 |
| 同名文件已存在 | push_english_daily.py 会覆盖，无需处理 |

## Troubleshooting

| 问题 | 原因 | 解决 |
|------|------|------|
| 推送了错误的卡片风格 | cron payload 中 python 路径写错用了系统 python3 | 确认 cron payload 中用的是 `python3.9` |
| 进度不前进 | 脚本出错但 agent 没有检查 | 看脚本输出 JSON 是否有 `image_path` |
| IMA 存档空白 | COS 上传权限问题 | 检查 `get-token.sh` 是否有效 |
| 图片在微信中显示异常 | 中文图片触发 OCR 违规（腾讯文档已弃用，改用 IMA） | 确认用的是 IMA 而非腾讯文档 |

## 手动测试

```bash
# 1. 生成卡片（检查输出）
/usr/local/opt/python@3.9/bin/python3.9 ~/workspace/scripts/push_english_daily.py

# 2. 确认图片存在
ls ~/workspace/cards/card_$(date +%Y-%m-%d).png

# 3. 手动发送
openclaw cron run <YOUR_CRON_JOB_ID>
```

## Cron 配置（参考）

```json
{
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "openclaw-weixin",
    "to": "o9cq800qdEr8F9W0A_BulcOhDiCk@im.wechat",
    "accountId": "e7aef5bc05d2-im-bot"
  },
  "wakeMode": "now"
}
```

## 文件结构

```
~/.qclaw/skills/daily-english-card/
├── SKILL.md      # 本文件
└── README.md     # 详细文档（含脚本逻辑、重建指南）

~/workspace/scripts/
├── push_english_daily.py       # 主推送脚本（生成卡片 + IMA上传）
├── generate_english_card.py     # 卡片图片生成器
└── learning_manager.py          # 遗忘曲线进度管理

~/workspace/
├── english_learning.json        # 440场景数据
```

## 卡片效果图

![英语卡片效果图](https://r2.image-upload.app/ptImg/4OOX6Lbi.jpeg)
