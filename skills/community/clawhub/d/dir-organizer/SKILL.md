---
name: dir-organizer
description: 文件夹整理器 — 按扩展名把杂乱目录归类到 图片/文档/表格/音视频/压缩包/代码/其他 子目录，默认预览 --apply 才移动（零依赖） 适用场景：当需要文件夹整理器能力时使用本技能；触发词：dir-organizer。
slug: dir-organizer
version: 1.0.5
display_name: 文件夹整理器
display_name_en: Directory Organizer
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
read_when:
  - 一个文件夹里扩展名混杂、想批量归类到 图片/文档/表格/音视频/压缩包/代码/其他
  - 桌面/下载夹/项目目录乱，想先预览整理方案、确认不误移关键文件再动手
  - 要一条命令完成日常文件整理（默认 dry-run，--apply 才真移动）
  - 用户说「整理一下这个文件夹」「把文件按类型分好」
description_zh: "文件夹整理器 — 按扩展名把杂乱目录归类到 图片/文档/表格/音视频/压缩包/代码/其他 子目录，默认预览 --apply 才移动（零依赖）"
description_en: "Sort messy folders by extension into images, docs, sheets, audio-video, archives, code and other; preview by default, --apply to move (zero-dependency)."
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [dir-organizer, 效率工具]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/dir_organizer.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.5: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
Use this skill when a directory holds a mix of file extensions with no clear classification logic, making everyday lookup or batch processing slow. It fits project setup, document archiving and desktop cleanup — any moment where media, documents and code files need to be standardized into categories before bulk work. It is especially suited to the safe workflow of validating the plan (e.g. making sure key files are not moved by mistake) before any real change is executed.

### Usage
The core command is `dir-organizer`. It acts on the current working directory by default; parameters let you point at a target path or pick a behavior mode. Key parameters: `--preview` produces a classification report without moving anything; `--apply` performs the actual migration into the preset subdirectories. Under the hood the skill wraps the `dir_organizer.py` script, so no extra Python installation is required to run the organizing logic.

### Workflow
Step 1: confirm the target folder path and enter it, making sure it holds the mixed file set to be sorted. Step 2: run the command without the move flag to analyze it, and read the generated classification statistics and suggested directory structure. Step 3: manually check the preview report — verify that the categorization rules match expectations, especially the matching of audio/video and archive types. Step 4: run the command with `--apply` to trigger the internal Python script's actual rename-and-move flow. Step 5: inspect the subfolders under the root and confirm every target file has landed in the right type container with nothing left behind.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.5
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
本技能适用于文件目录内混杂多种扩展名且缺乏清晰分类逻辑，导致日常检索或批量处理效率低下时。当用户处于项目初始化、资料归档或桌面清理等阶段，需要批量将媒体、文档及代码文件进行标准化归类前使用。此外，该技能特别适合希望先验证整理方案准确性（例如确保不会误移动关键文件）再执行实际变更的安全需求场景。

### 用法
核心调用命令为 `dir-organizer`，默认作用于当前工作目录，支持通过参数指定目标路径或行为模式。主要参数包括 `--preview` 用于生成分类报告而不移动文件，以及 `--apply` 用于直接执行文件迁移操作至预设子目录。技能底层封装了 `dir_organizer.py` 脚本逻辑，无需用户额外安装 Python 环境即可直接执行内部整理功能。

### 流程
第一步：确认目标文件夹路径并进入该目录，确保其中包含需整理的混合文件集合。第二步：使用不带移动参数的命令运行分析，查看系统生成的分类统计及建议的目录结构。第三步：人工核对预览报告中文件归类规则是否符合预期，特别是音视频、压缩包等类型的匹配度。第四步：执行带 `--apply` 参数的指令，触发内部 Python 脚本启动实际的文件重命名与移动流程。第五步：进入根目录检查子文件夹状态，确认所有目标文件已无遗漏地归位至对应类型容器内。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.5
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
