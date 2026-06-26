# 拒绝签约（sign-reject）

> 命令为写入操作（高风险）；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py sign-reject --draft-no 88SYT20260324419018
```

- `--draft-no`: 必填，采购单合同号

## 功能

拒绝签署采购单。**高风险操作**，执行前须用户**二次确认**。

## 响应字段（业务含义）

- `data.success`：是否拒绝成功。
- `data.responseCode`：响应码，`SUCCESS` 表示成功。
- `data.draftNo`：采购单号。
- `data.contractCurrentStatus`：合同当前状态（已转换为中文）：
  - `SIGN_INIT`：签署初始化
  - `AUTHING`：核身中
  - `SIGNING`：签署中
  - `SIGN_SUCCESS`：签署成功
  - `SIGN_FAIL`：签署失败
  - `SIGN_EXPIRED`：签署过期

- 成功后再次调用 [contract-detail.md](contract-detail.md) 查询最新状态并反馈用户。


## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。
- **卖家需校验绑卡**，未绑卡则不能继续；**买家无需绑卡**。
- 执行前须请用户**明确确认**（二次确认）。
