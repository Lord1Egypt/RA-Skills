---
name: convert2docx
title: 文档转 Word（convert2docx）
description: 把 Markdown / 纯文本 / HTML / RTF / LaTeX / reStructuredText / Org-mode 转成 .docx，并套用用户自己指定的 reference.docx 样式模板。支持单文件、批量、拖拽操作。当用户说"把 XX 转成 Word"、"批量转 docx"、"用我自己的样式模板转换文档"时使用本技能。
agent_created: true
version: 1.0.0
license: MIT
---

# convert2docx — 文档转 Word

## 用途

本技能用于把各种常见文档格式（`.md` `.markdown` `.txt` `.html` `.htm` `.rtf` `.tex` `.rst` `.org`）统一转换成 `.docx`，并套用**用户自己指定的 `reference.docx`** 作为样式模板。

## 重要原则：reference.docx 由用户自己提供

**本技能不附带任何默认 `reference.docx` 模板。**

用户必须：
1. 自己准备一个 `reference.docx`（可以用 Word 打开 Pandoc 导出的 docx，改好样式后另存）
2. 首次运行时指定该文件路径
3. 路径会被记忆到 `config.ini`，之后自动使用

如果用户没有准备 `reference.docx`：
- **不要**自动下载或生成一个"默认模板"来用
- 提示用户："请先准备一个 reference.docx（用 Word 打开任意 pandoc 生成的 docx，改好样式后另存），然后告诉我路径"

## 首次运行流程

1. 检测 `config.ini` 是否存在
2. 不存在 → 依次询问用户：
   - `pandoc.exe` 路径（若 PATH 中已有 `pandoc`，直接回车即可）
   - `reference.docx` 路径（必填，不提供则退出）
3. 把两个路径写入 `config.ini`
4. 之后每次运行直接读取，不再询问

## 使用方法

### 方式 A：拖拽（推荐，Windows 资源管理器）

把一个或多个文件**一次性拖到** `scripts/convert2docx.bat` 上，自动批量转换。bat 通过环境变量 `C2D_FILES`（`|` 分隔）把文件列表传给 ps1，规避 PowerShell 5.1 的参数绑定限制。

### 方式 B：命令行（PowerShell）

```powershell
# 单文件
.\convert2docx.ps1 input.md

# 批量：从文件列表读取（一行一个路径）
.\convert2docx.ps1 -FileList list.txt

# 指定 reference（覆盖 config.ini 中的记忆值）
.\convert2docx.ps1 input.md -ReferencePath "C:\path\to\your\reference.docx"

# 指定输出目录
.\convert2docx.ps1 input.md -OutputDir "C:\output"
```

> **注意**：不要用 `.\convert2docx.ps1 a.md b.md` 这种写法。PowerShell 5.1 的 `-File` 调用会把第二个路径当成参数名并抛 `PositionalParameterNotFound`。批量请用拖拽或 `-FileList`。

### 方式 C：在 WorkBuddy 对话中

直接对 WorkBuddy 说：
- "把 D:\docs\report.md 转成 Word，用我自己的 reference.docx"
- "批量转换 D:\docs\ 下所有 .md 文件"

WorkBuddy 会生成文件列表后调用 `-FileList` 来执行。

## 输入格式支持

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Markdown | `.md` `.markdown` | 默认 |
| 纯文本 | `.txt` | 自动识别编码 |
| HTML | `.html` `.htm` | 含 CSS 的内联样式 |
| RTF | `.rtf` | 富文本 |
| LaTeX | `.tex` | 数学公式可转 OMML |
| reStructuredText | `.rst` | |
| Org-mode | `.org` | |

## 输出规则

- 输出文件名：`<原文件名>.docx`
- 如果输入是 `.docx`：输出 `<原文件名>_restyled.docx`（**不覆盖原件**）
- 默认输出到与输入文件相同目录，可用 `-OutputDir` 指定
- 若输出文件已存在：**自动跳过**，不覆盖

## 配置文件 `config.ini`

首次运行后自动生成于 skill 根目录：

```ini
[pandoc]
path=C:\Program Files\Pandoc\pandoc.exe

[reference]
path=C:\Users\YourName\Documents\reference.docx
```

用户想改路径：直接编辑 `config.ini`，或删掉后重新运行。

## 脚本说明

| 文件 | 用途 |
|------|------|
| `scripts/convert2docx.ps1` | 主转换脚本（PowerShell，推荐） |
| `scripts/convert2docx.bat` | Windows 拖拽入口（调 ps1） |

## 依赖

- **pandoc**：必须单独安装（https://pandoc.org/installing.html）。技能不打包 pandoc。
- **PowerShell 5.1+**：Windows 自带。

注意：Windows PowerShell 5.1 读取含中文字符的 `.ps1` 脚本时，文件必须存为 **UTF-8 with BOM**。`scripts/convert2docx.ps1` 已按此格式保存，直接运行不会乱码或解析失败。修改该文件时务必保持 BOM。

## 常见坑

1. **批量传文件不要用位置参数**：`ps1 a.md b.md` 在 PS 5.1 下会抛 `PositionalParameterNotFound`。用拖拽或 `-FileList`。
2. **路径含空格**：所有脚本内部已对路径加引号，可放心使用
3. **中文乱码**：`.bat` 已加 `chcp 65001`；`.ps1` 必须存为 UTF-8 with BOM（已处理，修改时勿丢 BOM）
4. **reference.docx 不存在**：脚本会报错并提示，不会静默用默认样式
5. **pandoc 不识别 `-f auto`**：脚本已按扩展名显式映射输入格式（markdown/html/rtf/latex/rst/org/docx）
6. **批量转换时某个文件失败**：继续转换剩余文件，最后汇总报错
7. **子进程输出编码**：Windows PowerShell 5.1 的 stdout 是 GBK/ANSI，不是 UTF-8。程序化调用时按 GBK 解码

## 参考文档

- 详细配置说明：`references/config.md`
- reference.docx 制作指南：`references/make-reference.md`
