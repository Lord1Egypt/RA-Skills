---
purpose: cert-lifecycle-harness skill 的版本演进记录
maintained_by: skill-creator 优化流程
---

# Cert-Lifecycle-Harness · CHANGELOG

> 本文件集中记录 skill 的版本演进，使 SKILL.md 主文件保持"当下即真理"的干净表述。
> SKILL.md 正文不再夹带 `v0.3 新增 / v0.7 修正` 等版本印记。
> 需要追溯某条规则的历史动机时，请查本文件。

---

## v1.0.1 · 2026-04-28（运维增强 · 新增在线版本自检能力）

### 触发动机
Skill 的核心规则（拓扑识别、证书链核查 D1-D5、通配符盘点）会持续演进，但用户本地安装的版本可能滞后数月。
需要一个"提醒但不打扰"的版本自检机制，让用户随时知晓是否该更新。

### 主要变更

**新增**
- `scripts/version-check.sh`：静默的版本自检脚本
  - 读取本地 `SKILL.md` frontmatter `version` 字段
  - 调用 GitHub Releases API（`api.github.com/repos/dimayip/cert-lifecycle-harness/releases/latest`）拉取最新 tag
  - 用 `sort -V` 做语义版本对比
  - 本地 `scripts/.version-check-cache` 带 **24h TTL**，避免频繁打扰 GitHub
  - curl 硬超时 **3s**，网络失败 / API 限流 / 解析失败 **一律退出码 0**（铁律：绝不阻塞 Agent）
  - 输出机器可读 KEY=VALUE 字段：`CHECK_STATUS` / `LOCAL_VERSION` / `REMOTE_VERSION` / `UPDATE_CMD`

- SKILL.md §11.4：新增 **Phase 0.0 · 版本自检协议**
  - 定义 Agent 如何调用脚本、如何解析 4 种 `CHECK_STATUS`
  - 明确仅当 `needs_update` 时才在 Phase 0 首条回复开头**一次性**贴提醒
  - 明确 `offline` / `skipped` / 脚本失败全部**静默**处理，不制造对话噪音

**硬边界**
- ❌ 绝不因为版本检查失败就不回答用户问题
- ❌ 绝不追问用户"是否需要更新"（尊重用户处置权）
- ❌ 绝不在 Phase 1-6 重复贴提醒（仅 Phase 0 一次）
- ✅ 用户明确要求"帮我更新" → Agent 可以受托执行 `npx skills add ...`

**更新命令**
```
npx skills add https://github.com/dimayip/cert-lifecycle-harness
```

### 为什么版本号停在 v1.0.x 而非跳 v1.1
- 本次变更**不改变 SOP 语义**（所有 Phase 行为、发问协议、闸门逻辑都没变）
- 本次变更**不新增或删除任何规则**（只是加了一个"提醒自己更新"的运维脚手架）
- 属于"运维侧增强"，走 patch 号更贴切；跳 minor 号会暗示 SOP 有实质变化，误导使用者

### 与 v1.0 的兼容性
- 完全向后兼容：删除 `scripts/version-check.sh` 或断网都不影响原有 Phase 0-6 行为
- SKILL.md frontmatter `version` 字段保持 `1.0`，待正式发版 Release 时才跟 GitHub tag 对齐到 `v1.0.1`

---

## v1.0 · 2026-04-28（当前版本 · skill-creator 重构版）

### 重构目标
解决 v0.9.4 SKILL.md 臃肿问题（1327 行 / 80KB，严重违反 skill-creator 渐进披露原则）。

### 主要变更

**结构重组**
- SKILL.md 从 1327 行瘦身到 ≤ 500 行，仅保留决策流、触发规则、索引
- 新建 `references/` 目录，8 块深度规则作为独立文件按需加载：
  - `topology-detection.md`（基础设施拓扑识别）
  - `wildcard-inventory.md`（通配符子域盘点）
  - `cert-chain-verification.md`（证书链完整性 + 多客户端兼容性）
  - `san-closure-discovery.md`（SAN 闭包发现）
  - `dns-probing.md`（DNS 探针与基础设施反推）
  - `inquiry-protocol.md`（四档发问协议）
  - `csr-persona-talks.md`（CSR 三档选项与三档话术）
  - `cloud-api-naming.md`（跨云厂商 API 命名差异）

**章节重排**
- SKILL.md 章节编号改为连续的 1-14（原本 `0.0 / 0. / 0.3 / 0.4 / 0.5 / 0.1 / 0.2 / 1 / 2...` 非线性顺序）
- 新的主章节：
  1. 核心定位与元原则
  2. 证书有效期时代背景
  3. 复杂度分流（Fast / Standard / Full Path）
  4. 授权与写 API 闸门
  5. 技术-治理边界（α 严格版）
  6. 交付产物落盘原则
  7. Harness 硬约束 · 七问验收
  8. 发问协议与 CSR 策略
  9. 分层 Review 架构
  10. 脚本产物规范
  11. Agent 工作流 SOP
  12. 自检清单
  13. 反模式
  14. 文件加载策略

