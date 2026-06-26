# AI Humanizer Skill 使用指南

**安装位置**: `~/.openclaw/workspace/skills/ai-humanizer/`  
**版本**: 2.1.0  
**来源**: ClawHub (高 Star Skill)

---

## 📋 功能概述

检测并移除 AI 写作痕迹，让文本更自然、更像人类书写。

**核心能力**:
- 24 种 AI 写作模式检测
- 500+ AI 词汇库（3 个等级）
- 统计文本分析（burstiness、词汇多样性、可读性）
- 提供修改建议或自动改写

---

## 🛠️ 使用方式

### 方式 1: CLI 命令行工具

```bash
cd /home/admin/.openclaw/workspace/skills/ai-humanizer

# 快速评分（0-100，越高越像 AI）
echo "你的文本" | node src/cli.js score

# 完整分析报告
node src/cli.js analyze -f draft.md

# 生成 Markdown 报告
node src/cli.js report article.txt > report.md

# 改写建议（按优先级分组）
node src/cli.js suggest essay.txt

# 自动改写（带修改建议）
node src/cli.js humanize --autofix -f article.txt

# 仅统计分析
node src/cli.js stats essay.txt

# JSON 输出（编程使用）
node src/cli.js analyze --json < input.txt
```

---

### 方式 2: 作为 OpenClaw Skill

SKILL.md 已自动加载到 OpenClaw 中。

**使用场景**:
- 写完文章后，让 AI 检查是否有 AI 味
- 修改 AI 生成的草稿
- 审查写作风格

**示例指令**:
```
帮我去掉这篇文章的 AI 味
检查这段文字是否有 AI 写作痕迹
让这段话听起来更像人写的
```

---

## 📊 24 种 AI 写作模式

| # | 模式 | 类别 | 示例 |
|---|------|------|------|
| 1 | 意义膨胀 | Content | "marking a pivotal moment in the evolution of..." |
| 2 | 媒体堆砌 | Content | 列出一堆媒体但没有具体说法 |
| 3 |  superficial -ing 分析 | Content | "...showcasing... reflecting... highlighting..." |
| 4 | 宣传语言 | Content | "nestled", "breathtaking", "stunning" |
| 5 | 模糊归因 | Content | "Experts believe", "Studies show" |
| 6 | 公式化挑战 | Content | "Despite challenges... continues to thrive" |
| 7 | AI 词汇 | Language | "delve", "tapestry", "landscape" |
| 8 | 避免系动词 | Language | "serves as" 代替 "is" |
| 9 | 否定平行句 | Language | "It's not just X, it's Y" |
| 10 | 三法则 | Language | "innovation, inspiration, and insights" |
| 11 | 同义词循环 | Language | "protagonist... main character... central figure..." |
| 12 | 虚假范围 | Language | "from the Big Bang to dark matter" |
| 13 | 破折号滥用 | Style | 太多 —— 破折号 —— 到处都是 |
| 14 | 粗体滥用 | Style | **机械的** **强调** **到处都是** |
| 15 | 内联标题列表 | Style | "- **主题:** 这里讨论主题" |
| 16 | 标题大小写 | Style | 每个主要单词都大写 |
| 17 | 表情符号滥用 | Style | 🚀💡✅ 装饰专业文本 |
| 18 | 弯引号 | Style | "智能引号" 代替 "直引号" |
| 19 | 聊天机器人痕迹 | Communication | "I hope this!", "Let me know if..." |
| 20 | 截断免责声明 | Communication | "As of my last training..." |
| 21 | 奉承语气 | Communication | "Great question!", "You're absolutely right!" |
| 22 | 填充短语 | Filler | "In order to", "Due to the fact that" |
| 23 | 过度谨慎 | Filler | "could potentially possibly" |
| 24 | 通用结论 | Filler | "The future looks bright" |

---

## 🚫 AI 词汇库

### Tier 1（明显 AI 词）
delve, tapestry, vibrant, crucial, comprehensive, meticulous, embark, robust, seamless, groundbreaking, leverage, synergy, transformative, paramount, multifaceted, myriad, cornerstone, reimagine, empower, catalyst, invaluable, bustling, nestled, realm

### Tier 2（可疑词汇）
furthermore, moreover, paradigm, holistic, utilize, facilitate, nuanced, illuminate, encompasses, catalyze, proactive, ubiquitous, quintessential

### AI 短语
- "In today's digital age"
- "It is worth noting"
- "plays a crucial role"
- "serves as a testament"
- "in the realm of"
- "delve into"
- "harness the power of"
- "embark on a journey"
- "without further ado"

---

## 📈 统计指标

| 指标 | 人类写作 | AI 写作 | 说明 |
|------|---------|--------|------|
| Burstiness | 0.5-1.0 | 0.1-0.3 | 人类写作有起伏；AI 是机械的 |
| 类符比 | 0.5-0.7 | 0.3-0.5 | AI 重复使用相同词汇 |
| 句长变化 | 高 CoV | 低 CoV | AI 句子长度几乎相同 |
| 三词组重复 | <0.05 | >0.10 | AI 重复使用 3 词短语 |

---

## ✅ 核心原则

### 像人一样写作，不要像新闻稿
- 自由使用"is"和"has"——"serves as"很做作
- 每个主张一个限定词——不要堆砌
- 说出具体来源或删除主张
- 以具体内容结束，不要"未来很光明"

### 增加个性
- 有观点。对事实做出反应，不要只是报告
- 变化句子节奏。短句。然后是长句。
- 承认复杂性和混合情感
- 让一些混乱进来——完美的结构感觉像算法

### 删掉废话
- "In order to" → "to"
- "Due to the fact that" → "because"
- "It is important to note that" → (直接说)
- 删除聊天机器人填充语："I hope this helps!", "Great question!"

---

## 📝 示例

### Before (AI 味重)
> Great question! Here is an overview of sustainable energy. Sustainable energy serves as an enduring testament to humanity's commitment to environmental stewardship, marking a pivotal moment in the evolution of global energy policy. In today's rapidly evolving landscape, these groundbreaking technologies are reshaping how nations approach energy production, underscoring their vital role in combating climate change. The future looks bright. I hope this helps!

### After (人类写作)
> Solar panel costs dropped 90% between 2010 and 2023, according to IRENA data. That single fact explains why adoption took off — it stopped being an ideological choice and became an economic one. Germany gets 46% of its electricity from renewables now. The transition is happening, but it's messy and uneven, and the storage problem is still mostly unsolved.

---

## 🔧 集成到工作流

### 写作后检查
```bash
# 写完文章后检查 AI 分数
node src/cli.js score < article.md

# 如果分数>50，运行改写建议
node src/cli.js suggest article.md
```

### Always-On 模式
将核心规则添加到 AGENTS.md 或 SOUL.md：
- 禁止 Tier 1 词汇
- 删除填充短语
- 不要奉承、聊天机器人痕迹、通用结论
- 变化句子长度，有观点，用具体细节
- 如果不会在对话中说，就不要写

---

*使用指南 v1.0 | 2026-04-01 | 基于 ai-humanizer-2.1.0*
