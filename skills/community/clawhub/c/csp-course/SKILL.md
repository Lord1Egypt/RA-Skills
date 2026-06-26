---
name: CSP课件制作技能
description: 这个技能用于为信息学/CSP竞赛 C++ 课程（小学高年级到初中竞赛班）生成完整的教学资料套件：游戏化趣味课件（.pptx）、详细教案（.docx）、学生任务单（.docx）、代码示例（.cpp）以及网页版互动闯关游戏（.html）。支持单课制作和批量（从PDF教材）批量生成全套课程资料。当用户需要制作 C++/CSP/信奥/NOIP 编程课课件、教案、任务单，或需要从PDF教材批量生成课程资料时应使用此技能。触发词：CSP课件、信奥课件、NOIP课件、C++课件、编程课件、CSP教案、信奥教案、做课件、做教案、做任务单、PPT三件套、批量生成课件、PDF转课件。
---

# CSP课件制作技能

## 技能简介

为信息学 / CSP / NOIP C++ 课程生成完整教学资料套件，支持**单课手动制作**和**批量 PDF→全套资料**两种模式：

| 产出物 | 格式 | 说明 |
|--------|------|------|
| 🎮 游戏化趣味课件 | `.pptx` | pptxgenjs 生成，闯关主线 |
| 📄 详细教案 | `.docx` | 默认 40 分钟课时，可指定课时长度 |
| 📝 学生任务单 | `.docx` | 递进式练习，填空+补代码+追踪 |
| 💻 代码示例 | `.cpp` | UTF-8 BOM，含注释 |
| 🎯 网页闯关游戏 | `.html` | 单文件，无依赖，双击可用 |

> **适用范围**：小学高年级零基础 / 初中普通班 / CSP-J/S 竞赛班，均可通过年级参数切换难度风格。

---

## 触发场景

- "帮我做 C++ 课件" / "做一节信息学课的课件"
- "做 CSP / NOIP / 信奥 课件"
- "生成教案和任务单" / "做 PPT 三件套"
- "把这些 PDF 做成课件"（批量模式）
- "做一节排序算法的课件" / "讲 STL 的课件"
- "重新制作课件" / "帮我更新教案"
- 涉及 C++ 任意知识点（变量/循环/函数/数组/指针/STL/图论/DP 等）的课程制作需求
- 涉及竞赛算法（贪心/搜索/动态规划/图论/树结构等）的讲解课件制作

---

## 工作流程

### 模式 A：单课制作

#### 步骤 1：收集需求

若用户未指定，询问：
1. **课件风格**：活泼游戏化 / 专业简洁 / 科技暗色
2. **适用年级**：
   - 小学高年级（零基础，多比喻，少公式）
   - 初中普通班（兼顾趣味与严谨）
   - CSP-J/S 竞赛班（算法导向，代码优先）
3. **知识点**：函数/变量/循环/数组/字符串/STL/图论/DP 等
4. **课时长度**（可选，默认 40 分钟）：40 / 45 / 60 分钟

> ⚠️ **重要**：确认输出目录（绝对路径），避免文件散落。推荐格式：`D:\课程资料\第XX课_知识点名\`

#### 步骤 2：生成 PPT

以 `assets/make_ppt.js` 为模板：
- 修改标题、主题色、关卡数量、内容文字
- 小学版用比喻（榨汁机=函数、盒子=变量、侦探=判断）
- 代码用 Consolas 字体 + `#0D1117` 深色背景
- 输出文件名加 `_v2` 避免覆盖已打开文件
- 运行：`node make_ppt.js`

#### 步骤 3：生成教案 + 任务单

以 `assets/make_docs.js` 为模板：
- 教案：目标/重难点/教学过程（逐分钟）/板书/评价量规
- 任务单：圈数 → 填空 → 补代码 → 追踪表 → 挑战题
- 运行：`node make_docs.js`

#### 步骤 4：生成代码示例

