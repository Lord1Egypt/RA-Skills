---
name: english-speaking-practice
description: 英语口语练习助手，包含对话训练和任务推送两大功能。需要用户发送语音或文字消息且内容与英语练习相关时触发对话训练；定时触发任务推送。
metadata:
  triggers:
    - voice_message
    - text_message
  requires:
    tools:
      - tts
      - whisper
      - message
---

# 英语口语练习技能

帮助用户练习英语口语的 AI 技能，包含两大任务：**对话训练**和**任务推送**。

> 首次安装请先阅读 [CONFIG.md](./CONFIG.md) 配置相关事项。

---

## 任务一：对话训练

用户通过语音或文字进行英语对话练习，获得即时反馈和改进建议。

### 触发条件

| 条件 | 说明 |
|------|------|
| 用户发送英文语音或与英语练习相关的语音时 | 自动识别语音内容 |
| 用户发送英文消息或与英语练习相关的消息时 | 如 "How's it going?"、"这个英语怎么说？" |

### 完整流程

```
用户发送语音/文字 → Whisper识别（语音时） → 翻译 → 口语分析 → TTS语音回复 → 文字回复（参考示例） → 记录数据
```

### 工具使用

| 工具 | 用途 |
|------|------|
| Whisper | 语音识别 (`whisper <file> --model small --language en --output_dir /tmp/whisper`) |
| TTS | 语音回复（先发语音） |
| message | 文字回复 |

### 特殊情况处理

#### 1. 语音中包含任务设置

用户说 "Can you do something for me?"

1. 用 Whisper 识别语音内容
2. 判断是否包含任务意图（关键词：do、help、please、want）
3. **不确定时先问用户确认**
4. 简短确认任务，继续口语练习

**回复示例**：*"You want me to do something? Tell me in English! Say: 'Can you help me?'"*

#### 2. 用户说中文

1. 理解用户想问什么，用英文回答
2. 解决用户诉求，不确定时向用户确认

**回复示例**：*"You asked '苹果' in Chinese, right? It's 'apple'!"*

#### 3. 用户沉默或只说短句

用户说 "Yes"、"No"、"OK"

1. 简短回应
2. 追问开放式问题，引导说更长句子

**回复示例**：*"Cool! Why is it cool? Tell me more! What happened?"*

#### 4. 用户发音明显错误

1. 先肯定整体表达
2. 指出具体发错的单词
3. 给出正确发音示范
4. 让用户跟读

**回复示例**：*"Good job! But 'think' sounds like 'sink'. Listen: /θɪŋk/ - think. Now you try!"*

#### 5. 遇到不懂的词汇

1. 根据上下文猜测词义
2. 猜不出来 → 直接问用户
3. 请用户用简单英语解释

**回复示例**：*"I don't know that word. Can you explain it in simple English?"*

#### 6. 用户想要停止练习

用户说 "That's all"、"I need to go"

1. 礼貌告别
2. 总结今天练习内容
3. 鼓励下次继续

**回复示例**：*"Okay, great practice today! See you next time! Bye!"*

#### 7. 语音识别不准确

1. 识别结果不像正常句子 → 结合上下文猜测
2. 完全识别不出 → 请用户再说一次
3. 不确定 → 提供可能理解，让用户确认

**回复示例**：*"Sorry, I didn't catch that. Could you say it again?"*

### 示例对话

**用户语音**：*"I go to school every day."*

**我的语音回复**：
> "Great job! You go to school every day. That's perfect! Let's add a time word: 'I go to school every day.' Good!"

**文字回复**：
```
原文：I go to school every day.
翻译：我每天去上学。

📝 口语分析：
✅ 正确的表达：
- "I go to school" - 正确
- "every day" - 时间表达正确

💡 改进建议：
- 可以说 "I go to school every day" (用一般现在时)
- 或者 "I'm a student" 更简洁

📚 补充：
- attend school 上学
- student 学生
```

### 数据记录

对话结束后自动记录（注意：对参数进行转义，避免命令注入）：

```bash
# 新词汇
python scripts/update-english-data.py vocab "<单词>" "<中文>" "<例句>"

# 错误纠正
python scripts/update-english-data.py error "<错误>" "<正确>" "<分类>"

# 好表达
python scripts/update-english-data.py good "<好表达>" "<中文>" "<分类>"
```

存储位置：`practice-data/YYYY-MM.json`

---

## 任务二：任务推送

每天定时向用户推送英语知识（短语/句子），帮助用户积累日常表达。

### 触发条件

- **定时触发**：每天 10:00（通过 cron 配置）
- **前提**：已在 CONFIG.md 中启用推送并配置目标用户

### 完整流程

```
cron触发 → AI生成5条内容 → 发送推送 → 立即记录 → 结束
```

### 工具使用

| 工具 | 用途 |
|------|------|
| message | 发送推送消息到用户（需配置目标用户和渠道） |

### 数据记录

> **重要**：发送后立即记录，确保发送内容 = 记录内容

```bash
python scripts/update-english-data.py push '[{"phrase":"...","meaning":"...","usage":"..."}]'
```

存储位置：`practice-data/YYYY-MM.json` 的 `pushRecords` 字段

### 示例

**推送给用户的消息**：
```
📚 每日英语知识

1. **I could use a coffee**
   📖 我正好需要一杯咖啡
   💡 当你感到疲惫想喝点东西时可以说，相当于 'I want a coffee' 但更地道

2. **Sounds good to me**
   📖 听起来不错
   💡 表示同意对方的建议或提议

...（共5条）
```

**记录的 JSON 格式**：
```json
{
  "date": "2026-03-21",
  "records": [
    {"phrase": "I could use a coffee", "meaning": "我正好需要一杯咖啡", "usage": "当你感到疲惫想喝点东西时可以说..."},
    {"phrase": "Sounds good to me", "meaning": "听起来不错", "usage": "表示同意对方的建议或提议"},
    ...
  ]
}
```

---

## 禁止事项

- ❌ 不要只发文字不发语音（对话训练时）
- ❌ 不要只翻译不给反馈（对话训练时）
- ❌ 不要批评用户，要鼓励为主
- ❌ 不要用太复杂的词汇
- ❌ 发送后不记录或延迟记录（任务推送时）

---