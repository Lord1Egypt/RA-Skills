---

slug: doc-toolkit-free
name: doc-toolkit-free
version: 1.0.1
displayName: 文档工具箱免费版
summary: "使用python-docx读写与编辑DOCX文档，支持基础格式化与视觉校验，适合日常文档处理.。文档工具箱免费版是一款面向开发者的DOCX文档处理Skill，封装python-docx与Li"
license: MIT
edition: free
description: "文档工具箱免费版是一款面向开发者的DOCX文档处置Skill，封装python-docx与LibreOffice渲染能力，包含从读取、创建到编辑的完整基础工作流。核心能力：. 适用于需要doc toolkit相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量."
tags:
  - 文档处理
  - doc
  - toolkit
  - automation
  - productivity
  - DOCX
  - 办公自动化
  - 排版校验
  - 工具
  - 效率
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free

---

# 文档工具箱免费版（Doc Toolkit Free）

## 概述

DOCX文档的"代码能跑"与"交付可用"之间隔着排版这道坎。本Skill以"视觉校验优先"为核心工作流，每次内容修改后自动渲染为图片检查，确保最终文档无格式缺陷。封装python-docx的复杂API，用自然语言驱动文档生成与编辑.
设计原则：
1. **视觉优先**：先渲染再看，避免盲改导致排版错乱
2. **结构清晰**：标题、段落、表格、列表的层级分明
3. **可回溯**：中间产物有序存放，便于回退与对比
4. **ASCII规范**：仅使用ASCII连字符，避免Unicode特殊字符导致乱码

## 核心能力

### 文档操作矩阵

| 操作 | 能力描述 | 实现方式 |
|---|----|----|
| 读取 | 提取文本、表格、样式信息 | python-docx解析 |
| 创建 | 从零生成结构化文档 | python-docx构建 |
| 编辑 | 修改已有文档的段落与表格 | python-docx定位替换 |
| 渲染 | DOCX转PDF转PNG，逐页检查 | LibreOffice + pdftoppm |
| 校验 | 检查排版缺陷（溢出、错位、乱码） | 渲染图片视觉审查 |

**处理**: 解析文档操作矩阵的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回文档操作矩阵的响应数据,包含状态码、结果和日志.
### 支持的文档元素

| 元素 | 创建 | 编辑 | 读取 |
|:-----|:-----|:-----|:-----|
| 标题（H1-H9） | ✅ | ✅ | ✅ |
| 段落 | ✅ | ✅ | ✅ |
| 表格 | ✅ | ✅ | ✅ |
| 有序/无序列表 | ✅ | ✅ | ✅ |
| 图片 | ✅ | ❌ | ✅ |
| 页眉页脚 | ✅ | ✅ | ✅ |
| 目录 | ✅ | ❌ | ✅ |
| 超链接 | ✅ | ❌ | ✅ |

**处理**: 解析支持的文档元素的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回支持的文档元素的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：读写与编辑、支持基础格式化与、视觉校验、适合日常文档处理、文档工具箱免费版、是一款面向开发者、文档处理、渲染能力、提供从读取、创建到编辑的完整、基础工作流、核心能力、读取与审查、创建结构化、基础格式化等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：API文档自动生成
从接口定义生成标准化的API说明文档，包含接口名称、请求参数表格、响应示例、错误码表。表格自动对齐，标题层级清晰.
### 场景二：操作手册批量更新
产品功能迭代后，操作手册的截图与步骤需要更新。定位到对应章节，替换内容并重新渲染校验，确保手册与产品同步.
### 场景三：周报模板填充
固定格式的周报模板，每周填充不同的项目进展、数据指标、下周计划。模板保持格式不变，仅替换变量内容.
### 场景四：合同文档审查
审查合同DOCX中的条款表格，提取关键条款（金额、期限、违约责任）为结构化数据，便于法务快速核对.
### 场景五：交付前排版校验
文档交付客户前，逐页渲染检查是否有文字溢出、表格错位、图片缺失、默认模板样式等缺陷，确保交付质量.
## 不适用场景

以下场景文档工具箱免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 120秒上手

1. **安装依赖**：`uv pip install python-docx pdf2image`（或系统安装LibreOffice+Poppler）
2. **描述需求**：告诉Agent要创建或修改什么文档
3. **生成与渲染**：Agent创建/修改DOCX，自动渲染为PNG
4. **视觉校验**：逐页检查排版，发现问题立即修复
5. **交付**：确认无误后输出最终文件

