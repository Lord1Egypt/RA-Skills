---
phase: 6
name: verify-rollback-playbook
purpose: Phase 6 验证与回滚方法论（基线采集 / TTL 对齐 / 时间窗标定 / 回滚粒度分级 / 降级路径 / 短周期适配）
parent: ../SKILL.md
updated: 2026-04-23
---

# ✅ Phase 6 · 验证与回滚 Playbook

> Phase 6 不是"换完证书 curl 一下看返回 200"，而是**6 层验证矩阵 + 分级回滚触发器 + 过渡期长度科学标定**。

---

## 1. 六层验证矩阵

| 层 | 验证项 | 工具 / 指标 | 合格阈值 |
|----|--------|-----------|---------|
| **L1 协议层** | TLS 握手 **+ Full Chain 完整性** | `openssl s_client -showcerts` / `sslyze` | 100% 节点返回新证书指纹 **且** 链条完整（详见 §11）|
| **L2 应用层** | HTTPS 业务请求 | `curl -sw %{http_code}` + 业务关键接口 | 2xx/3xx ≥ 99.9% 持续 {{T}} min |
| **L3 观测层** | CDN/LB 监控 | 云监控 SSL 握手失败率、4xx/5xx | 无异常尖刺 |
| **L4 客户端** | 真实 UA 采样 **+ 多客户端兼容性评级** | RUM / CDN 日志 TLS 版本分布 **+ SSL Labs 外部评级** | 与基线一致（见 §2）**且** SSL Labs ≥ A 级（详见 §11）|
| **L5 CT 日志** | 新证书已公开 | crt.sh 查询 | 能查到且 precert 已落 |
| **L6 合规** | 旧证书吊销状态 | OCSP / CRL | 仅在过渡期结束后吊销 |

> 📌 **cert_role 对 L1-L6 的裁剪**：
> - `edge` cert_role → L1-L6 全部验证
> - `origin` cert_role → 只验证 L1（回源握手）+ L3（CDN 回源监控），**跳过 L4/L5**（终端看不到）
> - `internal` cert_role → 只 L1+L2+L3（内网链路）
> - `mtls-*` cert_role → 双端验证，且加 "**客户端证书链完整性**" 这一项

---

## 2. 基线对照方法

### 为什么需要基线

L4 "与基线一致" 意味着"变更前后对比"。但**基线何时采集、存在哪里、如何对比**？骨架必须明文规定。

### 采集时机

Phase 5 Dry-Run 阶段**同步采集**各层基线，落盘到变更证据包（change evidence bundle）：

```
change-evidence-bundle/
├── baseline/
│   ├── L1-tls-handshake.txt      # Phase 5 时 openssl s_client 输出
│   ├── L2-business-probes.txt    # 关键接口成功率采样
│   ├── L3-monitoring.png         # CDN/LB 监控截图
│   ├── L4-client-ua-dist.csv     # 一周 TLS 版本分布
│   └── L5-ct-precheck.txt        # 变更前的 CT log 状态
└── post-change/
    └── [变更后对应文件 · Phase 6 采集]
```

### 对比方法

```bash
# L1 对比
diff baseline/L1-tls-handshake.txt post-change/L1-tls-handshake.txt
# 期望：仅证书指纹/有效期差异，其他一致

# L4 对比（容忍 ±5% 偏差）
compare-tls-version-dist.sh baseline post-change
```

### 基线存储

- 客户内部文档系统 / 工单系统附件
- 本次变更的独立目录（按变更单号命名）
- **保留期**：至少 1 年（SOC 2 / 等保审计需要）

---

## 3. 等待时长参考表

不同验证层有不同的**合理等待时长**，Agent 不应凭感觉写数字：

| 验证对象 | 等待依据 | 最小等待 | 推荐等待 |
|---------|---------|---------|---------|
| **CDN 回源连接池** | 连接池 TTL（通常 5 min）| 10 min | 15 min |
| **CDN 边缘缓存** | 边缘缓存 TTL（视配置，通常 30 min - 24 h）| 配置 TTL × 2 | 同左 |
| **DNS 缓存传播** | 最长 DNS TTL + 递归缓存 | 最长 TTL | 最长 TTL + 2 h |
| **OCSP Stapling** | 服务端 stapling 刷新周期（默认 1-24 h）| 1 h | 4 h |
| **客户端 OCSP 缓存** | 浏览器 / 客户端缓存（通常 1-7 天）| 无法缩短 | 分阶段吊销 |
| **CT log 落账** | Google/Apple CT log 刷新 | 1 h | 2 h |
| **浏览器 UA 采样（L4）** | RUM 采样周期 + 业务低峰 | 24 h | 48-72 h |

