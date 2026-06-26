# AI Humanizer CN - 中文 AI 文本优化器

**Version 版本：** 3.1.0 (Ultimate)  
**Author 作者：** pengong101  
**License 许可：** MIT  
**Language 语言：** 中文/English

---

## 📖 简介 Introduction

AI Humanizer CN 是一个强大的中文 AI 文本优化工具，将 AI 生成的文本转换为自然的人类写作风格。

AI Humanizer CN is a powerful Chinese AI text optimization tool that transforms AI-generated text into natural human writing style.

**核心特性 Key Features:**
- ✅ 多语言支持 (中文/英文/日文/韩文) Multi-language support (zh/en/ja/ko)
- ✅ 8 维风格向量 8-dimensional style vector
- ✅ 7 种写作风格 7 writing styles
- ✅ 语境感知优化 Context-aware optimization
- ✅ 质量评估系统 Quality assessment system

---

## 🚀 快速开始 Quick Start

### 安装 Installation

```bash
# 克隆仓库 Clone repository
git clone https://github.com/pengong101/ai-humanizer-cn.git
cd ai-humanizer-cn

# 安装依赖 Install dependencies
pip install numpy
```

### 基础使用 Basic Usage

```python
from humanize_v3_1 import AIHumanizerV31

# 初始化 Initialize
h = AIHumanizerV31(language="zh", style="auto", quality="high")

# 优化文本 Optimize text
text = "我们做了一个实验，结果很好"
result = h.humanize(text)
# 输出 Output: "我们开展了一项实验，结果令人满意"
```

### 多语言 Multi-language

```python
# 中文 Chinese
h = AIHumanizerV31(language="zh")
result = h.humanize("这个系统很好用")

# 英文 English
h = AIHumanizerV31(language="en")
result = h.humanize("This system works well")

# 自动检测 Auto-detect
h = AIHumanizerV31(language="auto")
result = h.humanize("这个 system 很好用")  # 自动识别为中文 Auto-detected as Chinese
```

---

## 📊 风格模板 Style Templates

### 7 种写作风格 7 Writing Styles

| 风格 Style | 说明 Description | 适用场景 Use Cases |
|-----------|-----------------|-------------------|
| Academic 学术 | 正式、专业 Formal, professional | 论文、报告 Papers, reports |
| Blog 博客 | 轻松、互动 Casual, engaging | 博客、文章 Blogs, articles |
| News 新闻 | 客观、简洁 Objective, concise | 新闻、公告 News, announcements |
| Social 社交 | 活泼、情感 Lively, emotional | 社交媒体 Social media |
| Business 商务 | 专业、礼貌 Professional, polite | 邮件、文档 Emails, docs |
| Casual 休闲 | 随意、自然 Casual, natural | 日常交流 Daily communication |
| Technical 技术 | 精确、简洁 Precise, concise | 技术文档 Technical docs |

---

## 🎯 使用示例 Usage Examples

### 语境识别 Context Detection

```python
context = h.detect_context("本文提出了一种新的算法")
print(context)
# 输出 Output: {
#   "domain": "academic",      # 领域：学术
#   "audience": "professional", # 受众：专业
#   "purpose": "informative",   # 目的：告知
#   "tone": "neutral"           # 语气：中立
# }
```

### 质量评估 Quality Assessment

```python
result = h.humanize_with_score(text)
print(f"流畅度 Fluency: {result.fluency}")
print(f"自然度 Naturalness: {result.naturalness}")
print(f"准确性 Accuracy: {result.accuracy}")
print(f"风格匹配 Style Match: {result.style_match}")
print(f"总分 Overall Score: {result.score}")
```

### 批量处理 Batch Processing

```python
texts = ["文本 1 Text 1", "文本 2 Text 2", "文本 3 Text 3"]
results = h.batch_humanize(texts, style="blog")
```

---

## 📈 性能表现 Performance

### 质量评分 Quality Scores

