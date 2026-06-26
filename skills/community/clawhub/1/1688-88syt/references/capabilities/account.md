# 查询用户账号状态（account）

> 命令为只读；依赖 AK 签名，无需额外 token。

## CLI 调用

```bash
python3 {baseDir}/cli.py account
```

- 无额外参数。


## 功能

判断当前用户是否为 **1688 主账号**，以及是否已 **签约协议**、**实名认证**、**绑定收款卡**。

## 典型触发场景
- “查看账号状态”

## 响应字段（业务含义）

- `data.success`：接口业务是否成功。
- `data.responseCode`：失败时的错误码；若为 **`NOT_1688_MAIN_ACCOUNT`**，表示**非 1688 主账号**，应引导用户使用主账号或前往网页端。
- `data.responseMessage`：失败原因（对用户转述为中文）。
- `data.hasSign`：是否已签署 88 生意通协议。
- `data.hasVerified`：是否已完成实名认证。
- `data.hasBoundCard`：是否已绑定收款银行卡。

## 主账号判断方法

1. 调用本接口；
2. 若返回表明非主账号（如 `NOT_1688_MAIN_ACCOUNT` 或业务失败说明为子账号），则**停止**技能内代操作，引导至带 `tracelog=88sytskill` 的 88 生意通页面。

## 签约 / 认证 / 绑卡未满足时

- **未签约**、**未认证**、**未绑卡**：不向用户展示接口细节，友善说明当前缺哪一步，并给出 [product-overview.md](../faq/product-overview.md) 中的网页入口链接（须含 `tracelog=88sytskill`），引导在浏览器完成。