---

## 4. 回滚触发器分级

### 回滚粒度分级

| 级别 | 范围 | 决策权 | 举例 |
|------|------|-------|------|
| **L0 无操作** | — | — | 观察继续，不做回滚 |
| **L1 单节点** | 1 个绑定点 | SRE 自决 | 1 个 CDN 边缘异常，跳过继续其他 |
| **L2 批次** | 1 批（本轮推送的节点组） | SRE + 主管 | 一批 3 个节点全异常 |
| **L3 zone 级** | 1 个 DNS zone 内全部节点 | L2 策略层 | 整个 zone 的 FQDN 都异常 |
| **L4 资产分类级** | A/B/C/D/E 其中一类的全部 | L2 策略层 | C 类收购遗留资产全部异常 |
| **L5 全局资产** | 本次变更涉及的所有节点 | L3 决策层 | 新证书本身有问题 |
| **L6 方案重规划** | 回到 Phase 4 重做 | L3 决策层 + CTO | CA 签发就出错 |
| **L7 中止迁移保留旧证书续签** | 不换 CA，老证书找 CA 应急续一张 | L3 + 财务 | 过期迫在眉睫但新证书无法如期签发 |

### 粒度选择的判定规则

```
失败范围 ≤ 1 个节点 → L1
失败范围 = 1 批（按 Dry-Run 规划的批次）→ L2
失败蔓延 2+ zone → L3
失败跨资产分类 → L4（考虑 L4 是否因分类共性而集中）
新证书本身故障（OCSP / CT 异常）→ L5
CA 签发就错 → L6
签发延期超出过期日 → L7（最后兜底）
```

---

## 5. 时间窗口标定方法

Phase 6 的回滚触发器常含"持续 X 分钟"阈值，X 不应凭感觉定。

### 标定公式

```
X = max(监控采样周期 × 3, DNS TTL / 2, 业务 SLA 宽容窗口)
```

### 标定依据

| 因子 | 数据来源 |
|------|---------|
| 监控采样周期 | 监控系统配置（如 Prometheus 30s / 1 min）|
| DNS TTL | Phase 1 采集的 zone 配置 |
| 业务 SLA 宽容窗口 | 客户 intake §2.2（99.9% = 43.2 min/月 / 99.95% = 21.6 min/月 / 99.99% = 4.3 min/月）|

### 示例

```
F1 客户 SLA 99.9%，监控采样 1 min，DNS TTL 300s

X = max(1 × 3, 300/120, 43.2) = max(3, 2.5, 43.2) = 43.2 分钟
→ 过于宽松（因 SLA 已累积）

实战推荐：X = max(监控采样 × 3, DNS TTL / 2, 3 min) = 3 min
```

> Agent 应输出标定过程，让客户看懂"为什么是 X 分钟而不是 5 分钟"。

---

## 6. TTL 对齐验证时刻表

跨 zone / 多 DNS 商场景，不同 zone 的 TTL 可能差别极大：

```
DNSPod 默认 TTL: 600s
阿里云万网默认 TTL: 3600s
自建 BIND 可能 TTL: 86400s（老服务器遗留）
```

若按最短 TTL 验证 → 漏掉最长 TTL zone 还在吃旧缓存。

### TTL-aligned Validation Schedule

```markdown
## TTL 对齐验证时刻表

| Zone | TTL | 变更时刻 | 预计全量传播 | 验证完成时刻 |
|------|-----|---------|-------------|-------------|
| example.com | 600s (10 min) | T0 | T0 + 10 min | T0 + 2 h |
| example.cn | 3600s (1 h) | T0 | T0 + 1 h | T0 + 2 h |
| legacy.example.com.cn | 86400s (24 h) | T0 | T0 + 24 h | T0 + 26 h |

**真正"验证完成"时刻 = max(各 zone 完成时刻) = T0 + 26 h**
```

> ⚠️ 若不能等到最长 TTL 过期，应**先改短 TTL**（变更前 2 × TTL 时间）。

---

## 7. 降级路径（Fallback Mode Switching）

