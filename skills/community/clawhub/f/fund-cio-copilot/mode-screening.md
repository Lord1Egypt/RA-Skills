# Mode 1 — Screening（BP 初筛）

## 定位
高通量过滤器。对应基金工作流「3000 BP → 200 立项」。目标：**30 秒 - 2 分钟**完成一份 BP 筛选意见。超过 2 分钟说明已进入 Evaluation，应切换模式。

## 唯一核心决策
> **进入立项？YES / NO / WATCH**

不讨论估值、席位、退出、条款。超出范畴立即收敛（One Decision, One Owner）。

## 执行三步（顺序不可乱）

### Step 1：Mandate Check（硬门槛，调用 mandate.md）
逐项核对基金画像硬约束：
- Stage（阶段）：项目阶段是否在基金投资范围？
- Sector（赛道）：是否在基金产业方向？
- Region（区域）：是否符合落地/返投区域？
- Ticket（单项目额度）：拟融资额是否超单项目上限？
- Government Constraints（返投/招商）：是否满足？

输出：`Mandate Fit` + 命中/违反的硬约束清单
- 任一硬约束违反 → 标记 ❗，提示"建议终止深度分析，除非存在战略投资理由"

### Step 2：Quick Deal Killer（Hard Killer 快速检查，不展开 DD）
只跑，不深入分析，对应 Quality Gate 的 Hard Killers（K1–K4）：
1. K1 创始人诚信：有无明显诉讼/造假/圈钱信号？（仅基于用户提供信息判断）
2. K2 IP 权属：归属是否明显不清/存在诉讼？（→ 另走 Compliance Gate）
3. K3 收入真实性：有无合同造假/关联方交易迹象？
4. K4 技术存在性：是否纯 PPT 无 MVP/客户案例？
5. 合规（环保/安全/数据）→ 另走 Compliance Gate，不在此处展开

任一触发 → 直接 `NO`（记录触发项），终止后续分析，**不得被评分覆盖**。

### Step 3：Market Sanity Check（市场存在性，非产业分析）
只回答三个问题（不展开 Industry Layer 动态护城河）：
- 市场存在吗？（赛道是否真实存在、有付费方）
- 赛道还活着吗？（是否在上升期 / 非衰退）
- Timing 合理吗？（技术成熟度 + 政策周期是否支持现在进入）

输出：✅/⚠️/❓ 三档。❓ 标注"需 Evaluation 阶段核实"。

## 输出：Screening Card（一页内）
```
【Screening Card】
项目：XXX
时间：YYYY-MM-DD

Mandate Fit：✅ 82 / ❗ 42（违反：超阶段 / 超额度）
Deal Killer：None / ❗ 触发（技术不可验证）
Market Sanity：✅ 存在且上升 / ⚠️ 需核实

决策：进入立项 YES / NO / WATCH
理由（≤3 条）：
1. ...
2. ...
3. ...

Confidence：High / Medium / Low
免责：分析建议 · 非投资决定 · 需 IC 审议
```

## 决策映射
| 结果 | 动作 |
|------|------|
| Mandate ❗ 或 Deal Killer ❗ | NO（Capture，记录否决原因） |
| Market Sanity ❓ | WATCH（建议补充信息后重评） |
| 全部通过 | YES（进入 Evaluation） |

## 强制 Capture
无论 YES/NO/WATCH，生成 Decision Object（mode=screening）并存储。被筛掉的 NO 项目是机构记忆里最值钱的部分。
