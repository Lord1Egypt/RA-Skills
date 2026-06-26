# DeFi Risk Scanner 🛡️

**结构化 DeFi 协议与代币风险评估工具**

> ⚠️ 本工具仅供教育参考，不构成财务建议。加密货币投资有极高风险，可能导致本金全损。

## 功能

- **协议风险评估**: 输入协议名称（slug），通过 DefiLlama API 获取 TVL、链上数据
- **代币风险扫描**: 输入合约地址，通过 DexScreener API 分析流动性、市值、FDV
- **综合评分**: 0-100 分结构化风险评分
- **风险因子拆解**: 逐项分析优点与风险点
- **操作建议**: 提供具体验证步骤和工具推荐

## 快速开始

### 协议模式
```bash
./scripts/risk-check.sh aave ethereum
./scripts/risk-check.sh uniswap-v3 ethereum
./scripts/risk-check.sh curve-finance ethereum
```

### 代币模式
```bash
./scripts/risk-check.sh 0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9 ethereum
./scripts/risk-check.sh 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 ethereum
```

## 依赖

- `bash` (4.0+)
- `curl`
- `jq`
- `awk`
- `bc`

## 数据来源

- **DefiLlama API** (`api.llama.fi`) — 协议 TVL 和基本信息
- **DexScreener API** (`api.dexscreener.com`) — 代币流动性和市值数据

两个 API 均为免费、无需 API Key。

## 评分维度

### 协议模式
| 维度 | 权重 | 说明 |
|------|------|------|
| TVL | 40% | >$1B=40分, >$100M=30分, >$10M=20分 |
| 链多样性 | 10% | ≥5链=10分, 2-4链=6分 |
| 知名度 | 10% | 知名协议额外加分 |

### 代币模式
| 维度 | 权重 | 说明 |
|------|------|------|
| 流动性/市值比 | 40% | ≥10%=20分, ≥5%=10分 |
| 市值/FDV比 | 20% | ≥80%=20分, ≥50%=10分 |
| 市场活跃度 | 10% | 24h成交量/流动性≥5%=10分 |

## 评分等级

- 🟢 **80-100**: 低风险 — 安全
- 🟡 **60-79**: 中低风险 — 可接受
- 🟠 **40-59**: 中高风险 — 谨慎
- 🔴 **20-39**: 高风险 — 警告
- ⚫ **0-19**: 极高风险 — 危险

## 发布到 ClawHub

```bash
clawhub login --token <YOUR_TOKEN>
clawhub sync --root defi-risk-scanner --all
```

或直接发布：

```bash
clawhub publish ./defi-risk-scanner \
  --slug defi-risk-scanner \
  --name "DeFi Risk Scanner" \
  --version 1.0.0 \
  --changelog "Initial release - 5-dimension risk scoring framework"
```

## 后续规划（Pro 版）

- Rug Pull 评分（Token Sniffer 集成）
- 实时预警（价格异常、TVL 大幅下降）
- 历史风险追踪
- PDF 报告导出
