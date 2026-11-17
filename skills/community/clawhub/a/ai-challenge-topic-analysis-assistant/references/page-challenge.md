# 页面题（Vibe Coding）专属规则

当题目要求"可运行页面 / 原型 / 设计助手 / 看板 / 产品界面"时读本文件。非页面题（如测试用例、数据分析 SQL、运维告警等）无需遵循此处规范。

## 页面挑战流程差异

在通用 8 步骤之上，页面题的产物层要展开为：

1. `02-page-solution.md` 页面方案
2. `03-information-architecture.md` 信息架构（字段级契约）
3. `04-demo-data.json` 演示数据
4. `index.html` 可运行单文件页面（v1 → v2 → v3）
5. `05-ux-review.md` UX 走查
6. `06-judge-scorecard.md` 评委模拟打分

## 页面最小交互集（必须有）

- 列表/详情切换
- 筛选或搜索
- 状态更新（如"标记消解""代为通过"）
- ≥3 处 AI 模拟动作（每处有可视化反馈）
- 异常状态一键切换（Debug 面板）
- 双模式切换（评审/演示 或 编辑/预览）

## 技术栈红线

- 单文件 HTML + Tailwind CDN + 原生 JS
- 无外部 JS 库（除 Tailwind CDN）
- 无 emoji、无渐变、单强调色（推荐 `#F97316`）
- 图标一律内联 SVG（Heroicons 24 outline 风格）
- 中文字体栈，slate 中性色

## 页面质量红线

- 单文件、可直接双击打开、无脚本报错
- 至少 3 处 AI 按钮点击后有可视化反馈（打字机 / 骨架屏 / 进度条）
- 至少 4 种异常状态可切换
- 演示数据来自具体行业场景，不是"测试 1/测试 2"
- 视觉无渐变、无 emoji、单强调色
- 路演稿可在 3 分半钟内讲完（写完自己朗读计时）

## 页面 v1 分三次生成（不要一次让 AI 写 500 行）

1. **骨架**（5 min）：单文件 + Tailwind CDN + 深色左导航 + 顶栏 + 内容区
2. **模块渲染**（10 min）：5 模块的 render 函数 + `<template id="demo-data">` 内嵌 JSON
3. **AI 交互 + 异常态**（5 min）：3 个 AI 按钮的模拟交互 + 右下 Debug 面板切换 4 种异常态

### v1 骨架必须默认给上的三件事（别拖到 v3）

以下三条**放到 v1 骨架里成本几乎为零**，等 v3 再补则要大改代码/漏掉扣分：

- **`:focus-visible` 全局焦点环 + 常用 ARIA**：`.case-item / .api-head / .card` 这类 click 驱动的 div，在 v1 就带 `tabindex="0" role="button" aria-label="..."` + 全局 CSS `:focus-visible { outline: 2px solid #F97316; outline-offset: 2px }`。v3 补这个要挨个改 template，v1 顺手就能带上。
- **首屏自跑一条最戏剧的 case**：`boot()` 里 `setTimeout(() => runCase(FEATURED[0]), 800)`。目的：评委打开页面就看到彩色徽章、Judge 面板、告警条——而不是"选择用例开始执行"的空态（原则见 pitfalls.md 坑 5）。
- **`console.assert` 一致性 lint**：boot 时跑一次 demo-data 一致性检查（详见 pitfalls.md 坑 10），把 case name 和 payload 对不上的低级错误暴露出来。

## 交互深化 → v2（5–8 min）5 个必查点

1. **按钮反馈**：全局 button 加 120ms 过渡 + `:active` 下沉 1px + hover/active 三色
2. **模态可用性**：ESC 关闭 + 遮罩点击 + 打开后自动聚焦第一个可交互元素
3. **焦点管理**：`:focus-visible` 全局橙色 2px 环 + 自定义交互元素补 `tabindex="0"` + `role="button"` + `aria-label` + Enter/Space 触发
4. **移动端 375px**：`html/body { overflow-x: hidden }` 兜底 + 顶栏收窄 + Debug 面板/模态自适应视口
5. **空态引导**：跨模块通用空态 + "前往首模块 / 使用演示数据" 双 CTA

## v3 优化清单（拿高分的关键循环）

把评委扣分点和 UX Top 5 落到代码里：

1. AI 输出差异化：`DRAFT_VARIANTS` × N 角色 × 3 版本（详见 pitfalls.md 坑 4）
2. 置信度徽章：`.conf-badge` CSS + 4 处 AI 输出旁挂载
3. 演示模式差异化：深色渐变背景 + `.stat-big` 类 + 大数字看板（详见 pitfalls.md 坑 3）
4. 相似历史召回（或类似的记忆型 AI 能力）
5. 剪贴板 fallback 三级降级（详见 pitfalls.md 坑 2）
6. 首次欢迎横幅 + 降级模式持续横幅
7. 失败态错误码 + 追踪 ID
8. 补齐所有自定义交互元素的 ARIA（若 v1 骨架已默认给上，此处 double-check 遗漏点即可）
9. 移动端头像行 `grid grid-cols-2`
10. 语义 Judge 改造为"取最差"累加器（详见 pitfalls.md 坑 9）——一条 case 多点几次，输出应稳定而不是飘忽

**文件末尾追加 `<!-- v3 优化清单 -->` 注释**，让评委看代码时看到迭代过程。

同步更新 `05-ux-review.md`（Top 5 表格加"v3 状态"列）和 `06-judge-scorecard.md`（追加"优化后重估（v3 版本）"章节）。

## 演示数据（`04-demo-data.json`）真实感清单

- 需求原文 180–260 字，含具体金额（如"3.8 亿利息口径"）、具体系统名（如"T24 分期账户模块 v3.8"）、具体监管条款（如"银保监令 2020 年第 9 号"）
- 至少 5 条风险覆盖 4 种类型（歧义/遗漏/冲突/合规）
- 至少一条"戏剧转折点"数据（如某干系人 rejected，用于路演）
- 至少一条 `isAiDraft: true` 数据用于演示 AI 起草 + 人工确认协作
- 时间戳用绝对日期（`2026-08-01`），不要"下周"这种相对时间
- JSON 严格合法（末尾无逗号、字符串引号统一）
