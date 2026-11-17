---
name: cat-sticker
description: 猫猫表情包技能系统。分析输入文本情绪，从 custom_stickers.json 自动匹配对应表情，支持概率/开关/冷却调节指令。
metadata:
  openclaw:
    emoji: 🐱
    version: "2.0"
---

# 🐱 Cat Sticker — 猫猫表情包技能系统

> **图片来源声明**：本技能内置的所有表情包图片均来源于互联网公开渠道搜集整理，仅供个人学习与研究使用。如有侵权请联系删除。

---

## 📌 技能简介

**Cat Sticker** 是一款为 AI 对话场景设计的**自动表情包匹配技能**。夜玖会根据用户输入的文本内容，自动分析情绪关键词，从 161 张内置表情图中挑选最匹配的一张附在回复中，让对话更加生动可爱。

主要特点：
- 🧠 **智能情绪分析** — 支持撒娇、开心、害羞、难过、生气、惊讶等 21 种情绪识别
- 🎲 **概率触发机制** — 可调节表情发送频率，不再每句都发
- 🔄 **智能冷却** — 避免连续发送同一张表情
- ⚙️ **灵活配置** — 支持指令实时调整概率、开关、冷却轮数
- 🐱 **纯离线运行** — 无需联网，零依赖

---

## 📁 文件结构

```
cat-sticker/
├── SKILL.md              # 本文件，技能说明文档
├── cat_sticker_skill.py  # 🐱 核心 Python 模块（纯函数，无第三方依赖）
├── custom_stickers.json  # 表情元数据库（161条记录，含文件名与描述）
├── sticker_config.json   # 用户配置文件（首次运行自动生成）
├── sticker_cooldown.json # 冷却状态记录（运行中自动维护）
└── __stickers/          # 表情图片目录（161张 PNG 图片）
```

---

## 🚀 安装方式

### 方式一：通过 ClawHub 安装（推荐）

```bash
clawhub install cat-sticker
```

### 方式二：手动安装

```bash
# 克隆到本地技能目录
git clone <repository-url> /path/to/your/skills/cat-sticker
```

---

## 📖 使用方法

### 基础调用

```python
import sys
sys.path.insert(0, "/path/to/cat-sticker")
import cat_sticker_skill as cs

# 分析文本情绪并返回表情
result = cs.pick_sticker("我好开心喵~")
print(result)
# 输出示例：
# {
#     "triggered": True,
#     "sticker_path": "/path/to/cat-sticker/__stickers/sticker_xxx.png",
#     "description": "开心的猫猫",
#     "emotion": "开心",
#     "confidence": 0.85,
#     "message": "我好开心喵~",
#     "cooldown_remaining": 2
# }
```

### 强制指定情绪

```python
# 不分析文本，强制使用指定情绪分类
result = cs.pick_sticker("hello", explicit_emotion="开心")
```

### 覆盖概率阈值

```python
# 强制触发（概率 = 1.0）
result = cs.pick_sticker("我难过", probability=1.0)
```

### 关闭表情功能

```python
result = cs.pick_sticker("正常文本", override_enable=False)
# 返回 triggered: False
```

### 处理配置指令

```python
# 解析并执行用户发送的指令
cmd_result = cs.handle_command("表情概率 0.5")
if cmd_result:
    print(cmd_result["reply"])
    # 例如："表情触发概率已调整为 50% 喵~"
```

---

## 📋 pick_sticker 参数详解

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `text` | `str` | 必填 | 用户输入的原始文本 |
| `probability` | `float?` | `None` | 覆盖全局概率阈值（0.0 ~ 1.0） |
| `explicit_emotion` | `str?` | `None` | 强制指定情绪类型，跳过情绪分析 |
| `override_enable` | `bool?` | `None` | 强制开启/关闭表情功能 |

---

## 📤 返回值详解

| 字段 | 类型 | 说明 |
|------|------|------|
| `triggered` | `bool` | 本次是否触发了表情发送 |
| `sticker_path` | `str` | 表情图片的**完整绝对路径**（用于 `<qqmedia>` 标签） |
| `sticker_rel` | `str` | 表情图片的**相对路径**（用于 Markdown 图片格式） |
| `fileName` | `str` | 表情文件名 |
| `description` | `str` | 表情的描述文字 |
| `emotion` | `str` | 匹配到的情绪类型 |
| `confidence` | `float` | 情绪匹配置信度（0.0 ~ 1.0） |
| `original_text` | `str` | 原始输入文本 |
| `message` | `str` | 给用户看的输出文本 |
| `cooldown_remaining` | `int` | 剩余冷却轮数 |
| `reason` | `str` | 未触发时的原因说明 |

---

## 🎭 支持的情绪类型（21种）

