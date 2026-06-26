---
name: asf-v4
description: ASF V4.0 工业化增强模块 - 治理门禁 + 成本模型 + 安全优化。提供否决权执行、所有权证明、经济学评分、返工风险预测、安全在线优化等工业级能力。
metadata:
  {
    "openclaw":
      {
        "requires": { "nodeVersion": ">=20.0.0" },
        "install": [],
      },
  }
---

# ASF V4.0 - 工业化增强模块

**版本**: v0.9.0  
**OpenClaw 兼容性**: >=2026.3.24

---

## 功能说明

ASF V4.0 为 OpenClaw 提供工业级治理和优化能力：

- **否决权执行** - 硬/软否决规则验证变更
- **所有权证明** - 可验证的 single-writer 证明
- **经济学评分** - 基于成本的角色分配优化
- **返工风险** - 预测性风险分析
- **安全优化器** - 带回滚保护的在线优化

---

## 工具

| 工具 | 说明 |
|------|------|
| `veto-check` | 检查变更是否通过硬/软否决规则 |
| `ownership-proof` | 生成可验证的所有权证明 |
| `economics-score` | 计算角色分配经济学评分 |
| `interface-budget` | 计算跨角色依赖成本 |
| `rework-risk` | 预测任务返工风险 |
| `hot-contract` | 分析契约耦合度并建议角色数量 |
| `conflict-resolve` | 解决所有权冲突 |
| `safe-optimize` | 安全在线优化 |

---

## 命令

| 命令 | 说明 |
|------|------|
| `asf:status` | 检查 ASF V4.0 状态 |
| `asf:veto` | 运行否决检查 |
| `asf:proof` | 生成所有权证明 |
| `asf:score` | 计算经济学评分 |
| `asf:risk` | 预测返工风险 |
| `asf:hot-contracts` | 分析热契约 |

---

## 配置

编辑 `config/asf-v4.config.yaml`：

```yaml
veto:
  mode: default  # default | strict | custom
  
economics:
  scoreWeights:
    interfaceCost: -0.30
    bottleneck: -0.20
    skillMatch: 0.20
    parallelismGain: 0.15
    reworkRisk: -0.15

optimizer:
  enabled: true
  cooldownMs: 1800000  # 30 分钟
  failureThreshold: 2
```

---

## 依赖

- Node.js >=20.0.0
- OpenClaw >=2026.3.24

---

## 使用示例

```bash
# 检查状态
asf:status

# 运行否决检查
asf:veto --changes='[{"resourceType":"contract","resourcePath":"/orders","action":"update"}]'

# 生成所有权证明
asf:proof --resources='[{"type":"contract","path":"/orders#POST"}]' --roles='[{"id":"backend-team"}]'
```

---

## 架构影响

激活 ASF V4.0 后，ANFSF 架构获得以下增强：

1. **Layer 4 (Requirement Graph)** - 增加变更追溯和热力图
2. **Layer 8.5 (Role Control Plane)** - 增加 Interface Budget v2 和否决门禁
3. **Layer 9 (Agent OS)** - 增加角色 KPI 仪表板
4. **Layer 13 (Semantic Consistency)** - 增加契约语义化 diff
5. **Layer 16 (Runtime Intelligence)** - 增加自动回滚和进化守卫

---

## 许可证

MIT License
