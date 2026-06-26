---
purpose: references 目录索引 · 按需加载的深度规则文件清单
---

# References · 深度规则索引

> SKILL.md 主文件遵循 skill-creator 渐进披露原则保持 ≤ 500 行。
> 以下深度规则作为独立 reference 文件，由 SKILL.md 主文件按场景显式引用加载。
> Agent 在命中对应场景时**必须读取**这些文件后再执行。

---

## 按加载场景索引

| 文件 | 触发场景 | blocking | 关联自检项 |
|---|---|---|---|
| [`topology-detection.md`](./topology-detection.md) | Phase 1 · 需要识别 IP 是 CLB / CVM EIP / CDN 边缘 | ✅ 是 | G14 |
| [`wildcard-inventory.md`](./wildcard-inventory.md) | Phase 1 · 发现通配符证书（`*.example.com`） | ✅ 是 | G14 |
| [`cert-chain-verification.md`](./cert-chain-verification.md) | Phase 5 / Phase 6 · 换证书后的完整性验证 | ✅ 是 | L1 协议层证书链核查 |
| [`san-closure-discovery.md`](./san-closure-discovery.md) | Phase 1 · 多 SAN / 跨 zone 证书的闭包遍历 | ✅ 是 | — |
| [`dns-probing.md`](./dns-probing.md) | Phase 0-1 · 从 DNS 记录反推基础设施 | ✅ 是 | — |
| [`inquiry-protocol.md`](./inquiry-protocol.md) | 所有 Phase · 发问时选择档位 🔵/🟢/🟡/🔴 | ✅ 是 | G · 开场流程强制要求 |
| [`csr-persona-talks.md`](./csr-persona-talks.md) | Phase 2 · 需要向客户说明 CSR 生成策略 | ✅ 是 | G11, G12, G13 |
| [`cloud-api-naming.md`](./cloud-api-naming.md) | Phase 1+ · Agent 要调用某云厂商 API 时 | ⚪ 可选 | — |

---

## 使用指引

1. **Agent 侧**：SKILL.md 正文提到"详见 `references/XXX.md`"时必须加载对应文件后再继续
2. **人类 Review 侧**：这些文件是骨架的深度规则，review 时按需查阅
3. **维护侧**：所有版本号演进和历史印记集中在 `/CHANGELOG.md`，这些文件保持"当下即真理"的表述
