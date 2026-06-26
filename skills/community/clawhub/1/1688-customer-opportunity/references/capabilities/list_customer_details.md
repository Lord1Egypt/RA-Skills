# list_customer_details

按人群类型查询客户列表，或指定买家 loginId 列表查询其客群信息（订单+询盘双维度）。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 主账号 userId 由后端通过 AK 自动解析，无需传参

## 两种使用模式

### 模式 1：按买家 loginId 查询客群信息（新）

```bash
python cli.py list_customer_details \
  --buyer-login-ids '["alice","bob"]' \
  --date-type RECENT_30
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--buyer-login-ids` | JSON 数组字符串 | 是 | 买家 loginId 列表，与 `--crowd-type` 二选一 |
| `--date-type` | string | 否 | RECENT_1/RECENT_7/RECENT_30（默认 RECENT_7）|
| `--page-no` | int | 否 | 页码（默认 1）|
| `--page-size` | int | 否 | 每页条数 1-50（默认 10）|
| `--stat-date` | string | 否 | YYYYMMDD（默认昨日）|

**返回结构：**

```json
{
  "order_list": [...],    // 订单维度客群信息
  "inquiry_list": [...],  // 询盘维度客群信息
  "unresolved_login_ids": [],
  "stat_date": "20260423",
  "date_type": "recent30"
}
```

每条 item 包含：`buyer_login_id` / `nick` / `buyer_credit_level` / `procurement_mode` / `if_ka` / `ord_cnt_1m_level` / `gmv_1m_level` / `lst_inq_time` / `inq_relation`

---

### 模式 2：按人群类型查询列表（原有）

```bash
python cli.py list_customer_details -t 流失买家 -d RECENT_7
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `-t/--crowd-type` | string | 否 | 流失买家/周期采购/询盘未成交/老客促活；**不传则返回全量老客列表** |
| `-d/--date-type` | string | 否 | RECENT_1/RECENT_7/RECENT_30（默认 RECENT_7）|
| `-p/--page-no` | int | 否 | 页码（默认 1）|
| `-s/--page-size` | int | 否 | 每页条数 1-50（默认 10）|
| `--stat-date` | string | 否 | YYYYMMDD（默认昨日）|

**返回结构：**

`data.list[]` 每条包含：`buyer_login_id` / `nick` / `buyer_credit_level` / `procurement_mode` / `if_ka` / `ord_cnt_1m_level` / `gmv_1m_level` / `lst_inq_time` / `inq_relation`

### 模式 2 全量拉取(新增)

```bash
python cli.py list_customer_details --crowd-type 流失买家 --date-type RECENT_30 --fetch-all
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `--fetch-all` | 开关 | 否 | 自动循环翻页(每页 50 条),直到 `has_next=false`,合并所有 list 后返回 |

**约束:**
- `--fetch-all` 与 `--buyer-login-ids` 互斥
- `--fetch-all` 时 `--page-no` / `--page-size` 由内部控制,用户传值无效
- 软保护:最多 50 页(2500 条),防上游异常死循环

**返回结构:** 与模式 2 一致,但:
- `list` 为合并后的全量结果
- `page_no=1`、`page_size=len(list)`、`has_next=false`

**典型场景:客户机会监控的 4 类细分直查**

| 场景 | 命令 |
|------|------|
| 流失客户预警 | `--crowd-type 流失买家 --date-type RECENT_30 --fetch-all` |
| 复购客户提醒 | `--crowd-type 周期采购 --date-type RECENT_30 --fetch-all` |
| 老客促活发现 | `--crowd-type 老客促活 --date-type RECENT_30 --fetch-all` |
| 询盘未成交 | `--crowd-type 询盘未成交 --date-type RECENT_30 --fetch-all` |

---

## 错误处理

| 情况 | 表现 |
|------|------|
| `--crowd-type` 和 `--buyer-login-ids` 都未传 | `❌ 参数错误：至少传一个` |
| `--buyer-login-ids` JSON 格式错误 | `❌ --buyer-login-ids JSON 解析失败` |
| `crowd_type` 不在枚举 | 参数错误提示 |
| 上游超时 | 服务错误，提示重试 |
| `--fetch-all` 与 `--buyer-login-ids` 同时使用 | `❌ 参数错误：--fetch-all 与 --buyer-login-ids 互斥（按买家 ID 查询本身不分页）` |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
