---
name: custom-ai-pptx-generator
description: "Custom AI PPTX Generator — Design-driven, editable PowerPoint creation from your content. 可定制化AI 演示文稿（PPT）生成器 · 千题千境 (QianTi QianJing) AI-PPT workflow. This skill should be used when the user asks to create a PPT / presentation / training deck / project briefing / policy explainer from requirement notes, emails, tables or dictated content, and wants a PowerPoint-native editable deliverable (real native shapes and text boxes, not image-slab slides). Pipeline: content analysis → Design Intent Brief → structure confirmation → ASCII storyboard → visual prototype approval → native python-pptx rebuild → COM visual QA. 内容决定设计：先解析内容与设计意图，再经三轮用户确认（结构 / ASCII 草稿 / 样图），最终交付原生可编辑 PPTX 与逐页渲染图。"
license: MIT
version: 1.0.1
---

# 千题千境 AI-PPT v1.0 Baseline

## 定位与边界

本 skill 封装「千题千境」AI-PPT 工作流的**原始基线版本**（2026-09-12 ~ 09-14 三案例实战定版）。
**边界声明（重要）：**

- 本 skill 只按本文档的 5 步工作流执行，**不使用、不引用** M00-M08 模块化架构
  （`modules/00_design_direction_gate` ~ `modules/08_visual_qa`）、不使用 SlideSpec /
  Style DNA / Anti-Repetition 等新架构概念。
- 最终交付物必须为 **PowerPoint 原生可编辑对象**（原生形状 + 原生文本框），
  不做整页图片贴片。
- 触发场景：用户给需求文字 + 基本素材（图片 / 邮件 / 表格 / 口述），要求出 PPT。

完整知识底稿见 `references/千题千境_项目经验总结.md`（10 节：三案例复盘、
5 步工作流详解、python-pptx 坑全集、COM/PowerShell 环境坑、素材抠像、
排查方法论、用户硬规则、目录规范、可复用资产清单）。执行任何一步前，
先查阅该文档对应章节。

**验收状态：** 验收测试一（制度/流程说明类，SSC 口径）、验收测试二
（Employee Onboarding Journey，2026-09-15：Design Intent Brief 驱动 8 页全异构构图、
人物贴图第 2 步前置确认 + AI 圆形徽章素材椭圆嵌入、全流程零返工交付）均已通过，
覆盖「员工体验叙事类」与「制度说明类」两类典型场景。

## 标准工作流（5 步 + 1 个轻量设计意图步骤 + 交付自检）

```
① 需求文字+素材 → ①.5 Design Intent Brief（轻量，无确认节点）
  → ② 结构确认 → ③ ASCII 草稿确认 → ④ 终稿预览样图 → ⑤ 原生重建 PPTX → ⑥ 视觉自检交付
                                                      ↘ (不满意) 提示词交付兜底
```

**铁律：②③④ 三步各有用户确认节点，必须停下等用户拍板，不得自行批准推进。**
（①.5 Design Intent 是 AI 内部思考步骤，**不新增用户确认节点**，随②的结构稿一并呈现即可。）

### 第 1 步 · 需求收集与内容解析

- 从任意来源（图片、邮件 .eml、口述、表格）提取内容骨架：核心数字、分类、流程、结论。
- 把「数值 + 单位 + 口径」三元组写死在结构稿里（数字单位是高危区，单位错了整页就错）。
- 问清内部受众 vs 对外受众（决定细节保留度）。

### 第 1.5 步 · Design Intent Brief（轻量设计意图，无确认节点）

**定位：** 这不是 Style Engine、不是 Narrative Engine、不是 Template Library、不是 Design System。
它只是一段 concise 的 **Design Intent Brief**，让 AI 在画 ASCII 草稿之前先主动思考：
「这份 presentation 最适合如何被视觉表达？」——而不是直接套用过去成功过的 layout、
template 或 corporate PPT pattern。

**Brief 必须包含 6 项（纯文本，一段到底，控制在 ~150 字/项以内）：**

1. **Core Visual Idea** — 这份 presentation 最核心的视觉概念是什么？
2. **Audience Feeling** — 希望观众看到后产生什么感受？
   （如 trust / curiosity / urgency / clarity / inspiration / confidence）
3. **Visual Language** — 如 organic / editorial / cinematic / playful / structured /
   immersive / minimal / human-centered（≠颜色，只是视觉语言倾向）
