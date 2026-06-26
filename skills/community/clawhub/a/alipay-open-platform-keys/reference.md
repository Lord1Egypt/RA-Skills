# 参考：依赖、脚本、排错与文档

## 环境与工具

本目录为 Agent Skills 包（`SKILL.md` 入口）；安装路径与 slash 调用见各产品文档：[agentskills.io](https://agentskills.io/)、[Cursor Skills](https://cursor.com/docs/skills)、[Claude Code Skills](https://code.claude.com/docs/en/skills)。用户级常见路径：`~/.cursor/skills/`、`~/.claude/skills/`；项目级：`.cursor/skills/`、`.claude/skills/`。

---

## 环境与依赖

执行 **`scripts/generate_alipay_rsa2_keys.sh` 仅需 OpenSSL**（`openssl version`）。未安装时：macOS 可用 Xcode CLT / Homebrew；Windows 可用 Git for Windows 或独立 OpenSSL；Linux 用发行版包管理器安装。

**Python**：仅在「用代码生成密钥」时需要 **`cryptography`**（`python3 -m pip install cryptography`，建议 venv）。若用户报错 `ModuleNotFoundError: cryptography`，按下表处理；本 Skill **不依赖** Python 跑一键脚本。

---

## 一键脚本（主路径）

**`scripts/generate_alipay_rsa2_keys.sh`**：在指定父目录下创建 `alipay_keys_<UTC>/`，写入 `app_private_key.pem`、`app_public_key.pem`；**`--cert`** 时额外生成 **`app.csr`**（SHA256）。默认在终端打印 PEM 与下一步；**`--no-print`** 适合 CI。

```bash
bash skills/alipay-open-platform-keys/scripts/generate_alipay_rsa2_keys.sh --help
```

自检（脚本行为与 OpenSSL 校验，无需额外测试框架）：`bash skills/alipay-open-platform-keys/scripts/test_generate_alipay_rsa2_keys.sh`

公钥模式：直接执行脚本（路径按仓库调整）。证书模式：`--cert`，并用 **`--subj '...'`** 或 **`ALIPAY_CSR_SUBJ`** 提供 CSR Subject；字段以 [生成密钥](https://opendocs.alipay.com/common/02kipl) 为准。未提供 Subject 时脚本使用占位值并告警。

脚本在实现上等同于：2048 位 RSA、`openssl genpkey` + `pkey -pubout`；证书模式再加 `openssl req -new -sha256`。若已有旧式 `BEGIN RSA PRIVATE KEY`，可 **`openssl pkcs8 -topk8 -nocrypt`** 转为 PKCS#8 再接入 SDK。若在应用内用 Python 生成，需输出 **PKCS#8 私钥** 与 **SPKI 公钥** PEM，与脚本一致即可，无需在此重复示例代码。

支付宝**桌面密钥工具**与脚本二选一即可；**勿混用**未配对的公私钥。

---

## 常见报错引导

| 报错或现象 | 处理 |
|------------|------|
| `openssl: command not found` | 安装 OpenSSL 并加入 `PATH` |
| `Unable to load PEM` / `bad decrypt` | 检查路径、PEM 是否完整、私钥是否加密 |
| `Permission denied` | 换可写目录或调整父目录权限 |
| `ModuleNotFoundError: cryptography` | `pip install cryptography`（建议 venv） |
| `pip` hash 与 lock 不符 | 在 venv 内单独安装，或按团队规范调整锁文件 |

---

## 官方文档（以最新页为准）

| 链接 | 内容 |
|------|------|
| [生成密钥](https://opendocs.alipay.com/common/02kipl) | 格式、公钥/证书模式、控制台 |
| [如何生成及配置 RSA2 密钥](https://opendocs.alipay.com/support/01raut) | RSA2、开发信息 |
| [支付宝密钥工具](https://opendocs.alipay.com/mini/02c7i5) | 官方工具（可选） |

证书模式 SDK 侧常见：**应用公钥证书**、**支付宝公钥证书**、根证书（若文档要求）；CSR DN **以文档为准**。

---

## 常见业务侧错误（密钥相关）

| 现象 | 常见原因 | 方向 |
|------|----------|------|
| 验签失败 / invalid signature | 公私钥不配对；支付宝公钥错；参数编码破坏待签串 | 核对控制台与 env；检查 query/body |
| 与签名相关的 sub_code（以文档为准） | 缺参、`sign_type` 不一致 | 对照待签串与 RSA2 |
| 沙箱/正式混用 | APPID、网关、密钥交叉 | 分环境 |
| 仅回调失败 | 支付宝公钥或 URL 解析 | 更新公钥；勿错误解码 `sign` |

---

## PEM 与安全

- **`BEGIN PRIVATE KEY`**：PKCS#8 私钥；**`BEGIN PUBLIC KEY`**：SPKI；**`BEGIN CERTIFICATE`**：先解析证书再取公钥。  
- 同步跳转里 **`sign` 为 Base64**，勿破坏其中的 `+`。  
- 私钥泄露须轮换；**勿**将 `*.pem`、`*.csr`、本地 env 提交仓库；勿在聊天中发完整私钥。
