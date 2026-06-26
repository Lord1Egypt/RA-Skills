---
phase: 5
name: dry-run-matrix
purpose: Phase 5 干跑演练矩阵（按绑定点类型的演练方法库 + 成本清单 + 审批节点 + 跨团队协调演练）
parent: ../SKILL.md
updated: 2026-04-23
---

# 🧪 Phase 5 · Dry-Run 矩阵

> Phase 5 的"演练"不是"假装操作一遍"，而是**用最接近生产的方式把每一类绑定点的部署-回滚流程跑通**，同时验证**协调、审批、成本**三个非技术维度。

---

## 1. Dry-Run 方法库（按绑定点类型）

每个绑定点类型对应一条演练路径。所有演练都使用**测试证书**（不影响生产）。

| 绑定点类型 | Dry-Run 方法 | 测试证书来源 | 典型耗时 |
|-----------|-------------|-------------|---------|
| **CDN 边缘（通用）** | 选 1 个低流量子域，用测试证书走上传+绑定+回滚完整流程 | LE staging / 自签 | 30 min |
| **CLB / ALB 监听器** | 预发 CLB 上用测试证书验证 API 调用和滚动更新 | LE staging / 自签 | 20 min |
| **K8s Ingress（cert-manager）** | 在测试 namespace 创建 Certificate 资源 + staging issuer | LE staging | 15 min |
| **K8s Secret（手工）** | 创建测试 Secret → 更新 Ingress ref → 验证 TLS 握手 → 回滚 | 自签 | 15 min |
| **Nginx（ssl_certificate）** | reload 热切换测试，验证配置解析 + 证书链加载 | 自签 | 10 min |
| **Java JKS** | SSH 备份 → 导入测试证书 → 热重载（信号要客户确认）→ 回滚 | 自签（导成 PKCS12）| 40 min |
| **PFX / IIS** | PowerShell 备份 → Import-PfxCertificate → IIS reset → 回滚 | 自签 | 30 min |
| **API 网关自定义域名** | 绑定测试域名走签名验证链路 | LE staging | 25 min |
| **mTLS 服务端** | 双端同步演练（服务端 + 客户端）必须同步换 | LE staging 双端 | 1 h |
| **mTLS 客户端** | 同上 | 同上 | 同上 |

### 测试证书来源选择

| 来源 | 免费 | 签发快 | 与生产 CA 一致 | 适用 |
|------|-----|-------|--------------|------|
| **LE staging** | ✅ | ✅（秒级）| ❌ | 结构性演练（Nginx 解析 / 链加载 / 部署 API 调通）|
| **自签证书** | ✅ | ✅（秒级）| ❌ | 内网 mTLS / Java JKS 导入 / keytool 流程 |
| **生产 CA 的 staging / test order** | ⚠️ 按 CA 政策 | 视 CA 而定 | ✅ | 需验证 "CA 签发流程本身" 时 |

---

## 2. Dry-Run 成本清单

| CA | staging / test | 成本 | 备注 |
|----|--------------|------|------|
| Let's Encrypt | ✅ 免费 staging | 0 元 | `https://acme-staging-v02.api.letsencrypt.org` |
| ZeroSSL | ✅ 免费 staging | 0 元 | 测试环境 |
| DigiCert | ⚠️ 按合同 | 视合同 | 企业客户常有 test order 额度；个人/小客户可能按 SAN 计费 |
| Sectigo / Comodo | ⚠️ 按合同 | 视合同 | 同 DigiCert |
| 阿里云 CA | ✅ 免费证书可做结构演练 | 0 元（免费证书款）| 付费证书按合同 |
| 腾讯云 CA | ✅ 同上 | 0 元（免费证书款）| — |
| 自签 | ✅ 永久免费 | 0 元 | 完全不触碰 CA 流程 |

> 📌 **Agent 建议**：结构性演练**优先走 LE staging + 自签**，只有"需验证生产 CA 的签发流程本身"时才花钱走生产 CA staging。

---

## 3. 客户审批节点

### 强制审批节点清单

Phase 5 以下动作**必须**获得客户书面/口头批准后才能执行：

| 动作 | 批准层级 | 原因 |
|------|---------|------|
| SSH 到生产主机做演练 | L1 执行批准 + 主机所有者 | 直接接触生产资源 |
| 写生产 Nginx 配置（即使是临时） | L1 + 具体窗口约定 | 改生产配置 |
| K8s apply 到 prod namespace | L1 + 具体窗口 + 观察期 | 改生产资源 |
| 把测试证书绑到任何"**客户生产 SAN**" | L2 策略批准 | 即使是测试证书，绑到生产域名仍有 CT 暴露风险 |
| 写 Vault / KMS 任何生产 path | L1 + SOC 值班（如 F3 场景）| 写密钥系统 |
| 触发 CA 正式签发（非 staging）| L1 + 采购/财务审批 | 产生费用 |
| Phase 5 演练产生任何**产品侧告警**| 先通知再做 | 避免值班被吓到 |

### 审批话术模板

Agent 发起每一项受约动作前必须发出标准话术：

```markdown
## 准备执行 {{动作名}}
- 作用对象：{{资源 ID / 路径 / 域名}}
- 用途：{{为什么做}}
- 风险：{{如操作失败/执行中异常的后果}}
- 回滚方案：{{如何撤回}}
- 预计耗时：{{分钟数}}

请明示批准：
  [ ] 批准 · 立即执行
  [ ] 批准 · 等 [时间] 再执行
  [ ] 修改方案：______
  [ ] 中止
```

