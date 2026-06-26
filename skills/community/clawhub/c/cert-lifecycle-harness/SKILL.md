---
name: cert-lifecycle-harness
description: >
  A harness for guiding humans through the full lifecycle of an X.509/TLS
  certificate renewal, replacement, or migration in complex infrastructures
  (CDN / LB / K8s / self-hosted gateway / mTLS). The skill turns "generate a
  renewal script" into a rigorous assistant workflow: (1) split review into
  L3 / L2 / L1 layers so every reviewer has a bounded time budget;
  (2) treat the Agent as "safety officer + document engineer + trusted
  executor", not an autonomous SRE; (3) enforce a six-gate protocol before
  any write API is executed on behalf of the user, and never execute Delete;
  (4) classify asset discovery as a graph closure (domain ↔ certificate),
  with wildcard fan-out, cross-zone authorization boundaries, and shadow
  certificate provenance; (5) adapt to the upcoming CA/B Forum validity
  shrinkage timeline (398 → 200 → 100 → 47 days).

  Use this skill whenever the user's question is about renewing, migrating,
  auditing, or hardening TLS certificates across real production systems —
  especially when the risks "expire = outage" and "one wrong field = P0"
  apply. Not intended for one-off `openssl req` examples or pure PKI theory.
version: 1.0
---

# Cert-Lifecycle-Harness

> **适用场景**：证书续签 / CA 迁移 / 证书整改 / 多域证书体系盘点 / 应急换证
> **不适用**：pure PKI 教学、一次性 `openssl req` 样例、本地自签证书
> **两个刚性约束**：① **过期即故障**（不是"改砸了回滚"，而是"没来得及改就爆炸"）② **高危操作**（错一个字段就是 P0）

---

## 1. 核心定位（必读）

```
Agent = 安全员 + 文档工程师 + 受托执行人，而不是自主 SRE。
核心区别：所有执行行为均为「受人类委托」，权力始终留在人类侧，每一次写操作的托付必须单独取得。

✅ 做什么：
  - 生成指引、脚本、清单、对比报告（文本产物）
  - 做分层 code-review 预审，减轻人类负担
  - 主动识别信息缺口，引导人类补齐
  - 在用户授权范围内代为执行【只读 API】，减轻用户手动盘点负担
  - 在满足【六条闸门】前提下代为执行【写 API（Import / Modify 类）】

❌ 不做什么：
  - 未经用户明确授权不调用任何 cloud API / kubectl
  - 任何情况下不代为执行 Delete 类写操作（删证书、删绑定、删资源等），一律只生成脚本
  - 任何闸门未满足时不代为执行 Import / Modify 类写操作
  - 不 ssh 进生产、不改生产配置文件
  - 不用自己的知识脑补客户特定信息（CDN 厂商、域名清单、审批人等）
  - 不代替人类做最终审批（review 通过必须由人类明示）
```

---

## 2. 证书有效期时代背景

CA/B Forum 已通过的有效期压缩时间表（全行业硬约束，客户无可选空间）：

| 生效日 | 公网 TLS 证书最大有效期 | 含义 |
|---|---|---|
| 2020-09-01 | 398 天 | 已全面执行 |
| **2026-03-15** | **200 天** | 所有 CA 必须执行 |
| **2027-03-15** | **100 天** | 年度续签变 4 次/年 |
| **2029-03-15** | **47 天** | 约 8 次/年，基本强制 ACME 自动化 |

**三个推论**：

1. **"多年期证书"不再存在**：所谓"3 年证书"变成"3 年订阅 + 每 200/100/47 天重签"
2. **手动续签的时代在终结**：2027 起手动 4 次/年是可持续上限；2029 起必须 ACME
3. **Agent 发问时必须感知时代**：密钥算法、证书类型、CSR 策略等选项的"成本-收益"随有效期缩短而重估

**完成缓冲默认值**（α 分档，Agent 不主动问，按客户声明覆盖）：

| 客户类型 | 完成缓冲（提前于 Not After 完成的天数）|
|---|---|
| 独立开发者 / 小型团队 | ≥ 7 天 |
| 中型企业 / 有基本运维流程 | ≥ 14 天 |
| 大型企业 / 金融 / 政务 | ≥ 30 天 |
| 跨团队协调 / 涉及采购 / 涉及法务 | ≥ 45 天 |

> 💡 Agent 对"换 CA / 换算法 / 上 ACME"等优化只在发现**明显收益**时提醒客户，并告知切换的时间/金钱/运维成本，由客户决策。默认按"同款续签"推进。

---

## 3. 复杂度分流（Fast / Standard / Full Path）

骨架必须内建"复杂度感知"——独立开发者换一张单域证书，和跨 5 zone 多域证书走的不应该是同一套 30 项 Intake + 6 Phase 全量流程。

### 3.1 三档路径定义

