# 📊 代码分析技能 (Code Analysis Skills)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](skill.yaml)

一款全面的 Git 仓库分析工具，可扫描代码仓库并生成多维度的开发者洞察报告——涵盖**提交模式**、**工作习惯**、**开发效率**、**代码风格**和**代码质量**五大维度。

---

## ✨ 功能特性

- 🔍 **仓库扫描** — 分析单个 Git 仓库，或递归扫描目录下所有 `.git` 仓库
- 📝 **提交模式** — 提交频率、提交大小分布、合并比例、提交信息质量评分
- ⏰ **工作习惯** — 工作时段分布、周末/深夜编码比例、连续编码天数统计
- 🚀 **开发效率** — 代码流失率、返工比例、巴士因子、文件归属分析
- 🎨 **代码风格** — 编程语言分布、约定式提交合规率、文件分类统计
- 🔎 **代码质量** — Bug 修复比例、回退频率、大提交比例、测试覆盖率、Python 复杂度分析（基于 radon）
- 👥 **多开发者对比** — 所有维度的横向对比表格
- 📄 **多种输出格式** — 支持 Markdown、JSON 或带样式的 HTML 报告

## 📦 安装

### 前置要求

- Python 3.9+
- Git

### 安装依赖

```bash
pip install -r requirements.txt
```

或单独安装各依赖包：

```bash
pip install gitpython pydriller radon tabulate jinja2 click pyyaml reportlab
```

## 🚀 使用方法

### 基本命令

```bash
# 分析单个仓库（所有贡献者）
python -m src.main -r /path/to/repo

# 递归扫描目录下所有 Git 仓库
python -m src.main -r /path/to/projects --scan-all

# 对比指定开发者
python -m src.main -r /path/to/repo -a "Alice" -a "Bob"

# 按日期范围过滤
python -m src.main -r /path/to/repo -s 2024-01-01 -u 2024-12-31

# 生成 HTML 报告
python -m src.main -r /path/to/repo -f html -o report.html

# 同时生成 Markdown + HTML + PDF
python -m src.main -r /path/to/repo -f "markdown,html,pdf" -o report

# 生成 PDF 报告
python -m src.main -r /path/to/repo -f pdf -o report.pdf

# 将 Markdown 报告保存到文件
python -m src.main -r /path/to/repo -o report.md
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `-r, --repo` | Git 仓库或父目录路径 | *（必填）* |
| `--scan-all` | 递归扫描所有 `.git` 仓库 | `false` |
| `-a, --author` | 要分析的作者名/邮箱（可重复指定） | 所有贡献者 |
| `-s, --since` | 起始日期（ISO 格式：`YYYY-MM-DD`） | — |
| `-u, --until` | 截止日期（ISO 格式：`YYYY-MM-DD`） | — |
| `-b, --branch` | 要分析的分支 | 当前分支 |
| `-f, --format` | 输出格式：`markdown`、`json`、`html`、`pdf`（逗号分隔可多选） | `markdown` |
| `-o, --output` | 输出文件路径（多格式时为基础文件名） | 标准输出 |

## 📁 项目结构

```
code-analysis-skills/
├── src/
│   ├── main.py                 # CLI 入口
│   ├── scanner.py              # 仓库扫描器（单仓库 & 递归扫描）
│   ├── analyzers/
│   │   ├── base_analyzer.py    # 基础分析器（Git 遍历 & 作者过滤）
│   │   ├── commit_analyzer.py  # 提交模式分析
│   │   ├── work_habit_analyzer.py  # 工作习惯分析
│   │   ├── efficiency_analyzer.py  # 开发效率分析
│   │   ├── code_style_analyzer.py  # 代码风格分析
│   │   ├── code_quality_analyzer.py # 代码质量分析
│   │   └── slacking_analyzer.py # 摸鱼指数分析
│   ├── evaluator/
│   │   └── developer_evaluator.py  # 开发者评估引擎
│   ├── reporters/
│   │   ├── base_reporter.py    # 报告生成器基类
│   │   ├── markdown_reporter.py # Markdown 报告生成器
│   │   ├── json_reporter.py    # JSON 报告生成器
│   │   ├── html_reporter.py    # 带样式的 HTML 报告生成器
│   │   └── pdf_reporter.py     # PDF 报告生成器
│   └── utils/
│       └── helpers.py          # 工具函数
├── tests/
│   ├── test_analyzers.py       # 分析器单元测试
│   └── test_scanner.py         # 扫描器单元测试
├── references/
│   └── metrics-guide.md        # 指标定义与健康范围参考
├── SKILL.md                    # ClawHub 技能定义
├── skill.yaml                  # 技能配置文件
├── requirements.txt            # Python 依赖清单
├── pyproject.toml              # 项目元数据
└── pytest.ini                  # 测试配置
```

## 📊 分析维度详解

### 1. 📝 提交模式
- 提交频率（日/周维度）
- 提交规模（每次提交的增删行数）
- 合并提交占比
- 提交信息质量评分

### 2. ⏰ 工作习惯
- 工作时段热力图（按小时分布）
- 周末编码百分比
- 深夜编码百分比（22:00–06:00）
- 最长连续编码天数

### 3. 🚀 开发效率
- 代码流失率（删除行数 / 新增行数）
- 返工比例（对近期修改文件的再次修改）
- 巴士因子（代码集中度风险指标）
- 文件归属分布

### 4. 🎨 代码风格
- 编程语言分布
- 约定式提交（Conventional Commits）合规率
- 文件类型分类（源码 / 测试 / 配置 / 文档）

### 5. 🔍 代码质量
- Bug 修复提交占比
- 回退（Revert）提交频率
- 大提交占比（潜在代码异味）
- 测试文件覆盖率
- Python 代码复杂度（基于 radon 的圈复杂度分析）

### 6. 🐟 摸鱼指数
- 综合 7 大信号评估开发者投入度（0-100 分）
- 信号包括：稀疏度、琐碎提交、消失模式、低产出、非代码提交、拖延症、复制粘贴
- 等级：🔥 工作狂 → ✅ 正常 → 😏 有嫌疑 → 🐟 摸鱼达人 → 🏆 摸鱼大师

### 7. 🏆 开发者评估
- 六维度加权评分（提交纪律 15% + 工作一致性 15% + 效率 20% + 代码质量 25% + 风格 10% + 参与度 15%）
- 等级：S / A / B / C / D / E / F
- 严肃直接的优点、缺点点评
- 可立即执行的改进建议
- 一句话定论

## 🧪 测试

```bash
# 运行所有测试
pytest