> 回滚不只是"回到上一个状态"，还应支持"**降级到更原始但更可靠的状态**"。

### 降级路径示例

| 故障场景 | 降级方向 |
|---------|---------|
| acme.sh 脚本崩 | 退回到手动 SCP 部署 + 邮件告警 |
| cert-manager Operator 异常 | 退回到手工 K8s Secret 更新 |
| Vault 拉密失败 | 退回到一次性临时 token（事后轮换）|
| 自动化批量部署失败 | 退回到逐节点手动验证 + 手动部署 |

### 降级原则

1. **先降级，后复盘**：不在故障现场调试自动化，先用最原始方式恢复业务
2. **降级要留痕**：记录降级的时间、范围、原因
3. **降级不是"永久"**：故障复盘后恢复自动化

---

## 8. 短周期证书的过渡期公式（按 CA/B Forum 节奏）

> ⚠️ **时代背景**：2026-03-15 起公信证书最长 200 天，2027 起 100 天，2029 起 47 天。
> "1 年证书"/"3 年证书"概念已不存在于公信 PKI，详见 `SKILL.md §0.0`。

### 按有效期分档的旧证书保留期与过渡期

| 单张证书有效期 | 旧证书建议保留期 | 过渡期公式 | 说明 |
|---|---|---|---|
| **≤ 398 天**（2026-03-15 前存量）| **≥ 14 天** | `max(14天, 监控采样×10, RUM采样周期)` | 覆盖一个工作周 + 安全缓冲；对应 HP-4 |
| **≤ 200 天**（2026-03-15 起主流）| **≥ 7 天** | `max(7天, 监控采样×10, RUM采样周期)` | 有效期缩短，保留期等比压缩 |
| **≤ 100 天**（2027-03-15 起）| **≥ 5 天** | `max(5天, 监控采样×10, RUM采样周期)` | 续签频率 ≥ 4次/年，保留期需再压缩 |
| **90 天**（Let's Encrypt / ACME）| **≥ 3 天** | `max(3天, 监控采样×10, RUM采样周期)` | ACME 场景通常全自动，3天已足够 |
| **≤ 47 天**（2029-03-15 起）| **≥ 2 天** | `max(2天, 监控采样×10, RUM采样周期)` | 近乎全自动化节奏，**必须 ACME**，人工不可行 |

### 过渡期长度决策因子

| 因子 | 长周期（≥200天）权重 | 短周期（≤100天）权重 |
|------|-----------|----------|
| 业务周期（日/周/月批）| 高 | 低 |
| 客户端缓存 TTL | 高 | 中 |
| 合作方切换节奏 | 高 | 中 |
| CA 吊销响应时延 | 中 | 中 |
| 证书本身有效期 | 中 | **高（因占比敏感）** |

### 自动化紧迫性提示

当客户当前证书有效期 ≤ 200 天时，Agent 应在 L3 交付物中附注：

```
⚠️ 当前证书有效期 ≤ 200 天（CA/B Forum SC-081 已生效）。
   每年需续签 ≥ 2 次；2027 年起 ≥ 4 次；2029 年起 ≥ 8 次。
   强烈建议本次续签完成后立即评估 ACME 自动化方案，
   否则手动续签将在 1-2 年内成为不可持续的运维负担。
```


---

## 9. 回滚触发器产物格式

```markdown
## Rollback Triggers v1.0

| # | 条件 | 持续时长标定 | 回滚粒度 | 权责 |
|---|------|-------------|---------|------|
| T1 | 单节点 L2 失败 | 3 min（标定见 §5）| L1 单节点 | SRE 自决 |
| T2 | 2+ 节点同时异常 | 3 min | L2 批次 | SRE + 主管 |
| T3 | 整个 zone 异常 | 5 min | L3 zone 级 | L2 策略 |
| T4 | CT log 异常 / OCSP 异常 | 立即 | L5 全局 | L3 决策 |
| T5 | 合作方投诉 | 立即 | L5 或 L4（看影响面）| L3 决策 |
| T6 | CA 签发超时未出 | 依签发 SLA | L6 重规划 | L3 决策 |
| T7 | 过期日将到但新证书仍未签 | 倒计时 7 天 | L7 保留旧 + 应急续 | L3 + 财务 |
```

---

## 10. 相关文件