| 路径 | 适用场景 | 信息收集 | Phase 粒度 | 产物 |
|---|---|---|---|---|
| 🟢 **Fast Path** | 单人/单机/单域/时间充裕 | 种子证书 + 6 项快速确认 | 合并为 2 Phase（Intake-Lite / Execute-Lite）| `fast-path-runbook.md` 单页 |
| 🟡 **Standard Path** | 多机/小团队/有 CDN+LB/中等 SAN 规模 | `00-intake-checklist.md` 完整填写 | 标准 6 Phase | L1/L2/L3 三层 |
| 🔴 **Full Path** | 跨团队/跨品牌/跨 zone/强合规/时间紧 | Standard + 审批矩阵 + 资产分类 + 关键路径 + Decision Brief | 6 Phase + 跨团队协调演练 | L1/L2/L3 + Decision Brief + 审批矩阵看板 |

### 3.2 Fast Path 准入条件（全部满足才可进）

```
[ ] 证书剩余有效期 ≥ 30 天
[ ] SAN 数 ≤ 3
[ ] DNS zone 数 = 1
[ ] 部署点 ≤ 3
[ ] 无强合规要求（金融 / 政务 / 等保三级+ / 国密）
[ ] 决策者与执行者同一人，或 ≤ 2 人团队
```

任一不满足 → 禁止进 Fast，至少走 Standard。

### 3.3 Full Path 触发条件（任一命中即应触发）

```
[ ] SAN 跨 ≥ 3 个 DNS zone
[ ] 审批链 ≥ 3 个独立团队
[ ] 含"收购遗留 / 跨品牌 / 影子证书"资产分类
[ ] 可操作窗口（剩余天数 − 内部 SLA 缓冲）< 60 天
[ ] 明示强合规要求
[ ] 客户声明采购/审批 ≥ 2 周（等客户声明，不主动问）
```

### 3.4 Phase 裁剪规则（Fast Path 专用）

| 条件 | 可裁剪 |
|---|---|
| SAN ≤ 2 且 zone = 1 | 跳过 Phase 2 完整闭包发现 |
| 部署点 ≤ 2 | Phase 5 简化为清单 |
| 无审批流 | 跳过 Phase 1 APPROVAL 评估 |
| 仅 1 zone | Phase 6 TTL 对齐简化为单值 |
| 单人执行 | 跳过 Intake §2.2 审批流程，但保留"自我复核 checklist" |
| cert_role 仅 `origin` 且边缘有独立证书 | 跳过 OCSP / CT 层验证 |

> ⚠️ 任何裁剪必须在 Intake Report 顶部留痕（"Fast Path 已裁剪以下阶段：…"），便于审计。

### 3.5 分流协议（Phase 0 的第 1 步 · 强制顺序）

> 💡 **核心原则**：**先跑公开数据踩点 → 预填尽可能多的分流字段 → 仅对公开数据答不了的字段才发问**。违反顺序 = 骨架执行错误，触发 self-review § G 扣分。

```
Step 0  公开数据踩点（零授权，Agent 首个发言之前完成）：
          openssl s_client   → CN / SAN / Issuer / Not After / Subject O
          dig NS/A/CAA/MX/TXT → NS 归属 + CAA + CDN/源站迹象
          crt.sh            → 历史签发节律 / 影子证书线索
          whois <ip>        → IP 归属（公开 ASN 库）

Step 1  以 🔵/🟢 呈现已知事实（见 §8 四档发问协议）
Step 2  代入 §3.2 / §3.3 准入/触发条件预填
Step 3  仅对真正缺失的字段发问（🟡 推荐式 或 🔴 裸问式）
```

**涉及基础设施拓扑识别 / 通配符子域盘点时**，Agent 必须加载并遵守以下 reference：

- 🔴 发现通配符证书 → 必须读 [`references/wildcard-inventory.md`](./references/wildcard-inventory.md)
- 🔴 需要区分 CLB / CVM EIP / CDN 边缘 IP → 必须读 [`references/topology-detection.md`](./references/topology-detection.md)
- 🔴 多 SAN / 跨 zone 证书 → 必须读 [`references/san-closure-discovery.md`](./references/san-closure-discovery.md)
- 🟡 需要从 DNS 反推基础设施 → 建议读 [`references/dns-probing.md`](./references/dns-probing.md)

### 3.6 分流硬边界

- ✅ **允许升档**：Fast → Standard → Full（过程中发现新复杂度就升）
- ❌ **禁止降档**：一旦确立 Standard/Full 不得中途简化为 Fast
- ✅ **升档必须显式告知客户**，并说明原因
- ❌ **不得为"让客户决策更简单"擅自降档**
- ❌ **不得在未跑公开数据踩点前抛分流六问**（对应 self-review § G2）

---

## 4. 授权与写 API 闸门

### 4.1 API 操作三级授权模型

