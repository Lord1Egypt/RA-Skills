# E-commerce Ad Performance Diagnostic Skill

Comprehensive diagnostic framework for identifying and resolving e-commerce advertising performance anomalies through systematic funnel analysis and cross-metric validation.

---

## Core Principles

1. **Funnel-first diagnosis** — Every anomaly must be traced through the complete conversion funnel: 曝光 → 点击 → 加购 → 下单
2. **Cross-metric validation** — Never diagnose based on a single metric. Always validate with correlated indicators
3. **Blocking factors first** — Check data validity and critical blockers (stockout, system errors) before nuanced optimization
4. **Priority-driven triage** — P0 (system failures) → P1 (performance issues) → P2 (efficiency optimization)

---

## Patterns with Signatures

### Pattern 1: High Marketing Cost Ratio 🟡

#### Signature A: Aggressive ROI Bidding
**Metrics Pattern**:
- ✓ 转化率: Normal
- ✓ CTR: Normal  
- ✗ 营销占比: >50%
- ✗ ROAS: Low but positive (1.1-2.9x)

**Key Evidence**:
- Conversion funnel is **healthy** — problem is purely cost-side
- ROI bid settings are **too aggressive** for current market conditions

**Likely Cause**: ROI出价设置过激进，成本端问题

**Recommended Action**: 直接降低ROI目标出价，无需改动产品或详情页

**关联诊断**:
- 若转化率同时偏低 → see Pattern 2 (转化问题)
- 若ROAS接近0 → see Pattern 3 (漏斗断裂)

### Pattern 2: Conversion Funnel Issues 🔴🟠

#### Signature A: Complete Funnel Breakdown (Stockout/System Error)
**Metrics Pattern**:
- ✓ CTR: Normal (2-4%)
- ✓ 加购率: Normal (5-20%)
- ✗ 转化率: Zero (0%)
- ✗ 库存: Zero or critical low

**Key Evidence**:
- Traffic and engagement are **healthy** until final conversion step
- **Sudden drop** to zero conversion (not gradual decline)
- Funnel breaks at 加购 → 下单 stage

**Likely Cause**: 商品下架/缺货/价格错误/链接异常

**Recommended Action**: 
1. 检查商品是否下架
2. 检查库存是否清零  
3. 检查价格是否异常
4. 检查活动设置错误

#### Signature B: Detail Page Blocking (Zero Add-to-Cart)
**Metrics Pattern**:
- ✓ CTR: Normal
- ✗ 加购率: Zero (0%)
- ✗ 转化率: Zero
- ✓ 曝光/点击: Normal volume

**Key Evidence**:
- Users reach detail page but **cannot or will not** add to cart
- Complete failure at 点击 → 加购 stage
- Detail page has **technical or content failure**

**Likely Cause**: 详情页内容无法触发加购行为

**Recommended Action**:
1. 检查详情页图片是否加载失败
2. 检查SKU选项是否可选
3. 检查价格是否显示异常

**关联诊断**:
- 若库存正常但加购率=0% → 详情页技术问题
- 若CTR也偏低 → see Pattern 4 (定向问题)

### Pattern 3: Low Overall Conversion Rate 🟠

#### Signature A: Detail Page Conversion Weakness  
**Metrics Pattern**:
- ✓ CTR: Normal (3-5%)
- ✗ CVR: <2%
- ✓ 曝光量: Adequate
- ✓ 库存: Available

**Key Evidence**:
- **主图吸引力OK** (proven by healthy CTR)
- Users enter detail page but are **not convinced** to purchase
- Problem at 详情页说服 stage

**Likely Cause**: 落地页转化弱，产品竞争力不足

**Recommended Action**:
1. 检查详情页卖点是否清晰
2. 检查评价是否有负面积累  
3. 检查产品价格与竞品对比是否失去优势

**关联诊断**:
- 若CTR同时偏低 → see Pattern 4 Signature B (双重问题)
- 若加购率正常但CVR低 → see Pattern 2 Signature A (系统问题)

### Pattern 4: Traffic Quality Issues 🔴🟠

#### Signature A: Poor Ad Targeting (Very Low CTR)
**Metrics Pattern**:
- ✗ CTR: <2% (基准≥3%)
- ✓ 曝光数: Adequate volume
- ✗ 点击成本: High due to low relevance
- ~ CVR: May be normal or low

