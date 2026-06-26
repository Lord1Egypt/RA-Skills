---
name: Bank Regulatory Reporting Assistant
slug: bank-regulatory-report
description: AI-powered banking regulatory reporting assistant - generate NFRA/PBOC/SAFE reports, 1104 statistical submissions, Basel III capital reports, and compliance documentation. Updated for 2024-2026 including new capital management reporting templates, FATF compliance reporting, and digital currency reporting. Keywords: bank regulatory reporting, 1104, Basel III, NFRA, PBOC, SAFE, AML reporting, capital adequacy, 监管报告, 监管报送, NRTA报告, 1104报表, 资本充足率, 反洗钱报告, 统计报送, 季度报告, 年度报告.
version: "4.0.0"
triggers:
  - 监管报告
  - 监管报送
  - NRTA报告
  - 1104报送
  - 统计报告
  - 合规报告
  - 监管统计
  - 数据报送
  - 监管合规报告
  - 银保监报告
---

# Bank Regulatory Reporting Assistant
# 银行监管报告助手

## Skill Overview

### 0. 2024-2026 银行监管报送最新变化

| 时间 | 动态 | 报送影响 |
|------|------|---------|
| **2024年1月** | 中国版巴三（新资本管理办法）正式实施 | 1104报表风险加权资产计算逻辑升级 |
| **2024年** | NFRA统一接管原CBRC/CIRC职能 | 报送机构改为国家金融监管总局 |
| **2025年** | 反洗钱大额报告起报金额优化 | 可疑交易报告标准细化，报送时效要求提升 |
| **2025年** | 数字人民币业务纳入1104统计 | 新增数字货币相关统计科目 |
| **2025年** | 碳核算/绿色信贷统计新增 | 绿色贷款统计科目新增，支持监管考核 |
| **2026年** | FATF互评估后AML报送升级 | 可疑交易报告质量要求提高 |

| Attribute | Value |
|-----------|-------|
| **Skill Type** | Pure Conversation / Reporting Workflow |
| **Target Users** | Bank compliance officers, data analysts, IT systems teams, regulatory affairs |
| **Core Capability** | Data collection → Basel III capital report → 1104 submission → AML report → Compliance check |
| **Industry** | Commercial bank regulatory affairs, compliance management, green finance reporting |

---

## How to Use

Tell me the type of regulatory report you need, and I'll guide you through the preparation.

**Example prompts:**
- "帮我生成1104监管统计报表"
- "写一份季度资本充足率报告"
- "准备一份反洗钱监管报告"
- "生成一份理财业务专项报告"
- "帮我写银保监现场检查的数据说明"

---

## Phase 1: Report Type Identification

### Common Regulatory Reports in Chinese Banks:

| Report System | Frequency | Key Content |
|-------------|----------|-------------|
| **1104监管统计** | Daily/Monthly/Quarterly | 资本充足率、资产质量、流动性指标 |
| **非现场监管报表(NRTA)** | Quarterly | 法人机构全面监管评价 |
| **EAST系统** | Monthly | 业务明细数据报送 |
| **反洗钱大额/可疑交易** | Real-time | 可疑交易识别与报告 |
| **理财信息登记** | Weekly | 理财产品发行/到期/净值 |
| **征信数据报送** | Monthly | 企业/个人征信数据 |
| **普惠金融统计** | Quarterly | 小微企业贷款、涉农贷款 |
| **绿色信贷统计** | Quarterly | 绿色贷款分类与统计 |
| **房地产金融监测** | Monthly | 开发贷款、按揭贷款数据 |
| **重大事项报告** | Event-driven | 高管变动、重大风险事件 |

---

## Phase 2: Data Collection & Verification

### For each report type, I will help collect:

**Capital Adequacy Report (资本充足率报告):**
```
数据清单：
□ 资本净额（核心一级/其他一级/二级资本）
□ 风险加权资产（信用风险/市场风险/操作风险）
□ 资本充足率 = 资本净额 / 风险加权资产
□ 一级资本充足率
□ 核心一级资本充足率
□ 杠杆率
□ 流动性覆盖率 (LCR)
□ 净稳定资金比例 (NSFR)
□ 流动性比例
□ 最大十家客户贷款集中度
□ 最大单家同业融出比例
```