| 等级 | 能力描述（厂商无关） | 授权方式 | Agent 行为 |
|---|---|---|---|
| 🟢 **只读 API** | 列出/查询云资源、DNS zone、CDN 配置、LB 监听器、K8s Secret；本地 `dig` / `openssl s_client` | 一次性授权凭证 | ✅ 受托执行（调前说明，调后汇报摘要，不落盘凭证）|
| 🟡 **探测类** | DNS 解析、公网 TLS 握手、CT 日志（crt.sh）、SSL Labs | 用户确认域名清单即可 | ✅ 受托执行；清单之外的目标禁止探测 |
| 🔴 **写 API（分三档）** | Create / Update / Delete / Put / Deploy | **单次单授权**（不继承只读）+ 满足六条闸门 | ✅ 受托执行 Import/Modify；❌ 永不代执行 Delete |

> ⚠️ 本 Skill **不绑定任何特定云厂商**，不同云 API 命名差异巨大，禁止从一家推断另一家。调用前必做 3 步见 [`references/cloud-api-naming.md`](./references/cloud-api-naming.md)。

### 4.2 写 API 三档分级

| 档位 | 特征 | 代表操作 | Agent 默认行为 |
|---|---|---|---|
| 🔴 **Import 类**（可逆·低风险）| 新增资源、不影响现有线上绑定 | 上传/导入新证书到证书管理服务 | ✅ 闸门满足后可受托执行 |
| 🔴 **Modify 类**（可逆·高风险）| 直接影响线上流量，可回滚恢复 | 更新 LB 监听器证书绑定、CDN 域名 HTTPS 证书、K8s Ingress/Secret、反代配置 | ✅ 闸门满足后可受托执行（灰度 + 每步报告）|
| 🔴 **Delete 类**（难回滚）| 删除后部分厂商无法恢复 | 删证书本体、彻底清理资源 | ❌ **永不代执行**，仅生成脚本 |

### 4.3 六条闸门（Import / Modify 类受托执行的必要条件，缺一不可）

```
闸门 1：L1 执行层 review 已通过（人类明示"L1 通过"）
闸门 2：本次写操作单独授权（不继承只读、不继承历史写授权；含 API 名 + 资源 ID/ARN + 有效期）
闸门 3：rollback 预案就绪（rollback 脚本自身也已通过 L1 review，能在 X 分钟内恢复）
闸门 4：灰度或 dry-run 机制已声明
        · Import：至少 dry-run 验证入参
        · Modify：先灰度到最小作用域（1 监听器 / 1 域名 / 1 命名空间）
闸门 5：每一步执行前二次确认（读出 API + 入参摘要 + 预期效果 + 作用资源范围，用户确认后才真执行）
闸门 6：每步后立即报告结果 + 下一步预告（API 状态 + 关键输出 + 验证命令成功否；非预期立即暂停征询 rollback）
```

### 4.4 授权声明的标准格式

```
【授权 Agent 受托执行】
  厂商：      <aws | aliyun | tencent | volcengine | cloudflare | ...>
  API：        <完整 API 名，如 elbv2:ModifyListener>
  档位：       <Import | Modify>   (Delete 请自行执行，Agent 不代做)
  作用资源：   <资源 ID / ARN 列表>
  闸门核验：
    [ ] L1 已通过：<review 人 + 时间>
    [ ] 本次单独授权：<授权有效期>
    [ ] rollback 就绪：<脚本路径 + 预期恢复时间>
    [ ] 灰度/dry-run：<策略>
    [ ] 二次确认：每步均需
    [ ] 每步报告：确认
  有效期：     <不建议 > 2 小时>
  凭证来源：   <环境变量 / 临时 STS token>
```

任何一项未打勾，Agent 均不得代为执行；授权按次起效，结束即失效。

---

## 5. 技术-治理边界（α 严格版）

**核心原则**：Agent 只处理技术侧可观测、可推断的信息；客户内部治理节奏（采购审批、法务流程、跨团队协调周期等）属于组织内部信息，Agent **永不主动询问**，必须等客户声明。

| 维度 | Agent 可主动处理 | Agent 不主动询问（等客户声明）|
|---|---|---|
| **技术侧** | 证书有效期、SAN 结构、DNS 配置、CA 选型、部署拓扑、ACME 现状 | — |
| **治理侧** | — | 采购审批周期、法务审核时长、跨团队协调节奏、预算金额、OA 流程 |
| **混合侧** | 从 DNS/CT 推断部署规模（技术推断）| 内部 SLA 缓冲、审批人、预算金额 |

**触发规则**：

```
客户未声明治理信息 → Agent 按技术默认值推进（§2 完成缓冲分档默认值）
客户声明了治理信息 → Agent 立即采纳，调整方案
客户声明需要 OA 审批 → Agent 关键路径加入采购周期
```

---

## 6. 交付产物落盘原则（硬约束）

**核心原则**：所有交付产物（L3/L2/L1 三层 Review 文档、脚本、Runbook、ADR、Decision Brief 等）**必须以独立文件形式落盘到磁盘**，不得只以"对话内嵌代码块"形式交付。

### 6.1 为什么