**Key Evidence**:
- **广告曝光充足** but users don't click
- Targeting mismatch between ad content and audience
- Problem at 曝光 → 点击 stage

**Likely Cause**: 主图/定向关键词与受众不匹配

**Recommended Action**: 
1. 检查主图与目标受众不符
2. 检查关键词匹配模式过宽
3. 检查广告定向标签错位
4. 优化主图+收窄关键词至精确匹配

#### Signature B: Combined Targeting + Conversion Issues
**Metrics Pattern**:
- ✗ CTR: <3%
- ✗ CVR: <2%  
- ✗ ROAS: Low (1.2-2.9x)
- ✗ 整体效率: Poor across funnel

**Key Evidence**:
- **双重漏斗损耗** — problems at multiple stages
- Both traffic quality AND conversion quality are subpar
- Requires **parallel optimization** of targeting and landing page

**Likely Cause**: 流量精准度差+详情页说服力弱

**Recommended Action**: 优先收窄广告定向（优化关键词/人群标签）同步改善详情页，二者都需要处理

**关联诊断**:
- 若仅CTR低 → see Pattern 4 Signature A (单纯定向问题)
- 若仅CVR低 → see Pattern 3 (单纯转化问题)

### Pattern 5: Cost Efficiency Degradation 🟡

#### Signature A: Bidding/Pricing Issue (Non-Funnel)
**Metrics Pattern**:
- ✓ CTR: Normal
- ✓ CVR: Normal  
- ✗ ROAS: 1-3x (low but not zero)
- ✓ 转化流程: Healthy

**Key Evidence**:
- **流量转化正常** — funnel is working
- Problem is **unit economics**, not user behavior
- Issue is competitive bidding or pricing strategy

**Likely Cause**: 竞价或单价问题，非漏斗问题

**Recommended Action**: Review bidding strategy and competitive pricing position

**关联诊断**:
- 若转化率也偏低 → see Pattern 3 (复合问题)
- 若营销占比>50% → see Pattern 1 (ROI出价问题)

---

## Decision Trees

### Tree 1: Zero Conversion Diagnosis
```
IF 转化率 = 0%:
    IF 数据量 < 最小样本要求:
        → 等待更多数据
    ELIF 库存 ≤ 0 OR 商品状态 = 下架:
        → Pattern 2 Signature A (stockout/delisting)
    ELIF 加购率 = 0%:
        → Pattern 2 Signature B (detail page blocking)
    ELIF 加购率 > 0% AND CTR > 0%:
        → Pattern 2 Signature A (checkout/system error)
    ELSE:
        → 需要更多数据验证
```

### Tree 2: Low CTR Diagnosis  
```
IF CTR < 2%:
    IF 曝光量 < 1000:
        → 数据不足，等待更多曝光
    ELIF CVR 同时 < 2%:
        → Pattern 4 Signature B (targeting + conversion)
    ELIF CVR 正常:
        → Pattern 4 Signature A (pure targeting issue)
    ELSE:
        → 检查主图和关键词匹配度
```

### Tree 3: Normal Traffic, Low Conversion
```
IF CTR ≥ 3% AND CVR < 2%:
    IF 加购率 = 0%:
        → Pattern 2 Signature B (detail page blocking)
    ELIF 加购率 > 0% AND 最终转化率 = 0%:
        → Pattern 2 Signature A (checkout issue)
    ELIF 加购率 > 0% AND 转化率 > 0% but low:
        → Pattern 3 Signature A (conversion optimization needed)
    ELSE:
        → 深入分析详情页表现
```

### Tree 4: Cost Efficiency Issues
```
IF 转化率正常 AND CTR正常:
    IF 营销占比 > 50%:
        → Pattern 1 Signature A (ROI bidding too aggressive)
    ELIF ROAS 1-3x:
        → Pattern 5 Signature A (competitive/pricing issue)
    ELSE:
        → 检查其他成本因素
```

---

## Sample Size Validity Gates

| Metric | Minimum for Valid Evaluation |
|--------|------------------------------|
| CTR | ≥1,000 impressions |
| CVR | ≥100 clicks OR ≥500 page views |
| 加购率 | ≥50 detail page visits |
| ROAS | ≥10 conversions OR ≥¥500 spend |
| 营销占比 | ≥7 days of data |

---

## Cross-Metric Validation Framework

