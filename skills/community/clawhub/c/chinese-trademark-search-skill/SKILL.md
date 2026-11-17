---
name: chinese-trademark-search-skill
description: 连接中国商标查询托管平台 API，处理商标查询、详情、导出、点数与模块检查、绑定引导，适用于 OpenClaw / ClawHub 中通过本地 Node CLI 调用公开 Skill。
homepage: https://tm.zhengquai.com
metadata: {"skillKey":"chinese-trademark-search-skill","homepage":"https://tm.zhengquai.com","tags":["china","trademark","商标","search","openclaw","clawhub"]}
---

# 中国商标查询 Skill

本 Skill 用于在 OpenClaw / ClawHub 中连接“自有商标 SaaS 平台 API”，完成中国商标查询、详情查看、导出、模块查看、点数检查与绑定引导。

## 连接边界

- 本 Skill 只连接托管平台 API，不直连上游商标数据提供商。
- 不向用户索要上游商标接口账号密码。
- 用户只需要配置平台用户级 token。
- 若用户尚未绑定平台账号或组织，先引导绑定，再执行查询、详情、导出等动作。
- 不伪造商标数据；查不到就明确说明查不到。
- 优先摘要展示，避免一次输出过长。

## OpenClaw 调用方式

OpenClaw 应通过本地 Node CLI 调用本 Skill：

```bash
node {baseDir}/scripts/cli.mjs help
node {baseDir}/scripts/cli.mjs bind-help
node {baseDir}/scripts/cli.mjs capabilities
node {baseDir}/scripts/cli.mjs search --query "华源科技"
node {baseDir}/scripts/cli.mjs detail --tmid "tm_20260310_0001"
node {baseDir}/scripts/cli.mjs export --queryId "qry_20260310_0008" --tmids "tm_001,tm_002"
node {baseDir}/scripts/cli.mjs export-status --jobId "exp_20260310_0003"
node {baseDir}/scripts/cli.mjs modules
```

## 对话策略

### 1. 未绑定优先引导绑定

若 `capabilities`、`search`、`detail`、`export`、`modules` 任一响应表明用户未绑定：

- 先调用 `bind-help`
- 告诉用户绑定网址：`https://tm.zhengquai.com`
  - 注册页：`https://tm.zhengquai.com/register`
  - API Key 生成：登录后在设置页 `https://tm.zhengquai.com/settings/api-keys`（Key 为 `tmu_` 前缀，仅创建时显示一次）
- 告诉用户绑定步骤
- 告诉用户完成绑定后再继续执行查询或导出
- 不执行收费动作

### 2. 查询 / 详情 / 导出前先提示预计扣点

在发起收费动作前先提示用户：

- 查询前提示：预计消耗 1 点（返回前 50 条结果）
- 详情前提示：预计消耗 2 点（同一商标已购详情后再次查看不重复扣点）
- 导出前按条数提示预计扣点

导出预计扣点规则：

- 1~10 条：1 点
- 11~50 条：3 点
- 51~100 条：5 点
- 101 条及以上：10 点

翻页说明：**暂不支持翻页**。每次查询固定返回第一页前 50 条；`--page` 大于 1 由 CLI 本地直接拒绝（`PAGINATION_NOT_SUPPORTED`），不扣点也不产生请求。`--pageSize` 已废弃，平台固定 50。如用户要求翻页，请说明当前暂不支持，建议细化查询关键词。

体验点：新注册组织赠送 100 点体验点（90 天有效），具体余额以 `capabilities` 返回为准。

计费可靠性：查询失败（上游异常）会自动退点；详情上游失败会自动退点；导出任务创建失败会自动退点。CLI 已自动附带幂等请求头 `X-OC-Request-Id`，网络重试不会重复扣点；平台在退点时会释放该幂等键，所以退点之后再重试是会重新正常扣点的（不是免费重试）。

### 3. 点数不足时的处理

若平台返回点数不足（HTTP 402，错误码 `POINTS_NOT_ENOUGH`）：

- 明确说明“点数不足”
- 引导用户前往平台充值：402 响应中的 `rechargeUrl`（`https://tm.zhengquai.com/billing`）可直接给用户
- 不伪造结果
- 不重复重试收费接口

### 4. 模块未开通时的处理

若平台返回模块未开通：

- 明确说明具体模块名
- 引导用户购买对应模块
- 不绕过平台模块限制

涉及模块可能包括：

- 续展监控
- 通知提醒
- 微信端
- 公司页 / 客户页
- 外部监控
- 白牌门户

### 5. 输出风格

- 先给摘要，再给必要明细
- 查询结果过多时，优先展示前几条，并说明当前仅返回前 50 条、暂不支持翻页
- 导出任务优先展示任务状态、预计扣点、导出文件获取方式
- 对任何不确定的信息直接说明“以平台返回为准”

## 推荐工作流

### 查询

1. 必要时先 `capabilities`
2. 提示“预计消耗 1 点”
3. 执行 `search --query "<关键词>"`
4. 摘要展示结果与剩余点数（固定返回第一页前 50 条，暂不支持翻页）

### 详情

1. 提示“预计消耗 2 点”（同一商标已购详情后再次查看不重复扣点）
2. 执行 `detail --tmid "<tmid>"`
3. 返回商标名称、申请人、国际分类、申请号、注册号、状态、有效期等核心信息

### 导出

1. 先确认用户要导出的条数
2. 按条数提示预计扣点
3. 执行 `export --queryId "<queryId>" --tmids "<comma-separated>"`
4. 返回导出任务号、任务状态、预计或实际扣点
5. 如需查询导出状态，执行 `export-status --jobId "<exportJobId>"`（每次只查一次，不在 CLI 内轮询）
6. 若响应带 `pending: true`（状态为 `queued` / `processing`），稍后重新执行本命令；若为 `completed`，返回下载链接

### 模块 / 余额 / 能力

1. 执行 `capabilities` 或 `modules`
2. 说明余额、可用模块、受限动作
3. 若有未开通模块，明确指出模块名和用途
