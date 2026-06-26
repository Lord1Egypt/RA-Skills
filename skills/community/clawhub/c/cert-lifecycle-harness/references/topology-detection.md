---
purpose: 基础设施拓扑识别规则（CLB / CVM EIP / CDN 边缘 IP 区分）
loaded_by: SKILL.md §3 Phase 1 拓扑识别章节按需引用
blocking: true
---

# 基础设施拓扑识别规则

> **核心教训**：公开网络探测**无法可靠区分** CLB VIP / CVM EIP / CDN 边缘 IP。
> 不靠谱的探测信号已在下表明确撤除。

---

## 1. 不可靠的探测信号（禁止作为拓扑判断依据）

| 探测信号 | ❌ 错误用法 | 原因 |
|---|---|---|
| DNS TTL 值 | "TTL=600 → CVM EIP，TTL=60 → CLB" | TTL 由用户在 DNS 控制台自由配置，与 CLB/CVM 无关 |
| `Server: nginx/版本号` | "带版本号 → CVM EIP，无版本号 → CLB" | CLB 七层模式会透传后端 Server 头，版本号照样出现 |
| `nc` 端口探测 OPEN | "端口 OPEN → 服务存在" | CLB 安全组 / 端口映射可导致 TCP 握手成功但无服务响应，OPEN ≠ 服务存在 |
| TLS ALPN 协商结果 | "No ALPN → CVM EIP" | CLB 配置差异可导致不同结果，不稳定 |

---

## 2. 唯一可靠的识别方法（按优先级）

```
优先级 1（零歧义）：云厂商只读 API
  腾讯云：DescribeLoadBalancers + DescribeInstances
  阿里云：DescribeLoadBalancers + DescribeInstances
  AWS：   DescribeLoadBalancers + DescribeInstances

优先级 2（客户确认）：直接问客户
  "X.X.X.X 是 CLB VIP 还是 CVM EIP？"

优先级 3（有限参考）：以下信号有一定参考价值但不能单独作为结论
  ✅ 响应头含 X-Forwarded-For（非业务注入）→ 倾向 CLB 七层模式
  ✅ CNAME 指向已知 CLB/CDN 域名后缀 → 倾向 CLB/CDN
  ✅ IP 归属 ASN 可确认云厂商（但 CLB/CVM 都在同一 ASN）
```

---

## 3. Phase 1 开场强制动作

Agent 在 Phase 1 第一个发言时，**必须主动询问**：

> 🔴【必问】能否提供腾讯云/阿里云/AWS 的只读 SecretID/Key（或临时 STS token）？
> 我可以调用 `DescribeLoadBalancers` + `DescribeInstances` 直接确认基础设施拓扑，1 分钟出结论，零歧义。
> 所需最小权限：只读（`Describe*` 类，无写权限）。
> 如不方便提供，请直接告诉我 IP 是 CLB VIP 还是 CVM EIP。

---

## 4. nc 探测结果的正确用法

```
nc 端口 OPEN → 只能说明"TCP 连接可建立"
nc 端口 OPEN + curl/openssl 有 HTTP/TLS 响应 → 才能说明"服务存在"
nc 端口 OPEN + curl/openssl 无响应 → 可能是 CLB/防火墙 TCP 透传但无后端服务
```

---

## 5. Agent 硬边界

```
✅ 必须做：
- 任何拓扑判断都必须标注判断依据（API / 客户确认 / 有限参考信号）
- 仅靠"有限参考信号"得出的结论必须以 🟢 假设式呈现（【假设】...【如有错请纠正】）
- Phase 1 开场必问只读云 API 凭证

❌ 严禁做：
- 仅凭 TTL / Server Header / nc / ALPN 任一信号断言 CLB vs CVM EIP
- 将"nc OPEN"写入资产清单当作"服务存在"的证据
- 把公开探测的低置信度结论以 🔵 陈述式呈现
```

---

## 6. 自检对应项

本文件的规则落到自检清单的 **G14 基础设施拓扑识别 + 通配符证书子域名盘点自检**，
见 `review-guides/self-review-checklist.md` G14 条目。