将课件中所有代码片段保存为 `.cpp`：
```javascript
const fs = require('fs');
fs.writeFileSync('代码示例.cpp', '\uFEFF' + content, 'utf8'); // UTF-8 BOM
```

#### 步骤 5：生成网页闯关游戏

以 `references/game_template.html` 为起点：
- 每关对应一个知识点，包含知识展示+交互题目
- 题型：选择题、判断题、填空题
- 功能：自动判对错、进度条、星级评价、通关彩纸动画
- 全部题答对才解锁下一关
- 单 HTML 文件，无需网络，双击即用

#### 步骤 6：整理文件夹

```powershell
# ⚠️ Windows 路径用双反斜杠或正斜杠，避免转义错误
$topic = "函数"
$dest = "D:\课程资料\$topic"
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Move-Item -Path ".\*.pptx", ".\*.docx", ".\*.cpp", ".\*.html" -Destination $dest
Write-Host "✅ 文件已整理到：$dest"
```

---

### 模式 B：批量 PDF → 全套课程资料

当用户提供**多个 PDF 教材文件**并要求批量生成时使用此模式。

#### 步骤 1：安装依赖

```powershell
# Python 依赖（PDF 提取）
python -m pip install pdfplumber

# Node.js 依赖（PPT/Word 生成）
npm install pptxgenjs docx
```

> **说明**：Windows 下优先使用 `python`，如提示命令不存在则改用 `python3`。Node.js 需 v16+，建议全局安装。

#### 步骤 2：创建目录结构

```powershell
# 示例：31课完整课程
$base = "C:\...\C++"
$courses = @("第00课_信息学竞赛介绍", "第01课_计算机中的数制", ...)
foreach ($c in $courses) {
  New-Item -ItemType Directory -Path "$base\$c" -Force | Out-Null
}
```

#### 步骤 3：批量提取 PDF 内容

使用 `scripts/extract_pdf_content.py` 提取所有 PDF 文本：

```powershell
# Windows 下使用 PowerShell 执行
python scripts/extract_pdf_content.py `
  --input_dir "E:\课程\信奥初级教程\" `
  --output "course_content.json"
```

脚本输出标准 JSON 格式，供后续生成脚本使用。参见 `references/course_schema.md` 了解 JSON 结构。

> ⚠️ 若 PDF 为扫描版（无文本层），pdfplumber 会返回空内容，需先用 OCR 工具处理（见常见问题）。

#### 步骤 4：批量生成 PPT

为每课分别运行 `make_ppt.js`（修改课程数据参数）：
- 以 `assets/make_ppt.js` 为模板，将课程数据参数化
- 每课输出到对应子文件夹：`第XX课_课题名/课题名_课件.pptx`

#### 步骤 5：批量生成教案 + 任务单

以 `assets/make_docs.js` 为模板，参数化课程数据：
- 每课输出：`第XX课_课题名/课题名_教案.docx` + `课题名_任务单.docx`

#### 步骤 6：批量生成网页闯关游戏

以 `references/game_template.html` 为基础，为每课生成独立 HTML 游戏：
- 每课输出：`第XX课_课题名/课题名_闯关游戏.html`
- 关卡数量与课程知识点数量对应（通常 5～9 关）

---

## 文件结构规范

批量生成后的目录结构：
```
C++/
├── 第00课_信息学竞赛介绍/
│   ├── 信息学竞赛介绍_课件.pptx
│   ├── 信息学竞赛介绍_教案.docx
│   ├── 信息学竞赛介绍_任务单.docx
│   ├── 信息学竞赛介绍_代码示例.cpp
│   └── 信息学竞赛介绍_闯关游戏.html
├── 第01课_计算机中的数制/
│   └── ...（同上）
└── ...（共31课）
```

---

## 参考资源

- `references/game_template.html`：网页闯关游戏完整模板（含所有 JS/CSS 逻辑）
- `references/course_schema.md`：PDF 内容提取后的 JSON 数据结构说明
- `references/素数判断讲解.md`：适合小学生的素数讲解（矩形法、排队游戏、√n 原理）
- `references/代码示例.cpp`：素数计数完整代码（慢/快方法对比 + Bug 分析）
- `assets/make_ppt.js`：PPT 生成脚本模板（pptxgenjs，小学游戏化风格）
- `assets/make_docs.js`：教案+任务单生成脚本模板（docx 库）
- `scripts/extract_pdf_content.py`：批量 PDF 文本提取脚本

---

## 技术栈

- **PPT 生成**：[pptxgenjs](https://gitbrent.github.io/PptxGenJS/)，`npm install pptxgenjs`
- **Word 生成**：[docx](https://docx.js.org/)，`npm install docx`
- **PDF 提取**：[pdfplumber](https://github.com/jsvine/pdfplumber)，`pip install pdfplumber`
- **网页游戏**：纯 HTML + CSS + JS，无框架，无外部依赖
- **运行环境**：Node.js（PPT/Word）+ Python（PDF 提取）
- **文件编码**：UTF-8 with BOM（Windows 中文兼容）

---

## 设计规范（小学版）

| 元素 | 规范 |
|------|------|
| 主色调 | 暖白底 `#FFFBF0` + 深蓝黑 `#1E293B` |
| 代码背景 | `#0D1117`（GitHub 暗色） |
| 关键词色 | 黄 `#D97706`（类型）、粉 `#DB2777`（关键字）、青 `#0891B2`（函数名） |
| 字体 | 正文：系统默认中文；代码：Consolas |
| 动效 | 静态为主；HTML 游戏可加星星弹出 + 彩纸动画 |
| 比喻风格 | 榨汁机（函数）、盒子（变量）、侦探（判断逻辑）、闯关（课程进度）|