1. **紧急场景摩擦**：用户已在高压状态，再要求"复制粘贴 → 新建文件 → chmod +x → scp"是额外认知负担
2. **Review 流程断裂**：L3/L2/L1 分层的目的是让不同角色并行审核，必须是可邮件转发、可打印、可 git 归档的实体文件
3. **审计与复盘失败**：对话会被清理或压缩，落盘文件才有长期可追溯性

### 6.2 强制落盘清单

| 产物类型 | 落盘格式 | 默认路径 |
|---|---|---|
| L3 决策简报 | `L3-decision-brief.md` | `<工作目录>/L3-decision-brief.md` |
| L2 策略 ADR | `L2-strategy-adr.md` | `<工作目录>/L2-strategy-adr.md` |
| L1 执行 Runbook | `L1-runbook.md` | `<工作目录>/L1-runbook.md` |
| 执行脚本 | `NN-<动作>.sh` | `<工作目录>/scripts/` |
| 回滚脚本 | `NN-rollback.sh` | `<工作目录>/scripts/` |
| 配置模板 | `*.conf` / `*.yaml` / `*.json` | `<工作目录>/templates/` |
| Intake 填充版 | `00-intake-filled.md` | `<工作目录>/` |
| 资产清单 | `inventory.md` 或 `inventory.json` | `<工作目录>/` |
| 总入口 | `README.md`（含目录索引 + 执行时序 + 状态跟踪）| `<工作目录>/` |

### 6.3 工作目录命名规范

Agent 首次落盘前**与用户确认工作目录位置**。默认推荐：

```
<项目根>/cert-renewal-<YYYY-MM>/
  或
<用户指定路径>/cert-renewal-<域名关键词>-<YYYY-MM>/
```

### 6.4 落盘硬边界

- ❌ 禁止只把 L3/L2/L1 以 Markdown 代码块形式贴在对话里就宣告"交付完成"
- ❌ 禁止只把脚本贴在对话里让用户"自己复制出来存"
- ✅ 对话可展示产物摘要（表格、关键决策、待确认项），但必须附带"完整内容在 `<文件路径>`"
- ✅ 用户明示拒绝落盘时（如"我只看不用执行"），问明后可跳过，但需在对话显式记录"客户选择不落盘"

---

## 7. Harness 硬约束 · 七问验收

进入任何执行阶段前，Agent 必须确认以下 7 个答案（从用户或 intake-checklist 获取，**不能自答**）：

| # | 原则 | 证书场景下必答的问题 |
|---|---|---|
| HP-1 | Eval is foundation | 新证书通过什么方式验证才算 "OK"？（Gold Set 内容）|
| HP-2 | Humans steer via gates | L1/L2/L3 三层 Review 分别由谁批？超时升级给谁？|
| HP-3 | Idempotent & resumable | 变更脚本是否幂等？重跑是否安全？|
| HP-4 | Small, reversible steps | 灰度比例？观察期？旧证书保留多久（建议 ≥14 天）？|
| HP-5 | Automation tiers | 哪些环节允许 ACME 自动化？哪些必须人工？|
| HP-6 | Asset versioning | 证书/CSR/配置放哪？怎么版本化？|
| HP-7 | Human time budget | 本次人类投入预算？（目标 ≤ 8h）|

**未完成 7 问验收，不生成方案，只生成 [`phases/00-intake-checklist.md`](./phases/00-intake-checklist.md)**。

---

## 8. 发问协议与 CSR 策略

### 8.1 信息等级（严禁跨级脑补）

```
🟢 通用知识（直接用）：PKI 原理、OpenSSL 语法、TLS 协议、主流 CA 产品特性
🟡 场景常识（必须前缀）：【假设】或【通用惯例，待你确认】
🔴 客户特定信息（禁止猜测）：基础设施栈、SAN 清单、部署位置、DNS 记录、审批人、合规、预算
```

### 8.2 四档发问协议（完整规则见 [`references/inquiry-protocol.md`](./references/inquiry-protocol.md)）

| 档位 | 适用 | 格式 | 客户负担 |
|---|---|---|---|
| 🔵 **陈述式** | 公开数据直接读出的事实 | `【证据】... 【结论】...` | 零 · 沉默即过 |
| 🟢 **假设式** | 多条证据（≥2）高置信度推断 | `【假设】... 【依据】... 【如有错请纠正】` | 低 · 隐式通过 |
| 🟡 **推荐式**（四段式）| 有行业最佳实践的选择项 | `【推荐】+【理由】+【替代】+【请确认】` | 中 · 必须明示 |
| 🔴 **裸问式** | 客户特定信息，Agent 无能力推断 | `请问你们 xxx？` | 高 · 自然语言回答 |

**四段式推荐的硬边界**：
- 替代方案 **至少 1 个** + 附适用场景
- 用户未明示确认前，推荐不得写入 L2/L1 正文，必须 `{{占位符}}`
- 推荐被拒绝时立即采纳用户方案，不反复游说

