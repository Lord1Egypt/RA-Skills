# frontend-ui-pipeline

把模糊的 UI 想法变成可落地的前端工作流。

## 这是什么

`frontend-ui-pipeline` 是一个面向非前端用户、以工作流为核心的 UI Skill。它帮助用户把模糊的页面、产品或 App 想法，逐步转化为结构化的前端 brief、设计方向、构建计划、评审流程和下一轮迭代方案。

它不是单纯的设计生成器，也不是单纯的前端代码生成器，而是支持完整 UI 交付流程的 pipeline：

1. 澄清目标与用户需求
2. 定义策略、风格、布局和交互方向
3. 产出可执行的前端构建计划
4. 评审首轮 UI 结果
5. 将反馈转化为下一轮迭代

## 适合谁

- 创业者
- 产品经理
- 设计师
- 前端开发者
- 独立开发者
- 运营或业务人员
- 有 UI 想法、初稿或流程问题，但没有清晰下一步的人

## 何时使用

当你需要一个有步骤的 UI workflow 时使用，尤其适合：

- 把模糊的页面或产品想法整理成结构化前端 brief
- 在开始实现前定义策略、风格、布局和交互方向
- 把产品目标转成可执行的前端构建计划
- 评审一版早期 UI，并决定下一轮优先修改什么
- 用一条流程串起 brief → direction → build → review → iteration

## 何时不要使用

以下情况不建议使用：

- 任务是后端、API、数据库、基础设施或非视觉逻辑工作
- 已经有最终设计稿或完整 spec，只需要直接写前端代码
- 只做纯审查，不打算继续修改或构建
- 只是很小的视觉微调，不需要规划或迭代流程
- 单独使用某个专门 skill 更合适

## 可选 companion skills

为了获得更完整的体验，推荐与以下可选 companion skills 配合使用：

- `ui-ux-pro-max`：增强策略、风格与交互方向定义
- `frontend-design`：增强 UI 实现输出
- `web-design-guidelines`：增强审查、可访问性与 polish 评估

即使没有安装它们，`frontend-ui-pipeline` 仍然应该可以完成 brief、direction、build plan、review structure 和 iteration guidance，只是下游执行的专业度会弱一些。

当运行环境支持时，建议在路由到这些 skill 之前先检查它们是否已安装。
可参考 `references/guides/companion-skills.md` 查看 fallback 行为和推荐表述。

## 它能做什么

- 把模糊的 UI 想法整理成结构化前端 brief
- 帮助定义策略、风格、布局与交互方向
- 生成可实现的构建计划
- 将评审意见转化为下一轮迭代任务
- 当通过 skill 创建或修改前端文件时，生成或更新 `DESIGN.md` 记录当前设计方案
- 支持 Landing Page、SaaS Dashboard、Admin Panel、Mobile App 等典型场景

## 工作流阶段

- UI Brief
- Design Direction
- Build Plan
- Review Plan
- Iteration Plan

## 场景流程

- Landing Page
- SaaS Dashboard
- Admin Panel
- Mobile App

## 内置 references

### 核心模板
- `references/templates/ui-brief-template.md`
- `references/templates/design-direction-template.md`
- `references/templates/build-plan-template.md`
- `references/templates/review-plan-template.md`
- `references/templates/iteration-plan-template.md`
- `references/templates/design-record-template.md`

### 场景指南
- `references/pipelines/landing-page-pipeline.md`
- `references/pipelines/saas-dashboard-pipeline.md`
- `references/pipelines/admin-panel-pipeline.md`
- `references/pipelines/mobile-app-pipeline.md`

### Prompt 帮助
- `references/guides/prompt-help.md`

### Companion skill 指南
- `references/guides/companion-skills.md`

### 示例
- `examples/landing-page-brief.md`
- `examples/dashboard-build-plan.md`
- `examples/review-to-iteration.md`

## 最适合的使用场景

- “我有一个产品想法，但不知道页面怎么组织。”
- “帮我在写代码前先定义页面、结构和流程。”
- “把这个模糊想法变成前端构建计划。”
- “帮我评审这版 UI，并告诉我下一轮先改什么。”
- “帮我判断这版是只需要 polish，还是应该重做结构。”

## 示例调用

- “帮我把这个产品想法整理成 UI brief 和 build plan。”
- “我有一个 dashboard 概念，帮我定义结构、交互方向和下一步构建计划。”
- “评审这版 UI 初稿，找出最大问题，并给我下一轮 iteration plan。”
- “为这个产品规划一个 landing page workflow，并告诉我应该先做什么。”

## Companion skill 说明

如果你的环境支持 companion skills，建议同时具备：
- `ui-ux-pro-max`
- `frontend-design`
- `web-design-guidelines`

如果它们没有安装，这个 skill 仍然应继续完成流程引导，并输出当前阶段应有的主产物。

推荐组合方式：
- **只做规划：** `frontend-ui-pipeline`
- **策略 + 规划：** `frontend-ui-pipeline` + `ui-ux-pro-max`
- **规划 + 实现：** `frontend-ui-pipeline` + `frontend-design`
- **审查 + 迭代：** `web-design-guidelines` + `frontend-ui-pipeline`
- **完整交付闭环：** `frontend-ui-pipeline` → `ui-ux-pro-max` → `frontend-design` → `web-design-guidelines` → `frontend-ui-pipeline`

## 设计记录

当这个 skill 创建或修改前端文件时，应在项目根目录或功能根目录创建/更新 `DESIGN.md`。

`DESIGN.md` 用来记录当前设计方案：目标用户、核心目标、风格方向、布局、导航、组件、状态、响应式规则、可访问性决策、已使用或推荐的 companion skills、开放问题和下一轮 review focus。

## 一句话定位

一个以工作流为核心的 UI 规划与交付 Skill，适用于从想法、草稿到评审和迭代的前端流程。

## 版本说明

**当前版本：** v1.1.0

### 本次发布重点
- 稳定的工作流结构
- 面向典型场景的 UI pipelines
- 可复用的 brief / direction / build / review / iteration 模板
- 对非前端用户友好的 prompt 引导
