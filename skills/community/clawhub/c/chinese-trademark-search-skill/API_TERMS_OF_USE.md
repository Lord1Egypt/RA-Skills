# API Terms of Use / API 使用条款

**Effective Date:** 2026-03-28
**Last Updated:** 2026-03-28

---

## English

### 1. Acceptance

By accessing or using the Chinese Trademark Search API ("the API"), you agree to be bound by these Terms of Use. If you do not agree, you must not use the API.

### 2. Rate Limits

The following rate limits apply to all API consumers:

| Endpoint | Rate Limit |
|---|---|
| Search | 10 requests per minute |
| Detail | 20 requests per minute |
| Export | 5 requests per day |

Rate limits are enforced per API key. Exceeding rate limits will result in HTTP 429 responses. Repeated or systematic attempts to circumvent rate limits may result in key revocation.

### 3. Acceptable Use

Users **shall**:
- Use the API solely for legitimate trademark research and due diligence purposes
- Comply with all applicable laws and regulations
- Maintain the confidentiality of their API credentials

Users **shall not**:
- Scrape, crawl, or systematically extract data from the API beyond normal search usage
- Perform bulk downloads of trademark data
- Commercially resell, sublicense, or redistribute API data or search results without a separate commercial license from the platform
- Attempt to reverse-engineer, decompile, or probe the API infrastructure
- Use automated tools to circumvent rate limits, authentication, or access controls
- Misrepresent the source of data obtained through the API

### 4. Data Retention

- **Query history**: Retained for **12 months** from the date of the query for audit, compliance, and dispute resolution purposes.
- After the retention period, query logs are anonymized or deleted in accordance with applicable data protection laws.
- Users may request early deletion of query history subject to legal retention obligations. See [GDPR_COMPLIANCE.md](GDPR_COMPLIANCE.md) and [CCPA_NOTICE.md](CCPA_NOTICE.md) for data subject rights.

### 5. Service Level

| Metric | Target |
|---|---|
| Uptime | 99.5% monthly availability (service target) |
| Search Response Time | < 5 seconds (95th percentile) |

- The 99.5% uptime figure is an **availability target, not a contractual guarantee**, and does not constitute a basis for compensation claims. Service level targets are goals; the platform will use commercially reasonable efforts to meet them.
- Scheduled maintenance windows will be announced at least 48 hours in advance when possible.
- The platform is not liable for downtime caused by force majeure, third-party infrastructure failures, or circumstances beyond its reasonable control.

### 6. Limitation of Liability

**The platform is not liable for any decisions made based on search results.** Trademark search results are informational only and do not constitute legal advice. See [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md) for full details.

To the maximum extent permitted by law:
- The platform's total aggregate liability shall not exceed the fees paid by the user in the 12 months preceding the claim.
- The platform shall not be liable for indirect, incidental, special, consequential, or punitive damages.

### 7. Termination

The platform reserves the right to suspend or terminate API access, including key revocation, if:

- The user violates these Terms of Use
- The user's account is associated with sanctions violations (see [SANCTIONS_COMPLIANCE.md](SANCTIONS_COMPLIANCE.md))
- The user engages in abusive, fraudulent, or unauthorized use
- Required by law or regulatory order

Upon termination:
- The user's API key will be immediately revoked
- Outstanding point balances are forfeited unless otherwise required by law
- The user may request export of their personal data within 30 days of termination

### 8. Modifications

The platform may modify these Terms of Use at any time. Material changes will be communicated via email or platform notification at least 30 days in advance. Continued use of the API after the effective date of changes constitutes acceptance.

### 9. Governing Law

These Terms of Use are governed by the laws of the People's Republic of China. The platform currently operates a single-region deployment in mainland China with the entry point `tm.zhengquai.com`; an overseas region is planned, and governing-law terms for it will be published when it launches.

---

## 中文

### 1. 接受条款

访问或使用中国商标查询 API（以下简称"API"）即表示您同意受本使用条款的约束。如不同意，请勿使用 API。

### 2. 速率限制

以下速率限制适用于所有 API 使用者：

| 接口 | 速率限制 |
|---|---|
| 查询（Search） | 每分钟 10 次请求 |
| 详情（Detail） | 每分钟 20 次请求 |
| 导出（Export） | 每天 5 次请求 |

速率限制按 API 密钥执行。超出速率限制将返回 HTTP 429 响应。反复或系统性尝试绕过速率限制可能导致密钥被吊销。

### 3. 可接受使用

用户**应当**：
- 仅将 API 用于合法的商标检索和尽职调查目的
- 遵守所有适用的法律法规
- 妥善保管 API 凭据的机密性

用户**不得**：
- 超出正常查询使用范围，对 API 进行抓取、爬取或系统性数据提取
- 批量下载商标数据
- 未经平台另行授予商业许可，不得对 API 数据或查询结果进行商业转售、再许可或再分发
- 试图对 API 基础设施进行逆向工程、反编译或探测
- 使用自动化工具绕过速率限制、身份验证或访问控制
- 虚假陈述通过 API 获取的数据来源

### 4. 数据保留

- **查询历史**：自查询之日起保留 **12 个月**，用于审计、合规和争议解决。
- 保留期满后，查询日志将根据适用的数据保护法律进行匿名化或删除。
- 用户可在法定保留义务范围内申请提前删除查询历史。有关数据主体权利，请参阅 [GDPR_COMPLIANCE.md](GDPR_COMPLIANCE.md) 和 [CCPA_NOTICE.md](CCPA_NOTICE.md)。

### 5. 服务水平

| 指标 | 目标 |
|---|---|
| 可用性 | 每月 99.5%（目标可用性，service target） |
| 查询响应时间 | < 5 秒（95 分位） |

- 99.5% 可用性为**目标可用性（service target），不构成合同承诺或赔偿依据**。服务水平目标是努力目标，平台将尽商业上合理的努力达成上述目标。
- 计划维护窗口将尽可能提前至少 48 小时通知。
- 对于因不可抗力、第三方基础设施故障或超出合理控制范围的情况导致的停机，平台不承担责任。

### 6. 责任限制

**平台对基于查询结果所做的任何决策不承担责任。** 商标查询结果仅供参考，不构成法律建议。详情请参阅 [LEGAL_DISCLAIMER.md](LEGAL_DISCLAIMER.md)。

在适用法律允许的最大范围内：
- 平台的累计总责任不超过用户在索赔发生前 12 个月内支付的费用。
- 平台不对间接、附带、特殊、后果性或惩罚性损害承担责任。

### 7. 终止

在以下情况下，平台保留暂停或终止 API 访问（包括吊销密钥）的权利：

- 用户违反本使用条款
- 用户账户涉及制裁违规（参见 [SANCTIONS_COMPLIANCE.md](SANCTIONS_COMPLIANCE.md)）
- 用户从事滥用、欺诈或未授权的使用行为
- 法律或监管命令要求

终止后：
- 用户的 API 密钥将被立即吊销
- 除法律另有要求外，未使用的点数余额将被没收
- 用户可在终止后 30 天内申请导出个人数据

### 8. 条款修改

平台可随时修改本使用条款。重大变更将通过电子邮件或平台通知提前至少 30 天告知。变更生效后继续使用 API 即视为接受。

### 9. 适用法律

本使用条款受中华人民共和国法律管辖。平台当前为单区域部署（中国大陆，入口 `tm.zhengquai.com`）；海外节点在规划中，其适用法律条款将在上线时另行公布。