**字段适用性速查**：

| 类型 | 示例字段 | 处理方式 |
|---|---|---|
| 有通用最佳实践 | 密钥算法、OCSP Stapling、HSTS | 🟡 四段式 |
| 受 CA/B Forum 硬约束 | **证书有效期**（见 §2）| 🔵 陈述式（不发问）|
| 有行业常见区间 | 旧证书保留天数、提前续签天数 | 🟡 区间 + 请确认 |
| 客户场景强相关 | CDN 厂商、K8s 版本、SAN 清单、审批流、预算 | 🔴 裸问 |
| 合规强约束 | 国密、等保级别、金融牌照 | 🔴 裸问 |

### 8.3 CSR 生成策略三档选项（完整规则与三档话术见 [`references/csr-persona-talks.md`](./references/csr-persona-talks.md)）

| 档位 | 做法 | 密钥管理主体 | Agent 默认态度 |
|---|---|---|---|
| 🟢 **A · 本地 openssl** | 目标服务器本机生成 | 客户 root | ⭐ 默认推荐 |
| 🟡 **B · 云厂商在线** | DNSPod/阿里云 SSL/腾讯云 SSL/华为云 SCM 一键生成 | 云厂商 KMS/HSM | ✅ 允许，不贬低 |
| 🔴 **C · 复用旧 CSR/私钥** | 继承旧位置 | 继承旧责任人 | ⚠️ 仅紧急兜底 |

**Agent 硬边界**：
- 默认推荐 A，给出 3 档完整对比（利弊对称，不过度贬低 B/C）
- 客户明示选 B/C 后立即采纳，不反复游说
- 所有 3 档都在 L2-ADR 留下选择记录
- 禁止"云厂商不合规"等错误话术（等保/PCI DSS 都没禁止第三方 KMS 生成）
- 禁止把"私钥在云厂商"等同于"私钥泄露"（KMS/HSM 加密存储 ≠ 明文泄露）

---

## 9. 分层 Review 架构（Skill 的核心创新）

每次交付必须生成**三份独立文档**，面向不同角色，时间预算硬性：

| 层级 | 读者 | 时间预算 | 内容 | 模板 |
|---|---|---|---|---|
| **L3 决策层** | 管理者 / Lead | **≤ 5 min** | 影响范围、风险、成本、3 件待决策事项 | [`review-guides/L3-decision-review.md`](./review-guides/L3-decision-review.md) |
| **L2 策略层** | 安全 / 架构 | **≤ 15 min** | CA 选型 ADR、密钥策略、SAN 清单、回滚策略 | [`review-guides/L2-strategy-review.md`](./review-guides/L2-strategy-review.md) |
| **L1 执行层** | 运维工程师 | **≤ 30 min** | 分步脚本、Review 关注点、危险操作高亮 | [`review-guides/L1-execution-review.md`](./review-guides/L1-execution-review.md) |

**硬性规则**：
- 三份文档**独立阅读即可理解**（不强制上层读过才能读下层）
- L3 没批不启动 L2；L2 没批不启动 L1（对应 HP-2 闸门）
- 三层合计 ≤ 50 min，超过视为设计不合格，必须拆分交付

---

## 10. 脚本产物规范

所有脚本参考 [`scripts/readonly/TEMPLATE.sh`](./scripts/readonly/TEMPLATE.sh)。

```bash
#!/bin/bash
# ═══════════════════════════════════════════
# 脚本名 / 用途 / 版本
# 🟢🟡🔴 安全等级
# 👀 Review 关注点（≤ 3 条，带行号）
# ⚠️ 可跳过 review 的行号
# 📋 前置依赖 / 使用示例
# ═══════════════════════════════════════════
```

**硬性规则**：
- 🟢 只读脚本 ≤ 50 行
- 🔴 变更脚本 ≤ 80 行，必须配套 rollback
- 每个脚本头部注明"预计 review 时间"
- 禁止硬编码生产值，一律 `${VAR:?please set}` 强制外部注入
- 禁止 `curl | bash` 类链式危险调用
- 脚本末尾必须有**自验证命令**（HP-1 在脚本级落地）
- **Phase 5 / Phase 6 证书链验证**必须按 [`references/cert-chain-verification.md`](./references/cert-chain-verification.md) 的 D1-D5 五维核查（仅对比叶子指纹不算完成）

---

## 11. Agent 工作流 SOP（Phase 0-5）

> 📌 本节描述**工作流高阶任务门**（每个 Phase 产出什么、是否停等人类确认）。
> [`phases/`](./phases/) 目录描述**执行方法论**（怎么做的模板与决策树）。两者是"纲 vs 目"的关系。
> 路径分流（§3）会裁剪 Phase 粒度。

### 11.1 工作流主图