4. **Preferred Visual Expressions** — 这份内容特别适合哪些视觉表达？
   （如 hero visual / diagram / timeline / journey / ecosystem / comparison /
   typography / metaphor / data visualization）
5. **Avoid** — 明确哪些视觉套路**不适合**当前内容；特别警惕因历史案例而自动重复相同 layout。
6. **Special Visual Opportunities** — 当前主题中有哪些可转化为视觉语言的独特元素？

**硬规则（A~H）：**

- A. **内容驱动设计**：不因过去做过某种 PPT 就默认重复使用。
- B. **不建立固定 page templates**。
- C. **Visual Language ≠ 颜色**（颜色仍由第 2 步用户拍板）。
- D. **不要求每页同一种视觉语言**：整体 style 可一致，但 individual slide
  expression 应根据内容变化。
- E. **不为视觉多样性破坏内容逻辑**。
- F. **不虚构数据或事实**。
- G. **用户已明确指定视觉要求时，必须优先使用用户要求**（Brief 相应项直接写「用户指定：…」）。
- H. **用户未指定视觉要求时，AI 主动提出设计方向，但不要求用户额外确认**。

**Token 效率铁律：** 本步骤必须轻量——不做多轮 design exploration、不生成多个完整
style alternatives、不生成图片、不生成 PPT、不重复 Content Analysis 已完成的分析。
**只输出一个 concise Design Intent Brief**，然后进入第 2 步。

### 第 2 步 · 结构确认（用户确认节点 #1）

必须让用户拍板四件事，缺一不可：

1. **页面结构**：横/竖版、页数、每页角色（封面/指标/分类/流程/结尾）
2. **主配色**：最好给色值（用户惯用色直接问）
3. **受众与细节粒度**
4. **人物/贴图元素**（2026-09-15 用户硬规则，Onboarding 案例教训：贴图需求
   若不在本步确认，到 ASCII 甚至样图阶段才冒出来，会返工）：**每次确认设计方向时
   必须主动问一句「是否需要人物/贴图元素？」**，且必须问清两个维度：
   - **素材来源**：用户上传（等传图后抠像摆位）/ AI 生成（统一风格插画）/
     只预留位置（占位框 + 尺寸标注，后续用户自行替换）
   - **使用范围与密度**：重点页使用（2~3 处）/ 全片轻量点缀（多数页面有但克制）/
     仅某一特定页

风格偏好必须显式确认：给出候选风格 + 每种「看起来是什么样」的白话描述让用户选，
**AI 不能默认替用户决定**，也不得默认裸排版。用户自定义的名字/文案是一等公民，
AI 只提供候选。

### 第 3 步 · ASCII 草稿确认（用户确认节点 #2）

- 用纯文本画出每页版式骨架（区块位置、层级、信息密度）。
- ASCII 草稿里**每一处文案写成最终定稿文字**，不写占位符——它是后续内容口径的合同。
- **必须显式读取并使用第 1.5 步的 Design Intent Brief**：每一页除 content / title / layout 外，
  还要标注两项（各一行短句即可，不展开成复杂 JSON）：
  - `visual expression:` — 本页采用 Brief 中哪种视觉表达（对应 Preferred Visual Expressions /
    Avoid 两项做取舍；整体 style 保持一致，individual expression 按内容变化）
  - `key visual idea:` — 本页的核心视觉想法是什么（一句话，对应 Core Visual Idea 在本页的落地）
  - 命中 Brief 的 **Avoid** 项的方案不得出现在草稿里。

### 第 4 步 · 终稿预览样图（用户确认节点 #3）

**输入继承（三层）：** Original Content（source of truth）+ Approved ASCII Storyboard
（已确认的结构/视觉规格）+ Design Intent Brief（设计意图）。
Visual Prototype **不得重新发明与已确认方向完全不同的设计**——样图是 ASCII 稿
（含每页 visual expression）的视觉落地，不是另起炉灶。

三条路径，按优先级：

| 路径 | 条件 | 说明 |
|---|---|---|
| A. hy-image-generation（混元生图 3.0） | 已配置 TENCENTCLOUD_SECRET_ID/KEY | 首选；密钥未配时路径空闲 |
| B. 内置 image_gen | 快速验证视觉走向 | 中文易出错字；样图仅用于确认视觉走向 |
| C. **提示词交付兜底（默认主路径）** | 用户对样图不满意 | **立即停止反复生成**，输出 N 个可复制提示词，用户去外部工具出图，回传后做原生重建 |

