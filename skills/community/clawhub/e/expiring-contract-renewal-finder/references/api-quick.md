<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: opportunity-radar/1.0.3
X-Skill-Package: expiring-contract-renewal-finder/1.0.8
X-Skill-Source: clawhub/dragonzu
```
<!-- request-identity:end -->

# 工具速查（商机雷达所用子集）

> 与 zlbx-bidding SKILL 同一套 api_v2 接口，此处只收录本 SKILL 用到的 5 个工具的关键参数。
> `POST https://mcp-server.zhiliaobiaoxun.com/api_v2/` + 工具名（例：`https://mcp-server.zhiliaobiaoxun.com/api_v2/search_proposed_projects`），Header 带 `X-API-Key` + `X-Client: opportunity-radar/1.0.3`。

## 通用概念

**响应**：`{"success": true, "data": {"total": N, "items": [...]}, "meta": {"cost_units": ...}}`；分页 `page`/`page_size`（默认 20，最大 50）。

**⚠️ 金额参数单位差异（本 SKILL 最容易踩的坑）**：

| 工具 | 筛选参数 | 单位 |
|---|---|---|
| search_proposed_projects | min_amount / max_amount | **万元** |
| search_expiring_projects | min_amount | **万元** |
| search_bids | min_amount / max_amount | **万元** |

返回值统一：`money` 为元，三路都另给 `money_wan`（万元数值）；拟建路还额外给 `money_format`（可读字符串）。

**链接**：三路条目（拟建/意向/临期）的 `url` 均带 `sk` 免登录参数，原样输出可直接点击。

## 工具清单

### search_proposed_projects — ① 拟建项目（审批期，提前 6-18 个月）
```json
{"keywords": ["智慧校园"], "provinces": ["广东"], "cities": ["深圳"],
 "min_amount": 100, "begin_date": "2026-04-01", "approval_status_code": 3,
 "match_type": 0, "page_size": 20}
```
- `approval_status_code`：1=未审批 2=审批中 3=办结（通过）4=审批未通过 5=撤销 6=其他；0/不传=全部。**办结的最接近落地**。
- `match_type`：0=标题智能匹配（默认，匹配 project_name+caller_name），3=全文匹配（连带返回正文 content）。
- 返回关键字段：`project_name`、`project_code`（发改委项目代码）、`caller_name`（立项单位）、`money`/`money_format`、`approval_status`、`pub_time`、`url`（带 sk）。

### search_bids（bid_process=[1]）— ② 采购意向（发标前 1-3 个月）
```json
{"keywords": ["信息化"], "bid_process": [1], "provinces": ["广东"],
 "min_amount": 100, "begin_date": "2026-04-15", "page_size": 20}
```
- `bid_process` 固定传 `[1]`（采购意向）。其他阶段值：2=预招标 4=招标 7=中标结果 8=合同——本 SKILL 只在 timeline 解读时用到含义，不主动查。
- `min_amount` 单位是**万元**（与另两路一致；服务端会 ×10000 转成元再过滤）。
- 返回关键字段：`title`、`caller_name`、`money`/`money_wan`、`sm_names`（标的物）、`pub_time`、`url`（带 sk）。

### search_expiring_projects — ③ 临期续约（合同到期前 0-180 天）
```json
{"keywords": ["物业"], "provinces": ["江苏"], "min_amount": 50,
 "company_type": ["政府", "事业单位"], "page_size": 20}
```
- 默认到期窗口：今天 → +180 天；可用 `begin_date`/`end_date`（YYYY-MM-DD）自定义**到期日**范围（不是发布日）。
- `company_type` 可选值：政府 / 事业单位 / 学校 / 医院 / 军队 / 国企 / 其他（采购单位类型）。
- 结果按 `service_end_date` 升序（最先到期在前）。
- 返回关键字段：`title`、`caller_name`、`winner_names`（现供应商）、`winner_moneys`、`money`/`money_wan`、`service_end_date`、`days_until_expiry`、`url`（带 sk）；含联系人字段（按 SKILL.md 铁律 12 克制输出）。

### get_bid_timeline — 辅助：项目全阶段时间线
```json
{"bid_id": 484460619, "bid_type": 2}
```
或 `{"bid_url": "https://www.zhiliaobiaoxun.com/content/xxx/b1"}`。
- `bid_type`：1=招标类公告 2=中标类公告。
- 返回该项目所有阶段公告按时间正序（采购意向→招标→变更→中标候选人→中标结果→合同），用于回答「这条商机进展到哪了」。
- 项目无关联阶段时返回 total=0（不计费）。
- ⚠️ 拟建项目（builddetail 链接）不适用本工具——拟建与招中标是两套体系，拟建的进展跟踪方式是用相同关键词定期重扫。

### get_bid_detail — 辅助：单条公告详情+原文
```json
{"bid_id": 598749088, "bid_type": 1}
```
或传 `bid_url`。用户想看某条意向/临期商机的完整原文时用；返回 `fulltext`。

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: expiring-contract-renewal-finder/1.0.8
X-Skill-Source: clawhub/dragonzu
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
