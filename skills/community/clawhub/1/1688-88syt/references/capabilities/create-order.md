# 创建采购单（create-order）

## CLI 调用

```bash
python3 {baseDir}/cli.py create-order --role BUYER --counterparty "对方1688登录名" --items '[{"productName":"商品","quantity":10,"unitPrice":"1.00","subtotal":"10"}]'
```

- `--role`: 必填，己方角色：`BUYER`（买家）或 `SELLER`（卖家）
- `--counterparty`: 必填，对方 1688 会员登录名 或者完整的 企业名称
- `--items`: 必填，采购清单 JSON 字符串，格式如：`[{"productName":"商品","quantity":10,"unitPrice":"1.00","productSpec":"件","subtotal":"10"}]`

## 功能

创建采购单（发起交易）,并自动完成采购单签署。

## 请求参数说明

采购单项字段：
- `productName`: 商品名称（必填）
- `quantity`: 商品数量（必填，整数，最小 1）
- `unitPrice`: 商品单价（必填，数字，最小 0.001 元）
- `productSpec`: 商品规格（必填）
- `subtotal`: 各商品小计 0.001 元, 等于`quantity`乘以 `unitPrice`）

**校验规则**：
- 对方登录名中的空格会被自动移除
- 各商品小计 = 数量 × 单价（保留三位小数）
- 总金额不能低于 0.01 元，为各商品小计之和

## 响应字段（业务含义）

- `data.success`：是否创建成功。
- `data.draftNo`：**采购单号**，创建成功后返回。
- `data.contractCurrentStatus`：创建后的合同状态。

- `data.draftNo`：**采购单号**，必须告知用户（可称「交易单号」）。
- 成功后务必再调 [contract-detail.md](contract-detail.md) 同步最新状态。

## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。
- 创建前须请用户**确认信息无误**（二次确认）。
