# Changelog

All notable changes to this project will be documented in this file.

## [1.3.2] - 2026-04-17

### Fixed
- config.json 补齐顶层 `env` 和 `security.contact` 声明，消除"元数据缺少 env"审查提示
- config.json name 字段修正为正确 slug `a2amarket-agent`
- setup.md 修正 webhook 描述：明确 Skill 不会自动注册 webhook，需用户主动配置
- setup.md MCP Server 方案增加 npx 外部代码执行风险提示
- setup.md API 数量描述从 10 更正为 17

## [1.3.1] - 2026-04-17

### Added
- 新增"安全与隐私"章节，明确 Skill 行为边界
  - 声明不会自动注册账号或生成凭证
  - Webhook 仅在用户明确要求时配置，设置前需用户确认
  - 寻源时间线（agent_thinking）仅用户主动查询时返回
  - 建议首次使用低余额 Key 验证行为
  - 所有写操作均为用户显式触发，无后台静默操作

### Fixed
- 修复 ClawHub 安全审查提出的 5 项信任与透明度问题

## [1.3.0] - 2026-04-17

### Added
- API 从 10 个扩展到 17 个核心端点
- 新增 `GET /intents/{id}/sourcing/timeline` — 寻源时间线（Agent 每步思考过程）
- 新增 `GET /intents/{id}/negotiations` — 议价交流记录
- 新增 `GET /intents/{id}/events` — 完整事件流
- 新增 `POST /supply-declarations` — 声明供给能力
- 新增 `POST /subscriptions` — 订阅感兴趣的品类
- 新增 `GET /supply-products` — 查看我的供给列表
- 新增 `DELETE /intents/{id}` — 撤回采购意图
- 新增 `GET /intents/{id}/sourcing` — 寻源状态概览

### Changed
- 买卖同源叙事重构：不分买卖只分场景，同一个身份可以同时采购和供给
- Skill 描述和触发词全面更新，覆盖买卖双侧场景
- examples.md 重写为"小明的完整交易日"端到端示例

### Fixed
- 修复路径错误：`/supply/products` → `/supply-products`（P0，之前导致 Agent 调用 404）
- 修复触发词覆盖不足：「发布商品」不再被误识别为采购意图
- 修复 API 数量不一致：SKILL.md 声称数量与 reference.md 实际端点数对齐
- 修复供给声明数据库表结构缺失字段（owner_user_id 等 10 个字段）

## [1.2.1] - 2026-04-16

### Fixed
- 修复 SKILL.md frontmatter YAML 缩进错误，metadata/requires/env 现在能被 ClawHub 正确解析
- 修复 homepage 字段格式（markdown 链接 → 纯 URL）
- "隐藏 API 活动"措辞改为透明化表述：默认用自然语言汇报结果，用户要求时如实提供技术细节
- 明确 API Key 必须由用户自行获取，Agent 不会自动注册或生成凭证
- setup.md 同步修正"自动注册"描述

## [1.2.0] - 2026-04-16

### Added

- 新增 Agent Behavior 行为指令区块（角色定义 / 首次激活 / 意图识别 / 异步处理 / 结果呈现）
- AI 安装 Skill 后会主动自我介绍、展示官网和开发者平台、汇报余额并引导用户
- 核心能力各子标题增加触发条件说明
- 异步通知机制增加环境自动判断指令

### Changed

- "三步上手" 改为 "快速验证"，措辞从被动改为主动执行
- 整体文档语气从"技术文档"转为"AI 行为指令"

## [1.1.0] - 2026-04-15

### Changed

- 移除议价能力（`POST /negotiations`、`GET /negotiations/{code}`、offers/accept/reject），议价由平台自动处理
- 新增 `GET /supply/products` — 查看我的供给列表
- 新增 `PUT /agents/me` — 更新 Agent 配置（Webhook 等）
- API 清单从混合能力收缩为 10 个核心 API
- examples.md 移除幽灵 API（`POST /supply/subscriptions`、`GET /agents/mine`）
- examples.md 去角色化（"卖家声明供给" → "声明供给"）
- setup.md 明确 MCP Server 为独立方案，非 Skill 依赖
- reference.md 重新编号，统一邮箱验证路径为 `/agents/verify-email`

### Added

- README.md — 仓库说明
- CHANGELOG.md — 变更日志
- LICENSE — MIT 许可证

### Fixed

- SKILL.md 核心 API 表格编号修正

## [1.0.0] - 2026-04-14

### Added

- 从 `a2amarket-mcp-server` 仓库解耦，独立仓库
- SKILL.md — 主 Skill 文件（OpenClaw/ClawHub 格式）
  - 10 个核心 REST API（发布意图/查看意图/查看匹配/声明供给/通知/注册/余额）
  - 异步通知双模式（Webhook 推送 + 轮询拉取）
  - 买卖同源（无 agent_type 区分）
  - 纯 REST curl 调用，不依赖 MCP Server
- reference.md — 完整 API 参数说明
- examples.md — 5 个端到端使用示例
- setup.md — 4 种安装方式（OpenClaw/Cursor/自建/SSE）
- .clawhub/config.json — ClawHub 发布配置

### 版本对应关系

本仓库从 `@hz-abyssal-heart/a2amarket-mcp-server` v0.3.6 时期解耦独立。
MCP Server 继续维护 47 个 MCP Tools，本仓库维护 10 个核心 REST API。
两者共享同一套 ACAP REST API，独立版本号，独立迭代。