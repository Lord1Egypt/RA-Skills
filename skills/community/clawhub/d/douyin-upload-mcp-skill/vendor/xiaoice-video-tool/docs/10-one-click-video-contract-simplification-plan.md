# 精简对齐方案：以官方字段为主，收敛 One Click Video 对外契约

## Summary

当前版本确实偏冗。冗杂点不在“字段总数”，而在“混了三层心智”：

- 对外 create 输入用了自定义的 `prompt + options`
- 插件配置和 service 侧 provider 配置混在一起解释
- 一些 service 侧高级字段，如 `VIDEO_PROVIDER_MODEL_ID`、`VIDEO_PROVIDER_AUTH_HEADER`，进入了主路径，放大了理解成本

本次方案目标是：

- 对外 create 输入改为官方字段名优先
- `callbackUrl` 继续由服务端托管，不对外暴露为常规调用参数
- `get` 维持现状，继续用 `taskId`
- 插件配置只保留 `serviceBaseUrl`、`internalToken`、`requestTimeoutMs`
- XiaoIce provider 凭据明确归属 `video-task-service`，不再让 skill 或文档把它误导到插件配置里

## Key Changes

### 1. 收敛对外 create 契约到官方字段名

把 create 的公开输入改成：

- 必填：`topic`、`vhBizId`
- 可选：`title`、`content`、`materialList`、`ttsConf`、`aigcWatermark`
- 继续保留：`sessionId`、`traceId` 作为内部追踪元数据
- 不对外暴露：`callbackUrl`，仍由服务端根据当前运行配置自动生成
- 不再把 `prompt` 和 `options` 作为主契约；它们从公开文档、tool schema、skill 描述中移除，并作为已淘汰字段处理

实现上需要统一三层输入定义：

- `src/mcp/tool.js`
- `src/service/server.js`
- `adapters/openclaw-plugin/index.js`

对 provider 的映射改为“字段同名优先”：

- `topic -> topic`
- `title -> title`
- `content -> content`
- `materialList -> materialList`
- `ttsConf -> ttsConf`
- `aigcWatermark -> aigcWatermark`
- `vhBizId -> vhBizId`
- `callbackUrl` 继续由服务端注入
- `modelId` 继续只从 service 侧 runtime config 注入，不提升为对外 create 字段

### 2. 精简配置心智，只保留两层

把配置解释收敛成两层：

- 插件层
  - `serviceBaseUrl`
  - `internalToken`
  - `requestTimeoutMs`
- 服务层
  - `VIDEO_PROVIDER_API_BASE_URL`
  - `VIDEO_PROVIDER_API_KEY`
  - `VIDEO_PROVIDER_AUTH_HEADER`
  - `VIDEO_PROVIDER_VH_BIZ_ID`
  - `VIDEO_PROVIDER_MODEL_ID`（高级可选）

文档和 skill 明确写死这条规则：

- XiaoIce API key 不属于 `plugins.entries.one-click-video.config`
- 更换小冰 key 时，只改 service 侧配置，不改 plugin config
- `subscription-key` 不是另一把 key，只是当前环境要求的 header 名
- `VIDEO_PROVIDER_MODEL_ID` 与 `VIDEO_PROVIDER_VH_BIZ_ID` 语义不同，即使当前环境值相同，也不视为同一字段

这部分主要更新：

- `adapters/openclaw-plugin/skills/xiaoice-video/SKILL.md`
- `adapters/openclaw-plugin/README.md`
- `README.md`
- `docs/02-provider-api-mapping.md`

### 3. 把文档分成“最小必填”和“高级配置”两层

对团队文档按使用频率重写，不再把所有字段并列：

- 最小必填
  - `serviceBaseUrl`
  - `internalToken`
  - `VIDEO_PROVIDER_API_BASE_URL`
  - `VIDEO_PROVIDER_API_KEY`
  - `VIDEO_PROVIDER_AUTH_HEADER`
  - `VIDEO_PROVIDER_VH_BIZ_ID`
- 高级配置
  - `VIDEO_PROVIDER_MODEL_ID`
  - `VIDEO_PROVIDER_AUTH_SCHEME`
  - `requestTimeoutMs`
  - 重试相关字段
  - admin/callback token 解释

目标是同事第一次看文档时，只需要理解 6 个关键字段，其余折叠到进阶部分。

## Test Plan

- 工具 schema、插件 schema、MCP schema 统一接受官方 create 字段，不再把 `prompt/options` 作为公开输入
- create 校验要求：
  - 缺 `topic` 报错
  - 缺 `vhBizId` 报错
  - `materialList` 或 `ttsConf` 类型错误时报错
- provider 请求映射测试：
  - top-level 官方字段被原样映射到 provider payload
  - `callbackUrl` 仍由服务端生成
  - `VIDEO_PROVIDER_MODEL_ID` 非空时才注入 `modelId`
- `get` 回归测试：
  - `taskId` 查询行为保持不变
- skill 和文档行为测试：
  - 当用户询问“更换小冰 API key”时，skill 明确指向 service 侧配置，不再指向 plugin config
  - 当用户询问 plugin config 时，只提 `serviceBaseUrl`、`internalToken`、`requestTimeoutMs`

## Assumptions

- `get` 继续保留 `action=get + taskId`，不强行对齐到官方 create 文档风格
- `callbackUrl` 继续服务端托管，不对外开放为常规调用参数
- `topic + vhBizId` 作为新的 create 最小必填，优先保证当前可用性
- `VIDEO_PROVIDER_MODEL_ID` 保持 service 侧高级可选项，不进入对外 create 主路径
- `prompt/options` 视为旧接口并准备淘汰，不再作为公开契约继续维护
