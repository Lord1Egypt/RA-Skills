---
purpose: DNS 探针与基础设施反推能力（从只读 DNS 记录反推 CDN / 源站云厂 / CA 偏好 / ACME 现状）
loaded_by: SKILL.md §3 Phase 1 资产盘点按需引用
blocking: true
---

# DNS 探针与基础设施反推

> 客户的 DNS 记录是"基础设施反向探针"：一组只读记录，可在客户"什么都没说"的情况下
> 阐明许多结构性事实。本文档定义探针的**能力、作用域、透明度、隐私自律**。

---

## 1. 能力：DNS 记录 → 基础设施事实映射（示意，不全）

| DNS 观测 | 能反推出的事实（仅示意，必须由客户确认）|
|---|---|
| `CNAME` 指向某云厂商的 CDN 域 | 客户可能在用该厂商 CDN |
| `CNAME` 指向 ELB/CLB/SLB 类域 | 源站可能在该厂商 |
| `A` 指向公网 IP | 结合 IP 段归属可推源站平台 |
| `CAA` 记录 | 现有 CA 偏好和限制 |
| `_acme-challenge` TXT 存在 | 已有 ACME 自动化流水线 |
| `NS` 记录 | DNS 托管在哪家（可能与资源云不同店）|
| `MX` 记录 | 邮件服务商（可能有独立证书）|

> ⚠️ 上表**仅为推理线索**，绝不能当结论直接写进 L2/L1 交付物。
> 每一条推断都必须按 "证据 + 推断 + 请确认" 的格式呈现给用户。

---

## 2. 作用域原则（N2′：按证书作用域定向查询）

Agent 查询 DNS 记录时，默认作用域**严格由当前证书场景决定**，
绝不因为拿到全 zone 只读权限就扩大窥探面：

| 证书上下文 | DNS 探针作用域 | 不进入作用域 |
|---|---|---|
| 单域证书 `api.domain.com` | 仅查 `api.domain.com` + `domain.com` 的 CAA | `www.*` / `mail.*` 等兄弟子域 |
| 通配符 `*.api.domain.com` | 查 `api.domain.com` 及其所有子域 | `domain.com` 顶级、兄弟分支 |
| 多 SAN `a.d.com, b.d.com` | 查清单内每个 FQDN + 其直接父域（CAA 用）| 清单外子域 |
| 顶级通配 `*.domain.com` | 查 `domain.com` zone 全貌是合理的 | — |
| 客户明示"统一盘点整个 zone" | 查 zone 全貌 | — |

---

## 3. 透明度原则（M1-b：明示推理）

- Agent 查询前**先明示**："我将查询以下 FQDN 的 A/AAAA/CNAME/CAA/TXT 记录：[列表]"
- Agent 对每条从 DNS 反推的基础设施结论，必须按格式呈现：

```
【证据】  api.domain.com CNAME → xxx.cdn.dnsv1.com
【推断】  你们可能在用该厂商的 CDN
【请确认】是否正确？如有多可用/分阶段使用等特殊情况请补充。
```

- 不用 DNS 推断结果隐式推进 Phase 2，所有推断在用户确认前均标记为【待确认】

---

## 4. 隐私自律硬边界

- 即使拥有全 zone 只读权限，Agent 也**不主动列出**与证书无关的子域（如 `hr.*` / `finance.*` / `internal.*`）
- 客户可以明示扩大作用域（如 "也帮我看看 mail 域"），Agent 才可进入
- DNS 写 API（Modify Record / Delete Record / ACME DNS-01）**当前不纳入受托执行范围**，仅生成脚本交客户执行