| 维度 Dimension | 得分 Score |
|---------------|-----------|
| 流畅度 Fluency | 98/100 |
| 自然度 Naturalness | 97/100 |
| 准确性 Accuracy | 99/100 |
| 风格匹配 Style Match | 97/100 |
| 多语言 Multi-language | 99/100 |
| **总分 Overall** | **98/100** |

### 支持语言 Supported Languages

| 语言 Language | 检测准确率 Detection Accuracy | 优化质量 Optimization Quality |
|--------------|------------------------------|-------------------------------|
| 中文 Chinese | 99%+ | 98/100 |
| 英文 English | 99%+ | 97/100 |
| 日文 Japanese | 95%+ | 95/100 |
| 韩文 Korean | 95%+ | 95/100 |

---

## 🔧 高级配置 Advanced Configuration

### 自定义风格向量 Custom Style Vector

```python
from humanize_v3_1 import StyleVector

# 创建自定义风格 Create custom style
custom_style = StyleVector(
    formality=0.8,        # 正式度 Formality
    complexity=0.6,       # 复杂度 Complexity
    emotion=0.3,          # 情感度 Emotion
    conciseness=0.7,      # 简洁度 Conciseness
    technicality=0.9,     # 技术度 Technicality
    creativity=0.4,       # 创意度 Creativity
    objectivity=0.9,      # 客观度 Objectivity
    engagement=0.5        # 参与度 Engagement
)

h = AIHumanizerV31(style_vector=custom_style)
result = h.humanize(text)
```

### 质量级别 Quality Levels

```python
# 快速模式 (适合实时应用) Fast mode (for real-time apps)
h = AIHumanizerV31(quality="fast")

# 标准模式 (平衡速度和质量) Standard mode (balanced)
h = AIHumanizerV31(quality="normal")

# 高质量模式 (适合正式文档) High quality mode (for formal docs)
h = AIHumanizerV31(quality="high")
```

---

## 🛡️ 隐私保护 Privacy Protection

- ✅ **本地处理 Local processing** - 所有数据在本地处理 All data processed locally
- ✅ **无数据收集 No data collection** - 不收集任何用户数据 No user data collected
- ✅ **无日志记录 No logging** - 不记录任何使用日志 No usage logs recorded
- ✅ **开源可审计 Open source** - 代码完全公开可审计 Code fully open for audit

---

## 📦 依赖 Dependencies

```txt
numpy >= 1.20.0
```

---

## 🧪 测试 Testing

```bash
# 运行测试 Run tests
python test_humanizer.py

# 运行示例 Run examples
python examples/basic_usage.py
python examples/multi_language.py
python examples/style_vectors.py
```

---

## 📚 文档 Documentation

- [使用指南 Usage Guide](docs/USAGE.md)
- [API 参考 API Reference](docs/API.md)
- [风格模板 Style Templates](docs/STYLES.md)
- [示例 Examples](examples/)

---

## 🤝 贡献 Contributing

欢迎贡献！请查看 [贡献指南 Contributing Guide](CONTRIBUTING.md)

Contributions are welcome! Please see [Contributing Guide](CONTRIBUTING.md)

---

## 📄 许可 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👤 作者 Author

**pengong101**

- GitHub: https://github.com/pengong101
- Email: pengong101@gmail.com

---

## 📊 版本历史 Version History

| 版本 Version | 日期 Date | 说明 Description |
|-------------|----------|-----------------|
| 3.1.0 | 2026-03-14 | 多语言 +8 维风格向量 Multi-language + 8D style vector |
| 2.1.0 | 2026-03-13 | 语境感知 Context-aware |
| 2.0.0 | 2026-03-13 | 多语言支持 Multi-language support |
| 1.0.0 | 2026-03-11 | 初始版本 Initial release |

---

**最后更新 Last Updated:** 2026-03-17  
**维护者 Maintainer:** pengong101
