# 主Agent报告汇总任务

> 阶段二6个子任务 + 阶段三五子任务全部完成后，主Agent执行本汇总任务，生成最终报告 report.md

---

## 执行条件

**前提：以下11个文件全部存在：**

```
阶段二（6个分析文件）：
  data/{代码}/quick_profile_analysis.md
  data/{代码}/industry_moat_analysis.md
  data/{代码}/financial_quality_analysis.md
  data/{代码}/governance_analysis.md
  data/{代码}/valuation_analysis.md
  data/{代码}/fund_market_analysis.md

阶段三（5个汇总文件）：
  data/{代码}/c1_three_questions.md
  data/{代码}/c2_five_rules.md
  data/{代码}/c3_risk_warnings.md
  data/{代码}/c4_summary_profile.md
  data/{代码}/c5_tracking_metrics.md
```

---

## 汇总步骤

### 步骤1：确认所有文件存在

检查11个文件是否全部存在于：
`C:\Users\pd\.openclaw\workspace-analysts\data\{股票代码}\`

如有缺失，主Agent直接补充生成缺失的章节内容。

---

### 步骤2：读取所有文件

依次读取所有11个文件，提取关键内容填充到最终报告模板中。

---

### 步骤3：生成最终报告

按照以下模板生成 `report.md`：

```markdown
# {股票名称}（{代码}）基本面分析报告

> 报告日期：{当天日期}
> 报告性质：基本面研究分析，不构成任何投资建议

---

## 一、快速画像
{从 quick_profile_analysis.md 提取核心内容}

## 二、行业与护城河
{从 industry_moat_analysis.md 提取核心内容}

## 三、财务质量
{从 financial_quality_analysis.md 提取核心内容}

## 四、公司治理
{从 governance_analysis.md 提取核心内容}

## 五、估值与资本运作
{从 valuation_analysis.md 提取核心内容}

## 六、资金与市场情绪
{从 fund_market_analysis.md 提取核心内容}

---

## 七、投资哲学分析

### 三大核心问题判断（来自 c1_three_questions.md）
| 核心问题 | 结论 | 核心依据 |
|----------|------|---------|
| 问题1：好生意？ | 好/中/差 | |
| 问题2：好管理层？ | 信任/基本可信/需谨慎 | |
| 问题3：好价格？ | 低估/合理/高估 | |

### 五大经验法则验证（来自 c2_five_rules.md）
| 法则 | 验证结果 | 说明 |
|------|----------|------|
| ROE核心 | ✅通过/⚠️一般/❌差 | |
| 现金流 | ✅通过/⚠️一般/❌差 | |
| 管理层 | ✅通过/⚠️一般/❌差 | |
| 估值 | ✅通过/⚠️一般/❌差 | |
| 风险排查 | ✅通过/⚠️有风险/❌排除 | |

### 风险提示（来自 c3_risk_warnings.md）
**综合风险评级：** P0/P1/P2/P3

{提取P0和P1风险清单}

---

## 八、分析总结（来自 c4_summary_profile.md）

### 公司画像
{一段话概括公司是什么、做什么、处于什么阶段}

### 核心优势
1. {优势1}
2. {优势2}
3. {优势3}

### 主要关注点
1. {关注点1}
2. {关注点2}
3. {关注点3}

---

## 九、关键跟踪指标（来自 c5_tracking_metrics.md）

| 指标 | 当前值 | 预警条件 | 跟踪频率 |
|------|--------|---------|---------|
| ROE(%) | X% | <10%连续2季度 | 每季度 |
| 毛利率(%) | X% | 连续下降>5个百分点 | 每季度 |
| 经营现金流/净利润 | X | <0.8持续2季度 | 每季度 |
| 大股东质押比例(%) | X% | >50% | 每季度 |
| PE历史分位 | X% | >90% | 每月 |
| 融资余额 | X亿 | >流通市值15% | 每周 |

---

**声明：本报告仅为基本面分析，不构成任何投资建议。投资决策请根据自身情况独立判断。**
```

---

## 输出要求

完成后将最终报告写入：
`C:\Users\pd\.openclaw\workspace-analysts\data\{股票代码}\report.md`

回复格式：
```
✅ 最终报告已生成：report.md
📊 分析维度：6个
🧠 投资哲学：三问题 + 五法则
⚠️ 风险评级：P0/P1/P2/P3
📝 关键跟踪指标：X个
```

---

## 异常处理

| 情况 | 处理方式 |
|------|---------|
| 某分析文件缺失 | 主Agent直接撰写该章节内容 |
| 某汇总文件缺失 | 主Agent直接补充该章节内容 |
| 文件全部存在 | 直接汇总 |
