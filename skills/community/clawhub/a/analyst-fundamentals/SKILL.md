---
name: "analyst-fundamentals"
description: "A股基本面深度分析工具。当用户提供股票代码或要求分析股票基本面时调用。"
---

# 股票基本面分析 Skill（完整版）

> **定位：纯基本面分析工具，不做投资决策建议**
>
> **分析哲学：宁可错过，不可做错。投资是认知的变现。**

---

## 触发条件

**立即调用本 Skill 当：**
- 用户提供股票代码（如 `002594`、`SH600519`、`300032`）
- 用户要求分析某只股票的基本面
- 用户询问某公司的财务状况、经营情况

---

## 执行流程总览

```
用户输入股票代码
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 阶段一：数据获取（16并行子Agent，一次性全量派发）              │
│ • sessions_spawn 启动16个子Agent（mode=run，并行执行）       │
│ • 每个子Agent独立browser，抓取1个F10模块写入对应md文件       │
│ • 全部完成后主Agent汇总                                      │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 阶段二：分析生成（6并行子Agent）                               │
│ • sessions_spawn 一次性启动6个子Agent（mode=run）            │
│ • 每个Agent读取2-5个原始数据文件                              │
│ • 按投资哲学框架输出结构化分析报告                            │
│ • B1-B6并行执行，完成后主Agent汇总                           │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ 阶段三：报告汇总（5并行子Agent + 主Agent汇总）                  │
│ • sessions_spawn 一次性启动5个子Agent（mode=run）            │
│ • C1-C5并行：三大核心问题/五法验证/风险提示/画像优劣势/跟踪指标│
│ • 主Agent读取11个分析文件，合成最终report.md                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 阶段一详解

### 16个F10模块并行抓取

| # | 模块 | Hash | 文件 |
|---|------|------|------|
| 1 | 公司概况 | gsgk | gsgk.md |
| 2 | 经营分析 | jyfx | jyfx.md |
| 3 | 财务分析 | cwfx | cwfx.md |
| 4 | 核心题材 | hxtc | hxtc.md |
| 5 | 操盘必读 | cpbd | cpbd.md |
| 6 | 同行比较 | thbj | thbj.md |
| 7 | 股东研究 | gdyj | gdyj.md |
| 8 | 分红融资 | fhfx | fhfx.md |
| 9 | 公司高管 | gsgg | gsgg.md |
| 10 | 资金流向 | zjlx | zjlx.md |
| 11 | 资本运作 | zbyz | zbyz.md |
| 12 | 公司大事 | gsds | gsds.md |
| 13 | 资讯公告 | zxgg | zxgg.md |
| 14 | 股本结构 | gbjg | gbjg.md |
| 15 | 关联个股 | glgg | glgg.md |
| 16 | 龙虎榜单 | lhbd | lhbd.md |

### 子Agent任务消息格式

每个子Agent接收以下格式的任务：

```
请抓取以下F10数据模块：

股票代码：{代码}
市场：SZ（深圳以00/3开头）/ SH（上海以6开头）
URL：https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={市场}{代码}&color=b#/{hash}
输出文件：C:\Users\pd\.openclaw\workspace-analysts\data\{代码}\{hash}.md

执行步骤：
1. browser.start()（如未启动）
2. browser.open(url)
3. browser.snapshot(compact=true)
4. 提炼关键数据，写入输出文件
5. 完成后回复"模块{hash}.md已完成"
```

### 主Agent执行步骤（阶段一）

```
1. mkdir -p data/{代码}
2. sessions_spawn 一次性启动16个子Agent（mode=run）
   - 每个Agent分配1个模块（hash）
   - runtime: "subagent"
   - runTimeoutSeconds: 120
