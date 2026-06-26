---
name: biaoshu-writer
description: 标书撰写器 v5.4.0 - 投标技术标文档自动生成工具。支持解析 txt/pdf/docx/xlsx 招标文件，生成符合评分标准的技术标 Word 文档。适用：技术标编写、交通工程（高速/航道）投标。
metadata:
  openclaw:
    requires:
      python: ["python-docx", "pdfplumber", "openpyxl", "PyPDF2"]
    install:
      - id: pip
        kind: pip
        packages:
          - python-docx
          - pdfplumber
          - openpyxl
          - PyPDF2
        label: 安装 Python 依赖库
---

# 标书撰写器 v5.4.0

投标技术标文档自动生成工具。发送招标文件 → 自动生成符合评分标准的技术标 Word 文档。

---

## 更新日志

### v5.4.0 (2026-04-14)
- 🐛 **修复：** `merge_chapters.py` 确保章节间空行分隔，修复章节不连续问题
- 🐛 **修复：** 禁止章节末尾写「本章小结」，避免一级标题导致结构错乱
- 🐛 **修复：** 章节序号统一为中文数字，禁止混用阿拉伯数字
- ⚙️ **优化：** 新增 `merge_chapters.py` 合并脚本，替代直接 cat 拼接

### v5.3.0 (2026-04-01)
- 🐛 **修复：** Word 文档元数据创建时间从 2013 年修正为当前时间；creator/description 改为 User
- ⚙️ **优化：** `convert_to_word.py` 保存后自动修复 docx 元数据

### v5.2.1 (2026-03-27)
- 新增 `check_chapter_words.py` 章节字数检查脚本

---

## 环境安装

### 依赖库
```bash
pip install python-docx pdfplumber openpyxl PyPDF2
```

### 字体
将 `SimSun.ttf`（宋体）复制到 `~/Library/Fonts/`（从 Windows `C:\Windows\Fonts\` 复制或网上下载）

---

## 执行流程（标准）

```
① 发送招标文件 → ② 解析评分标准与采购需求
③ 生成4级标题详细大纲 → Owen 审核大纲
④ 审核通过后派发子进程并发编写各章节
⑤ 章节字数检查（必须步骤）
⑥ humanizer-zh 去 AI 痕迹（必须步骤）
⑦ 汇总整合 → 转换 Word
```

### 字数检查（必须）

公式：`目标字数 = 评分分值 × (总页数 ÷ 总分) × 780`  
合格范围：`目标 × 0.75 ~ 1.25`

| 分值 | 目标字数 | 合格范围 |
|------|---------|---------|
| 5分  | 20,000字 | 15,000~25,000字 |
| 4分  | 16,000字 | 12,000~20,000字 |

不达标 → 打回对应章节重写 → 达标后继续

---

## 格式参数

### 格式指令（Markdown 顶部加注释块）

```markdown
<!-- doc-format
font: SimSun
body-size: 16pt
title-level: 36pt
sub-level: 32pt
line-spacing: 26pt
margins: 2cm
first-line-indent: 0.74cm
-->
```

### 默认值

| 参数 | 默认值 | 说明 |
|------|--------|------|
| font | SimSun | 正文字体 |
| body-size | 16pt | 正文字号（三号） |
| title-level | 36pt | 一级标题 |
| sub-level | 32pt | 二级标题 |
| line-spacing | 26pt | 行距 |
| margins | 2cm | 页边距 |
| first-line-indent | 0.74cm | 首行缩进（2字符） |

### 常用模板

| 模板 | 参数 |
|------|------|
| 政府标书 | SimSun / 16pt / 26磅 / 2cm |
| 高速公路 | SimSun / 16pt / 28磅 / 2.5cm |
| 航道工程 | SimSun / 16pt / 26磅 / 2cm |

---

## 内容编写规则

| 规则 | 说明 |
|------|------|
| 段落结构 | 每小节（`### X.X.X`）≥ 3 个独立段落，禁止单一长段落 |
| 表格展示 | 每个章节尽量包含表格，不能全是文字 |
| 禁用词汇 | ❌ 不用"我方/我们"；✅ 用"将/项目组/本方案" |
| 金额描述 | ❌ 禁止在技术标中出现金额/预算描述 |
| 内容贴合 | 严格按评分标准和采购需求编写，不泛泛而谈 |
| 章节结尾 | ❌ 禁止写「本章小结」「本章小结」「本章总结」等章节总结段；章节正文写完即结束，禁止添加任何以 `#` 开头的总结性标题 |
| 章节序号 | ✅ 统一使用中文数字（一、二、三…），禁止混用阿拉伯数字（第3章 vs 第三章）|

---

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `parse_bid_files.py` | 解析 txt / pdf / docx / xlsx 招标文件 |
| `convert_to_word.py` | Markdown → Word（含元数据修复 v5.3.0） |
| `check_chapter_words.py` | 章节字数检查 |
| `check-font.sh` | 检查 SimSun.ttf 字体是否安装 |
| `install-deps.sh` | 一键安装 Python 依赖 |

---

## 输出规范

- 输出路径：`/Users/owen/Desktop/{项目名称}/`
- Word 文件命名：`{项目名称}_技术标_{日期}.docx`
- 项目目录模板：

```
/Users/owen/Desktop/{项目名称}/
└── 章节/
    ├── 01_第一章.md
    └── {项目名称}_技术标_{日期}.docx
```
