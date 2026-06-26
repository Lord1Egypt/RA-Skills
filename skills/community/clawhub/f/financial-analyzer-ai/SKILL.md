---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_fb4b5b6f618411f19f62525400d9a7a1
    ReservedCode1: C9sNiJf0jkuokg5HtyQhBvUThvyTxhWif9+cJrPu9MXkEK/mFh0OOcRHUkmw1kPzXUP+OVfrCQ6P6JzJ7mBtrJjmsg73GMLneSZ5npoJToySreJv5p9yDJ5wF44x7Q0MaKbKQt6FKMlehstYfc6SGTiBBSEkkeSG052ldWK1C7GE4DIlhekP3hNkW9w=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_fb4b5b6f618411f19f62525400d9a7a1
    ReservedCode2: C9sNiJf0jkuokg5HtyQhBvUThvyTxhWif9+cJrPu9MXkEK/mFh0OOcRHUkmw1kPzXUP+OVfrCQ6P6JzJ7mBtrJjmsg73GMLneSZ5npoJToySreJv5p9yDJ5wF44x7Q0MaKbKQt6FKMlehstYfc6SGTiBBSEkkeSG052ldWK1C7GE4DIlhekP3hNkW9w=
---



# AI 财务报表分析 (Financial Statement Analyzer)

## 概述

Financial Statement Analyzer 是一款 AI 驱动的财务报表分析技能，基于 IFRS / US GAAP / 中国会计准则对照体系、财务比率公式库、行业基准数据和杜邦分析法，自动对资产负债表、利润表、现金流量表进行多维度深度分析，输出综合评分、风险预警与改进建议。

## 适用场景

- 企业年度财务报告分析与解读
- 投资标的财务健康状况评估
- 信贷审批中的企业偿债能力分析
- 内部审计与财务合规性检查
- 财务造假风险信号筛查
- 同行业公司财务状况对比分析

## 分析维度

| 维度 | 说明 |
|------|------|
| 偿债能力 | 流动比率、速动比率、现金比率、资产负债率、利息保障倍数、产权比率 |
| 盈利能力 | 毛利率、净利率、ROE、ROA、EBITDA 利润率、营业利润率 |
| 营运能力 | 存货周转率、应收账款周转率、总资产周转率、营业周期、现金转换周期 |
| 成长能力 | 营收增长率、净利润增长率、总资产增长率、经营活动现金流增长率 |
| 现金流 | 经营/投资/筹资现金流结构、自由现金流、现金流覆盖比率 |
| 杜邦分析 | ROE 拆解：净利率 × 资产周转率 × 权益乘数，逐层归因分析 |
| 财务造假预警 | Beneish M-Score、财务数据异常波动、关联交易、收入确认异常 |
| 行业对标 | 与行业基准值对比，识别竞争优势与短板 |

## 支持的会计准则与行业基准

| 会计准则 | 覆盖范围 | 特色分析 |
|---------|---------|---------|
| IFRS | 全球通用 | 公允价值计量、减值测试 |
| US GAAP | 美国市场 | LIFO/FIFO对比、规则导向分析 |
| 中国会计准则 (CAS) | 中国市场 | 与 IFRS 差异调整、增值税影响 |
| 行业基准库 | 20+行业 | 制造业/零售/科技/金融/医疗等 |

## 评分体系