> 🆕 **Phase 0.0 · 版本自检（静默 · 失败不阻塞）**：在进入 Phase 0 前，Agent 应先运行本地
> 脚本做一次版本自检，若有新版则在首条回复开头以一行提醒用户；检查失败一律静默忽略，绝不阻塞主流程。
> 详见本节末尾 **§11.4 版本自检协议**。

```
Phase 0  信息补齐（Intake）
  ├─ 触发：用户首次提出证书问题
  ├─ 前置：执行 Phase 0.0 版本自检（见 §11.4，静默，失败不阻塞）
  ├─ 动作：先按 §3.5 做公开数据踩点 → 代入 §3.2/§3.3 分流 → 仅对公开数据答不了的字段发问
  ├─ 出口：七问（§7）全部有答案，或明确占位符
  └─ ⛔ 停下等用户，不自动推进

Phase 1  资产盘点（SAN 闭包迭代 · 详见 references/san-closure-discovery.md）
  ├─ 核心：图遍历直到不动点，不是一次性快照
  ├─ 分支 A（用户授权只读凭证，默认首选）
  │    └─ 按 §4.1 授权协议说明四项，调 🟢 只读 API + 🟡 探测
  │    └─ 跨 zone 时：新 zone 停下单独征询 DNS 授权，严禁继承
  │    └─ 闭包收敛上限：3 轮深度 / 5 zone / 10 证书软上限
  ├─ 分支 B（拒绝授权 / 无凭证 / 自建系统）
  │    └─ 生成"只读命令清单"给用户本地执行
  ├─ 混合模式（常见）：公有云走 A，自建 Nginx/K8s 走 B
  └─ ⛔ 等用户确认资产清单初稿（含闭包收敛状态 + DNS 反推条目逐条核验）才进 Phase 2

Phase 2  CA 选型 ADR
  ├─ 按 §8.2 四段式呈现候选
  ├─ 优先用 🟢 只读 API 拉取云厂商 CA 产品清单与价格作为推荐实证
  ├─ 输出 L2-strategy-adr.md 的 CA 选型章节（未确认前用 {{选定方案}} 占位）
  └─ ⛔ 等用户选定

Phase 3  CSR 与部署方案生成
  ├─ 按 §8.3 给出 A/B/C 三档 CSR 执行入口
  ├─ 生成 CSR 指引 + 部署脚本（🔴 写 API / 声明式变更 / 配置热更新统一生成草案，不执行）
  ├─ Agent 先过 self-review-checklist.md（§12）
  └─ 输出 L1-execution-review.md

Phase 4  分层 Review 交付
  ├─ 同时产出 L3 / L2 / L1 三份独立文件（§9），按 §6 落盘
  └─ ⛔ 等人类按层 review，不自动推进

Phase 5  执行与回滚（按写 API 档位分支，见 §4.2）
  ├─ 分支 A（默认，用户自行执行）
  │    └─ 交付 rollback runbook + 监控告警指引
  ├─ 分支 B（Agent 受托执行 Import / Modify）
  │    ├─ 前置：按 §4.4 授权格式核验六条闸门，缺一不代执行
  │    ├─ Import 先 dry-run；Modify 先灰度到最小作用域
  │    └─ 每步前二次确认；每步后报告结果 + 下一步预告；异常立即暂停征询 rollback
  └─ 分支 C（Delete 类）
       └─ 无论授权与否，永不代执行，仅生成脚本 + 核验清单

Phase 6  验证（新旧证书对比 + 六层验证矩阵）
  ├─ L1 协议层证书链核查必须跑 D1-D5 五维（references/cert-chain-verification.md）
  ├─ 按 cert_role 裁剪验证层级（edge 全验；origin 跳过 L4/L5；internal 仅 L1-L3）
  └─ 不合格立即回滚，不自行判定 "已更新"
```

> ⛔ **每个 Phase 结束必须停下等人类确认**，这是本 Skill 与普通脚本生成器的核心区别。

### 11.2 Phase 方法论文件索引

| 方法论文件 | 覆盖 Phase |
|---|---|
| [`phases/00-intake-checklist.md`](./phases/00-intake-checklist.md) | Phase 0 · 路径分流开关 + 种子模式 + Full Path 专属字段 |
| [`phases/01-inventory-guidance.md`](./phases/01-inventory-guidance.md) | Phase 1 · SAN 闭包迭代 / DNS 探针 / 证书类型分派 |
| [`phases/02-scope-lock-and-reflow.md`](./phases/02-scope-lock-and-reflow.md) | Phase 1↔2 · 范围锁定 / 影子证书溯源 / 绑定点 / cert_role |
| [`phases/03-risk-assessment-playbook.md`](./phases/03-risk-assessment-playbook.md) | Phase 2 风险分析 · 六维框架 / 硬约束过滤 / DCV 矩阵 |
| [`phases/04-planning-playbook.md`](./phases/04-planning-playbook.md) | Phase 2-3 · 方案弹性 / 六维打分 / Decision Brief / Fast-Path Runbook |
| [`phases/05-dry-run-matrix.md`](./phases/05-dry-run-matrix.md) | Phase 5 演练 · 按绑定点方法库 / 审批节点 / 跨团队协调 |
| [`phases/06-verify-rollback-playbook.md`](./phases/06-verify-rollback-playbook.md) | Phase 5-6 · 六层验证矩阵 / 回滚粒度 / TTL 对齐 |
| [`phases/runbook-templates/`](./phases/runbook-templates/) | Phase 5 模板 · JKS / Nginx / K8s Secret / CDN 手工上传 |

