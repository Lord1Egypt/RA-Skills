# 阶段二分析任务 - sessions_spawn 使用指南

> 本目录包含6个独立的任务提示词，用于通过 sessions_spawn 派遣子Agent执行分析任务。

---

## 6个分析任务一览

| 任务 | 提示词文件 | 输入数据文件 | 输出文件 |
|------|-----------|------------|---------|
| B-1 快速画像 | `b1_quick_profile.md` | cpbd.md + gsgk.md | quick_profile_analysis.md |
| B-2 行业与护城河 | `b2_industry_moat.md` | gsgk.md + hxtc.md + thbj.md | industry_moat_analysis.md |
| B-3 财务质量 | `b3_financial_quality.md` | cwfx.md + jyfx.md | financial_quality_analysis.md |
| B-4 公司治理 | `b4_governance.md` | gsgg.md + gdyj.md + gbjg.md | governance_analysis.md |
| B-5 估值与资本运作 | `b5_valuation.md` | thbj.md + fhfx.md + zbyz.md | valuation_analysis.md |
| B-6 资金与市场情绪 | `b6_fund_market.md` | zjlx.md + lhbd.md + glgg.md + gsds.md + zxgg.md | fund_market_analysis.md |

---

## sessions_spawn 使用方式

### 方式一：6个任务并行（推荐）

一次性启动6个独立子Agent，并行执行6个分析任务：

```json
// B-1 快速画像
sessions_spawn:
  task: "<读取 b1_quick_profile.md 的全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300

// B-2 行业与护城河
sessions_spawn:
  task: "<读取 b2_industry_moat.md 的全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300

// B-3 财务质量
sessions_spawn:
  task: "<读取 b3_financial_quality.md 的全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300

// B-4 公司治理
sessions_spawn:
  task: "<读取 b4_governance.md 的全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300

// B-5 估值与资本运作
sessions_spawn:
  task: "<读取 b5_valuation.md 的全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300

// B-6 资金与市场情绪
sessions_spawn:
  task: "<读取 b6_fund_market.md 的全部内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300
```

### 方式二：逐一派发（任务量较大时）

启动1个持久子Agent，依次执行6个任务：

```
sessions_spawn:
  task: "<b1_quick_profile.md 全部内容>"
  runtime: "subagent"
  mode: "session"
  runTimeoutSeconds: 0
```

然后通过 `sessions_send` 依次发送：
1. B-1 任务 → 等完成
2. B-2 任务 → 等完成
3. ... 共6个任务

---

## 任务状态追踪

主Agent维护6个任务的状态：

```
B-1: pending → running → completed / failed
B-2: pending → running → completed / failed
B-3: pending → running → completed / failed
B-4: pending → running → completed / failed
B-5: pending → running → completed / failed
B-6: pending → running → completed / failed
```

**完成标准：**
- 6个输出文件全部存在
- 每个文件 > 1KB
- 包含表格数据和结论文字（非空壳）

---

## 异常处理

| 情况 | 处理方式 |
|------|---------|
| 单个子Agent超时 | 重试该任务（最多2次） |
| 文件写入失败 | 检查目录权限，重试 |
| 输入文件不存在 | 跳过该任务，报告中注明"数据缺失" |
| 任务失败 | 标记failed，继续其他任务，最后重试失败项 |

---

## 阶段二完成标准

```
✓ 6个分析文件全部存在于 data/{代码}/ 目录
✓ 每个文件包含：表格数据 + 综合评分 + 结论文字
✓ 主Agent汇总6个分析结果，执行投资哲学检查
```

阶段二完成后，主Agent进入阶段三：报告汇总。
