---
name: alipay-open-platform-keys
description: >-
  支付宝开放平台 RSA2 密钥：用 scripts/generate_alipay_rsa2_keys.sh（OpenSSL）生成公钥模式密钥对或证书模式 CSR；控制台绑定与支付宝公钥配置为必需外部步骤。
  说明应用私钥/支付宝公钥职责、公钥与证书模式差异、验签排查要点。详见 SKILL 正文与 reference.md（依赖检查、报错表、官方文档链接）。
---

# 支付宝开放平台密钥（RSA2）

## 本 Skill 做什么

用 **`scripts/generate_alipay_rsa2_keys.sh`** + [reference.md](reference.md) 完成 **本地生成 → 控制台上传公钥或 CSR → 配置 env/SDK → 加签与回调验签**；**不依赖**桌面密钥工具或 MCP。必须在 [开放平台](https://open.alipay.com) **开发信息** 中完成 **应用侧密钥或证书配置**，并获取 **支付宝公钥/证书**（业务步骤，非脚本可代替）。

**脚本用法**：在仓库中路径一般为 `skills/alipay-open-platform-keys/scripts/generate_alipay_rsa2_keys.sh`。公钥模式直接执行；证书模式加 **`--cert`** 与 **`--subj`**（或 `ALIPAY_CSR_SUBJ`）。完整参数执行 **`bash …/generate_alipay_rsa2_keys.sh --help`**。

**公私钥是否成对**：用同目录下 **`scripts/verify_alipay_rsa2_keypair.sh`**（`bash …/verify_alipay_rsa2_keypair.sh <私钥.pem> <公钥.pem>`，顺序可互换）；或代码中调用项目里的 **`alipay_rsa2.rsa_keys_match`**。见下方 Agent 约束，**默认由用户在本地执行**，避免私钥进入对话上下文。

## 闭环边界

| 环节 | 是否依赖 Skill 外 |
|------|-------------------|
| 生成密钥/CSR（脚本 + OpenSSL） | 否 |
| 控制台上传、下载平台证书 | 是 |
| 网关权限、产品签约 | 是 |

执行前确认 **`openssl` 可用**（见 [reference.md](reference.md)）。脚本**不需要** Python。

## 何时用

- 生成或轮换 RSA2 密钥、区分公钥/证书模式、排查验签与密钥不匹配。

## 流程要点

**公钥模式**：脚本产出私钥 + 公钥 PEM → 控制台上传应用公钥 → 保存支付宝公钥用于验签。

**证书模式**：`--cert` 产出私钥 + **`app.csr`** → 控制台上传 CSR → 下载应用公钥证书与支付宝公钥证书（及根证书，若提供）→ SDK 按文档配置路径。

安全：私钥不入库；`.gitignore` 含 `*.pem`、`*.csr`、`alipay_keys_*` 等（按项目约定）。

## 执行清单

```text
- [ ] OpenSSL 可用；已用脚本生成密钥文件（或按 reference 手写等价命令）
- [ ] 控制台已绑定公钥或已完成证书流程
- [ ] 支付宝侧用于验签的公钥或证书与 APPID、环境（正式/沙箱）一致
- [ ] 密钥未进入版本库
```

## Agent 约束

1. **生成密钥**：优先执行 **`generate_alipay_rsa2_keys.sh`**；成功则终端已有 PEM、路径与下一步——向用户复述**目录绝对路径**与控制台操作，**非必要不重复粘贴完整私钥**。
2. **CI**：用 **`--no-print`**。
3. **失败**：对照 [reference.md「常见报错引导」](reference.md#常见报错引导)。
4. **密钥与证书职责**：公钥模式为「应用私钥 / 应用公钥 / 支付宝公钥」；证书模式为「应用私钥 / CSR→应用证书 / 平台证书链」，以文档为准。
5. **验签失败**：区分请求侧（应用私钥与控制台应用公钥/证书是否匹配）与回调侧（支付宝公钥或证书是否最新、参数编码是否破坏待签串）。
6. **公私钥匹配**：用户仅询问「是否成对 / 如何校验」时，**只说明**如何用 **`verify_alipay_rsa2_keypair.sh`** 或 **`rsa_keys_match`** 在**本机终端**执行，给出命令与预期输出即可；**不要**主动代跑会读取私钥路径的命令，**不要**要求用户粘贴私钥全文。若用户明确要求 Agent 代跑，可用 **`--no-print`** 类思路避免在回复中复述 PEM；仍优先让用户本地执行。

## 环境变量（示例）

| 用途 | 常见名 |
|------|--------|
| APPID | `ALIPAY_APP_ID` |
| 应用私钥 | `ALIPAY_APP_PRIVATE_KEY` 或 `*_PATH` |
| 支付宝公钥 | `ALIPAY_PLATFORM_PUBLIC_KEY` 或 `*_PATH` |

以目标项目为准。

## 延伸阅读

[reference.md](reference.md)（依赖、脚本说明、报错表、官方文档、PEM 与安全）。