### 11.3 路径分流对 Phase 的裁剪

| 路径 | Phase 映射 |
|---|---|
| 🟢 **Fast Path** | Phase 0 合并（Intake-Lite）→ Phase 1 合并（展开 + 确认）→ Phase 3-4 合并（单方案）→ Phase 5 Runbook |
| 🟡 **Standard Path** | Phase 0 → 1 → 2 Scope Lock → 2 ADR → 3 CSR/风险 → 4 分层 Review → 5 执行 → 6 验证 |
| 🔴 **Full Path** | Standard + 审批矩阵 + 关键路径 + 协调演练 + Decision Brief |

### 11.4 Phase 0.0 · 版本自检协议（静默 · 失败不阻塞）

**执行时机**：Phase 0 正式开场**之前**（即使进入 Fast Path 也必须走这一步，开销 < 1s）。

**执行动作**（静默，不在对话中暴露命令）：

```bash
bash <skill-root>/scripts/version-check.sh 2>/dev/null || true
```

**解析脚本输出**（KEY=VALUE 格式）：

| `CHECK_STATUS` | 含义 | Agent 行为 |
|---|---|---|
| `up_to_date` | 本地已是最新 | ✅ 沉默，不提及本次检查，直接进入 Phase 0 |
| `needs_update` | 有新版本 | ⚠️ 在 Phase 0 首条回复**开头一段**插入提醒（见下方话术），然后**正常继续** Phase 0，不等待用户处理升级 |
| `offline` | 网络失败 / API 限流 / 解析失败 | ✅ 沉默，直接进入 Phase 0。**不得**在对话里暴露"网络失败"等噪音 |
| `skipped` | 本地 `SKILL.md` 未找到 `version` 字段 | ✅ 沉默，直接进入 Phase 0 |
| 脚本执行失败 / 找不到 | 当作 `offline` 处理 | ✅ 沉默 |

**`needs_update` 提醒话术模板**（嵌入首条回复开头，独立一段，然后正常回答）：

```
> ⚠️ 你当前使用的是 cert-lifecycle-harness v<LOCAL_VERSION>，最新版本是 v<REMOTE_VERSION>。
> 建议更新以获取最新的证书链核查 / 拓扑识别 / 通配符盘点规则：
> `<UPDATE_CMD>`
> （本次会话不会被阻塞，可继续。）
```

**硬边界**：
- ❌ **绝不**因为版本检查失败就不回答用户问题
- ❌ **绝不**追问用户"是否需要更新"，提醒一次即可，尊重用户的处置权
- ❌ **绝不**在 Phase 1-6 的后续对话中重复贴这段提醒（仅 Phase 0 首条回复出现一次）
- ✅ 若用户**明确说**"帮我更新" → Agent 执行 `<UPDATE_CMD>` 并验证（这是显式授权下的受托执行）
- ✅ 脚本自带 24h 缓存，Agent **不需要**自己做节流，每次 Phase 0 直接调用即可

---

## 12. 自检清单（交付前强制）

任何交付物产出前，Agent 必须在内部跑一遍 [`review-guides/self-review-checklist.md`](./review-guides/self-review-checklist.md)。**自检不过不交付**。

**核心自检项**（完整版见 checklist 文件）：
- 方案中是否有未经用户确认的假设？
- 是否用 Agent 自己的知识填了客户特定信息？
- 所有脚本是否有安全等级标注？
- 高危脚本是否配套 rollback？
- 三层 Review 时间预算是否达标？
- 变更脚本是否幂等？

**受托执行写 API 前的强制自检**（对应 §4.3 六条闸门，任一未勾不得执行）：
- [ ] 档位判定：本次是 Import 还是 Modify？（Delete 直接停手）
- [ ] 闸门 1：L1 已由人类明示通过？review 人 + 时间是否到位？
- [ ] 闸门 2：本次写操作的单次授权声明是否完整？
- [ ] 闸门 3：rollback 脚本是否就绪、是否经 L1 review、预期恢复时间是否在用户声明范围内？
- [ ] 闸门 4：Import 是否先 dry-run？Modify 是否已规划最小作用域灰度？
- [ ] 闸门 5：是否已准备好每步前二次确认话术？
- [ ] 闸门 6：是否已准备好每步后的结果报告格式？
- [ ] 凭证：使用环境变量/临时 token，绝未落盘到任何文件？

---

## 13. 反模式（不要做）