**版本印记剥离**
- SKILL.md 正文移除所有 `v0.x 新增 / v0.x 修正 / v0.x 补丁` 标签
- 历史版本动机集中到本 CHANGELOG.md

### 迁移兼容性
- 所有旧版本的规则**零信息损失**保留在 `references/` 和 `CHANGELOG.md` 中
- self-review-checklist.md 的 G1-G14 自检项保持不变
- `phases/` 和 `review-guides/` 保持不变
- 外部引用如 L1-runbook / L2-ADR 若引用了旧章节编号（`§0.3`、`§2.1`），新版 SKILL.md 在对应新章节（§3、§8）仍能被自然找到

---

## v0.9.4 · 2026-04-28（证书链完整性与多客户端兼容性核查）

### 触发案例
用户对 `jianxianexuetang.cn` 询问"是否更新完成"，Agent 初版只对比叶子证书指纹即宣告"已完成"，
被用户追问"为啥没对比证书链"，暴露 4 大盲区：中间证书缺失/过期 / 链条顺序 / Root CA 兼容性。

### 变更
- SKILL.md §0.3 新增附录"证书链完整性与多客户端兼容性核查规则"
  - 定义 D1-D5 五个核查维度
  - 明确本机 `Verification: OK` 与多客户端信任的作用域差异
  - 补全不同客户端（老 Android / 老 iOS / 微信 WebView / 老 IE）的信任库更新节奏
  - 定义降级路径（SSL Labs 不可达时的方案 A/B/C）
- `review-guides/self-review-checklist.md` 新增 C 类 L1 协议层证书链核查强制项
- `phases/06-verify-rollback-playbook.md` 六层验证矩阵 L1 协议层补齐 Full Chain 核查

→ v1.0 迁移：全部内容保留，改为 `references/cert-chain-verification.md`。

---

## v0.9.3 · 2026-04-27（基础设施拓扑识别 + 通配符子域盘点）

### 触发案例
两个案例接连暴露系统性盲区：

1. `jianxianexuetang.cn` 案例：Agent 仅凭 DNS TTL / Server Header / nc 端口探测就断言 "CVM EIP"，
   被用户纠正为 CLB。所有公开探测信号均被证明不可靠。
2. `w1.cas.sdo.com` 案例：Agent 发现通配符证书后，**用猜测子域名**（www/api/m/app/login）的方式探测绑定点。
   被用户纠正："应该从 WHOIS 找到 DNS 权威，引导提供完整 DNS Zone"。

### 变更
- SKILL.md §0.3 新增附录"基础设施拓扑识别规则"
  - 撤除 4 类不可靠探测信号（TTL / Server Header / nc OPEN / ALPN）
  - 明确唯一可靠方法：云厂商只读 API 或客户确认
  - Phase 1 开场强制询问只读云 API 凭证
- SKILL.md §0.3 新增附录"通配符证书子域名盘点规则"
  - 禁止猜测/枚举子域名
  - 正确路径：WHOIS → DNS 平台判断 → 引导提供完整 Zone
  - CT 日志仅作辅助，DNS Zone 才是权威来源
  - 海外线路盲区处理
- `review-guides/self-review-checklist.md` 新增 G14 自检项（双案例教训合并）

→ v1.0 迁移：拆分为 `references/topology-detection.md` 和 `references/wildcard-inventory.md`。

---

## v0.9.1 · 2026-04（多选项中性化）

### 变更
- 新增 G13 自检项：多选项决策（CA 选型 / CSR 策略 / 密钥算法）的选项语言必须中性化
- 禁止"默认/允许/兜底""首选/次选""推荐/可选"等暗示性词汇（除非走四段式推荐协议）
- 应使用"场景驱动推荐"——每个选项附"适用场景"而非"推荐等级"
- 若必须给推荐，必须同时给出"反向场景"（在什么情况下应选另一个）

→ v1.0 迁移：G13 保留在 self-review-checklist.md。

---

## v0.9 · 2026-04（CSR 生成策略三档选项 + 合规话术修正）

### 触发案例
发现 v0.7 及之前的"等保二级禁止第三方 KMS 生成密钥"等话术属于事实错误，
导致 Agent 对客户选"云厂商在线生成"时错误劝退。

### 变更
- SKILL.md §2.2 新增"CSR 生成策略三档选项"
  - A 本地 openssl（默认推荐）
  - B 云厂商在线生成（允许选项）
  - C 复用旧 CSR（受限场景）
  - 三档话术：面对老板 / 安全 / 运维
