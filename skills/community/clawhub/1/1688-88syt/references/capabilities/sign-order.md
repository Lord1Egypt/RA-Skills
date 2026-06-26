# 采购单签署（sign-order）

> 命令为写入操作；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py sign-order --draft-no 88SYT20260323417003
```

- `--draft-no`: 必填，采购单号

## 功能

对采购单进行签署确认（用户口语中的「签署采购单」「确认采购单」「签约」等多指本能力）。

## 响应字段（业务含义）

- `data.success`：是否签署成功。
- `data.draftNo`：采购单号。
- `data.contractCurrentStatus`：签署后的状态摘要（已转换为中文）。

- 成功后再次调用 [contract-detail.md](contract-detail.md) 查询最新状态并反馈用户。

## 前置条件

- 须为 **主账号**，已 **签约**、已 **实名认证**。
