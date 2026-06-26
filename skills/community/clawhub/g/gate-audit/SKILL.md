---
name: gate-audit
description: Use this skill when the user provides AF2, ESMFold, AF3, Boltz-1, SASA, or MD results and needs a Gate 1-4 audit with a Go/Hold/Kill decision.
user-invocable: true
---

# Purpose
用于纳米载体疫苗计算设计中的结构、暴露、MD 与终审门禁判定。  
本 skill 专门负责 Gate 1–4 的证据整理与 Go / Hold / Kill 判断。

# When to use
当用户提供以下任一信息时调用：
- AF2 / ESMFold / AF3 / Boltz-1 预测结果。
- SASA / 表位暴露结果。
- 2–5 ns 平衡审计结果。
- 100 ns MD 结果。
- checkpoint、日志、NPT 密度、RMSD、Rg、关键距离等摘要。

# Audit dimensions
必须分开检查以下五项：
1. 结构可行性
2. 表位可及性
3. 动力学稳定性
4. 工程可制造性
5. 是否值得进入更昂贵计算

# Required checks
## Gate 1
- 结构拓扑是否合理
- 关键区段是否断裂
- linker 与展示端是否冲突
- 是否存在明显界面错误

## Gate 2
- 表位是否动态可及
- 是否长期遮挡
- SASA 是否支持进入 MD
- 是否存在构象塌陷导致暴露丢失

## Gate 3
- 2–5 ns 是否达到基本平衡
- 温度、压力、密度是否正常
- 是否存在日志缺失、checkpoint 缺失、输出文件异常
- 是否存在爆炸、持续漂移、异常离子行为

## Gate 4
- 100 ns 是否优于负对照或历史基线
- repeat 间是否趋势一致
- 长程下表位是否保持暴露
- 是否具备进入 CpHMD / TI-FEP 资格

# Required output format
1. 输入结果摘要
2. Gate 1 判定
3. Gate 2 判定
4. Gate 3 判定
5. Gate 4 判定
6. 主要失败模式
7. 决策：Go / Hold / Kill
8. 需要补跑的数据

# Default decision logic
- 只要存在关键日志缺失、checkpoint 异常或体系健康不明，默认 Hold。
- 若结构逻辑不成立或表位长期不可及，默认 Kill。
- 只有在结构、暴露、动力学三者同时满足时，才 Go。
- CpHMD 和 TI/FEP 仅作为高级终审，不得作为补救一切问题的默认手段。

# Warnings
- 不得用单次最佳轨迹替代重复结果。
- 不得只用单个评分指标下结论。
- 不得忽略失败日志。
- 不得把高模型置信度当作物理正确性。