客户回复后 Agent 才执行。**未收到明示批准 Agent 不得擅自执行**。

---

## 4. 跨团队协调演练

### 触发条件
- Full Path 场景
- 审批链 ≥ 3 个独立团队
- 涉及值班响应（SOC / NOC）

### 协调演练脚本

```markdown
# 跨团队协调演练（Coordination Drill）

## 演练目标
验证变更窗口内的协调链能按时响应，**不是**验证技术步骤。

## 演练项
1. **审批链 dummy 请求演练**
   - 发一个 "演练" 标识的审批请求走完 L1 → L2 → L3
   - 测量每层实际响应时长 vs intake 里声明的 SLA
   - 识别：哪层容易超时？超时升级路径是否到位？

2. **信息传递演练**
   - 把一条测试告警推到客户的 IM / 邮件 / 工单系统
   - 验证：是否到达 SRE？SRE 能否正确转给 L2 / L3？

3. **SOC / 值班对接演练**
   - 提前通知 SOC 值班经理"本次变更窗口会有 X 告警"
   - 演练告警抑制 / 手动确认 / 事件认领流程

4. **法务 / 合规响应演练**（若涉及 C 类资产）
   - 提前给法务一份变更摘要
   - 验证"法务签字"是否能在变更窗口内拿到

## 产物
- 每项响应时长实测
- 识别的瓶颈点清单
- 变更窗口时长**保守估算**（= 技术时长 × 协调倍数）
```

---

## 5. 密钥获取方式抽象层

Runbook 模板**不得硬编码**某一种密钥管理系统的命令。所有密钥以 **占位符 `${VAR}`** 出现：

```bash
# ❌ 错误：绑死 Vault
export JKS_PASS=$(vault kv get -field=jks_pass secret/legacy-api)

# ✅ 正确：占位符 + 注释说明获取方式
export JKS_PASS="${JKS_PASS:?please set via your key management system}"
# 获取方式（按客户环境选一）：
#   Vault:         vault kv get -field=jks_pass secret/legacy-api
#   AWS Secrets:   aws secretsmanager get-secret-value --secret-id legacy-jks --query SecretString --output text
#   K8s Secret:    kubectl get secret legacy-api-jks -o jsonpath='{.data.pass}' | base64 -d
#   腾讯云 KMS:    tccli kms GetSecret --SecretName legacy-api --VersionId v1
#   明文配置:      cat /etc/legacy/jks.pass
```

### 密钥获取方式对齐表（Phase 1 能力对齐就要问清楚）

```markdown
| 密钥项 | 存储系统 | 获取命令 | 谁可获取 |
|-------|---------|---------|---------|
| JKS password | Vault | `vault kv get -field=jks_pass secret/legacy-api` | SRE + SOC |
| CDN 证书 API key | 腾讯云 CAM | 通过子账号只读 token | 中台 SRE |
| Nginx 私钥 | 明文硬盘 | `cat /etc/ssl/site.key` | 主机 root |
| ... | ... | ... | ... |
```

---

## 6. 演练粒度的路径适配

| 路径 | 演练粒度 | 原因 |
|------|---------|------|
| 🟢 **Fast** | 演练 = 清单（5-10 步）| 单机单域，没必要做矩阵 |
| 🟡 **Standard** | 演练矩阵（6-10 项，按绑定点类型）| 多机多类型 |
| 🔴 **Full** | 完整矩阵 + 跨团队协调演练 + 审批链 dummy | 组织复杂 |

### Adaptive Runbook Granularity（按客户能力适配）

对同一 Path 下，按客户能力基线（Phase 1 能力对齐结果）自动调整：

- **能力高（有 IaC / Vault / cert-manager）**：演练步骤合并，允许客户自行展开
- **能力低（手工 SCP / 无密钥管理）**：演练步骤**更细**，多加截图提示、多加确认点

---

## 7. 自动化续签的监控闭环

若方案引入自动化续签（如 acme.sh / cert-manager），Phase 5 必须规划**监控闭环**：

### 最小监控包（Minimum Monitoring Bundle）

1. **cron 输出**：续签脚本的 stdout/stderr 写到日志文件（`/var/log/acme-renew.log`）+ `logrotate` 归档
2. **邮件告警**：cron `MAILTO` 配置 or `mail` 命令发送；失败时告警
3. **CT 日志告警**：注册 crt.sh email alert（免费），新证书签发时收到提醒
4. **过期监控**：至少再装一个"证书剩 30/7/1 天"的独立告警（不依赖续签脚本本身）

### 三重兜底原则

- 续签脚本自己的告警（可能跟着脚本一起坏）
- CT 告警（客观第三方视角）
- 过期告警（终极兜底，即使前两个都坏了也能提醒）

缺一不能算"自动化闭环"。

---

## 8. 相关文件

- [`03-risk-assessment-playbook.md`](./03-risk-assessment-playbook.md) — DCV 矩阵输入
- [`04-planning-playbook.md`](./04-planning-playbook.md) — 方案决定演练范围
- [`06-verify-rollback-playbook.md`](./06-verify-rollback-playbook.md) — 演练通过后的正式执行
- [`runbook-templates/`](./runbook-templates/) — 按绑定点类型的具体演练脚本模板
