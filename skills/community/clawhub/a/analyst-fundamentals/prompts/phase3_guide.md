# 阶段三：最终报告汇总 - sessions_spawn 多任务执行指南

> 本目录包含阶段三的汇总任务，通过 sessions_spawn 并行执行，最后合成最终报告。

---

## 阶段三任务架构

```
阶段二输出的6个分析文件
    │
    ├─ sessions_spawn ──→ C-1: 三大核心问题分析
    ├─ sessions_spawn ──→ C-2: 五大经验法则验证
    ├─ sessions_spawn ──→ C-3: 风险提示汇总
    ├─ sessions_spawn ──→ C-4: 公司画像+核心优势+主要关注点
    └─ sessions_spawn ──→ C-5: 关键跟踪指标
            │
            ↓ (5个任务全部完成后)
    主Agent汇总 ──→ 生成 report.md
```

---

## 5个汇总任务一览

| 任务 | 提示词文件 | 输入 | 输出 |
|------|-----------|------|------|
| C-1 三大核心问题 | `c1_three_questions.md` | 6个分析文件 | 三大问题结论表 |
| C-2 五大经验法则 | `c2_five_rules.md` | 6个分析文件 | 五法验证表 |
| C-3 风险提示 | `c3_risk_warnings.md` | 6个分析文件 | 风险清单 |
| C-4 总结画像 | `c4_summary_profile.md` | 6个分析文件 | 画像+优劣势 |
| C-5 跟踪指标 | `c5_tracking_metrics.md` | 6个分析文件 | 跟踪指标表 |

---

## sessions_spawn 并行执行（推荐方式）

一次性启动5个独立子Agent：

```json
// C-1: 三大核心问题分析
sessions_spawn:
  task: "<读取 c1_three_questions.md 全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 180

// C-2: 五大经验法则验证
sessions_spawn:
  task: "<读取 c2_five_rules.md 全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 180

// C-3: 风险提示汇总
sessions_spawn:
  task: "<读取 c3_risk_warnings.md 全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 180

// C-4: 公司画像+核心优势+主要关注点
sessions_spawn:
  task: "<读取 c4_summary_profile.md 全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 180

// C-5: 关键跟踪指标
sessions_spawn:
  task: "<读取 c5_tracking_metrics.md 全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 180
```

---

## 主Agent汇总逻辑

5个任务全部完成后，主Agent执行：

```
1. 读取 data/{代码}/c1_c3_*.md ~ c5_*.md 的5个汇总文件
2. 读取 data/{代码}/quick_profile_analysis.md
3. 读取 data/{代码}/industry_moat_analysis.md
4. 读取 data/{代码}/financial_quality_analysis.md
5. 读取 data/{代码}/governance_analysis.md
6. 读取 data/{代码}/valuation_analysis.md
7. 读取 data/{代码}/fund_market_analysis.md

8. 按最终报告模板合成 report.md

9. 回复用户：分析完成，报告已生成
```

---

## 最终报告结构

```markdown
# {股票名称}（{代码}）基本面分析报告

> 报告日期：{日期}
> 报告性质：基本面研究分析，不构成任何投资建议

---

## 一、快速画像
{quick_profile_analysis.md 全文}

## 二、行业与护城河
{industry_moat_analysis.md 全文}

## 三、财务质量
{financial_quality_analysis.md 全文}

## 四、公司治理
{governance_analysis.md 全文}

## 五、估值与资本运作
{valuation_analysis.md 全文}

## 六、资金与市场情绪
{fund_market_analysis.md 全文}

---

## 七、投资哲学分析

### 三大核心问题判断（来自C-1）
| 核心问题 | 结论 | 依据 |
|----------|------|------|
| 问题1：好生意？ | | |
| 问题2：好管理层？ | | |
| 问题3：好价格？ | | |

### 五大经验法则验证（来自C-2）
| 法则 | 验证结果 | 说明 |
|------|----------|------|
| ROE核心 | ✅/⚠️/❌ | |
| 现金流 | ✅/⚠️/❌ | |
| 管理层 | ✅/⚠️/❌ | |
| 估值 | ✅/⚠️/❌ | |
| 风险排查 | ✅/⚠️/❌ | |

### 风险提示（来自C-3）
1. ...
2. ...
3. ...

---

## 八、分析总结（来自C-4）

### 公司画像
[一段话概括：公司是什么、做什么、处于什么阶段]

### 核心优势
1. ...
2. ...
3. ...

### 主要关注点
1. ...
2. ...
3. ...

---

## 九、关键跟踪指标（来自C-5）
| 指标 | 当前值 | 跟踪意义 | 参考标准 |
|------|--------|---------|---------|
| | | | |

---

**声明：本报告仅为基本面分析，不构成任何投资建议。投资决策请根据自身情况独立判断。**
```

---

## 阶段三完成标准

```
✓ C-1 ~ C-5 五个汇总文件全部存在
✓ report.md 包含完整8个章节
✓ 声明文字完整
```

---

## 异常处理

| 情况 | 处理方式 |
|------|---------|
| 单个汇总任务失败 | 主Agent直接撰写该章节内容 |
| 某个分析文件缺失 | 跳过该章节，报告中注明"数据缺失" |
| 子Agent超时 | 主Agent直接执行该任务 |