**Asset Quality Report (资产质量报告):**
```
数据清单：
□ 正常类/关注类/次级类/可疑类/损失类贷款余额
□ 五级分类迁徙率
□ 不良贷款率 (NPL ratio) = 不良贷款 / 客户贷款总额
□ 拨备覆盖率 = 贷款损失准备 / 不良贷款
□ 拨贷比 = 贷款损失准备 / 客户贷款总额
□ 新发生不良贷款
□ 重组贷款
□ 逾期90天以上贷款
□ 核销及转出金额
□ 当期回收不良贷款
```

**Liquidity Risk Report (流动性风险报告):**
```
数据清单：
□ 流动性比例
□ 流动性覆盖率 (LCR ≥ 100%)
□ 净稳定资金比例 (NSFR ≥ 100%)
□ 优质流动性资产 (HQLA)
□ 未来30天现金流出/流入
□ 剩余期限错配情况
□ 流动性风险应急计划触发条件
```

---

## Phase 3: Report Generation

### 3.1 1104 System - Key Report Templates:

#### G01 资产负债项目统计表 (月度)
```
填报说明：
- 反映银行资产负债结构
- 按会计科目映射到监管统计项
- 需与1104系统数据核对一致

关键指标：
  资产类：客户贷款、金融投资、同业资产、固定资产
  负债类：客户存款、同业负债、应付债券、实收资本
```

#### G21 资产质量五级分类情况统计表 (季度)
```
不良贷款分析：
| 分类 | 余额(万元) | 占比 | 较上期变化 |
|------|-----------|------|-----------|
| 正常类 | | | |
| 关注类 | | | |
| 次级类 | | | |
| 可疑类 | | | |
| 损失类 | | | |
| 不良贷款合计 | | | |
```

#### G4B 资本充足率汇总表 (季度)
```
资本充足率计算：
分子（资本净额）：
  核心一级资本：实收资本+资本公积+盈余公积+未分配利润-扣减项
  其他一级资本：优先股、永续债
  二级资本：二级资本债、超额贷款损失准备
  资本净额 = 核心一级+其他一级+二级-扣减项

分母（风险加权资产）：
  信用风险加权资产
  + 市场风险加权资产
  + 操作风险加权资产
  = 风险加权资产合计

资本充足率 = 资本净额 / 风险加权资产 = [X]%

监管要求：
  资本充足率 ≥ 10.5%
  一级资本充足率 ≥ 8.5%
  核心一级资本充足率 ≥ 7.5%
  储备资本 = 2.5%（逆周期0-2.5%）
  系统重要性银行附加资本 = 1%-1.5%
```

---

### 3.2 Non-Performing Asset (NPA) Report Template:

```markdown
# 不良资产管理专项报告

## 一、总体不良贷款情况

| 指标 | 期末余额(万元) | 较上季度 | 较年初 |
|------|---------------|---------|-------|
| 不良贷款合计 | | | |
| 其中：次级类 | | | |
|      可疑类 | | | |
|      损失类 | | | |
| 不良率 | % | | |
| 拨备覆盖率 | % | | |
| 拨贷比 | % | | |

## 二、不良贷款结构分析

### 2.1 按行业分布
| 行业 | 余额(万元) | 占比 | 不良率 | 较上期 |
|------|-----------|------|--------|-------|
| 制造业 | | | | |
| 房地产 | | | | |
| 批发零售 | | | | |
| 交通运输 | | | | |
| 个人住房贷款 | | | | |
| 个人消费贷款 | | | | |
| 其他 | | | | |

### 2.2 按担保方式
| 担保方式 | 余额(万元) | 不良率 |
|---------|-----------|--------|
| 信用贷款 | | |
| 保证贷款 | | |
| 抵押贷款 | | |
| 质押贷款 | | |

### 2.3 按地区分布
[按分支机构/省份分解]

## 三、不良贷款成因分析
- [成因1]
- [成因2]
- [成因3]

## 四、清收处置情况

| 处置方式 | 本期金额(万元) | 累计金额(万元) |
|---------|---------------|---------------|
| 现金清收 | | |
| 核销 | | |
| 批量转让 | | |
| 资产证券化 | | |
| 担保人代偿 | | |
| 重组转化 | | |
| 其他 | | |
| **合计** | | |

## 五、专项计划与拨备充足性

- 专项准备金计提是否充足
- 核销计划执行情况
- 资产质量迁徙趋势

## 六、下一步工作措施
1. [措施1]
2. [措施2]
3. [措施3]

## 七、监管关注事项说明
[对监管机构的专项说明]
```