## 设计规范（CSP 竞赛班）

| 元素 | 规范 |
|------|------|
| 主色调 | 深灰底 `#0F172A` + 亮白字 `#F1F5F9` |
| 强调色 | 科技蓝 `#3B82F6` + 橙 `#F59E0B` |
| 代码背景 | `#0D1117`，代码块尽量宽 |
| 内容密度 | 可适当提高信息密度，减少装饰性图案 |
| 比喻风格 | 减少卡通比喻，改用算法原理图示（流程图、树状图、状态转移图）|
| 动效 | 最小化，重点放在代码演示步骤动画 |

---

## 常见问题

**Q：运行 `node make_ppt.js` 报文件被占用？**  
A：输出文件名改为 `_v2.pptx`，避免覆盖已在 PowerPoint 打开的文件。

**Q：生成的文件打开中文乱码？**  
A：用 Node.js 写出时加 `'\uFEFF'` BOM 头，或在 VS Code 右下角手动选 UTF-8 编码。

**Q：pptxgenjs 出现颜色警告？**  
A：8 位 16 进制色码（含透明度）会警告，改用 6 位 + `transparency` 参数即可，不影响文件。

**Q：PDF 文本提取乱码或内容为空？**  
A：部分 PDF 为扫描图片，pdfplumber 无法直接提取文字。可用 PaddleOCR 处理：`pip install paddlepaddle paddleocr`，运行 OCR 后得到文本再提取。

**Q：批量生成 31 课 PPT 耗时太长？**  
A：先用 Python 批量提取并保存 `course_content.json`，再一次性运行 Node.js 批量脚本，避免逐课交互。估计耗时：31 课约 3～8 分钟（取决于磁盘速度）。

**Q：竞赛班课件需要算法流程图 / 树状图怎么处理？**  
A：可在课件 PPT 中插入 SVG 图或用 Mermaid 生成 PNG 后嵌入。目前脚本暂不自动生成算法图，需手动补充或由 AI 生成 Mermaid 代码后转图片。

**Q：如何为不同年级生成不同难度版本？**  
A：在 `make_ppt.js` 中加入 `grade` 参数（`primary` / `junior` / `csp`），根据参数切换文字风格、比喻密度和代码复杂度。