- [`05-dry-run-matrix.md`](./05-dry-run-matrix.md) — Phase 5 基线采集的输入
- [`04-planning-playbook.md`](./04-planning-playbook.md) — 方案选定影响验证粒度
- [`02-scope-lock-and-reflow.md`](./02-scope-lock-and-reflow.md) — cert_role 决定验证层裁剪
- [`../review-guides/L1-execution-review.md`](../review-guides/L1-execution-review.md) — Review 产物落地

---

## 11. 证书链完整性与客户端兼容性核查（硬项）

> **核心教训（来自 jianxianexuetang.cn 案例）**：
> 只比对"叶子证书指纹是否一致"**无法**发现以下 4 类故障，但任何一类都会让浏览器直接报错：
> 1. 中间证书缺失（服务端未下发完整链）
> 2. 中间证书过期（独立于叶子有效期）
> 3. 链条顺序错误（叶子在后 / 中间在前）
> 4. Root CA 不被某些客户端信任（老 Android / 老 iOS / IoT）
>
> 本节将"证书链完整性"与"多客户端兼容性"列为 **L1/L4 层的强制子项**，替换之前"只看指纹"的做法。

### 11.1 Full Chain 完整性核查（L1 强制子项）

**核查项**：

| # | 核查项 | 工具 | 合格阈值 |
|---|-------|------|---------|
| L1.1 | 叶子证书指纹一致 | `openssl x509 -fingerprint -sha256` | 与预期一致 |
| L1.2 | **服务端下发链条长度** | `openssl s_client -showcerts \| grep -c "BEGIN CERTIFICATE"` | 通常为 2（叶子 + 中间），单张（仅叶子）= ❌ |
| L1.3 | **中间证书 Subject 与叶子 Issuer 匹配** | 对比两张证书的 Subject / Issuer | 必须逐级对应 |
| L1.4 | **链条顺序正确** | `openssl s_client -showcerts` 输出的 `0:` `1:` 顺序 | 叶子（0）在前，中间（1）在后 |
| L1.5 | **中间证书有效期覆盖本次变更** | `openssl x509 -noout -dates` 读中间证书 | Not After > 本次证书有效期末 |
| L1.6 | **OpenSSL 官方 verify** | `openssl s_client -verify_return_error` | `Verification: OK` |
| L1.7 | **服务端未发送 Root 证书**（最佳实践）| 链条长度 = 2 而非 3 | 发 Root 是反模式（浪费带宽 + 对安全无贡献）|

**标准核查脚本**（Agent 应在 Phase 6 Runbook 中内置）：

```bash
#!/bin/bash
# full-chain-verify.sh - 证书链完整性核查
# 用法: ./full-chain-verify.sh <domain> [<port>]

DOMAIN="${1:?usage: $0 <domain> [<port>]}"
PORT="${2:-443}"
OUT=$(mktemp)

echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:$PORT" -showcerts 2>/dev/null > "$OUT"

echo "=== L1.2 链条长度 ==="
COUNT=$(grep -c "BEGIN CERTIFICATE" "$OUT")
echo "服务端下发证书数: $COUNT"
[ "$COUNT" -lt 2 ] && echo "❌ 中间证书缺失（仅下发叶子）" && exit 1

echo "=== L1.3/L1.4 链条结构 ==="
sed -n '/Certificate chain/,/---/p' "$OUT"

echo "=== L1.6 OpenSSL 官方 verify ==="
grep -E "Verify return code|Verification" "$OUT"

echo "=== L1.5 中间证书有效期 ==="
awk '/-----BEGIN CERTIFICATE-----/{n++} n==2' "$OUT" \
  | awk '/-----BEGIN CERTIFICATE-----/{p=1} p{print} /-----END CERTIFICATE-----/{p=0; exit}' \
  | openssl x509 -noout -subject -issuer -dates

rm -f "$OUT"
```

### 11.2 多客户端兼容性核查（L4 强制子项）

**问题**：本机 `openssl verify = OK` 只代表**本机信任库**（通常是 macOS/Linux 最新版）信任，**不代表**所有终端客户端都信任，尤其是：

| 客户端 | 潜在风险 | 典型场景 |
|-------|---------|---------|
| Android ≤ 7.1 | 信任库停更，新 Intermediate CA 可能不在内 | 下沉市场 / 低端机用户 |
| iOS ≤ 12 | 同上 | 老设备用户 |
| 微信内置 WebView（老 Android）| 依赖系统信任库 | 大量 H5 / 小程序 |
| 老 IE / 某些 IoT 设备 | 信任库自 2017 前停更 | 企业内网 / 工控设备 |
| Java ≤ 8u161 | 旧 JDK 默认信任库 | 内部 Java 服务调用 |

