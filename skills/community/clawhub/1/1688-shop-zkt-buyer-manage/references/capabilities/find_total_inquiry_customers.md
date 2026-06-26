# find_total_inquiry_customers

查询当前商家的全部询盘客户列表，支持多维度筛选（客户类型、跟进状态、昵称、标签、时间范围、采购金额、业务员、身份、活跃状态等），以 Markdown 表格形式展示买家昵称、身份、主营类目、近半年成交金额及采购次数。

## 前置条件

- 已配置 AK（未配置时会提示运行 `python3 {baseDir}/cli.py configure YOUR_AK`）
- 主账号 userId 由后端通过 AK 自动解析，无需传参

## 参数

| 参数 | 类型 | 必传 | 说明 |
|------|------|------|------|
| `buyerType` | string | 否 | `lostRiskType`-风险流失 / `wakeUpType`-商机唤醒 |
| `followUpStateList` | Array<string> | 否 | 跟进状态，最多5个 |
| `nickName` | string | 否 | 买家昵称，支持模糊查询 |
| `tagList` | Array<string> | 否 | 旺旺标签，最多5个 |
| `startTime` | string | 否 | 询盘开始时间，`yyyy-MM-dd HH:mm:ss` |
| `endTime` | string | 否 | 询盘截止时间，`yyyy-MM-dd HH:mm:ss` |
| `minPayAmt180d` | int | 否 | 近半年最小采购金额 |
| `maxPayAmt180d` | int | 否 | 近半年最大采购金额 |
| `lastSalesName` | string | 否 | 最近跟进业务员 |
| `identityList` | Array<string> | 否 | 买家身份，最多5个 |
| `isBuyerActive` | int | 否 | `1`-近30天活跃 |

> 所有参数均为可选。无参数时返回全量询盘客户。

## 返回字段

`data.data` 为买家数组，每个元素包含完整画像字段。表格中展示以下 6 项：

| 字段 | 类型 | 说明 |
|------|------|------|
| buyerId | string | 客户 ID（**下游能力批量调用的凭证**，类型为字符串，可能为加密格式，需原样收集后作为字符串数组传入 `--buyer-id-list`） |
| nickName | string | 买家昵称 |
| identity | string | 买家身份（如 超级买家） |
| followUpState | string | 跟进阶段 |
| mainCate | string | 买家主营类目 |
| payAmt180d | int | 近180天成交金额（近半年类目额） |
| payCnt180d | int | 近180天付款订单数（采购次数） |

## 典型用法

**场景 1：查看店铺全部询盘客户**

```bash
python3 {baseDir}/cli.py find_total_inquiry_customers
```

**场景 2：查询流失风险客户**

```bash
python3 {baseDir}/cli.py find_total_inquiry_customers --buyer-type lostRiskType
```

**场景 3：查询商机客户（商机/流失类型不支持时间筛选）**

```bash
python3 {baseDir}/cli.py find_total_inquiry_customers --buyer-type wakeUpType
```

> ⚠️ 当 `--buyer-type` 为 `wakeUpType` 或 `lostRiskType` 时，**强制不传** `--start-time` / `--end-time`，即使对话中包含时间表述也要省略。

**场景 4：查询昵称包含"张三"的活跃客户**

```bash
python3 {baseDir}/cli.py find_total_inquiry_customers \
  --nick-name 张三 \
  --is-buyer-active 1
```

**场景 5：查询采购金额在 5000~10000 的客户**

```bash
python3 {baseDir}/cli.py find_total_inquiry_customers \
  --min-pay-amt-180d 5000 \
  --max-pay-amt-180d 10000
```

## 展示规则

- 全部结果以 Markdown 表格直接展示，不设数量阈值
- 表格列：买家昵称 | 买家身份 | 跟进阶段 | 主采类目 | 近半年类目额 | 采购次数
- 空值统一展示为 `—`

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "# 查询结果\n\n共查询到 **N** 位客户：\n\n| 买家ID | 昵称 | ... |\n...",
  "data": { "total": 11, "data": [...] }
}
```

### 失败

```json
{
  "success": false,
  "markdown": "错误描述信息"
}
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `python3 {baseDir}/cli.py configure YOUR_AK` 配置 AK |
| 暂无询盘客户 | success=true，表格显示「暂无询盘客户数据」 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
