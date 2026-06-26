# 查询采购单列表（contract-list）

> 命令为只读；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py contract-list --role BUYER --page 1 --size 10
```

- `--role`: 必填，角色：`BUYER`（买家）或 `SELLER`（卖家）
- `--page`: 可选，页码，默认 1
- `--size`: 可选，每页条数，默认 10

## 功能

查询当前用户采购单列表（分页）。

## 响应字段（业务含义）

- `data.success`：接口业务是否成功。
- `data.responseCode`：失败时的错误码；若为 **`NOT_1688_MAIN_ACCOUNT`**，表示**非 1688 主账号**。
- `data.responseMessage`：失败原因（对用户转述为中文）。
- `data.totalCount`：总条数。
- `data.data`：采购单列表，每项包含：
  - `gmtCreate`：创建时间
  - `draftNo`：采购单号
  - `status`：状态（已转换为中文）
  - `drafterRole`：起草方角色（已转换为中文）
  - `sellerName`：卖家名称
  - `buyerName`：买家名称
  - `amount`：金额（元）

- 用表格呈现每条：`draftNo`（单号）、`status`（中文状态）、`drafterRole`（起草方角色中文）、`sellerName`、`buyerName`、**金额（元）**（字段名在响应中可能为 `amount`，以实际返回为准；若无则省略不编造）。
- `totalCount` 可简述总条数。
- 失败码 `NOT_1688_MAIN_ACCOUNT` 等按 [common-rules.md](../common/common-rules.md) 处理。

## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。