- 新增 G11 自检项：交付物必须同时提供 A/B/C 三档执行入口
- 新增 G12 自检项：合规话术边界（修正 v0.7 过度断言）

→ v1.0 迁移：拆分为 `references/csr-persona-talks.md`，G11/G12 保留在 self-review-checklist.md。

---

## v0.8 · 2026-03（交付产物必须落盘）

### 触发案例
早期 Agent 把交付物作为"对话内嵌代码块"呈现，紧急场景下用户来不及复制粘贴+新建文件+chmod。

### 变更
- SKILL.md §0.5 新增"交付产物必须落盘原则（硬约束）"
- 三份 Review 必须是独立的 `.md` 文件
- 所有 `.sh` 脚本必须作为可执行文件落盘在 `scripts/` 子目录
- 交付目录必须有顶层 `README.md` 作为总入口
- 新增 G10 自检项

→ v1.0 迁移：主体保留在 SKILL.md §6 交付产物落盘原则。

---

## v0.7 · 2026-03（技术-治理边界 α 严格版 · 证书时代背景）

### 变更
- SKILL.md §0.0 新增"证书有效期时代背景"
  - CA/B Forum 四阶段压缩时间表（398 → 200 → 100 → 47 天）
  - "多年期证书"的真相（改为"多年期订阅"）
  - 完成缓冲默认值（α 分档 · 不主动问客户）
- SKILL.md §0.4 新增"技术-治理边界原则（α 严格版）"
  - Agent 不主动询问治理节奏字段（采购周期 / 法务 / OA / 预算金额）
  - 部署规模通过 DNS/CT 推断（而非裸问客户"几台机器"）
- 新增 G8（治理越权自检）、G9（证书时代背景自检）

→ v1.0 迁移：§0.0 保留为 §2，§0.4 保留为 §5。

---

## v0.6 · 2026-02（四档发问协议 · 开场流程强制）

### 变更
- SKILL.md §2.1.1 新增"四档发问协议"
  - 🔵 陈述式 / 🟢 假设式 / 🟡 推荐式 / 🔴 裸问式
  - 档位选择决策流
  - Phase 0 开场必须先跑公开数据踩点，再按档位分级发问

→ v1.0 迁移：拆分为 `references/inquiry-protocol.md`。

---

## v0.5 · 2026-01（复杂度分流 · cert_role · 影子证书溯源）

### 变更
- SKILL.md §0.3 新增"复杂度自评估与路径分流"（Fast / Standard / Full Path）
- 新增 cert_role 维度（edge / origin / internal / mtls-server / mtls-client）
- 新增影子证书溯源工作流
- 新增 SAN 极少时的反向扩展启发式
- 新增部分授权阻塞的降级策略
- 新增 G1-G7 自检项

→ v1.0 迁移：分流协议保留在 SKILL.md §3，cert_role 与影子证书迁移至 `references/san-closure-discovery.md`。

---

## v0.4 · 2025-12（SAN 闭包发现）

### 变更
- SKILL.md §0.1 新增"SAN 闭包发现（证书 ↔ 域名图遍历）"
  - 图遍历迭代直到不动点
  - 收敛条件与边界（≤ 3 轮 / ≤ 5 zone / 软上限 10 证书）
  - 通配符展开分层规则
  - 跨 zone 闭包硬边界
  - 新发现的批量呈现格式

→ v1.0 迁移：`references/san-closure-discovery.md`。

---

## v0.3 · 2025-11（DNS 探针能力）

### 变更
- SKILL.md §0.1 新增"DNS 探针与基础设施反推"
  - 能力：DNS 记录 → 基础设施事实映射
  - 作用域原则（按证书作用域定向查询）
  - 透明度原则（证据 + 推断 + 请确认）
  - 隐私自律硬边界

→ v1.0 迁移：`references/dns-probing.md`。

---

## v0.2 · 2025-10（API 操作三级授权模型）

### 变更
- SKILL.md §0.1 新增"API 操作三级授权模型"
- SKILL.md §0.2 新增"写 API 的三档分级与六条闸门"（Import / Modify / Delete）
- 六条闸门（F0-F7 自检项）

→ v1.0 迁移：保留在 SKILL.md §4 授权与写 API 闸门。

---

## v0.1 · 2025-09（初版）

### 范围
- 核心定位：Agent = 安全员 + 文档工程师 + 受托执行人
- Harness 硬约束 · 七问验收（HP-1 ~ HP-7）
- 分层 Review 架构（L1 / L2 / L3）
- 信息等级与发问协议（🟢 通用知识 / 🟡 场景常识 / 🔴 客户特定信息）
- 脚本产物规范（TEMPLATE 结构）

→ v1.0 迁移：核心骨架保留在 SKILL.md §1 / §7 / §8 / §9 / §10。
