# Chinese Trademark Search Skill / 中国商标查询 Skill

A public Skill for OpenClaw / ClawHub that connects to a proprietary trademark SaaS platform API, enabling users to search Chinese trademarks, browse results, view details, export data, check point balances, view modules, and get onboarding guidance. Currently deployed as a single region (mainland China, entry point `tm.zhengquai.com`); an overseas region is planned.

---

这是一个面向 OpenClaw / ClawHub 的公开 Skill，用于连接”自有商标 SaaS 平台 API”，帮助用户完成中国商标查询、详情查看、导出、点数检查、模块查看与绑定引导。

本 Skill 不直连上游商标数据商接口，也不要求用户提供上游账号密码。用户只需要配置自己在平台中的用户级 token。

---

> **Legal Disclaimer:** Trademark search results are for informational purposes only and do not constitute legal advice. Data may be delayed 1-7 days behind CNIPA. See [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md) for full details.
>
> **法律声明：** 商标查询结果仅供参考，不构成法律建议。数据可能滞后 CNIPA 1-7 天。详情请参阅 [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md)。

## 前置条件 / Prerequisites

**本 Skill 需要一个 https://tm.zhengquai.com 平台账号才能运行。** 它本身不含商标数据，
所有查询都转发给托管平台 API，由平台完成鉴权、扣点与上游数据访问。跑起来需要：

1. Node.js ≥ 18（仅用内置模块，无第三方依赖）
2. 在 https://tm.zhengquai.com/register 注册并创建组织
3. 在设置页生成 API Key（`tmu_` 前缀），配置为 `CHINA_TM_USER_TOKEN`
4. 新注册组织赠送 100 点体验点（90 天有效），足够完整体验查询 / 详情 / 导出

没有 API Key 时，除 `help` 外的所有命令都会返回 `ENV_MISSING`。

**This skill requires an account on https://tm.zhengquai.com.** It ships no trademark
data of its own — every command is forwarded to the hosted platform API, which handles
authentication, metering, and upstream data access. Without an API Key every command
except `help` returns `ENV_MISSING`.

## 适用场景

- 查询企业或个人名下商标（每次查询返回前 50 条结果，暂不支持翻页）
- 查看商标详情
- 发起导出任务
- 查看点数余额与能力限制
- 查看已开通增值模块
- 在未绑定时获取绑定说明

## 安装到 OpenClaw

可用任一方式安装：

1. 将整个 `chinese-trademark-search-skill/` 文件夹导入到 OpenClaw 的本地 Skill 目录
2. 或在 ClawHub 中上传 / 发布该 Skill 文件夹
3. 在 OpenClaw 中选择该 Skill，并确认运行命令为：

```bash
node {baseDir}/scripts/cli.mjs help
```

## 环境变量配置

在 OpenClaw 或宿主环境中配置以下变量：

### `CHINA_TM_PLATFORM_BASE_URL`

自有商标 SaaS 平台 API 基础地址：

```bash
CHINA_TM_PLATFORM_BASE_URL=https://tm.zhengquai.com
```

### `CHINA_TM_USER_TOKEN`

平台用户级 token，用于代表当前用户访问平台开放接口。

```bash
CHINA_TM_USER_TOKEN=tmu_xxx_your_user_token
```

### `CHINA_TM_TIMEOUT_MS`

请求超时时间，单位毫秒。建议 10000 到 30000。

```bash
CHINA_TM_TIMEOUT_MS=15000
```

### `CHINA_TM_SKILL_CHANNEL`

渠道标识。默认建议使用 `clawhub`。

```bash
CHINA_TM_SKILL_CHANNEL=clawhub
```

## 注册与绑定入口

平台入口统一为 `https://tm.zhengquai.com`（当前为单区域部署，中国大陆节点；海外节点在规划中）。三步完成绑定：

1. 访问 `https://tm.zhengquai.com/register` 注册账号并创建组织
2. 登录后在设置页 `https://tm.zhengquai.com/settings/api-keys` 生成 API Key（`tmu_` 前缀，仅创建时显示一次）
3. 配置环境变量：`CHINA_TM_USER_TOKEN`（填 API Key）与 `CHINA_TM_PLATFORM_BASE_URL=https://tm.zhengquai.com`

## 体验点说明

新注册组织赠送 100 点体验点，90 天有效。具体以平台实际返回为准。

## 点数规则

当前默认计费说明如下：

- 查询（每次）：1 点，返回前 50 条结果
- 翻页：暂不支持（每次查询固定返回第一页前 50 条；`--page` 大于 1 由 CLI 本地拒绝，不扣点也不发请求；`--pageSize` 已废弃）
- 详情（每条商标）：2 点（因需调用上游两次）；同一商标已购详情后再次查看不重复扣点
- 导出 1~10 条：1 点
- 导出 11~50 条：3 点
- 导出 51~100 条：5 点
- 导出 101 条及以上：10 点

计费可靠性：查询失败（上游异常）、详情上游失败、导出任务创建失败均自动退点；CLI 自动附带幂等请求头 `X-OC-Request-Id`，网络重试不会重复扣点。

点价：¥1 = 5 点（1 点 = ¥0.20）。点数不足时接口返回 HTTP 402，可前往充值页 `https://tm.zhengquai.com/billing` 充值。

使用前请以平台接口返回的实际计费提示为准。

