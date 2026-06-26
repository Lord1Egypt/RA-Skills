# 文档可视化 Skill

将任意格式文档（飞书文档/Word/PDF/Excel/Txt）一键生成深色指挥中心风格HTML可视化看板 + PDF/长图。

## 触发方式

用户在飞书发送以下任意形式即可自动触发：
- 飞书文档链接（如 `https://my.feishu.cn/docx/xxx`）
- 附件文件（Word/Excel/PDF/Txt）
- 任何包含数据的内容文本

## 使用流程

```
用户发送文档
    ↓
[Step 1] 解析文档（自动识别格式）
    ↓
[Step 2] 数据分析 + 生成可视化配置
    ↓
[Step 3] 生成5种主题HTML供用户选择
    ↓
[Step 4] 用户确认主题
    ↓
[Step 5] Playwright导出PDF + 长图
    ↓
[Step 6] 发送文件路径给用户
```

## 5种主题（发送时指定）

| 主题 | 参数 | 风格 |
|------|------|------|
| 科技蓝 | `--theme THEME_BLUE` | 顾家原版深蓝 |
| 商务红 | `--theme THEME_RED` | 红黑商务 |
| 自然绿 | `--theme THEME_GREEN` | 绿色清新 |
| 皇家紫 | `--theme THEME_PURPLE` | 紫金高端 |
| 活力橙 | `--theme THEME_ORANGE` | 橙暖活力 |

**示例指令：** "帮我把这个飞书文档做成可视化看板，用皇家紫主题"

## 支持格式

| 格式 | 解析方案 |
|------|---------|
| 飞书文档链接 | feishu_fetch_doc → markdown解析 |
| Word (.docx) | python-docx |
| Excel (.xlsx) | openpyxl（多Sheet） |
| PDF (.pdf) | pdfplumber |
| Txt / CSV | 直接字符串读取 |

## 可视化组件（自动匹配）

根据文档内容自动选择最合适的可视化方式：

- 📊 **财务卡片网格** - 自动提取数字指标
- 📰 **时间轴** - 2024/2025/2026年份事件
- ⚔️ **对比表** - 多列数据对比
- 💼 **SWOT四象限** - 优势/劣势/机会/威胁
- 🚀 **四维战略分析** - 进攻/防守/机会/威胁
- 📋 **通用数据表格** - 结构化数据
- 📚 **来源分布统计** - emoji统计图
- 🎯 **访谈切入点** - 场景+话题建议

## 技术栈

- 解析：python-docx / openpyxl / pdfplumber
- HTML生成：自定义模板（CSS变量主题系统，无外部依赖）
- 导出：Playwright `page.pdf()` + `screenshot(full_page=True)`
- 文件输出：`~/.openclaw/workspace/visual_exports/{timestamp}/`

## 文件结构

```
skills/doc-visualizer/
├── SKILL.md               ← 本文件
├── doc_visualizer.py      ← 主入口（CLI + 模块）
├── generator/
│   └── html_generator.py  ← HTML生成器（5种主题CSS内嵌）
└── exporter/
    └── exporter.py         ← PDF/长图导出（Playwright）
```

## CLI用法

```bash
python doc_visualizer.py <文件路径> [--theme THEME_XXX]

# 示例
python doc_visualizer.py /path/to/report.xlsx --theme THEME_PURPLE
python doc_visualizer.py https://my.feishu.cn/docx/xxx --theme THEME_GREEN
```

## Python模块调用

```python
from doc_visualizer import run, parse_input, analyze_data

# 方式1：完整流程
result = run("/path/to/file.xlsx", theme="THEME_BLUE")
# 返回: {"html": path, "pdf": path, "png": path, "output_dir": path}

# 方式2：分步调用
info = parse_input("/path/to/file.xlsx")
parsed = parse_document(info)
viz_config = analyze_data(parsed)
```

## 依赖安装

```bash
pip install python-docx openpyxl pdfplumber pandas playwright
playwright install chromium
```
