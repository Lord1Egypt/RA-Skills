# alipay-open-platform-keys（Agent Skill）

本 Skill 面向 **[支付宝开放平台](https://open.alipay.com)**：帮助在本地完成 **RSA2 应用密钥的生成、轮换与公私钥校验**，并说明如何把产物与开放平台 **开发信息**（应用公钥/证书上传、支付宝公钥获取）以及业务代码中的 **加签、回调验签** 对齐。它不替代控制台配置，但覆盖开放平台接口常用的密钥侧工作流。

**能力**：在支付宝开放平台约定的 PEM 格式下，提供 **公钥模式** 密钥对与 **证书模式** CSR 的本地生成（**`scripts/generate_alipay_rsa2_keys.sh`**，仅需 OpenSSL）、与开放平台控制台及加验签的衔接说明；密钥排错与官方文档见 **`reference.md`**。

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 流程、Agent 约束、YAML 描述（触发匹配） |
| `reference.md` | 依赖、脚本要点、报错表、文档链接、PEM/安全 |
| `scripts/generate_alipay_rsa2_keys.sh` | 公钥模式 / `--cert` 证书模式；`--help` 查看参数 |
| `scripts/test_generate_alipay_rsa2_keys.sh` | 自检脚本（需 `openssl`）：`bash scripts/test_generate_alipay_rsa2_keys.sh` |

## 安装

在 Cursor / Claude Code 等支持 Agent Skills 的环境中，需要把 **`alipay-open-platform-keys` 技能包**（即包含 `SKILL.md` 的完整文件夹，名称可保持 `alipay-open-platform-keys`）放到产品约定的 Skills 搜索路径下，以便助手加载该技能。

常见做法（具体以各产品当前文档为准）：

- **用户级**：`~/.cursor/skills/` 或 `~/.claude/skills/`
- **项目级**：仓库内的 `.cursor/skills/` 或 `.claude/skills/`

产品说明与目录约定见 [Cursor Skills](https://cursor.com/docs/skills)、[Claude Code Skills](https://code.claude.com/docs/en/skills)、[agentskills.io](https://agentskills.io/)。