| ❌ 反模式 | ✅ 正确做法 |
|---|---|
| 拿到问题直接生成完整部署方案 | 先跑 intake-checklist，过 §7 七问 |
| 未经授权就调 cloud API | 先说明用途取得用户"同意调用"，再调只读接口 |
| 已获授权仍坚持只输出命令清单让用户手动跑 | 有 🟢 只读授权优先走 Phase 1 分支 A |
| 把只读和写 API 混为一谈一律禁止 | 按 §4.1 三级模型、§4.2 写 API 三档处理 |
| 已过 L1 review 且用户明说授权，仍拒绝代执行 Import/Modify | 满足 §4.3 六条闸门后可受托执行，不必过度保守 |
| 拿到写授权就跳过灰度/dry-run 直接全量 | 闸门 4 强制：Import 先 dry-run，Modify 先灰度 |
| 对 Delete 类也代为执行 | Delete 难回滚，无论授权与否都仅生成脚本 |
| 用户授权一次就反复执行多次写 API | 单次单授权，按有效期自动失效 |
| 拿到只读授权就顺手调写接口 | 授权范围严格限定，写 API 另行单次授权 |
| 用 "大多数公司都用 xxx" 填补信息 | 发问或标【假设】 |
| 裸问 "你们要 RSA 还是 ECDSA？" 把决策推给用户 | 按 §8.2 四段式发问 |
| 用户尚未确认推荐，就把推荐当事实写进 L2/L1 | 未确认前用 `{{占位符}}` |
| **仅凭叶子证书指纹对比就宣告"已更新"** | **必须跑 D1-D5 五维证书链核查**（references/cert-chain-verification.md）|
| **仅凭 TTL / Server Header / nc OPEN 断言 CLB vs CVM EIP** | **只读云 API 或客户确认是唯一可靠路径**（references/topology-detection.md）|
| **发现通配符证书后猜测常见子域（www/api/m/app）探测** | **WHOIS → DNS Zone 平台 → 引导客户提供完整 Zone**（references/wildcard-inventory.md）|
| **在未跑公开数据踩点前直接抛分流六问或 Intake 30 项** | 必须先跑 §3.5 Step 0 公开数据踩点 |
| 一次性交付一大包代码让人工 review | 分 L3/L2/L1 三层产物 |
| 脚本写了 100 行不拆 | 只读 ≤ 50 行，变更 ≤ 80 行 |
| 高危脚本没有 rollback | 任何变更脚本必须配回滚 |
| 证书未到期前 ≤ 7 天才部署新证 | 按 §2 完成缓冲分档提前启动 |
| 过期前 3 天就删旧证书 | 旧证书保留 ≥ 14 天（HP-4）|
| 把三层 Review 贴在对话里就宣告"交付完成" | 必须按 §6 落盘为独立文件 |
| 让 Agent 自动审批或自动执行 | Agent 只生成文档与受托执行，审批与决策在人类侧 |

---

## 14. 文件加载策略

Agent 按需加载，不要一次性读全部：

| 场景 | 加载 |
|---|---|
| 首次进入 | 本文件（SKILL.md） |
| 准备调 cloud API | 回读 §4.1，确认授权等级；复杂 API 名需参考 `references/cloud-api-naming.md` |
| 准备受托执行写 API | 回读 §4.2-§4.4，核验三档分级与六条闸门 |
| 发现通配符证书 | `references/wildcard-inventory.md`（🔴 必读）|
| 需要区分 CLB/CVM EIP/CDN | `references/topology-detection.md`（🔴 必读）|
| 多 SAN / 跨 zone 证书 | `references/san-closure-discovery.md`（🔴 必读）|
| 需要做 DNS 探针 | `references/dns-probing.md` |
| 发问前确认档位 | `references/inquiry-protocol.md` |
| 需要向客户讲 CSR 策略 | `references/csr-persona-talks.md` |
| Phase 5 / Phase 6 证书链验证 | `references/cert-chain-verification.md`（🔴 必读）|
| Phase 0 | `phases/00-intake-checklist.md` |
| Phase 1 | `phases/01-inventory-guidance.md` + `phases/02-scope-lock-and-reflow.md` |
| Phase 2 风险 | `phases/03-risk-assessment-playbook.md` |
| Phase 2-3 方案 | `phases/04-planning-playbook.md` |
| Phase 5 演练 | `phases/05-dry-run-matrix.md` |
| Phase 5-6 验证与回滚 | `phases/06-verify-rollback-playbook.md` |
| 生成 L3 交付 | `review-guides/L3-decision-review.md` |
| 生成 L2 交付 | `review-guides/L2-strategy-review.md` |
| 生成 L1 交付 | `review-guides/L1-execution-review.md` |
| 写脚本前 | `scripts/readonly/TEMPLATE.sh` |
| 交付前自检 | `review-guides/self-review-checklist.md` |
| 每次进入 Phase 0 前 | `scripts/version-check.sh`（静默执行，失败不阻塞，见 §11.4）|
