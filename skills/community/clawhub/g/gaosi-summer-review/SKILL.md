---
name: gaosi-summer-review
description: "Build a structured summer review plan for the 高思导引 (Gaosi Guide) competition-math series, grades 4-6, following its 7-module knowledge tree. This skill should be used when a user asks to create a 高思导引 / 小学数学暑假总复习 plan, a knowledge-tree-based review schedule, or a quantifiable daily 打卡表 (check-in sheet) with red/yellow/blue tier marking and PDF export. Trigger phrases include 高思导引总复习, 暑假总复习计划, 按知识树复习, 高思打卡表."
agent_created: true
---

# 高思导引 暑假总复习计划

为《高思学校竞赛数学导引》四~六年级制定基于横向「七大专题」知识树的暑假总复习计划，
并产出可打印 PDF + 每日量化打卡表。路线、知识点、分级规则均已固化，可直接复用。

## 何时使用

- 用户要求制定「高思导引 / 小学数学暑假总复习计划」。
- 用户提供 IMA 知识库里的《高思导引专题知识树.jpg》并要按图排复习。
- 用户要一张可量化的每日/每周打卡表（错误题号、正确率、二刷）。
- 触发词：高思导引总复习、暑假总复习、按知识树复习、高思打卡表。

## 知识树真值（单一信息源）

完整专题清单见 `references/knowledge-tree.md`（七/八模块 × 四/五/六各讲次、讲号、红黄蓝分级）。
关键约定：

- 高思导引 四/五/六 每册 **24 讲**，三册共 72 个知识讲（六年级第 24 讲为阅读收尾篇，不刷题）。
- 七大专题：计算 · 几何 · 应用题 · 计数 · 数论 · 数字谜 · 组合数学；**行程** 作为应用题核心专题单列。
- 分级：🔴 红（超越篇全做）= 计算/几何/应用题/行程/计数/数论/组合（含各自「综合类」）；🟡 黄（超越建议做）= 仅数字谜。
- 基线（不分级）：**兴趣篇 + 拓展篇 所有板块、所有讲必须全部写完**。

## 工作流

### 1. 取图（可选）
若用户提供 IMA 图片，按 `references/workflow.md` 阶段 0 取图。**注意 `fetch_media_content` 只返回 OCR 且识别不出专题名** —— 知识树一律以 `references/knowledge-tree.md` 的官方结构为准，图片仅作路线示意。

### 2. 组装计划
复制 `assets/plan-template.html` 到工作目录，按 `references/workflow.md` 阶段 1 调整（章节顺序、时间约定、分级贯穿）。模板已含完整 8 周路线、W1–W8 逐日表与打卡表，通常只需平移日期。

### 3. 打卡表
按 `references/workflow.md` 阶段 2 维护两张表：
- **4.1 每日量化（40 学习日）**：列含 兴趣/拓展/超越篇「错误题号」、当日正确率、二次强化、打卡✅。删冗余列（错误类型/错题订正/自评/家长签字）。
- **4.2 每周不足汇总**：本周正确率（周维度）、薄弱讲次、强化措施、周打卡。**周正确率 < 85% 的模块优先二刷**。
- 题量参考：兴趣篇≈10 / 拓展篇≈14 / 超越篇≈8 题。

### 4. 导出 PDF
```bash
python scripts/build_pdf.py <输入.html> <输出.PDF>
```
脚本自动探测 Edge/Chrome 无头打印。详见 `references/workflow.md` 阶段 3。

### 5. 交付与排障
用户报「打不开」时几乎总是打开方式问题，非内容损坏。按 `references/workflow.md` 阶段 4：
生成 **ASCII 文件名副本** + 起 `python -m http.server` 用浏览器 URL 打开，最稳。

## 文件清单

- `references/knowledge-tree.md` — 知识树真值表（模块/年级/讲次/分级），推理用。
- `references/workflow.md` — 详细操作步骤（取图、组装、打卡表、PDF、排障）。
- `assets/plan-template.html` — 已验证成品模板，复制后调日期即可。
- `scripts/build_pdf.py` — HTML→PDF 无头打印（自动探测浏览器）。
