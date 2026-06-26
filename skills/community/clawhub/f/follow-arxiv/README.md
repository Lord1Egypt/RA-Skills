# Arxiv 论文搜索与分析工具

一个专业的 Arxiv 论文处理助手，具备论文搜索、内容提取和深度分析的能力。

## ✨ 功能特性

- 📚 **每日论文日报** —— 追踪指定领域的最新研究动态
- 🔍 **论文搜索** —— 支持关键词、时间窗口、分类等多维度搜索
- 📄 **PDF 处理** —— 自动下载 PDF 并提取文本，支持 LaTeX 公式保留
- 🤖 **深度分析** —— 生成全面的论文分析报告
- ⚙️ **灵活配置** —— 通过对话动态调整所有设置
- 🌐 **多语言支持** —— 支持中文、英文、双语报告

## 📦 安装依赖

```bash
pip install arxiv pymupdf requests
```

## 🚀 快速开始

### 1. 在 Claude Code 中使用

在 Claude Code 中调用此 skill：

```
/follow-arxiv-paper
```

首次运行时，会自动启动 onboarding 流程，引导你完成：
- 语言设置（中文/英文/双语）
- 时间窗口配置（24h/48h/72h/1周）
- 搜索关键词设置
- 搜索分类配置

### 2. 配置文件位置

所有配置和用户自定义文件都存储在用户主目录：

```
~/.arxiv-search/
├── config.json          # 用户配置
├── prompts/             # 用户自定义提示词（可选）
└── pdfs/                # PDF 缓存目录
```

### 3. 常用命令示例

**生成每日论文日报**：
```
帮我生成今天的 AI Agent 论文日报
```

**深度分析特定论文**：
```
分析论文 2401.12345
```

**调整配置**：
```
调整时间窗口为 48 小时
更改搜索关键词为 Large Language Model
添加分类 cs.CV
显示我的当前设置
```

**自定义报告风格**：
```
让日报更简洁一点
重点关注方法论
论文分析要更深入
```

## 📁 项目结构

```
arxiv-search/
├── SKILL.md                    # Skill 定义文件（Agent 工作流程）
├── config/
│   └── default_config.json     # 默认配置模板
├── prompts/
│   ├── daily_summary.md        # 日报提示词模板
│   └── deep_analysis.md        # 深度分析提示词模板
├── src/
│   ├── __init__.py
│   ├── utils.py                # 工具函数（配置、提示词管理）
│   ├── search.py               # 论文搜索模块
│   ├── pdf_processor.py        # PDF 处理模块
│   └── analyzer.py             # 分析模块
└── requirements.txt            # Python 依赖
```

## 🔧 配置说明

### 配置文件格式

配置文件位于 `~/.arxiv-search/config.json`：

```json
{
  "language": "zh",              // 语言设置: "zh", "en", "bilingual"
  "time_window_hours": 24,       // 时间窗口（小时）
  "default_query": "AI Agent",   // 默认搜索关键词
  "search_categories": [         // 搜索分类
    "cs.AI",
    "cs.CL",
    "cs.LG"
  ],
  "max_results": 10,             // 最大结果数
  "request_delay": 3,            // 请求延迟（秒）
  "pdf_download_dir": "~/.arxiv-search/pdfs",  // PDF 缓存目录
  "max_retries": 3,              // 下载重试次数
  "onboarding_complete": true    // Onboarding 是否完成
}
```

### 常见 Arxiv 分类

- `cs.AI` —— 人工智能
- `cs.CL` —— 计算与语言（NLP）
- `cs.LG` —— 机器学习
- `cs.CV` —— 计算机视觉
- `cs.RO` —— 机器人学
- `cs.CR` —— 密码学与安全
- `cs.SE` —— 软件工程

## 📝 使用场景

### 场景 1: 追踪最新研究

每天运行生成日报，了解特定领域的最新进展：

```
生成今天的 AI Agent 论文日报
```

### 场景 2: 深度理解论文

找到感兴趣的论文后，进行深度分析：

```
分析第 3 篇论文
```

