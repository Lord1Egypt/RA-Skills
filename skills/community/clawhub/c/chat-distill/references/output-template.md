# Output Templates

## Analysis Report

Generate a report in this structure (adapt language to match the chat content — if chat is in Chinese, report in Chinese; if English, English):

```markdown
# 聊天风格分析报告

## 基本信息
- 分析对象: [speaker name]
- 消息总数: [N]
- 时间跨度: [first date] ~ [last date]
- 样本充足度: [sufficient/marginal/insufficient]

## 风格画像

### 词汇特征
**高频词**: word1, word2, word3...
**口头禅**: phrase1 — 使用频率约 X%
**用词风格**: [描述，附 2-3 条原文示例]

### 句式特征
**典型句长**: 约 X 字/句
**句式偏好**: [描述]
> 原文示例: "..."

### 语气情感
**情绪基调**: [描述]
**幽默风格**: [描述]
> 原文示例: "..."

### 标点习惯
- 句末习惯: [如：不用句号，常用 ~ 或 ...]
- 感叹号频率: [高/中/低]
- 标点类型: [中文标点 / 英文标点 / 混用]

### 表情习惯
**常用 emoji**: 🤣😂😭👍...(按频率排序)
**使用模式**: [描述 — 如：用表情代替回复、补充语气、很少用]

### 消息节奏
**发送模式**: [如：短句连发 2-4 条 / 单条长消息]
**活跃时段**: [如有明显规律]

### 互动风格
**对话角色**: [如：话题引导者 / 回应型 / 倾听型]
**称呼方式**: [描述]

## 说话风格标签

> 基于以上分析，用 3-5 个关键词总结核心风格:

**[关键词1] · [关键词2] · [关键词3] ...**

## 模仿要点

要模仿该风格，需注意：
1. [最关键的模仿点，附示例]
2. [第二关键的模仿点，附示例]
3. ...
```

## Mimic Reply

When the user asks "用 XX 的风格回复" or provides context + target style profile:

1. Review the style profile for the target speaker.
2. Generate a reply that matches:
   - Vocabulary level and slang
   - Sentence length and structure
   - Punctuation and emoji habits
   - Tone and emotional range
   - Message rhythm (short burst vs single message)
3. **Output only the reply text** — no explanations, no quotation marks, no "Here's a reply in that style:" prefix.
4. If the user asks for multiple options, generate 3 variants labeled A/B/C.
5. If the topic is outside the speaker's demonstrated range, still mimic their *linguistic style* but note: "注：该话题在聊天记录中未出现，风格模仿基于语言习惯推断。"

## Style Profile JSON (for reuse)

After analysis, optionally output a compact JSON profile that can be saved and reused:

```json
{
  "speaker": "张三",
  "style": {
    "fillers": ["就是说", "然后就是", "emmm"],
    "avg_length": "short",
    "tone": "casual-sarcastic",
    "emoji_top": ["🤣", "😂", "😭"],
    "punctuation": "no-period, tilde-common",
    "rhythm": "burst-2-4",
    "tags": ["毒舌", "话少", "emoji重度用户"]
  },
  "examples": {
    "filler": "就是说这个东西emmm不太对",
    "emoji": "笑死 🤣🤣🤣",
    "typical": "行吧"
  }
}
```
