---
name: docx2pdf
title: Word 批量转 PDF (soffice / LibreOffice)
version: 1.0.0
agent_created: true
license: MIT
author: 赵加栋
tags:
  - windows
  - libreoffice
  - soffice
  - pdf
  - batch-conversion
  - powershell
  - docx
  - doc
description: |
  在 Windows 上用 LibreOffice 的 soffice.exe 无头模式，批量把当前目录下的
  .doc / .docx 转成 .pdf。不依赖 Microsoft Word 安装，纯命令行，适合一次性批量处理。
  无需 Office 许可证，跨 Windows 版本可用。
usage: |
  在 PowerShell 里 cd 到目标目录，执行：

    & 'C:\Program Files\LibreOffice\program\soffice.exe' --headless --invisible --convert-to pdf --outdir ./ *.doc *.docx

  只转 .docx（排除 .doc）就把末尾的 *.doc 去掉；
  输出到子目录 output_folder/ 就改 --outdir output_folder。
prerequisites: |
  - Windows 7+ / Windows Server 2012+
  - LibreOffice 已安装（https://www.libreoffice.org/download/）
  - soffice.exe 在 PATH，或把 SOFFICE 环境变量指向其完整路径
  - PowerShell 3.0+
inputs:
  - 当前目录下的 *.doc / *.docx（PowerShell 通配符自动展开，soffice 不解析通配符本身）
outputs:
  - 同目录（或 --outdir 指定目录）生成与源文件同名的 .pdf
  - 已存在的 .pdf 会被覆盖
config:
  SOFFICE: 默认 'C:\Program Files\LibreOffice\program\soffice.exe'；其它安装位置通过环境变量 SOFFICE 覆盖
notes: |
  - 路径含空格，PowerShell 必须用 & 调用运算符 + 单引号包路径，不要直接 `'xxx.exe' args`
  - 不要用 `./` 或 `.\*` 当输入 —— 实测会把目录当文件传入而失败；直接靠 shell 展开 `*.doc *.docx` 最稳
  - soffice 在转换时会启动一个 soffice.bin 后台进程，连续跑多轮可能报 "already running"，
    失败时先 `Get-Process soffice* | Stop-Process -Force` 再重试
  - --headless --invisible 两个都带上，避免弹窗挂起
  - 复杂 Word 排版（修订、嵌入对象、SmartArt）转 PDF 可能错位，重要文件抽查几份
  - 大批量（>50 个）建议分批，或先 `--convert-to pdf:writer_pdf_Export` 显式指定导出器
created: 2026-09-24
---

# docx2pdf — Word 批量转 PDF

不依赖 Microsoft Word，用 LibreOffice 在命令行批量把 `.doc` / `.docx` 转 `.pdf`。

## 一行命令（最常用）

```powershell
& 'C:\Program Files\LibreOffice\program\soffice.exe' --headless --invisible --convert-to pdf --outdir ./ *.doc *.docx
```

如果你的 LibreOffice 装在别的位置，把路径换成你的；或者先设环境变量：

```powershell
$env:SOFFICE = 'D:\Program Files\LibreOffice\program\soffice.exe'
& $env:SOFFICE --headless --invisible --convert-to pdf --outdir ./ *.doc *.docx
```

## 命令拆解

| 段 | 作用 |
|----|------|
| `& '...soffice.exe'` | PowerShell 调用带空格路径的可执行文件，必须用 `&`（调用运算符） |
| `--headless --invisible` | 无 UI、无弹窗；两个都带，缺一个都可能挂起 |
| `--convert-to pdf` | 输出格式；也可写 `pdf:writer_pdf_Export` 显式指定导出器 |
| `--outdir ./` | 输出目录，`./` = 当前目录；改 `output_folder` 输出到子目录 |
| `*.doc *.docx` | PowerShell 通配符展开后逐个传给 soffice（soffice 本身不解析通配符） |

## 常见变体

```powershell
# 只转 .docx
& $env:SOFFICE --headless --invisible --convert-to pdf --outdir ./ *.docx

# 输出到子目录
& $env:SOFFICE --headless --invisible --convert-to pdf --outdir ./pdf_out *.doc *.docx

# 递归子目录（PowerShell 展开）
Get-ChildItem -Recurse -Include *.doc,*.docx | ForEach-Object {
  & $env:SOFFICE --headless --invisible --convert-to pdf --outdir $_.DirectoryName $_.FullName
}

# 找到 soffice 真实路径（多版本共存时）
Get-ChildItem 'C:\Program Files','D:\Program Files' -Recurse -Filter soffice.exe -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty FullName
```

## 踩过的坑（来自真实历史）

1. **直接 `'path\soffice.exe' args`** → PowerShell 把字符串当字符串，不执行。必须 `& 'path' args`。
2. **传 `./` 或 `.\*`** → soffice 把目录当文件，转换失败。要靠 shell 通配符展开具体文件列表。
3. **路径里 `Program Fil`、`Program\ Fil` 这种截断/转义错乱** → 整段用单引号包起来，别自己拆。
4. **连续跑批第二次报 already running** →
   ```powershell
   Get-Process soffice* -ErrorAction SilentlyContinue | Stop-Process -Force
   Start-Sleep -Seconds 2
   ```
5. **`.pdf` 已存在会被静默覆盖**，源文件不会有事，但旧 PDF 不会提示。
6. **路径里没有 soffice.exe** → 用上面 `Get-ChildItem` 找一下真实位置；LibreOffice 32 位默认在 `C:\Program Files (x86)\LibreOffice\program\soffice.exe`。

## 故障排查

| 症状 | 原因 | 解决 |
|------|------|------|
| 命令没反应 | 缺 `&` 调用运算符 | `& 'path\to\soffice.exe' args` |
| 报 "is not recognized" | 路径错误或没引号 | 整段路径用单引号包起来 |
| 报 "source file could not be loaded" | 传了目录而非具体文件 | 用 `*.doc *.docx` 展开，别传 `./` |
| 报 "already running" | 上次 soffice.bin 没退 | `Stop-Process -Name soffice* -Force` |
| 输出 PDF 排版错乱 | Word 用了 LibreOffice 不支持的功能 | 用 Word 自己"另存为 PDF"，或换 PDF 导出器参数 |

## 什么时候用这个 skill

- 没有安装 Microsoft Word，或不想开 Word 批量另存
- 几十上百个 doc/docx 要一次性出 PDF
- 需要放进脚本 / 自动化流水线
- 跨 Windows 机器跑，不想装 Office

要保真排版（尤其有修订、SmartArt、嵌入 Excel 表）时，优先用 Word 自己的"另存为 PDF"。

## License

MIT，随便拿去用。