## 增值模块

平台可能按模块授权控制部分能力。典型模块包括：

- 续展监控
- 通知提醒
- 微信端
- 公司页 / 客户页
- 外部监控
- 白牌门户

如接口返回模块未开通，请前往平台购买对应模块后再使用。

## 本 Skill 做什么

- 调用平台 `capabilities` 查看绑定、点数、能力状态
- 调用平台 `search` 执行商标查询
- 调用平台 `detail` 查看商标详情
- 调用平台 `export` 发起导出
- 调用平台 `modules` 查看模块能力
- 调用平台 `bind-help` 获取绑定指引

## 本 Skill 不做什么

- 不保存私有密钥
- 不连接上游商标数据商
- 不向用户索要上游账号密码
- 不伪造查询结果
- 不绕过平台点数或模块限制

## 运行示例

```bash
node scripts/cli.mjs help
node scripts/cli.mjs bind-help
node scripts/cli.mjs capabilities
node scripts/cli.mjs search --query "华源科技"
node scripts/cli.mjs detail --tmid "tm_20260310_0001"
node scripts/cli.mjs export --queryId "qry_20260310_0008" --tmids "tm_001,tm_002"
node scripts/cli.mjs export-status --jobId "exp_20260310_0003"
node scripts/cli.mjs modules
```

## 返回格式

CLI 统一输出 JSON 到标准输出，便于 OpenClaw 解析。

成功示例：

```json
{
  "success": true,
  "command": "search",
  "data": {
    "queryId": "qry_20260310_0008",
    "results": []
  }
}
```

失败示例：

```json
{
  "success": false,
  "error": {
    "code": "POINTS_NOT_ENOUGH",
    "message": "点数不足"
  }
}
```

---

## License / 许可证

本仓库的**源代码**以 [Apache License 2.0](LICENSE) 开源。三条边界请注意：

| 对象 | 适用条款 |
|---|---|
| 本仓库源代码（CLI、测试、文档） | Apache-2.0：可自由使用、修改、再分发，含明示专利授权 |
| 「争取」/「争取AI」/「争取商标监控」/ ZhengQu 等商号与商标 | **不在授权范围**（Apache-2.0 §6）。fork 后不得以暗示官方出品的方式命名，详见 [NOTICE](NOTICE) |
| 调用 `tm.zhengquai.com` 平台 API 及其返回的数据 | 另受 [API_TERMS_OF_USE.md](API_TERMS_OF_USE.md)，其中 API 数据与查询结果不得商业转售、再许可或再分发 |

一句话：**代码随便拿，名字和数据不随代码走。**

The source code in this repository is licensed under the [Apache License 2.0](LICENSE).
The license does **not** grant rights to the ZhengQu trade names, trademarks, or logos
(Apache-2.0 §6, see [NOTICE](NOTICE)), and use of the hosted platform API — including
the data it returns — is separately governed by [API_TERMS_OF_USE.md](API_TERMS_OF_USE.md).

## Legal and Compliance / 法律与合规

### Data Privacy / 数据隐私

This Skill is deployed globally and is subject to multiple data protection regimes. Please review the applicable notices:

- **GDPR (EU/EEA users):** [GDPR_COMPLIANCE.md](GDPR_COMPLIANCE.md) - Legal basis, data subject rights, cross-border transfer mechanisms (SCCs)
- **CCPA (California residents):** [CCPA_NOTICE.md](CCPA_NOTICE.md) - We do not sell personal information. Right to know, delete, and opt-out.

### Data Residency / 数据驻留

The platform currently operates a single-region deployment:

| Region | Entry Point | Data Location | Applicable Law |
|---|---|---|---|
| China Mainland | `tm.zhengquai.com` | Mainland China | PIPL |

An overseas region is planned but not yet available. See [DATA_RESIDENCY.md](DATA_RESIDENCY.md).

### Export Control Warning / 出口管制警告

This service is subject to US EAR and OFAC sanctions regulations. Use is prohibited from Iran, North Korea, Syria, Cuba, Crimea, and by SDN-listed parties. See [SANCTIONS_COMPLIANCE.md](SANCTIONS_COMPLIANCE.md).

### All Legal Documents / 所有法律文件

| Document | Description |
|---|---|
| [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md) | Legal disclaimer - informational use only / 法律声明 |
| [SANCTIONS_COMPLIANCE.md](SANCTIONS_COMPLIANCE.md) | Export control and sanctions compliance / 出口管制与制裁合规 |
| [DATA_RESIDENCY.md](DATA_RESIDENCY.md) | Data residency and regional architecture / 数据驻留 |
| [API_TERMS_OF_USE.md](API_TERMS_OF_USE.md) | API terms of use, rate limits, SLA / API 使用条款 |
| [GDPR_COMPLIANCE.md](GDPR_COMPLIANCE.md) | GDPR compliance notice / GDPR 合规声明 |
| [CCPA_NOTICE.md](CCPA_NOTICE.md) | California Consumer Privacy Act notice / CCPA 通知 |
| [TIMEZONE.md](TIMEZONE.md) | Timezone and date conventions / 时区与日期参考 |
| [PRICING.md](PRICING.md) | Points pricing and refund policy / 定价说明 |
| [SECURITY.md](SECURITY.md) | Security notice / 安全说明 |
