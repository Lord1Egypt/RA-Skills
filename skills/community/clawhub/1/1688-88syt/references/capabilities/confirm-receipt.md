# 确认收货（confirm-receipt）

> 命令为写入操作（高风险）；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py confirm-receipt --draft-no 88SYT20260324419012
```

- `--draft-no`: 必填，采购单号

## 功能

买家确认收货。**高风险操作**，执行前须用户**二次确认**。

## 响应字段（业务含义）

- `data.success`：是否确认成功。
- `data.draftNo`：采购单号。

- 成功后再次调用 [contract-detail.md](contract-detail.md) 查询最新状态并反馈用户。


## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。
- 当前用户须为该单的 **买家** 角色。
- 执行前须请用户**明确确认**（二次确认）。