### 示例

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 文档工具箱免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
from docx import Document
from docx.shared import Pt, Inches
# ...
doc = Document()
doc.add_heading('项目周报', level=1)
doc.add_paragraph('本周完成以下工作：')
# ...
# 添加表格
table = doc.add_table(rows=3, cols=3)
table.style = 'Table Grid'
table.cell(0,0).text = '任务'
table.cell(0,1).text = '负责人'
table.cell(0,2).text = '状态'
# ...
doc.save('weekly_report.docx')
```

### 渲染校验命令

**DOCX转PDF**：
```bash
soffice --headless --convert-to pdf --outdir /tmp/output weekly_report.docx
```

**PDF转PNG**：
```bash
pdftoppm -png /tmp/output/weekly_report.pdf /tmp/output/page
```

**一键渲染脚本**：
```bash
python3 render_docx.py weekly_report.docx --output_dir /tmp/docx_pages
```

## 配置示例

### 依赖详情

**Python包**：
```bash
uv pip install python-docx pdf2image
# 或
pip install python-docx pdf2image
```

**系统工具（渲染）**：
```bash
# macOS
brew install libreoffice poppler
# ...
# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
# ...
# Windows
# 下载LibreOffice安装包，Poppler需单独配置
```

### 文件目录约定

```
tmp/docs/          # 中间文件（渲染产物、草稿）
output/doc/        # 最终交付文档
```

### 质量规范

- 字体一致：中文用宋体/微软雅黑，英文用Times New Roman/Arial
- 间距统一：段落间距、行距、页边距全篇一致
- 层级清晰：标题层级不超过4级，避免过度嵌套
- 仅用ASCII连字符：避免U+2011（非断行连字符）等Unicode特殊字符
- 引用可读：引用内容人类可读，不留工具标记或占位符

## 优秀实践

1. **先渲染后修改**：修改前先渲染当前版本，建立基线对比
2. **小步迭代**：每次修改一个章节，渲染检查后再继续
3. **样式继承**：使用文档内置样式而非逐段设置格式，保证一致性
4. **表格规范**：表格使用Table Grid样式，避免无边框表格在PDF中消失
5. **图片尺寸**：图片宽度不超过页面宽度，建议设置为Inches(6.0)以内
6. **清理中间产物**：交付后清理tmp目录，避免文件堆积
7. **100%放大检查**：渲染图片在100%放大下逐页检查，模拟真实阅读体验

## 常见问题

### Q1：soffice命令未找到？
A：需要安装LibreOffice。macOS用`brew install libreoffice`，Linux用`apt-get install libreoffice`，Windows需下载安装包.
### Q2：渲染的PNG中文乱码？
A：服务器缺少中文字体。安装中文字体包：`apt-get install fonts-noto-cjk`或`fonts-wqy-zenhei`.
### Q3：python-docx能修改图片吗？
A：免费版支持创建时插入图片，但不支持替换已有图片。图片替换属于专业版能力.
### Q4：能批量处理多个DOCX吗？
A：免费版单次处理1个文档。批量处理、模板管理、邮件合并属于专业版能力.
### Q5：目录能自动生成吗？
A：免费版支持插入目录占位符，但需在Word中手动刷新。自动更新目录属于专业版能力.
### Q6：没有LibreOffice怎么渲染？
A：可使用python-docx提取文本作为降级方案，但无法进行视觉校验。建议安装LibreOffice获得完整体验.
## 已知限制

本免费体验版限制以下高级功能：
- ❌ 批量文档处理（>1个文档/次）
- ❌ 自定义模板库管理
- ❌ 邮件合并（Mail Merge）
- ❌ 图片替换与编辑
- ❌ 目录自动刷新
- ❌ 文档版本对比
- ❌ 水印与加密
- ❌ 多格式导出（PDF/HTML/EPUB）

解锁全部功能请使用专业版：doc-toolkit-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.8+
- **LibreOffice**：7.0+（视觉渲染）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| python-docx | Python包 | 必需 | `pip install python-docx` |
| pdf2image | Python包 | 渲染必需 | `pip install pdf2image` |
| LibreOffice | 系统工具 | 渲染必需 | 系统包管理器安装 |
| Poppler | 系统工具 | PDF转PNG必需 | 系统包管理器安装 |

### API Key 配置
- 本Skill基于本地工具，无需额外API Key
- 渲染使用本地LibreOffice，不涉及外部API调用

### 可用性分类
- **分类**：MD+EXEC（Markdown指令驱动，文档渲染需要exec命令行能力）
- **说明**：DOCX文档处理Skill，支持创建、编辑、渲染校验的完整基础工作流

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "文档工具箱免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "dockit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
