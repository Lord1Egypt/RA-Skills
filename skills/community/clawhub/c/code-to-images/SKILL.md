---
name: "code-to-images"
description: "Convert code files into A4-ratio PNG/SVG images with line numbers, syntax highlighting and per-editor color families, then merge into a PDF. 把代码文件渲染成带行号、语法高亮的 A4 图片并合成 PDF。"
---

# Code → A4 图片 + PDF / Code → A4 Images + PDF

**v2.3.0** · 49 种语言 · 11 个编辑器配色族 · 忠实缩进 · 自动换行 · 裁剪导出

把源代码文件渲染成**带行号、语法高亮**的 A4 比例图片（SVG + PNG），再合成一个 PDF。
语言按扩展名 / 文件名 / 内容自动识别，不用手动指定。

---

## 什么时候用

- 代码要**打印**：作业、讲义、代码审查、比赛提交稿
- 代码要**发图**：贴到文档、PPT、社交平台，需要整齐的版式和行号
- 代码要**存成 PDF 归档**，又不想丢高亮和缩进

---

## 快速开始

```bash
# 依赖（先装一次）
npm install -g @resvg/resvg-js
pip install img2pdf

# 渲染指定文件（推荐）
python gen_code_pdfs.py main.c app.py schema.sql

# 或编辑 gen_code_pdfs.py 顶部的 FILES 列表后直接运行
python gen_code_pdfs.py
```

**输出**：

```
main.c.pdf                    ← 合成好的 PDF（默认裁掉空白，只留代码区域）
main.c_images/
├── code_page_1.svg           ← 矢量图，可再编辑
├── code_page_1.png           ← 位图
├── code_page_1_crop.png      ← PDF 实际使用的裁剪页
└── ...
```

---

## 核心能力

| 能力 | 说明 |
|---|---|
| **49 种语言自动识别** | 按扩展名 → 文件名 → 内容嗅探（`.m` 区分 Objective-C / MATLAB，`Makefile` / `Dockerfile` / `CMakeLists.txt` 按文件名） |
| **按编辑器配色（11 族）** | 每种语言用它最主流编辑器的亮色主题：VS Code、IntelliJ、Xcode、Visual Studio、Keil、Chrome DevTools、MATLAB、RStudio、TeXstudio、Arduino、微信暖色 |
| **小程序专属配色** | `.wxml` / `.wxss` 走微信开发者工具暖色，`{{ }}` 表达式单独着色 |
| **HTML 分区高亮** | `.html` 内 `<style>` 按 CSS 分词、`<script>` 按 JS 分词，整页共用 Chrome 色表 |
| **多行结构** | `/* */`、`<!-- -->`、`--[[ ]]`、`{- -}`、`#= =#`、`(* *)` 跨行注释；三引号字符串（Python / Julia / 仓颉） |
| **语言特性 token** | `@` 注解与装饰器、`$` 变量（含 `${}` / `$()`）、HTML/XML 标签、Makefile 目标行、YAML 键、Markdown 标题 |
| **忠实缩进** | 保留源码真实的前导空格 / Tab，大括号风格和空格缩进语言都对 |
| **自适应排版** | 字号按最长行自动缩放填满页宽（下限可设）；每页行数按字号自动计算 |
| **标点换行** | 超宽行在 `; , ( ) { } [ ]` 后折行，续行不占新行号 |
| **6 种等宽字体** | Cascadia Code / Fira Code / JetBrains Mono / Consolas / Courier New / Source Code Pro |
| **输出尺寸** | 默认 300 DPI（2480×3508），打印清晰；可改回 96 DPI（794×1123） |

---

## 支持的语言

**脚本 / 动态**：Python、JavaScript、TypeScript、Ruby、Perl、PHP、Lua、Shell、PowerShell、Batch、Visual Basic、R、MATLAB、Julia

**编译 / 系统**：C、C++、Arduino、Go、Rust、Zig、Swift、Kotlin、Dart、仓颉 Cangjie、Objective-C、Scala、Haskell、Erlang、Elixir、Clojure、F#、Pascal、Fortran、Assembly、Solidity

**标记 / 配置 / 数据**：Java、C#、Groovy、CSS、HTML/XML、JSON、YAML、INI/TOML、Markdown、LaTeX、SQL、Makefile、Dockerfile、CMake

> 未识别的扩展名会回退到通用规则，保证仍能正常出图。

---

## 常用配置

在 `gen_code_pdfs.py` 顶部：

| 参数 | 默认 | 作用 |
|---|---|---|
| `FILES` | — | 要渲染的文件列表（命令行参数可覆盖） |
| `FONT_KEY` | `cascadia` | 字体：`cascadia` / `firacode` / `jetbrains` / `consolas` / `courier` / `sourcecode` |
| `FONT_SIZE` | `14` | 基础字号（px），超宽代码会自动缩小 |
| `MIN_FONT_SIZE` | `7` | 自动缩小的下限 |
| `LINE_HEIGHT_RATIO` | `1.65` | 行高系数 |
| `TAB_WIDTH` | `4` | Tab 制表位宽度 |
| `WRAP_IDENT` | `2` | 续行额外缩进字符数 |
| `CROP_TO_CONTENT` | `True` | PDF 页裁剪到代码区域，去掉大片留白 |
| `A4_W, A4_H` | `2480, 3508` | 输出尺寸（300 DPI）；改 `794, 1123` 即 96 DPI |

**换配色**：改 `FAMILY_PALETTES[族]` 里某个 token 的颜色；**换族**：改 `LANG_TO_FAMILY[语言]`。

**新增语言**：在 `LANG` 里加一条规则（关键字、注释、字符串、特殊 token），再到 `EXT2LANG` 登记扩展名即可。

---

## 注意事项

- 必须能调用 `node`（渲染 SVG → PNG）。不在 PATH 时设环境变量 `NODE_EXE` 指向可执行文件。
- `@resvg/resvg-js` 装在本地目录时，设 `NODE_PATH` 指向对应 `node_modules`。
- 源文件按 UTF-8 读取；非 UTF-8 编码请先转码。
- 单文件页数由内容长度决定，超长文件会生成多页，每页独立 SVG/PNG，最后合成一个 PDF。

---

**仓库**：https://github.com/yon-gjun/code-to-images
