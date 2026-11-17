---
name: competitive-analysis-board-report
description: This skill should be used when a user (typically an executive, GM office, or strategy team) needs a board-level competitive analysis and strategic decision report for their company — especially a Chinese enterprise in a traditional consumer / agricultural / food-manufacturing sector. It generates two aligned deliverables (a DOCX "decision-spine" deep report and a 14-slide board PPT) from public competitive intelligence gathered via WebSearch, following a fixed architecture — data base → competition insight (9-box benchmarking matrix) → strategic decisions (3 board resolutions) → continuous monitoring. Trigger phrases include "竞品分析", "董事会报告", "董事会汇报", "战略决策", "九宫格对标", "决策脊柱", "竞品情报", or any request to build or refresh a competitive-landscape deck/brief from public data.
version: 1.0.0
author: 戴康俊 <dkj@vip.163.com>
license: MIT-0
tags: [竞品分析, 董事会报告, 战略决策, 九宫格对标, 食品行业]
compatibility: WorkBuddy / OpenClaw
---

# 竞品分析 · 董事会决策报告生成器

把一次"全方位竞品分析"需求，落地为两份口径严格对齐的董事会交付物：

1. **DOCX《竞品分析总报告（决策脊柱版）》** —— 深度正文（数据底座 → 竞争洞察 → 战略决策 → 持续监测 → 附录），带 A/B/C 可信度标注、九宫格矩阵、勾稽校验。
2. **PPT《竞品分析与战略决策（董事会汇报版）》** —— 14 页，决策脊柱型结构，流式布局、零重叠零越界。

核心卖点：**决策脊柱 + 九宫格对标**。报告不堆数据，而是先给董事会"要拍板的 3 件事"，再用九宫格把"我们在哪儿、对手是谁、差距在哪"一次讲清，最后把洞察转成"三大战略动作 + DO/DON'T + 出手节奏"。

## 何时使用

- 用户要做"竞品分析 / 战略分析 / 董事会汇报 / 行业对标"，且对象是消费/农产/食品加工类企业。
- 用户已有或愿意提供：① 企业自身简介/年报/内部规划 PDF；② 允许用 WebSearch 抓公开竞品数据。
- 用户希望产出"可上会"的两份文件（一深一浅、口径一致），而不是一段聊天文字。

## 工作流（严格按顺序）

### 0. 前置：读懂"决策脊柱"四层
贯穿所有页面的骨架（详见 `references/methodology.md`）：
- **数据底座**：A/B/C 三级可信度标注 + 信号—证据—置信度三段式 + 羊只×单价↔营收勾稽。
- **竞争洞察（核心）**：对手地图四层 + 品牌榜 TOP10 + **九宫格对标矩阵（8 维度 × 4 梯队）**。
- **战略决策**：3 项董事会决议 + 三大战略动作 + DO/DON'T + 出手节奏。
- **持续监测**：竞品情报闭环机制。

### 1. 抓取公开数据（WebSearch）
- 优先 A 级：国家统计局、海关总署、农业农村部、上市公司年报、政府通稿。
- B/C 级：行业协会榜单（chinabgao 品牌榜）、华经产业研究院、人民网、竞品官网/电商页。
- 必抓：竞品营收/屠宰量/线上 GMV、品牌榜名次、出口资质、渠道绑定（巴奴/锅圈/胖东来等）、月度收入占比（淡旺季）。
- **勾稽校验（硬纪律，见 methodology 1.2）**：用 `营收 ÷ 屠宰只数 ≈ 元/只` 反推行业区间（活羊 1,540–1,850 / 屠宰端 2,000–2,500 / 全产业链 2,500–3,500 元/只），识别注水与口径冲突。

### 2. 拿企业官方资料做交叉验证（关键步骤，易漏）
- 若用户给了企业简介/年报/三年规划 PDF，用 fitz 提取文本，与报告逐项比对。
- 重点校正：合并口径营收序列、区域品牌份额、渠道野心（千店计划/店中店）、设计产能、资质、净利率。
- 如发现公开口径与官方冲突 → **以官方为准**，旧口径标注"作废"，并补一章"§2.6 企业内部规划交叉验证"，把"内部已认同的方向"作为战略背书。

### 3. 生成 DOCX（先写，作为口径基准）
- 用 `scripts/gen_report_v2.py` 为模板：复制到自己项目目录，**只改数据常量与正文字符串**，保持函数骨架。
- 跑 `python gen_report_v2.py` → 校验"段落数 / 表格数 / 图片数"打印正常。

### 4. 生成 PPT（与 DOCX 口径逐字对齐）
- 用 `scripts/gen_ppt_v3.py`：同样的 Page 流式引擎（见 `references/engine_notes.md`）。
- **铁律**：PPT 每一处战略表述必须与 DOCX 同句同词（决策项 ②③、动作二/三、DO/DON'T、出手节奏、结语、总纲口号）。

### 5. 校验（必跑，不可跳过）
- `python scripts/validate_ppt.py`：检查 ①旧战略表述残留 ②决策页旧口径 ③新表述覆盖 ④零越界 ⑤总页数。
- 对 DOCX 用一段 python 抽取正文+表格文本，grep 旧口径是否清空、新事实是否写入。
- 见 `references/methodology.md` 末尾的"校验清单"。

### 6. 交付
- `present_files` 同时交付 DOCX + PPT 两份。

## 关键工程纪律（踩过的坑）

1. **Edit 回退现象**：本会话中多次出现"Edit 返回 success，但再 Read 仍见旧串"。对策——**每个关键编辑后，用 Grep 在源文件确认旧串消失 + 重生成 + 再读产物文本确认生效**，不要只信 Edit 返回。
2. **零越界流式布局**：PPT 用 `Page` 类自增 `self.y`，`view()` 观点条用 `top=min(self.y+0.18, 6.98-h)` 防压页脚。任何新增内容必须走 `sec/bul/tbl/box/view`，**禁止手动画死坐标**，否则会越界或叠字。
3. **两份口径一致性**：任何战略调整（如用户说"②财税不合适、改成数字化"），**先改 DOCX 并校验通过，再同步 PPT 全部 6 个节（P2/P8/P9/P10/P11/P13）+ 封面 KPI + 总纲 banner**，最后跑 validate_ppt.py 确认旧词全清。
4. **数据可信度诚实标注**：非上市竞品无分渠道/分旺季财务数据，全文明示 A/B/C 级与局限，不为凑结论伪造精度。

## 依赖

- `python-pptx`（PPT 生成与校验）、`python-docx`（DOCX 生成）、`PyMuPDF (fitz)`（企业 PDF 提取）。
- 用受管 Python：`C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe`（已装 python-pptx / python-docx）；fitz 在 default venv 的 Scripts 下。

## 适配新公司的做法

脚本当前是"雨轩食品"实例（数据硬编码）。适配时：
- `gen_report_v2.py`：改顶部颜色常量、正文 `para/bullets/add_table` 内容、九宫格 `M` 矩阵、基础数据卡、对手地图四层、品牌榜表。
- `gen_ppt_v3.py`：改封面 KPI、对手地图/九宫格/品牌榜复函、P2–P13 文字、决策表。
- 复用三段式组件：`kpi_row / scale_bars / month_chart / two_col / matrix_9box / rival_map` 与 `Page.sec/bul/tbl/box/view/note/finish`。
- 把 `out =` / `CHART =` / `PATH =` 改成你项目目录（脚本已用 `os.path.dirname(__file__)` 做相对化，开箱可跑）。