- 样图要做到 **8~9 成就是最终样子**（「终稿预览」而非「风格样图」）。
- image_gen 并行调用会撞输出文件名 → 每页素材独立 `output_dir`。
  **（2026-09-15 海洋案例补充：即使传了独立 output_dir，并行批次仍会把全部结果
  落进最后一个目录并互相覆盖——ImageGen 工具层会忽略并发调用的 output_dir。
  因此多图生成必须逐张串行调用；若已并行且部分文件被覆盖，先 Read 幸存文件
  逐张辨认是哪一页，再只补生成缺失页。）**
- **人物贴图素材（第 2 步已确认 AI 生成时）的工程化做法**（Onboarding 案例验证）：
  - 样图确认后**单独补生成**人物素材，不复用整页样图裁切（分辨率不够、构图不可控）；
  - 提示词统一用 **「Circular badge illustration, scene fills the entire circle」
    圆形徽章构图** + 严格 palette 限制 + 简洁面部（dot eyes）+ 圆润比例、无描边——
    圆形构图便于原生重建时椭圆裁切/椭圆底托摆位，与浅色页面底自然融合；
  - 生成 1024×1024，每张独立 `output_dir`（同前：并行撞名）。
- 提示词格式参照 `references/prompts/` 下三个范本：
  - `千题千境_单block提示词.txt` — 单 block 可复制版（含英文出图 + 中文对照）
  - `千题千境_6页提示词.md` — 6 页提示词包（Markdown 版）
  - `SSC自动化_单block提示词.txt` — 商务风 LEGO 黄+深蓝配色范本
- **回传样图必须逐张按内容核对映射，不能信文件名**（SSC 案例回传顺序与页序完全错位）。

**迭代修改规则（最小改动原则）：**

- **用户在 ASCII 阶段提修改** → 只更新受影响的页面/区块，**不重新运行**
  Content Analysis，也**不重新生成 Design Intent Brief**（除非内容本身变了）。
- **用户在 Visual Prototype 阶段提修改** → 优先修改该页的 visual expression，
  **不重新生成整个 presentation 的 design direction**。

### 第 5 步 · 原生重建可编辑 PPTX（python-pptx）

- 以样图为**视觉规格**、以已确认 ASCII 稿/原始材料为**内容口径**、以 Design Intent Brief
  为**设计意图参照**，全原生形状重建。
- 构建脚本结构（直接抄 `scripts/deck_ssc_v1.py` 或 `scripts/deck_qianti_v2.py` 骨架）：
  ```
  调色板常量 → helpers（S/box/para/set_font/conn/solid/bg）
  → 图标库（ic_*，统一签名 (slide,cx,cy,sz,col,bgc)，内细节用底色反白）
  → 每页一个 page*() 函数 → main 逐页构建 → 另存 ASCII 名渲染副本
  ```
- **内容口径决策**：外部出图工具几乎必然改写文案。原则 = 样图管「长什么样」，
  ASCII 稿管「写了什么」。交付时附差异对照表。
- 构建脚本同时**另存一份 ASCII 文件名渲染副本**（如 `deck_xxx_render.pptx`）——
  COM 打开中文路径会失败，全靠这份副本。
- 版式布局用英寸坐标硬编码（16:9 = 13.333×7.5），先算纵向层级再落码，避免压叠。
- **人物贴图嵌入**（Onboarding 案例验证）：AI 生成的圆形徽章素材在原生重建时用
  椭圆形状 + 图片填充（或等比裁切为圆）嵌入，外围可加一圈浅色底托椭圆增强融合感；
  贴图是点缀不是主角，尺寸克制（整页高度 1/5 ~ 1/4 以内），摆位避让正文区块。

### 第 6 步 · 视觉自检与交付

1. PowerPoint COM 打开渲染副本 → 逐页 `Export(png,'PNG',1920,1080)` → 逐张比对样图
   （导出脚本模板：`scripts/export_png_template.ps1`，改两个路径即用）
2. 修正 → 重建 → 复检（一般 2~3 轮）
3. 生成「样图↔成品对照表 + 口径差异说明」交付文档
4. 交付 PPTX + 说明 + 全部渲染图

## 用户协作硬规则（必须遵守）

1. **绝不静默覆盖制品**。同名再生成前必须先确认，或自动加版本后缀（`_v1`→`_v2`）；
   首版有缺陷也是移档留存（如 `draft0.pptx`），不是删除。