3. 等待所有子Agent完成
```

---

## 阶段二详解

### 6个并行分析任务

| 任务 | 文件 | 输入数据 | 输出 |
|------|------|---------|------|
| B-1 快速画像 | b1_quick_profile.md | cpbd+gsgk | quick_profile_analysis.md |
| B-2 行业护城河 | b2_industry_moat.md | gsgk+hxtc+thbj | industry_moat_analysis.md |
| B-3 财务质量 | b3_financial_quality.md | cwfx+jyfx | financial_quality_analysis.md |
| B-4 公司治理 | b4_governance.md | gsgg+gdyj+gbjg | governance_analysis.md |
| B-5 估值资本 | b5_valuation.md | thbj+fhfx+zbyz | valuation_analysis.md |
| B-6 资金情绪 | b6_fund_market.md | zjlx+lhbd+glgg+gsds+zxgg | fund_market_analysis.md |

### sessions_spawn 执行方式（阶段二）

```json
// 6个并行（一次性全量派发）
sessions_spawn × 6:
  task: "<读取对应提示词文件bX_xxx.md内容>"
  runtime: "subagent"
  mode: "run"
  runTimeoutSeconds: 300
```

---

## 阶段三详解

### 5个并行汇总任务

| 任务 | 文件 | 核心输出 |
|------|------|---------|
| C-1 三大核心问题 | c1_three_questions.md | 三维度判断结论表 |
| C-2 五大经验法则 | c2_five_rules.md | 五法验证表（✅/⚠️/❌） |
| C-3 风险提示 | c3_risk_warnings.md | P0/P1/P2/P3分级风险清单 |
| C-4 画像优劣势 | c4_summary_profile.md | 公司画像+核心优势+主要关注点 |
| C-5 跟踪指标 | c5_tracking_metrics.md | 关键指标+预警条件+跟踪频率 |

### 主Agent汇总

```
读取6个分析文件 + 5个汇总文件
→ 填充 report_synthesis.md 模板
→ 输出 data/{代码}/report.md
```

---

## 输出文件结构

```
data/{股票代码}/
├── gsgk.md ~ lhbd.md          # 16个原始数据
├── quick_profile_analysis.md     # B-1
├── industry_moat_analysis.md   # B-2
├── financial_quality_analysis.md # B-3
├── governance_analysis.md        # B-4
├── valuation_analysis.md        # B-5
├── fund_market_analysis.md      # B-6
├── c1_three_questions.md        # C-1
├── c2_five_rules.md            # C-2
├── c3_risk_warnings.md         # C-3
├── c4_summary_profile.md        # C-4
├── c5_tracking_metrics.md       # C-5
└── report.md                    # 最终报告
```

---

## 投资哲学框架（内置于每个提示词）

### 三大核心问题

| 问题 | 对应分析维度 | 判断标准 |
|------|------------|---------|
| 好生意？ | 行业护城河+财务质量 | ROE>15%、毛利率>30%、现金流健康、护城河≥8分 |
| 好管理层？ | 公司治理 | 管理团队>4分、任职>5年、持股、高质押<30% |
| 好价格？ | 估值资本运作 | PE分位<50%、PEG<1.5、股息率>3% |

### 五大经验法则

```
法则1：ROE核心 → 连续3年>15%优秀
法则2：现金流 → 净现比>1利润质量好
法则3：管理层 → 无违规+专注主业+利益一致
法则4：估值 → PE分位<50%合理，>70%高危
法则5：风险排查 → 存贷双高/现金流持续为负/质押>50% → 一票否决
```

### 一票否决项

```
□ 存贷双高
□ 经营现金流连续2年为负
□ 大股东质押>50%
□ 频繁关联交易
□ 审计非标
□ 商誉占净资产>30%
□ 毛利率远高于同行
□ 应收账款持续异常
```

---

## sessions_spawn 参数说明

### mode="run"（推荐用于一次性任务）

```json
{
  "task": "任务描述",
  "runtime": "subagent",
  "mode": "run",
  "runTimeoutSeconds": 120
}
```

### 关键约束

- `mode="run"`：**一次性任务**，发完即结束，无需 thread 参数
- `mode="session"`：**持久会话**，需要 `thread=true`（当前webchat不支持）
- 所有阶段均使用 `mode="run"`，避免使用 `mode="session"`