| 综合分数 | 等级 | 说明 |
|---------|------|------|
| 90-100 | A+ 优秀 | 财务健康，各项指标优于行业平均 |
| 75-89 | A 良好 | 整体稳健，个别指标可优化 |
| 60-74 | B 一般 | 存在一定财务风险，需关注改善 |
| 40-59 | C 关注 | 多项指标低于行业基准，风险较高 |
| 20-39 | D 风险 | 财务状况恶化，存在重大风险信号 |
| 0-19 | F 危险 | 财务危机，持续经营能力存疑 |

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/financial-analyzer` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起分析请求  POST /skill/financial-analyzer
2. 服务端返回 402 Payment Required
   Header: X-Payment-Needed: true
   Header: X-Short-Link: alipay_XXXXXXXXXXXXXXXX
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  POST /pay-confirm
   Header: X-Payment-Credential: <支付凭证>
5. 服务端验证通过 → 执行财务分析 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `X-Payment-Needed` | 服务端返回：`true` 表示需要支付 |
| `X-Short-Link` | 服务端返回：支付宝短链 URL 供用户支付 |
| `X-Payment-Credential` | 客户端回传：支付完成后的凭证字符串 |
| `X-Service-Tier` | 可选，`basic`（基础分析）或 `deep`（深度审计） |

## 服务档位

### 基础档（basic = ¥0.50）
- 三张报表输入（JSON 格式：资产/负债/收入/利润/现金流）
- 财务比率自动计算（偿债/盈利/营运/成长 4 维）
- 综合财务评分（0-100）
- 杜邦分析拆解
- 风险预警信号（Beneish M-Score 快速筛查）
- 输出 JSON 格式分析报告

### 深度档（deep = ¥1.00 - 预留）
- 全部基础功能
- 3-5 年财务趋势分析
- 行业对标详细对比
- 财务造假深度检测（多模型交叉验证）
- 现金流预测模型
- 估值模型（DCF / PE / PB）
- 输出 PDF 完整分析报告

## 数据底座

所有会计准则对照、财务比率公式、行业基准数据、杜邦分析框架、造假信号库存储于 `references/financial-analyzer.json`，结构如下：

```json
{
  "accounting_standards": { ... },     // IFRS/US GAAP/中国会计准则对照
  "financial_ratios": { ... },         // 财务比率公式库 (偿债/盈利/营运/成长)
  "industry_benchmarks": { ... },      // 20+ 行业基准数据
  "dupont_framework": { ... },         // 杜邦分析法拆解框架
  "fraud_signals": [ ... ],            // 财务造假红色信号库
  "valuation_models": [ ... ]          // 估值模型参数
}
```

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/financial-analyzer \
  -H "Content-Type: application/json" \
  -H "X-Service-Tier: basic" \
  -d '{"financial_data": {"assets": {"current": 500000, "non_current": 1500000, "total": 2000000}, "liabilities": {"current": 300000, "non_current": 700000, "total": 1000000}, "equity": 1000000, "revenue": 3000000, "cogs": 1800000, "operating_expenses": 600000, "net_income": 450000, "operating_cashflow": 520000, "investing_cashflow": -200000, "financing_cashflow": -100000}, "accounting_standard": "ifrs", "industry": "manufacturing"}'
```

### 响应（支付后）

```json
{
  "service": "AI 财务报表分析",
  "tier": "basic",
  "accounting_standard": "ifrs",
  "industry": "manufacturing",
  "composite_score": 78,
  "rank": "A 良好",
  "dimensions": {
    "solvency": {
      "score": 82,
      "ratios": {
        "current_ratio": 1.67,
        "quick_ratio": 1.20,
        "debt_to_asset": 0.50,
        "interest_coverage": 8.5
      },
      "verdict": "偿债能力稳健，资产负债率适中"
    },
    "profitability": {
      "score": 75,
      "ratios": {
        "gross_margin": 0.40,
        "net_margin": 0.15,
        "roe": 0.45,
        "roa": 0.225
      },
      "verdict": "盈利能力良好，ROE 表现突出"
    },
    "efficiency": {
      "score": 72,
      "ratios": {
        "inventory_turnover": 6.0,
        "receivables_turnover": 8.0,
        "asset_turnover": 1.5
      },
      "verdict": "营运效率中等，存货周转可优化"
    },
    "growth": {
      "score": 80,
      "indicators": {
        "revenue_growth": "15%",
        "net_income_growth": "12%",
        "cashflow_growth": "18%"
      },
      "verdict": "增长态势良好，现金流增速领先"
    }
  },
  "dupont_analysis": {
    "roe": "45%",
    "breakdown": "净利率 15% × 资产周转率 1.50 × 权益乘数 2.00 = 45%",
    "insight": "ROE 主要由较高的权益乘数（财务杠杆）驱动，净利润率贡献适中"
  },
  "risk_alerts": [
    { "severity": "low", "signal": "应收账款周转率略低于行业均值 (8.0 vs 10.0)" },
    { "severity": "low", "signal": "权益乘数 2.0，财务杠杆略高于行业中位数 1.6" }
  ],
  "recommendations": [
    "优化应收账款管理，缩短回款周期",
    "关注存货周转效率，减少资金占用",
    "适度控制财务杠杆，降低长期偿债压力"
  ]
}
```

## 许可

MIT License — 详见 LICENSE 文件
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
