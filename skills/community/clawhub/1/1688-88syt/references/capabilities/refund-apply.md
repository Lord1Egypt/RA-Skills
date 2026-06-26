# 申请退款（refund-apply）

> 命令为写入操作（高风险）；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py refund-apply --draft-no 88SYT20260324419019
```

- `--draft-no`: 必填，采购单合同号

## 功能

**仅限买家**发起退款申请。**高风险操作**，执行前须用户**二次确认**。

## 响应字段（业务含义）

- `data.success`：是否申请成功。
- `data.result.responseCode`：响应码，`SUCCESS` 表示成功。
- `data.result.draftNo`：采购单号。
- `data.result.refundNo`：**退款申请单号**，申请成功后返回。

## 前置条件

- 须为 **主账号**，**已签约**、**已实名认证**。
- 申请退款仅限**买家操作**，无需校验绑卡状态。
- 执行前须请用户**明确确认**（二次确认）。
