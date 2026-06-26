---
name: ai-density
description: AI含量检测工具 - 检测文本AI生成占比，输出0-10级客观分级 | AI Content Detector - Detect AI-generated text with 0-10 objective grading
homepage: https://github.com/openclaw/ai-density
category: ai
tags: [ai-detection, content-analysis, nlp, text-analysis, llm, text-classification]
---

# AI含量检测工具 | AI Content Detector

检测文本的AI生成占比，输出0-10级客观分级。

Detect AI-generated content in text, output 0-10 objective grading.

## 核心功能 | Core Features

- **AI含量检测**: 分析文本，返回0-10级的AI参与度等级
- **多维度分析**: 5个维度综合评估，带权重配置
- **便捷接口**: 一行代码调用，也支持高级定制

---

- **AI Content Detection**: Analyze text and return 0-10 AI participation level
- **Multi-dimensional Analysis**: 5 dimensions with weighted scoring
- **Easy Interface**: One-line code call, also supports advanced customization

## 安装 | Installation

```bash
git clone https://github.com/openclaw/ai-density.git
cd ai-density
```

无需额外依赖（基于Python标准库）

No additional dependencies required (based on Python standard library)

## 使用方法 | Usage

### 快速检测 | Quick Detection

```python
from ai_density import detect_ai_content

result = detect_ai_content("这是一段待检测的文本...")
print(f"AI含量等级: {result.level}/10")
print(f"AI参与度得分: {result.score}")
print(f"说明: {result.description}")
```

### Quick Detection (English)

```python
from ai_density import detect_ai_content

result = detect_ai_content("This is a sample text to detect...")
print(f"AI Level: {result.level}/10")
print(f"AI Score: {result.score}")
print(f"Description: {result.description}")
```

### 高级用法 | Advanced Usage

```python
from ai_density import AIDensityDetector

detector = AIDensityDetector()
result = detector.detect(text)

# 查看各维度得分 | View dimension scores
print(result.dimension_scores)
# {
#   'fingerprint': 75.2,      # 大模型生成指纹 | LLM fingerprint
#   'perplexity': 60.5,       # 文本困惑度 | Text perplexity
#   'semantic': 45.0,         # 语义逻辑结构 | Semantic structure
#   'style': 55.3,            # 语言风格用词 | Language style
#   'human_modification': 30.0 # 人工参与度 | Human modification
# }
```

## 分级说明 (0-10级) | Grading (0-10 Scale)

| 等级 | 名称 | 说明 |
|------|------|------|
| 0 | 完全人工 | 无AI辅助痕迹 |
| 1-3 | 人工为主 | AI轻度辅助 |
| 4-6 | 人机协同 | 混合生成 |
| 7-9 | AI为主 | 人工轻微修改 |
| 10 | 完全AI | 无人工参与 |

---

| Level | Name | Description |
|-------|------|-------------|
| 0 | Fully Human | No AI assistance traces |
| 1-3 | Human Dominant | Light AI assistance |
| 4-6 | Human-AI Collaboration | Mixed generation |
| 7-9 | AI Dominant | Minor human edits |
| 10 | Fully AI | No human participation |

## 检测维度权重 | Detection Dimensions

- **大模型生成指纹 (35%)**: 检测AI特有的句式模式
- **文本困惑度 (25%)**: 分析句子长度均匀度
- **语义逻辑结构 (15%)**: 检测总分总结构
- **语言风格用词 (15%)**: 检测标准化书面语
- **人工参与度 (10%)**: 检测个人经验、情绪化表达

---

- **LLM Fingerprint (35%)**: Detect AI-specific patterns
- **Text Perplexity (25%)**: Analyze sentence uniformity
- **Semantic Structure (15%)**: Detect structural patterns
- **Language Style (15%)**: Detect standardized language
- **Human Elements (10%)**: Detect personal experience, emotions

## 注意事项 | Notes

- 文本长度要求: 10-10000字
- 仅检测AI生成占比，**不评价内容质量**
- 结果仅供参考

---

- Text length requirement: 10-10000 characters
- Only detects AI generation ratio, **does not evaluate content quality**
- Results for reference only

## License

MIT License