| 情绪分类 | 关键词示例 | 说明 |
|----------|-----------|------|
| 🎀 **撒娇** | 撒娇, 抱抱, 贴贴, 蹭蹭, rua | 依赖、想被宠爱的感觉 |
| 🌸 **卖萌** | 可爱, 乖喵, 小可爱, 喵~ | 刻意表现得可爱 |
| 😳 **害羞** | 害羞, 脸红, 不好意思 | 被夸赞或尴尬时的反应 |
| 🎉 **开心** | 开心, 高兴, 好耶, happy | 正向情绪、兴奋 |
| 😠 **生气** | 生气, 气死, 哼, 讨厌 | 负向愤怒情绪 |
| 😢 **难过** | 难过, 伤心, 委屈, 哭哭 | 负向悲伤情绪 |
| 😲 **惊讶** | 震惊, 吓到, 卧槽, 惊呆 | 意外、震惊的反应 |
| 🤔 **疑惑** | 疑惑, 什么?, 为什么?, 嗯？ | 不理解、提问时的反应 |
| 😒 **嫌弃** | 嫌弃, 无语, 服了, 屑 | 不屑、轻度厌恶 |
| 😑 **无语** | 无语了, 无话可说 | 被搞无语的状态 |
| 😨 **害怕** | 害怕, 怕怕, 瑟瑟发抖 | 恐惧、紧张的反应 |
| 💭 **思考** | 思考, 想一想, 嗯... | 正在思考的状态 |
| 😴 **困** | 困, 累, 晚安, 想睡觉 | 疲倦、想休息 |
| 🍖 **饿** | 饿了, 好饿, 想吃东西 | 饥饿感 |
| 🐱 **喵叫** | 喵, 喵呜, 咪咪, 喵~ | 猫叫相关的文本 |
| 😏 **坏笑** | 嘿嘿嘿, 桀桀桀, 阴险 | 调皮、搞怪的笑 |
| 😭 **大哭** | 呜呜, 呜呜呜, 哇 | 大声哭泣 |
| 😂 **傻笑** | 哈哈哈, 笑死, 哈哈哈哈哈 | 开心大笑 |
| 🙌 **投降** | 投降, 服了, 认输, 求饶 | 认输、放弃抵抗 |
| ✅ **OK** | ok, 好, 行, 可以, 收到 | 肯定、确认 |
| 😜 **恶搞** | 笨蛋, 蠢, 傻, 杂鱼, 你不行 | 调侃、恶作剧 |

---

## ⚙️ 配置指令系统

### 表情开关

```text
表情开关 开
表情开关 关
```

开启或关闭表情自动发送功能。

### 表情概率

```text
表情概率 0.8
```

设置触发概率（0.0 ~ 1.0），每次回复时以该概率决定是否发送表情。

- `1.0` = 每次都发
- `0.7` = 70% 概率发送（默认）
- `0.0` = 关闭触发（但 `override_enable=True` 可强制触发）

### 表情冷却

```text
表情冷却 3
```

设置冷却轮数——发送一张表情后，隔几轮才能再发，防止同一表情连续出现。

### 表情列表

```text
表情列表
```

查看当前表情库中所有情绪分类及每类的表情数量。

### 表情帮助

```text
表情帮助
```

显示本帮助文档。

---

## ⚙️ 配置文件说明

### sticker_config.json

首次调用时自动生成，默认内容：

```json
{
  "enable": true,
  "probability": 0.7,
  "cooldown_rounds": 2,
  "max_per_turn": 1,
  "expose_path": false,
  "emotion_priority": [
    "撒娇", "卖萌", "害羞", "开心", "生气", "难过",
    "惊讶", "疑惑", "嫌弃", "无语", "害怕", "思考",
    "困", "饿", "喵叫", "坏笑", "大哭", "傻笑",
    "投降", "OK", "恶搞"
  ]
}
```

### sticker_cooldown.json

运行时自动维护，记录上次发送的表情文件名和剩余冷却轮数。

---

## 🧠 情绪分析原理

本技能采用**关键词匹配 + 加权评分**算法：

1. **分词**：将输入文本转为小写
2. **关键词命中**：遍历 21 种情绪的关键词列表，统计命中数量
3. **加权计分**：每个关键词有独立权重（默认 0.8），长关键词（≥3字）额外乘 1.5 倍加成
4. **优先级排序**：按总分降序排列，取最高分情绪作为匹配结果
5. **置信度计算**：用该情绪得分除以最高分情绪得分，得到 0~1 的置信度

---

## 🔧 在 OpenClaw 中集成

### 方式一：通过 MCP 工具调用

```json
// 调用 sticker_gen 工具，传入回复文本
sticker_gen(reply_text="我好开心喵~")
// 返回 base64 格式的表情图片
```

### 方式二：直接 import Python 模块

```python
# 在 OpenClaw Agent 代码中
import cat_sticker_skill as cs

async def on_message(text):
    result = cs.pick_sticker(text)
    if result["triggered"]:
        sticker = result["sticker_path"]
        return f"{result['message']}\n[MEDIA:{sticker}]"
    return result["message"]
```

---

## ⚠️ 注意事项

1. **图片来源**：所有表情图片均来源于互联网公开渠道搜集整理，仅供个人学习与研究使用。如有侵权，请联系删除。
2. **兼容性**：仅支持 Python 3.8+，无第三方依赖，可在任何环境中运行。
3. **性能**：161 张图片约 3.3MB，首次加载后缓存在内存中，后续调用无需重复读取文件。
4. **并发安全**：多进程/多线程环境下，`sticker_cooldown.json` 文件锁需自行处理。建议每个进程使用独立的技能副本。
5. **冷却机制**：`cooldown_rounds=2` 表示发完一张表情后，接下来 2 轮不会发任何表情，第 3 轮才能再发。

---

## 📄 许可证

MIT-0

---

*Powered by 夜玖 · 猫之森咖啡厅看板娘 🐱*
