# 采购单失效（invalidate-order）

> 命令为写入操作（高风险）；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py invalidate-order --draft-no 88SYT20260324419019
```

- `--draft-no`: 必填，采购单合同号

## 功能

将采购单标记为失效（作废/删除）。**高风险操作**，执行前须用户**二次确认**。

## 响应字段（业务含义）

- `data.success`：是否失效成功。
- `data.responseCode`：响应码，`SUCCESS` 表示成功。
- `data.responseMessage`：失败时的错误描述。

- 成功后再次调用 [contract-detail.md](contract-detail.md) 查询最新状态并反馈用户。


## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。
- **卖家需校验绑卡**，未绑卡则不能继续；**买家无需绑卡**。
- 执行前须请用户**明确确认**（二次确认）。
