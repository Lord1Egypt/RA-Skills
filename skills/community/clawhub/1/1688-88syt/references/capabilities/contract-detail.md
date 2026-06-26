# 查询采购单详情（contract-detail）

## CLI 调用

```bash
python3 {baseDir}/cli.py contract-detail --draft-no 88SYT20251125036067
```

- `--draft-no`: 必填，采购单号（88SYT 开头）

## 功能

根据采购单号查询当前详情。

## 响应字段（业务含义）

- `data.success`：接口业务是否成功。
- `data.responseCode`：失败时的错误码；若为 **`NOT_1688_MAIN_ACCOUNT`**，表示**非 1688 主账号**。
- `data.responseMessage`：失败原因（对用户转述为中文）。
- `data.contract`：采购单详情，包含：
  - `draftNo`：采购单号
  - `gmtCreate`: 创建时间
  - `status`：主状态（已转换为中文）
  - `drafterRole`：起草方角色（已转换为中文）
  - `drafterType`：起草方类型（个人/企业）
  - `buyerType` / `sellerType`：买家/卖家类型（个人/企业）
  - `buyerName` / `sellerName`：买卖双方展示名
  - `amount`：金额（元）

## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。
