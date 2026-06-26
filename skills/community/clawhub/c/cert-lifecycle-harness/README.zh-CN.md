# Cert-Lifecycle-Harness

<p align="left">
  <a href="./README.md">English</a> ·
  <a href="./README.zh-CN.md"><b>简体中文</b></a>
</p>

<p align="left">
  <a href="https://github.com/dimayip/cert-lifecycle-harness/stargazers"><img src="https://img.shields.io/github/stars/dimayip/cert-lifecycle-harness?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/dimayip/cert-lifecycle-harness/network/members"><img src="https://img.shields.io/github/forks/dimayip/cert-lifecycle-harness?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/dimayip/cert-lifecycle-harness/issues"><img src="https://img.shields.io/github/issues/dimayip/cert-lifecycle-harness?style=flat-square" alt="Issues"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/dimayip/cert-lifecycle-harness?style=flat-square" alt="License"></a>
</p>

> 证书生命周期管理的 Harness-style 协作 Skill。Agent 定位为「安全员 + 文档工程师 + 受托执行人」，
> 生成分层 Review 文档与人工执行脚本，在满足六条闸门前可受托执行 Import/Modify 类写 API，永不代执行 Delete。

---

## 安装

通过 [skills.sh](https://skills.sh) 安装（支持 Claude Code / Cursor / Codex / CodeBuddy / OpenCode 等 50+ Agent）：

```bash
# 全局安装（对所有项目可用）
npx skills add dimayip/cert-lifecycle-harness -g -a claude-code

# 仅安装到当前项目
npx skills add dimayip/cert-lifecycle-harness -a codebuddy
```

或者手动把仓库放到对应 Agent 的 skills 目录下（例如 `~/.claude/skills/cert-lifecycle-harness/` 或 `.codebuddy/skills/cert-lifecycle-harness/`）。

兼容 [Agent Skills Specification](https://agentskills.io)。

---

## 为什么需要这个 Skill

证书更换是典型的"**过期即故障**"的高危运维场景：

- 错一个 SAN 字段 → 整站 TLS 握手失败
- 过期前一天才想起更换 → 没有灰度窗口 → P0
- 一次性把几十个部署位置的证书换掉 → 运维 review 到眼瞎 → 漏掉关键风险
- 用 AI agent 直接操作生产 → 高危且不可控

本 Skill 把证书变更拆解为**可对齐 Harness 7 原则**的协作流程：
- Agent 负责生成指引、脚本、对比报告、Review 文档；在满足闸门时可受托执行 Import/Modify 类写 API
- 人类负责决策、审批、执行 Delete 类操作
- **核心创新是"分层 Review"**：L3 决策层 5 min / L2 策略层 15 min / L1 执行层 30 min，
  让不同角色并行审核，把人类总负担压到 ≤ 50 min

---

## 何时加载

用户提到以下关键词时自动触发：

- 证书到期 / 证书过期 / 证书续签 / 证书更换
- 泛域名证书 / 通配符证书 / SAN 证书
- SSL 证书 / TLS 证书 / HTTPS 证书
- CA 迁移 / 签发机构变更

---

## Agent 的硬边界

```
✅ 做：生成文档、脚本、清单、对比报告
✅ 做：主动识别信息缺口，引导用户补齐
✅ 做：分层 Review 预审，减轻人类负担
✅ 做：在用户授权范围内调用【只读 API】减轻手动盘点负担
✅ 做：在满足【六条闸门】前提下受托执行【Import / Modify 类写 API】

❌ 不做：未经用户明确授权不调用任何 cloud API / kubectl
❌ 不做：永不代为执行【Delete 类写 API】（删证书、删绑定、删资源），一律只生成脚本
❌ 不做：任一闸门未满足时不代为执行 Import / Modify 类写操作
❌ 不做：ssh 进生产、修改生产配置文件
❌ 不做：用自己的知识脑补客户特定信息
❌ 不做：代替人类做最终审批
```

### API 操作三级授权模型

| 等级 | 能力描述（厂商无关） | 授权方式 |
|---|---|---|
| 🟢 **只读 API** | 列出/查询云资源：证书清单、CDN 域名配置、LB 监听器、K8s Secret、DNS zone 记录等 | 一次性授权只读凭证后可反复调用 |
| 🟡 **探测类** | DNS 解析 / TLS 握手 / CT 日志（crt.sh）/ SSL Labs 打分 | 用户确认域名清单即可 |
| 🔴 **写 API（分三档）** | Create / Update / Delete / Put / Deploy | 单次单授权 + 满足六条闸门；Delete 永不代执行 |

> ⚠️ 各云厂商 API 命名差异大（AWS / 阿里云 / 腾讯云 / 华为云 / Cloudflare / 火山引擎），Agent 调用前必须
> 向用户确认云厂商并核对官方文档，禁止跨厂商套用 API 名。

完整协议与跨厂商 API 对照见 [`SKILL.md §4`](./SKILL.md) 与 [`references/cloud-api-naming.md`](./references/cloud-api-naming.md)。

---

## 仓库结构

遵循 skill-creator 的渐进披露原则：主 `SKILL.md` ≤ 600 行；深度规则下沉到 `references/`，按需加载。
```
cert-lifecycle-harness/
├── SKILL.md                              # Agent 加载执行的主规格（v1.0，14 章节）
├── README.zh-CN.md                       # 本文件
├── CHANGELOG.md                          # ⭐ 版本演进集中记录
│
├── references/                           # ⭐ 深度规则按需加载（v1.0 新增）
│   ├── README.md                         #   索引 · 按加载场景
│   ├── topology-detection.md             #   基础设施拓扑识别（CLB / CVM EIP / CDN 边缘）
│   ├── wildcard-inventory.md             #   通配符证书子域名盘点
│   ├── cert-chain-verification.md        #   证书链完整性 + 多客户端兼容性（D1-D5）
│   ├── san-closure-discovery.md          #   SAN 闭包发现 + cert_role + 影子证书溯源
│   ├── dns-probing.md                    #   DNS 探针与基础设施反推
│   ├── inquiry-protocol.md               #   四档发问协议（🔵/🟢/🟡/🔴）
│   ├── csr-persona-talks.md              #   CSR 三档选项 + 三档话术
│   └── cloud-api-naming.md               #   跨云厂商 API 命名差异
│
├── phases/                               # Phase 方法论文件（按需加载）
│   ├── 00-intake-checklist.md            #   Phase 0 · 路径分流 + 种子模式
│   ├── 01-inventory-guidance.md          #   Phase 1 · SAN 闭包迭代 + DNS 探针
│   ├── 02-scope-lock-and-reflow.md       #   Phase 2 · 范围锁定 + cert_role
│   ├── 03-risk-assessment-playbook.md    #   Phase 3 · 六维风险 + DCV 矩阵
│   ├── 04-planning-playbook.md           #   Phase 4 · 方案弹性 + Decision Brief
│   ├── 05-dry-run-matrix.md              #   Phase 5 · 演练方法库
│   ├── 06-verify-rollback-playbook.md    #   Phase 6 · 六层验证 + 回滚粒度
│   └── runbook-templates/                #   按绑定点类型的 Runbook 模板
│
├── review-guides/                        # ⭐ 分层 Review 架构（核心创新）
│   ├── L3-decision-review.md             #   5 min · 给管理者
│   ├── L2-strategy-review.md             #   15 min · 给安全/架构
│   ├── L1-execution-review.md            #   30 min · 给运维
│   └── self-review-checklist.md          #   Agent 交付前自检（A-G 七类）
│
└── scripts/
    └── readonly/
        └── TEMPLATE.sh                   # 所有脚本必须遵守的结构范本
```

---

## 标准工作流

```
Phase 0  信息补齐（先跑公开数据踩点 → 分流 → 仅问公开数据答不了的字段）→ ⛔ 等用户
   ↓
Phase 1  资产盘点（SAN 闭包迭代 + DNS 探针 + 跨 zone 独立授权）→ ⛔ 等用户
   ↓
Phase 2  CA 选型 ADR（四段式推荐 + 候选方案）→ ⛔ 等用户选定
   ↓
Phase 3  CSR + 部署方案生成（CSR 三档 A/B/C 选项）
   ↓
Phase 4  分层 Review 交付（L3/L2/L1 并行，独立落盘）→ ⛔ 等人类按层 review
   ↓
Phase 5  执行与回滚（按写 API 档位分支；受托执行 Import/Modify，Delete 仅给脚本）
   ↓
Phase 6  验证（D1-D5 五维证书链 + 六层验证矩阵；按 cert_role 裁剪）
```

每个 Phase 结束**必须停下等人类**，这是本 Skill 与普通脚本生成器的核心区别。

---

## 能力地图

| 能力域 | 关键特性 | 落地位置 |
|---|---|---|
| **复杂度分流** | Fast / Standard / Full 三档 + 准入/触发条件 + Phase 裁剪规则 | `SKILL.md §3` + `phases/00-intake-checklist.md §零` |
| **Intake** | 公开数据踩点先行 + 种子模式 + 三档路径对应字段 + Full Path 审批矩阵 | `SKILL.md §3.5` + `phases/00-intake-checklist.md` |
| **基础设施拓扑识别** | 撤除 TTL/Server/nc/ALPN 等不可靠信号；只读云 API 或客户确认为唯一可靠路径 | `references/topology-detection.md` |
| **通配符子域盘点** | WHOIS → DNS 平台 → 引导完整 Zone；CT 日志仅作辅助 | `references/wildcard-inventory.md` |
| **资产盘点** | SAN 闭包发现 + DNS 探针 + 反向扩展启发式 + 部分授权降级 + 影子证书溯源 | `references/san-closure-discovery.md` + `phases/01-inventory-guidance.md` |
| **范围管理** | Scope Lock + 盘点回流 + 资产分类（A/B/C/D/E）+ 绑定点定义 + cert_role 五角色 | `phases/02-scope-lock-and-reflow.md` |
| **风险评估** | 六维框架 + 硬约束过滤器 + DCV 矩阵 + 硬阻塞兜底树 | `phases/03-risk-assessment-playbook.md` |
| **方案规划** | 方案数量弹性 + 六维打分（含可逆性）+ Decision Brief + Fast-Path Runbook 模板 | `phases/04-planning-playbook.md` |
| **发问协议** | 四档发问（🔵 陈述 / 🟢 假设 / 🟡 推荐 / 🔴 裸问）+ 开场强制公开数据踩点 | `references/inquiry-protocol.md` + `SKILL.md §8.2` |
| **CSR 策略** | 三档选项（A 本地 / B 云厂 / C 复用）+ 三档话术（L1/L2/L3 受众）| `references/csr-persona-talks.md` + `SKILL.md §8.3` |
| **证书链验证** | D1-D5 五维（下发链 / 顺序 / 中间证书有效期 / 链可达 Root / 多客户端兼容）| `references/cert-chain-verification.md` |
| **分层 Review** | L3 / L2 / L1 三份独立产物，≤ 5 / 15 / 30 min，合计 ≤ 50 min，**必须落盘** | `review-guides/L{1,2,3}-*.md` |
| **Agent 自检** | A-G 七类清单，含 G1-G15 | `review-guides/self-review-checklist.md` |
| **写 API 代执行** | Import / Modify / Delete 三档分级 + 六条闸门 | `SKILL.md §4` |

### Fast / Standard / Full Path 路径选择指南

**选 🟢 Fast Path** 若你全部满足：
- 证书剩余 ≥ 30 天
- SAN ≤ 3（含裸域）
- 仅 1 个 DNS zone
- 部署点 ≤ 3
- 无金融 / 国密 / 等保三级+ 等强合规
- 决策者 = 执行者 或 ≤ 2 人小团队

**选 🔴 Full Path** 若你命中任一：
- SAN 跨 ≥ 3 个 DNS zone
- 审批链涉及 ≥ 3 个独立团队（中台 + 安全 + 法务）
- 资产包含"收购遗留 / 跨品牌 / 影子"分类
- 可操作窗口（剩余天数 − 内部 SLA 缓冲）< 60 天
- 明示的强合规要求
- 单笔预算决策需走采购流程（≥ 2 周审批）

**其余情况选 🟡 Standard Path**。

---

## 设计原则（元原则）

> 本 Skill 最重要的不是"替用户做"，而是"**把高危操作的认知负担分层拆解，让每一层的人类 review 时间可预算、可完成**"。
>
> Agent 永远不是证书的所有者，只是**把证书决策表达出来的协作者**；
> 在信息不足时诚实发问，在用户违反 Harness 原则时诚实指出，仅此而已。

---

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=dimayip/cert-lifecycle-harness&type=Date)](https://star-history.com/#dimayip/cert-lifecycle-harness&Date)

---

> 本翻译可能并非 100% 准确，以 [英文版本](./README.md) 为准。

---

## License

除非单独文件另有说明，本仓库内容遵循 MIT License。详见 [`LICENSE`](./LICENSE)。
