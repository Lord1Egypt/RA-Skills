---
name: caixu-skill
description: "Asset Library Skill. Use when the user expresses the overall end-to-end intent in one request, including “把这些材料建成资产库”“列出未来 60 天需要续办或补办的事项”“生成暑期实习申请材料包”, when the user wants to search materials by natural language but is unsure whether the local retrieval environment is ready, when the user is unsure which phase skill to run, or when the environment may not be installed yet. This skill routes only to the current child skill, sends first-time installation agents to references/install.md when keys, retrieval config, or runtime setup are missing, explains stage boundaries and next steps, and does not directly call MCP tools, extract files, build packages, or submit forms."
---

# Asset Library Skill

在用户把整条主线一次性说出来，或还不确定应该先跑哪个阶段 skill 时，先使用这个主入口 skill。

## Quick flow

1. 判断用户是在说整条主线，还是已经明确到某个阶段
2. 选择当前最小必要的子 skill
3. 说明当前阶段边界、缺失输入和下一步

## Read next only when needed

- 首次安装、缺 key、缺 MCP 注册、或不确定环境是否已就绪时，先读 [references/install.md](references/install.md)
- 用户希望用自然语言查材料、找“可用于某目标的材料”，或明确想找“相似/相关材料”但不确定检索增强是否已就绪时，先读 [references/install.md](references/install.md)
- 要确认整条主线的触发词和阶段顺序时，读 [references/workflow.md](references/workflow.md)
- 要确认子 skill route id 与阶段交接字段时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 遇到缺输入、阶段不明或前置条件不足时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- 不直接调用 MCP tools
- 只路由到默认 MVP 子 skill：`ingest-materials`、`build-asset-library`、`maintain-asset-library`、`query-assets`、`check-lifecycle`、`build-package`
- `submit-demo` 是高级可选扩展，不属于默认 route

## Required input

- 用户当前意图
- 当前可用事实：本地文件路径、`library_id`、`goal`、`package_plan_id` 或 `package_id`

## Workflow

1. 如果用户表达整条主线，或没有明确自己处在哪个阶段，先使用 `caixu-skill`。
2. 如果这是第一次安装，或当前缺 key、缺 profile、缺 MCP/skills 注册，先读 `references/install.md`，引导完成安装和验活。
3. 如果用户想做自然语言材料检索或显式要求语义扩展检索，且本地检索增强是否可用不明确，也先读 `references/install.md`，确认 embedding 配置和旧库索引是否已完成。
4. 环境就绪后，再区分当前是 raw materials ingest、资产建库、资产维护、资产查询、生命周期判断，还是打包导出。
5. 一次只选择一个当前阶段子 skill，不在这里展开整条流水线执行。
6. 返回当前阶段边界、最小缺失输入，以及一个短名 `next_recommended_skill`。
7. 路由完成后停止；后续执行责任属于对应子 skill。
8. 如果用户明确要求外部演示页自动提交，再说明这是高级可选扩展，并引导查看扩展文档或手动启用 `submit-demo`。

## Guardrails

- 不直接调用 MCP tools、OCR、SQLite、docgen 或浏览器动作。
- 不把多个子 skill 串在同一次执行里。
- 用户已经明确要求某个阶段时，不要强行改成整条主线。
- 从 raw materials 开始时，不要跳过必须阶段。
- 第一次安装或环境未就绪时，不要假装已经可运行；必须先引导到 `references/install.md`。
- 检索增强环境或旧库索引状态不明确时，不要假装语义检索一定可用；先引导检查 `references/install.md`。
- 不要改写子 skill 的输入输出契约。