---

### 3.3 Anti-Money Laundering (AML) Report Template:

```markdown
# 反洗钱监管报告

## 一、本期反洗钱工作概述

| 指标 | 本期 | 上期 | 环比变化 |
|------|------|------|---------|
| 客户总量 | | | |
| 新建客户 | | | |
| 高风险客户 | | | |
| 可疑交易预警数 | | | |
| 提交可疑交易报告数 | | | |
| 大额交易报告数 | | | |
| 黑名单命中数 | | | |

## 二、客户尽职调查情况

### 2.1 客户分类情况
| 客户风险等级 | 数量 | 占比 |
|-------------|------|------|
| 低风险 | | |
| 中等风险 | | |
| 高风险 | | |
| 禁止类 | | |

### 2.2 强化尽调执行情况
- [ ] 触发强化尽调客户数：[X]
- [ ] 完成强化尽调数：[X]
- [ ] 未完成待跟进数：[X]

## 三、可疑交易监测情况

### 3.1 重点可疑交易类型
| 可疑类型 | 预警数 | 核实非可疑 | 提交报告 | 涉及金额(万元) |
|---------|--------|-----------|---------|--------------|
| 疑似涉毒 | | | | |
| 疑似涉恐 | | | | |
| 疑似走私 | | | | |
| 疑似非法集资 | | | | |
| 疑似电信诈骗 | | | | |
| 疑似地下钱庄 | | | | |
| 其他 | | | | |

### 3.2 可疑交易特征
[Top 3 可疑交易特征分析]

## 四、名单监控情况
- 黑名单命中总数：[X]
- 其中真命中：[X]，误命中：[X]
- 名单更新执行情况：✅完成

## 五、监管配合情况
- 监管检查配合：[描述]
- 整改计划执行：[描述]

## 六、下一步工作计划
1. [计划1]
2. [计划2]
```

---

## Phase 4: Data Quality Verification

### Common Error Checks:

| Check | Rule | Error Type |
|-------|------|-----------|
| 资产规模匹配 | 与1104/G01一致 | 逻辑校验 |
| 资本充足率公式 | 净额/RWA计算正确 | 计算校验 |
| 不良率连续性 | 与上期衔接，无异常跳跃 | 趋势校验 |
| 五级分类迁徙 | 迁徙率在合理范围内 | 合理性校验 |
| 大额交易完整性 | 50万+现金报告全覆盖 | 完整性校验 |
| 跨表一致性 | G01/G04/G21数据口径一致 | 跨表校验 |

---

## Quick Report Templates

**Quarterly NPA Report:**
```
生成不良贷款季度报告：
- 不良贷款余额：[X万元]
- 不良率：[X]%
- 拨备覆盖率：[X]%
- 新发生不良：[X万元]
- 处置金额：[X万元]
- 主要成因：[描述]
- 重点关注客户：[列出]
```

**Monthly Regulatory Statistics:**
```
核对以下1104月报数据：
- 资产总额：[X万元]
- 负债总额：[X万元]
- 客户存款：[X万元]
- 客户贷款：[X万元]
- 存贷比：[X]%
- 不良率：[X]%
```

**Liquidity Risk Assessment:**
```
流动性风险评估：
- 流动性比例：[X]%
- LCR：[X]%
- NSFR：[X]%
- HQLA：[X万元]
- 主要风险点：[描述]
```

---

## Disclaimer

This skill generates regulatory report drafts for bank compliance teams. All reports must be reviewed and approved by authorized compliance officers before submission. Data accuracy is the responsibility of the submitting department. AI-generated reports do not replace official regulatory submissions and require human verification before filing.