**核查工具**（按可靠性排序）：

| # | 工具 | 覆盖范围 | 执行方式 |
|---|------|---------|---------|
| L4.1 | **SSL Labs** | 浏览器 + 主流客户端矩阵 | `https://www.ssllabs.com/ssltest/analyze.html?d=<domain>` |
| L4.2 | **Hardenize** | 兼容性 + 安全配置 | `https://www.hardenize.com/report/<domain>` |
| L4.3 | **ImmuniWeb SSL Security Test** | 合规（PCI-DSS / NIST / HIPAA）| `https://www.immuniweb.com/ssl/?id=<domain>` |
| L4.4 | **自建多 JDK / 多 Android 测试** | 企业专属客户端 | 内部 CI（按 cert_role `mtls-*` 场景必做）|

**合格阈值**：

```
SSL Labs 评级 ≥ A
客户端矩阵 "Trusted" 栏对主流客户端（Chrome / Firefox / Safari / Edge / 主流 Android / 主流 iOS）均为 ✓
如存在 ✗，必须在 L3 决策层显式说明受影响客户端比例（可从 RUM / CDN 日志估算）
```

### 11.3 cert_role 对 §11 核查的裁剪

| cert_role | L1 Full Chain | L4 多客户端兼容性 |
|-----------|--------------|------------------|
| `edge` | ✅ 必做 | ✅ 必做（终端看到）|
| `origin` | ✅ 必做（CDN 回源也走 TLS 握手）| ❌ 跳过（只有 CDN 回源看到，CDN 信任库通常足够新）|
| `internal` | ✅ 必做 | 🟡 按内网客户端清单定向测试（不必跑 SSL Labs 外部评级）|
| `mtls-server` / `mtls-client` | ✅ 必做 + **客户端证书链完整性** | ✅ 必做（且要核对 mTLS 双端 JDK / Go / Python 版本兼容性）|

### 11.4 变更证据包（change evidence bundle）新增项

`change-evidence-bundle/` 目录下新增：

```
baseline/
├── L1-full-chain.txt          # 变更前的完整链条输出（新增）
└── L4-ssl-labs-baseline.json  # 变更前 SSL Labs 评级快照（新增）

post-change/
├── L1-full-chain.txt          # 变更后链条对比（新增）
└── L4-ssl-labs-post.json      # 变更后 SSL Labs 评级（新增）
```

**对比方法**：

```bash
# L1 链条结构对比
diff <(sed -n '/Certificate chain/,/---/p' baseline/L1-full-chain.txt) \
     <(sed -n '/Certificate chain/,/---/p' post-change/L1-full-chain.txt)
# 期望：仅叶子证书指纹差异，链条结构 / 中间证书 Issuer 一致（除非本次变更就是换 CA）

# L4 SSL Labs 评级对比
jq '.endpoints[].grade' baseline/L4-ssl-labs-baseline.json
jq '.endpoints[].grade' post-change/L4-ssl-labs-post.json
# 期望：不降级（原 A+ 不能变 A；原 A 不能变 B）
```

### 11.5 反模式（不要做）

| ❌ 反模式 | ✅ 正确做法 |
|----------|-----------|
| 只比对叶子证书指纹，宣告"已完成更新" | 至少加 L1.2-L1.6 六项 Full Chain 核查 |
| 本机 `openssl verify = OK` 就宣告兼容性通过 | L4 必须跑外部评级工具（SSL Labs / Hardenize）|
| 发现 SSL Labs 降级就回滚 | 先核对降级原因（可能是 CA/B 新规导致的评分标准变化），再决定 |
| 对 `origin` cert_role 也跑 SSL Labs | 按 §11.3 裁剪表，`origin` 跳过 L4 外部评级 |
| 忽视"服务端发送 Root"的反模式 | 提醒客户修正服务端证书配置（Root 不应下发）|

### 11.6 与 §1 六层验证矩阵的关系

§11 是对 §1 L1 / L4 两层的**硬项扩展**，不是新增第 7 层：

- L1 协议层 = 叶子指纹（原）+ Full Chain 核查（§11.1）
- L4 客户端层 = RUM 采样（原）+ 外部评级（§11.2）