2. **样图不满意时不许反复生成 image_gen**，直接切「N 个可复制提示词 → 用户外部出图」
   兜底。触发词："差/不行/不好看/不太满意"。
3. **风格/配色/名字由用户拍板**，AI 只给候选 + 白话描述。
4. 交付时附：交付说明（页序映射、口径对照、视觉差异及理由）+ 全部渲染图。
5. 本项目的中间迭代不进长期记忆，统一沉淀进 skill 文档本身。

## 执行环境（Windows 本机）

- Python venv：`C:\Users\kenzj\.workbuddy\binaries\python\envs\ppt\Scripts\python.exe`
  （已装 python-pptx；中文输出加 `-X utf8` 并设 `PYTHONIOENCODING=utf-8` / `PYTHONUTF8=1`）
- PowerShell 执行 .ps1 必须用：
  `powershell -NoProfile -ExecutionPolicy Bypass -File <path>`
- .ps1 脚本内只写 ASCII 路径；中文路径用 ASCII 渲染副本 + 通配符定位。
- 不在命令里内联复杂 PowerShell（`$` 会被吞），一律写 .ps1 文件再跑。
- **COM 残留实例恢复（安全顺序，ClawHub T09 整改后）**：
  ① 首选预防——导出脚本用 `try/finally` 保证 `$pres.Close()` / `$app.Quit()`
  （`export_png_template.ps1` 已内置），不依赖事后清理；
  ② 仍有挂死实例时，**只终止本技能自己启动的那个实例**（能拿到 PID 就按 PID 终止；
  确认屏幕上没有用户打开的其他演示文稿时才可按进程名处理）；
  ③ **严禁无差别 `Get-Process POWERPNT | Stop-Process -Force`**——用户可能有
  未保存的无关演示文稿，强制终止会静默丢失数据；确需强制终止非本技能启动的
  进程前，必须先向用户说明未保存数据丢失风险并获得明确确认。

## 工具脚本清单（scripts/，全部为原始工作区脚本原样拷贝）

| 脚本 | 用途 |
|---|---|
| `deck_ssc_v1.py` | 构建器骨架范本（LEGO 黄+深蓝商务风，helpers + 10 图标函数） |
| `deck_qianti_v2.py` | 构建器骨架范本（童趣糖果色风） |
| `export_png_template.ps1` | COM 导出 PNG 模板（1920×1080；安全版：参数化输入、运行级输出目录、不删除既有文件、try/finally 清理 COM） |
| `bissect.py` | 增量变体二分（定位 XML 级损坏，PowerPoint 打不开时用） |
| `test_sync.py` / `test_sync2.py` | 同尺寸并列图标选型模板（候选并排 + 一轮导出定版） |
| `sample_ssc_colors.py` | 配色采样（从样图提取主色） |
| `cutout.py` | 素材抠像管线（alpha ramp + 水印擦除 + 绿边扩散，如需图片素材时） |

注：deck 骨架脚本**不含任何作者本机绝对路径**——输出目录默认在脚本旁 `output/`，
可用环境变量 `QIANTI_OUT` / `QIANTI_ASSETS` 覆盖；所有保存走 `safe_save_path()`
（已存在则自动 `_v2/_v3` 递增，**永不静默覆盖**，与用户协作硬规则 #1 一致）；
诊断脚本（test_sync* / bissect）输出到运行级目录，保留历史证据。复用时按新项目改写
输出文件名与内容即可。

## 排查方法论（出问题时按此姿势）

- **XML 级损坏**（PowerPoint 报 0x80070570 但 python-pptx/ZIP 校验正常）：
  dump `ppt/slides/slideN.xml` 查 `<a:avLst>` 重名 gd；再用 `bissect.py` 增量二分。
  两大已知根因：`<a:alpha val>` 单位是千分比（必须 `alpha*1000`）；
  `UP_DOWN_ARROW` 设 adjustment 会生成重复 adj1/adj2。
- **图标/小元素模糊**：按最终渲染尺寸写 `test_*.py` 同尺寸并列选型，一轮定版，
  不在主稿反复打补丁。
- **空 run / size=0 不合法**（Onboarding 案例 P5 卡片头部）：占位空段用
  `para_runs(tf, [("", 0, …)])` 会产出非法字号；改用 `parse_xml('<a:buNone/>')`
  挂到 `pPr` 的方案，不造空 run。
- **外部出图回传**：逐字段核对数值/单位/标签/日期/署名，产出差异对照表。

完整坑清单见 `references/千题千境_项目经验总结.md` 第三~六节。
