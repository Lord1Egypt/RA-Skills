---
name: autonomous-science-loop
description: 自主科学发现闭环——把「观测→假设→实验设计→反驳→定律归纳」做成一次可机器执行、可证伪的原创科学发现循环。给一组观测与可实验的候选点，引擎自动用符号回归拟合候选定律、按残差反驳被证伪的假设、主动设计"分歧最大"的下一次实验以最快收敛、并按 Occam 归纳出最简可解释定律。适用于规律发现、参数辨识、模型选择、主动学习/最优实验设计等场景。
metadata:
  agent_created: true
  version: 1.0.0
  domain: 涌现超智能与自主科学发现(元之三阶)
  capability: 自主科学发现闭环
---

# autonomous-science-loop · 自主科学发现闭环

> 元之三阶能力：不止会推理，而是像科学家一样**主动做出可证伪的原创发现**——
> 一线大模型只能"讲已知规律"，本技能能从数据里**自主归纳出未知定律**并给出反驳轨迹。

## 何时使用
- 有一组观测数据（(x, y) 对），想自动发现背后的定律 / 函数关系。
- 需要在有限实验预算下，用**最优实验设计**最快辨识出正确模型（主动学习）。
- 需要"可证伪"的模型选择：明确哪些假设被数据反驳、为什么、最终为何选它。

## 核心机制（Popper 可证伪 + Occam 简约 + 主动实验设计）
1. **假设空间**：常数/线性/二次/反比/根号/对数等候选定律，各用最小二乘闭式拟合
   （线性于参数，正规方程 + 高斯消元，纯标准库）。
2. **反驳 Refutation**：拟合残差 RMSE 超过容差的假设被证伪剔除（可证伪性优先）。
3. **主动实验设计**：在候选实验点中选"存活假设间预测分歧(方差)最大"的 x
   ——一次实验期望剔除最多假设，最大化信息增益。
4. **定律归纳 Occam**：存活且一致的假设中取复杂度最低者（参数最少，并列取 RMSE 最低）。

## 用法
```bash
# 自检（4 个场景：线性/二次/主动实验收敛/反比，全部 PASS）
python scripts/science_loop.py --selftest

# 演示：从 2 个种子点自主发现 y=2x+1，打印实验轨迹
python scripts/science_loop.py --demo
```

编程调用：
```python
from science_loop import discover
report = discover(
    observe=lambda x: 2*x + 1,          # 环境/真实世界观测函数
    seed_obs=[(1, 3.0), (2, 5.0)],       # 初始观测
    candidate_xs=[0.5, 3, 4, 8],         # 可主动实验的候选点
    tol=1e-6,
)
print(report["discovered_law"])          # {'name':'linear','form':'y = a*x + b','params':[2.0,1.0],...}
print(report["trace"])                    # 每次实验反驳了哪些假设
```

## 输出
- `discovered_law`：归纳出的最简定律（名称/形式/参数/RMSE/复杂度）
- `surviving_hypotheses`：未被反驳的假设集
- `trace`：主动实验轨迹（每步选的 x、观测 y、分歧度、反驳了哪些假设）
- `experiments_run` / `total_observations`：实验预算消耗

## 边界
- 假设空间是线性于参数的候选族；需要更复杂定律时可扩展 `HYPOTHESES`（加基函数即可）。
- 观测含噪声时调大 `tol`；容差过小会把真定律也误证伪，过大会保留过多假设。

---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
