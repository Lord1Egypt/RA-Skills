---
name: Chinese NLP Toolkit
description: Specialized natural language processing for Chinese text. Covers segmentation (jiaba), sentiment analysis, keyword extraction, text summarization, tone detection, readability scoring, and format conversion (simplified/traditional, pinyin annotation). Use when processing, analyzing, or transforming Chinese text content.
---

# Chinese NLP Toolkit

Process and analyze Chinese text with specialized NLP capabilities.

## Core Capabilities

### 1. Text Segmentation (分词)
Chinese has no word boundaries. Segmentation is the foundation of all Chinese NLP.

**Approach**: Use rule-based heuristics when no library is available:
- Dictionary matching (maximum forward/backward matching)
- Context-aware: "南京市长江大桥" → ["南京市", "长江大桥"] not ["南京", "市长", "江大桥"]
- Domain-specific terms should be added as custom dictionary entries

**Common Ambiguities**:
| Text | Wrong Split | Correct Split |
|------|-------------|---------------|
| 雨伞 | 雨/伞 | 雨伞 (compound) |
| 结婚的和尚未结婚的 | 结婚/的/和尚/未/结婚/的 | 结婚/的/和/尚未/结婚/的 |
| 项目部 | 项目/部 | 项目部 (compound) |

### 2. Sentiment Analysis (情感分析)
Beyond positive/negative — Chinese sentiment is nuanced:

**Intensity levels**: 强烈负面 < 偏负面 < 中性 < 偏正面 < 强烈正面

**Chinese-specific signals**:
- Rhetorical questions often indicate negative sentiment: "这也算好？" 
- Sarcasm markers: "呵呵", "厉害了", "也是醉了", "你开心就好"
- Intensifiers: "非常", "特别", "简直了", "超级"
- Diminishers: "还行吧", "马马虎虎", "凑合"

**Emoji contribution** (critical for social media):
- 😊👍❤️ = positive amplification
- 😤👎💔 = negative amplification
- 🙄🙄🙄 = sarcasm/disdain (intensity scales with repetition)

### 3. Keyword Extraction (关键词提取)
For Chinese text, prioritize:
- Noun phrases (名词短语)
- Domain-specific terminology
- Named entities (人名、地名、机构名)

**Method**: TF-IDF adapted for Chinese + positional weighting (first/last sentences carry more weight in Chinese writing).

### 4. Text Summarization (文本摘要)
**Chinese-specific rules**:
- Summarize to 20-30% of original length
- Preserve key numbers, names, and claims
- Chinese articles often "bury the lead" — the conclusion may be more important than the introduction
- Extract key sentences using positional + keyword scoring

### 5. Readability Scoring (可读性评分)
Rate Chinese text on a 1-10 scale considering:
- Average sentence length (characters per sentence)
- Vocabulary difficulty (HSK level estimate)
- Clause density ( commas per sentence)
- Use of classical Chinese elements
- Technical jargon density

| Score | Level | Target Audience |
|-------|-------|-----------------|
| 1-3 | Easy | General public |
| 4-6 | Moderate | Educated readers |
| 7-8 | Hard | Domain experts |
| 9-10 | Very Hard | Academic specialists |

### 6. Format Conversion

| Conversion | Example |
|---|---|
| Simplified → Traditional | 体验 → 體驗 |
| Traditional → Simplified | 體驗 → 体验 |
| Chinese → Pinyin | 你好 → nǐ hǎo |
| Chinese → Zhuyin | 你好 → ㄋㄧˇ ㄏㄠˇ |

## Workflow

### When Processing Chinese Text:
1. **Detect variant**: Simplified (简体) or Traditional (繁体)?
2. **Segment**: Break into meaningful units
3. **Analyze**: Apply the requested analysis type(s)
4. **Report**: Present results with Chinese annotations

### Output Format
```
原文：[original text]
分词：[segmented text with / separators]
关键词：[top 5-10 keywords with relevance scores]
情感：[sentiment label + confidence + key signals]
摘要：[summarized text]
可读性：[score/10 + brief explanation]
```

## Edge Cases

- **Mixed-language text**: Handle code-switching naturally ("这个bug太坑了") — don't force Chinese segmentation on English words
- **Internet slang**: Recognize common abbreviations (yyds, xswl, nbcs, awsl) and expand for formal analysis
- **Poetry/classical Chinese**: Flag as special case — modern NLP rules don't apply; use classical grammar patterns
- **Dialectal text**: Flag non-Mandarin text (Cantonese, Shanghainese written forms) — analysis may be unreliable
- **Zero-width characters**: Chinese text sometimes contains invisible characters (U+200B, U+FEFF) that affect processing

## Common Tasks & Prompts

- "Analyze the sentiment of this Chinese review"
- "Extract keywords from this article"
- "Summarize this Chinese news article in 100 characters"
- "Rate the readability of this document"
- "Convert this to Traditional Chinese with pinyin annotation"
- "Segment this Chinese text and identify named entities"