# 详细输出模式
pytest -v

# 运行指定测试文件
pytest tests/test_analyzers.py
```

## ⚠️ 注意事项

- 分析大型仓库（10 万+ 提交）可能耗时较长，建议限定日期范围
- Python 复杂度分析依赖 `radon`，仅适用于 `.py` 文件
- 作者匹配支持模糊匹配（名称或邮箱子串匹配）
- 目录扫描默认最大深度为 5 层，避免过深递归
- PDF 生成优先使用 weasyprint，回退到 pdfkit，最终回退到 reportlab
- 评估结果仅基于 Git 提交历史数据，不代表开发者的全部能力
- 摸鱼指数仅供参考，需结合实际工作场景理解

## ⚠️ 隐私与数据安全声明

> **重要提示**：本工具会从 Git 提交历史中提取开发者个人活动数据（提交时间、频率、行为模式等）。

**使用前请务必注意：**

- ✅ 本工具**完全本地运行**，不会向任何外部服务器传输数据
- ⚠️ 分析他人仓库前，请**获得相关开发者的知情同意**
- 🚫 分析结果**不应直接用于**绩效考核、薪酬决策或惩罚性管理
- 🔒 生成的报告包含个人信息，请**妥善保管**，不应公开分享
- 📋 使用前请确认符合组织的 HR 政策和当地数据保护法规（如 GDPR）

## 📄 许可证

本项目基于 MIT 许可证开源 — 详见 [LICENSE](LICENSE) 文件。