### Primary Validation Chains
1. **CTR + CVR together** — never evaluate conversion rate without checking traffic quality
2. **库存 + 转化率** — always verify stock availability before diagnosing conversion issues  
3. **曝光量 + CTR** — ensure sufficient impression volume before concluding targeting failure
4. **加购率 + 转化率** — distinguish detail page issues from checkout/system issues

### Correlation Patterns
- **High CTR + Low CVR** → Detail page problem (Pattern 3)
- **Low CTR + Low CVR** → Compound issue (Pattern 4B)  
- **Normal funnel + High cost** → Bidding issue (Pattern 1 or 5)
- **Zero conversion + Normal engagement** → System/stock issue (Pattern 2A)

---

## Detection Checklist

✅ **Step 1: Data Validity Check**
- Verify minimum sample sizes per metric
- Confirm data freshness (within 24-48 hours)
- Check for incomplete data collection periods

✅ **Step 2: Critical Blocker Scan**  
- Check inventory levels (库存 > 0)
- Verify product listing status (not delisted)
- Confirm pricing display is normal
- Test checkout process functionality

✅ **Step 3: Primary Anomaly Identification**
- Identify which metrics are outside normal ranges
- Note severity: P0 (zero performance) vs P1 (degraded) vs P2 (suboptimal)

✅ **Step 4: Funnel Stage Localization**
- Map anomaly to specific funnel stage: 曝光→点击→加购→下单
- Identify where the breakdown occurs

✅ **Step 5: Cross-Metric Validation**
- Validate primary finding with correlated metrics
- Rule out alternative explanations
- Confirm pattern consistency

✅ **Step 6: Pattern/Signature Matching**
- Match observed pattern to documented signatures
- Verify all signature criteria are met
- Check for mixed patterns requiring multiple actions

✅ **Step 7: Action Prioritization**
- Assign priority: P0 (immediate) → P1 (this week) → P2 (optimization)
- Confirm recommended actions align with root cause

---

## Common Misattribution Traps

### Trap 1: CTR vs CVR Confusion
**Symptoms**: Low overall performance
**Wrong Diagnosis**: "Conversion rate is low, need to optimize detail page"  
**Correct Diagnosis**: Check CTR first — if CTR <2%, the problem is targeting/creative, not detail page

### Trap 2: Cost vs Conversion Issues
**Symptoms**: Low ROAS
**Wrong Diagnosis**: "Need to improve conversion rate"
**Correct Diagnosis**: If conversion rate is normal, problem is bidding strategy or pricing, not funnel optimization

### Trap 3: System Issues vs Performance Issues  
**Symptoms**: Zero conversions
**Wrong Diagnosis**: "Detail page needs optimization"
**Correct Diagnosis**: Check stock and system status first — zero conversion with normal engagement = system/stock issue

### Trap 4: Single Metric Diagnosis
**Symptoms**: One metric is off
**Wrong Diagnosis**: Jump to conclusion based on single metric
**Correct Diagnosis**: Always cross-validate with related metrics before diagnosing

### Trap 5: Data Sufficiency Assumption
**Symptoms**: Poor performance in early data
**Wrong Diagnosis**: Immediate optimization action
**Correct Diagnosis**: Verify minimum sample size requirements are met before concluding performance issues

### Trap 6: Composite Pattern Oversimplification  
**Symptoms**: Both CTR and CVR are low
**Wrong Diagnosis**: "Just a general performance issue"
**Correct Diagnosis**: Pattern 4B requires **parallel** optimization of both targeting AND conversion — treating as single issue will only solve half the problem

---

## Dimensional Coverage Check

✅ **Data validity gate**: Covered in Sample Size Validity Gates table and Detection Checklist Step 1

✅ **Category/segment differentiation**: Implied by SKU-level analysis in data rows — different product categories (DT, YMJ, CBD, etc.) may have different baseline performance expectations

✅ **Time dimension**: Covered in validity gates (minimum 7 days for 营销占比) and diagnostic notes mentioning data freshness requirements

✅ **External factors**: Covered extensively in Pattern 2 Signatures (stockout, delisting, pricing errors) and Detection Checklist Step 2 (critical blockers)

⚠️ **SUGGESTED ADDITION**: **Currency/unit normalization** — The current framework assumes single currency analysis. For multi-currency operations, add standardization rules for ROAS calculations and cost comparisons across different markets.
