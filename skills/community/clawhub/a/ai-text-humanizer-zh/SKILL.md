---
name: ai-text-humanizer
description: 中文AI文本检测与改写工具。当用户需要检测AI生成文本、优化AI文本使其更自然、降低AI痕迹、文本去重、论文降重时使用。支持检测16+类AI特征，自动改写冗余表达，清理Markdown格式，移除chatbot痕迹，输出详细报告和AI概率分数。
---

# AI 文本净化器（中文版）

检测和改写 AI 生成的中文文本，识别 AI 写作的常见特征（如高频连接词、套话、宣传性语言、聊天机器人痕迹等），对文本进行自动优化，使文本更自然、更接近人类写作风格。

## 核心功能

- **检测分析**：按 16+ 类 AI 特征统计问题，输出详细报告和 AI 概率分数（0–100）
- **智能改写**：基于规则替换冗余表达、删除填充词、拆分长句
- **Markdown清理**：自动移除粗体、标题、代码块等格式标记
- **Chatbot痕迹清理**：移除"希望这对您有帮助"、AI署名等痕迹
- **前后对比**：对比改写前后的检测结果，评估改进效果
- **用户自定义规则**：可通过 JSON 文件添加或覆盖规则

## 使用方法

### 1. 检测文本

```bash
# 检测文件
python3 scripts/detect.py 文本.txt

# 输出 JSON 格式
python3 scripts/detect.py 文本.txt -j

# 仅输出分数
python3 scripts/detect.py 文本.txt -s
```

### 2. 改写文本

```bash
# 普通模式（推荐，平衡自然度与改进效果）
python3 scripts/transform.py 文本.txt -o 优化后.txt

# 激进模式（更多同义词替换、长句拆分，可能影响流畅度）
python3 scripts/transform.py 文本.txt -a -o 优化后.txt

# 静默模式
python3 scripts/transform.py 文本.txt -q -o 优化后.txt
```

**模式选择建议：**
- **普通模式（默认）**：25%同义词替换概率，保留专业术语，适合大多数场景
- **激进模式**：40%同义词替换概率 + 长句拆分，适合需要大幅改写的场景

### 3. 前后对比

```bash
# 对比改写前后的检测结果（默认普通模式）
python3 scripts/compare.py 文本.txt -o 优化后.txt

# 激进模式对比
python3 scripts/compare.py 文本.txt -a -o 优化后.txt
```

## 检测类别

| 类别 | 说明 |
|------|------|
| AI Jargon | AI 高频词汇（此外、因此、综上所述等） |
| Puffery | 夸大性短语（具有重要意义、至关重要等） |
| Marketing Speak | 宣传性语言（蓬勃发展、卓越贡献等） |
| Vague Attributions | 模糊归因（据专家分析、普遍认为等） |
| Hedging | 模棱两可表达（可能、或许、一定程度上等） |
| Chatbot Artifacts | 聊天机器人痕迹（作为AI、希望这对您有帮助等） |
| Citation Bugs | 引用痕迹（oaicite、turn0search等） |
| Knowledge Cutoff | 知识截止表述（截至我上次知识更新等） |
| Markdown Artifacts | Markdown痕迹（**、##等） |
| Filler Phrases | 填充短语（值得注意的是、需要指出的是等） |
| Sentence Starters | 句首连接词（此外，、因此，等） |
| Rhetorical Patterns | 反问句模式（难道……吗等） |

## 改写效果示例

**输入：**
> 值得注意的是，人工智能技术正在蓬勃发展。**专家认为**，这不仅是技术革新，更是深刻重塑。**综上所述**，我们坚信一定能够开创AI新局面。**希望这对您有帮助。**

**输出：**
> 人工智能技术正在蓬勃发展。专家认为，这是技术革新，是深刻重塑。能够开创AI新局面。

**改进统计：**
- Issues: 189 → 60 (减少 129 个，68% improvement)
- Markdown: 45 → 0 (完全清除)
- Chatbot Artifacts: 5 → 0 (完全清除)
- Filler Phrases: 7 → 0 (完全清除)

## 自定义规则

规则文件位于 `resources/zh_rules.json`，可复制并修改后通过 `-r` 参数指定：

```bash
python3 scripts/detect.py 文本.txt -r 我的规则.json
```

规则文件结构：

```json
{
  "replacements": {
    "值得注意的是，": "",
    "此外，": ""
  },
  "ai_jargon": ["此外", "综上所述"],
  "puffery_phrases": ["具有重要意义", "关键作用"],
  "chatbot_artifacts": ["希望这对您有帮助"],
  "punctuation": {
    "em_dash_threshold": 2,
    "curly_quote_weight": 1
  }
}
```

## 依赖

- Python 3.8+
- 仅使用标准库，无需安装额外包

## 文件结构

```
ai-text-humanizer-zh/
├── SKILL.md              # 本文档
├── core/
│   ├── __init__.py
│   ├── analyzer.py       # 检测引擎
│   ├── rewrite.py        # 改写引擎
│   ├── rules.py          # 规则加载
│   └── utils.py          # 工具函数
├── scripts/
│   ├── detect.py         # 检测命令
│   ├── transform.py      # 改写命令
│   └── compare.py        # 对比命令
└── resources/
    └── zh_rules.json     # 中文规则库
```

## 注意事项

- 本工具基于规则匹配，无法处理所有复杂句式，建议结合人工审阅
- 改写可能删除少量信息，请确认不会影响核心内容
- 规则库主要针对常见 AI 中文文本特征，专业领域可能需要扩充词表
- **推荐优先使用普通模式**，激进模式可能过度改写影响流畅度
- 专业术语（深度学习、图像识别等）已加入白名单，不会被误替换
