# convert2docx 使用指南

## 这是什么

一个把 Markdown / 文本 / HTML / RTF / LaTeX / reStructuredText / Org-mode 转成 Word (.docx) 的工具。

特点是：**样式完全由用户自己控制**，通过指定一个 `reference.docx` 作为模板。本工具**不提供任何默认模板**。

## 为什么用 reference.docx

Pandoc 默认生成的 docx 样式很朴素。通过 `--reference-doc` 参数，可以让 Pandoc 套用你自带的样式：
- 字体、字号、行距
- 标题层级样式
- 代码块、引用块样式
- 页面边距、页眉页脚

## 首次使用

### 1. 准备 reference.docx

**本工具不提供默认模板，你需要自己准备一份。**

方法一：拿一个已经调好样式的 Word 文档，另存为 `reference.docx`。

方法二：用 pandoc 导出空白模板，再用 Word 改样式：
```powershell
pandoc --print-default-data-file reference.docx > my_reference.docx
```

方法三：参考 `references/make-reference.md` 里的详细制作指南。

### 2. 配置路径

首次运行 `convert2docx.ps1` 或 `convert2docx.bat` 时，会提示你输入：
- pandoc.exe 路径（若已加入 PATH，直接回车）
- reference.docx 路径（必填，不填则退出）

配置会保存到 `config.ini`，下次自动使用。

## 日常使用

### 拖拽（推荐）
把一个或多个文件拖到 `scripts/convert2docx.bat` 上即可。bat 会通过环境变量把文件列表传给脚本，支持批量。

### 命令行
```powershell
# 单文件
.\scripts\convert2docx.ps1 input.md

# 批量：从文件列表读取（一行一个路径）
.\scripts\convert2docx.ps1 -FileList list.txt

# 指定 reference / 输出目录
.\scripts\convert2docx.ps1 input.md -ReferencePath "D:\styles\reference.docx"
.\scripts\convert2docx.ps1 input.md -OutputDir "C:\output"
```

> **不要用** `.\convert2docx.ps1 a.md b.md` 这种写法。PowerShell 5.1 的 `-File` 调用会把第二个路径当成参数名并报错。批量请用拖拽或 `-FileList`。

### 在 WorkBuddy 里
直接说："把 xx.md 转成 Word，用我的 reference.docx"

## 输出规则

| 输入 | 输出 |
|------|------|
| `.md` `.txt` `.html` `.rtf` `.tex` `.rst` `.org` | `xx.docx` |
| `.docx` | `xx_restyled.docx`（不覆盖原件） |

- 默认输出到与输入文件相同目录，可用 `-OutputDir` 指定
- 若输出文件已存在：**自动跳过**，不覆盖

## 配置文件 config.ini

```ini
[pandoc]
path=C:\Program Files\Pandoc\pandoc.exe

[reference]
path=C:\Users\YourName\Documents\reference.docx
```

改路径：直接编辑此文件，或删掉重新运行。

## 常见问题

**Q: 没有 reference.docx 怎么办？**
A: 必须自己准备。参考 `references/make-reference.md`。

**Q: 转换失败？**
A: 检查：
1. pandoc 是否安装并加入 PATH
2. reference.docx 路径是否正确
3. 输入文件格式是否支持（.md/.txt/.html/.rtf/.tex/.rst/.org/.docx）

**Q: 脚本报乱码/语法错误？**
A: `convert2docx.ps1` 必须存为 **UTF-8 with BOM**（Windows PowerShell 5.1 要求）。包内已按此格式打包。

**Q: 如何批量转换？**
A: 把多个文件拖到 bat 上（推荐），或生成文件列表（一行一个路径）后用 `-FileList list.txt`。

**Q: 输出文件已存在会怎样？**
A: 自动跳过，不会覆盖。