或直接使用 Arxiv ID：

```
分析论文 2401.12345
```

### 场景 3: 调整搜索策略

根据日报质量调整配置：

```
今天只找到 2 篇论文，调整时间窗口为 48 小时
我想看更多论文，每次最多返回 20 篇
添加计算机视觉相关的分类
```

### 场景 4: 自定义报告风格

调整提示词以生成更符合需求的报告：

```
让日报更简洁一点
论文分析要更深入
重点关注方法论
```

## 🛠️ 核心模块

### 1. 论文搜索 (`src/search.py`)

```python
from src.search import search_arxiv_papers

papers = search_arxiv_papers(
    query="AI Agent",
    max_results=10,
    time_window_hours=24
)
```

### 2. PDF 处理 (`src/pdf_processor.py`)

```python
from src.pdf_processor import process_pdf

paper_with_content = process_pdf(papers[0])
# 返回包含元数据和提取文本的字典
```

### 3. 分析准备 (`src/analyzer.py`)

```python
from src.analyzer import prepare_summary, prepare_analysis

# 准备日报
result = prepare_summary(papers)
# result['prompt'] 包含填充好的提示词

# 准备深度分析
result = prepare_analysis(paper_with_content)
```

### 4. 配置管理 (`src/utils.py`)

```python
from src.utils import load_config, save_config, load_prompt, save_prompt

# 配置管理
config = load_config()
config['time_window_hours'] = 48
save_config(config)

# 提示词管理
prompt = load_prompt('daily_summary')
save_prompt('daily_summary', modified_prompt)
```

## 🎯 最佳实践

1. **首次使用**：完整运行 onboarding 流程，确保配置符合需求
2. **定期调整**：根据日报质量动态调整搜索参数
3. **提示词定制**：根据个人偏好自定义报告风格
4. **缓存利用**：PDF 会缓存在本地，避免重复下载
5. **分类细化**：根据研究领域选择合适的 arxiv 分类

## 📊 示例输出

### 日报示例

```markdown
# 📚 Arxiv 论文日报 - 2024-01-15

## 📊 概览
- 论文数量：8 篇
- 时间范围：2024-01-14 至 2024-01-15
- 主要领域：AI Agent, Large Language Models

## 🔥 重点推荐

### Tool Learning for Large Language Models
- **Arxiv ID**: 2401.12345
- **一句话总结**: 提出了一种新的工具学习框架，使 LLM 能够更有效地使用外部工具
- **创新点**: 引入了工具选择和执行的多阶段学习策略
- **推荐理由**: 对 Agent 工具使用有重要启发

...

## 💡 研究趋势观察
本次论文主要集中在 Agent 的工具学习和推理能力提升上...
```

### 深度分析示例

```markdown
# 📄 论文深度分析报告

## 基本信息
- **标题**: Tool Learning for Large Language Models
- **作者**: Zhang et al.
- **Arxiv ID**: 2401.12345
- **推荐指数**: ⭐⭐⭐⭐☆ (4/5)

## 一、研究背景与动机
### 1.1 问题陈述
LLM 在处理需要外部知识和计算的任务时存在局限性...

## 二、核心贡献
1. **贡献点 1**: 提出了工具学习的统一框架
2. **贡献点 2**: 设计了工具选择的多阶段学习策略
...
```

## 🔍 常见问题

### Q: 搜索不到论文怎么办？
A: 尝试以下方法：
- 扩大时间窗口（如从 24h 调整为 48h）
- 简化搜索关键词
- 添加更多相关分类

### Q: PDF 下载失败怎么办？
A: 可能原因：
- Arxiv 服务暂时不可用 —— 稍后重试
- 论文暂无 PDF 版本 —— 基于摘要分析

### Q: 如何重置所有设置？
A: 使用命令：
```
重置为默认配置
```

或手动删除 `~/.arxiv-search/config.json`

### Q: 提示词自定义后想恢复默认？
A: 删除 `~/.arxiv-search/prompts/` 目录下的文件即可

## 📄 License

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Happy Research! 🎓**
