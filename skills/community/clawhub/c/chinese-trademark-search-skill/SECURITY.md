# Security Notice

## 报告安全漏洞 / Reporting a Vulnerability

**请不要通过公开 issue 报告安全漏洞。** 公开 issue 会让问题在修复前暴露给所有人。

- 邮箱：**lengqifeng11@gmail.com**，标题请以 `[SECURITY]` 开头
- 请附上：受影响的版本或 commit、复现步骤、影响面评估；如涉及计费或越权，请说明可复现的最小账号条件
- 响应时限：**3 个工作日内**首次回复，**30 天内**给出修复或缓解方案
- 请给我们合理的修复窗口后再公开披露；修复发布时会在 [CHANGELOG.md](CHANGELOG.md) 致谢报告者（如你不希望署名请说明）

请勿在报告中附上真实的 `tmu_` API Key。如果你怀疑自己的 Key 已泄漏，
请直接到 https://tm.zhengquai.com/settings/api-keys 吊销并重新生成，无需等待回复。

**Do not report security issues through public issues.** Email
**lengqifeng11@gmail.com** with a `[SECURITY]` subject prefix. We aim to acknowledge
within 3 business days and to ship a fix or mitigation within 30 days. Please allow a
reasonable disclosure window. Never include a live `tmu_` API Key in a report — revoke
it yourself at https://tm.zhengquai.com/settings/api-keys instead.

### 影响范围 / Scope

本文件覆盖的是**本仓库的 Skill 代码**（参数处理、token 处理、错误输出等）。
托管平台 `tm.zhengquai.com` 自身的漏洞同样发到上述邮箱，请在标题中注明 `platform`。

## 公开 Skill 说明

这是一个公开 Skill，适合发布到 ClawHub、代码仓库或公开分发渠道。

## 不包含私有密钥

本 Skill 不包含以下任何敏感信息：

- 平台管理员密钥
- 上游商标数据商账号密码
- 上游商标接口私钥
- 用户个人 token
- 平台数据库凭据

## 用户应使用的平台 token

用户应配置的是“自有平台的用户级 token”，而不是上游商标接口密钥。

推荐环境变量：

- `CHINA_TM_PLATFORM_BASE_URL`
- `CHINA_TM_USER_TOKEN`
- `CHINA_TM_TIMEOUT_MS`
- `CHINA_TM_SKILL_CHANNEL`

## 安全使用建议

- 不要把 token 写进 prompt
- 不要把 token 发到 issue
- 不要把 token 放进截图
- 不要把 token 硬编码到 Skill 文件中
- 不要把 token 提交到 Git 仓库

## 平台侧建议

平台应支持以下安全能力：

- token 吊销
- token 轮换
- token 过期控制
- 用户级权限隔离
- 操作日志审计
- 限流与异常访问检测

## 日志与输出要求

本 Skill 的 CLI 不应打印 token，也不应在错误堆栈中回显 Authorization 头或完整请求体中的敏感字段。

## 泄露处理建议

若怀疑 token 泄露：

1. 立即在平台吊销该 token
2. 重新生成新 token
3. 检查最近访问日志
4. 如有必要，通知相关用户轮换凭据

## Export Control and Sanctions / 出口管制与制裁

This Skill and the associated platform are subject to US Export Administration Regulations (EAR) and OFAC sanctions programs. Access is prohibited from sanctioned jurisdictions (Iran, North Korea, Syria, Cuba, Crimea) and by individuals or entities on the OFAC SDN List.

The platform may implement IP-based geoblocking and automated sanctions screening to enforce compliance. Violations may result in immediate account termination and referral to authorities.

For full details, see [SANCTIONS_COMPLIANCE.md](SANCTIONS_COMPLIANCE.md).

本 Skill 及相关平台受美国出口管理条例（EAR）和 OFAC 制裁计划约束。禁止从受制裁司法管辖区（伊朗、朝鲜、叙利亚、古巴、克里米亚）及 OFAC SDN 名单上的个人或实体访问。详情请参阅 [SANCTIONS_COMPLIANCE.md](SANCTIONS_COMPLIANCE.md)。

## Data Residency Architecture / 数据驻留架构

The platform currently operates a single-region deployment:

| Region | Entry Point | Data Location | Applicable Law |
|---|---|---|---|
| China Mainland | `tm.zhengquai.com` | Mainland China | PIPL, DSL, CSL |

An overseas region is planned but not yet available. Key security properties:

- **Independent infrastructure:** The deployment runs on dedicated infrastructure with strict access controls.
- **Regional compliance:** The deployment is configured to comply with its applicable data protection framework (PIPL, DSL, CSL).

For full details, see [DATA_RESIDENCY.md](DATA_RESIDENCY.md).

平台当前为单区域部署（中国大陆，入口 `tm.zhengquai.com`），海外节点在规划中。详情请参阅 [DATA_RESIDENCY.md](DATA_RESIDENCY.md)。

## GDPR Cross-Border Mechanisms / GDPR 跨境传输机制

The platform currently operates only the mainland China region (`tm.zhengquai.com`), so personal data of EU/EEA users is stored in mainland China. The following safeguards are in place:

- **Standard Contractual Clauses (SCCs):** Commission Implementing Decision (EU) 2021/914, supplemented by a Transfer Impact Assessment (TIA).
- **Encryption:** TLS 1.2+ in transit, AES-256 at rest.
- **Access controls:** Data access restricted to authorized personnel with role-based permissions.
- **Sub-processor management:** DPAs with all sub-processors; 30-day advance notice of changes.
- **Data Processing Agreement (DPA):** Available on request for enterprise customers (contact: lengqifeng11@gmail.com).

For full GDPR compliance details, see [GDPR_COMPLIANCE.md](GDPR_COMPLIANCE.md).

平台当前仅运营中国大陆区域（入口 `tm.zhengquai.com`），欧盟/EEA 用户的个人数据存储在中国大陆。平台通过标准合同条款（SCCs）及传输影响评估（TIA）保障跨境数据传输合规。详情请参阅 [GDPR_COMPLIANCE.md](GDPR_COMPLIANCE.md)。
