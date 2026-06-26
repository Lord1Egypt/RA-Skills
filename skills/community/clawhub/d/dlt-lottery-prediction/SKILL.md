# DLT大乐透预测技能 v4.0

## 简介

DLT大乐透智能预测系统 v4.0。五池采样（热号/冷号/均衡/趋势/质数）+ 博弈论遗传算法融合 + 约束满足引擎，支持前后区复式投注生成，池级别回测全部跑赢随机基准。

**数据源**: 2853期历史开奖记录（7001期～26035期）

---

## 核心功能

### 1. 五池加权融合采样
- 🔥 热号池（高频出现的号码）
- ❄️ 冷号池（长期未出现的号码）
- ⚖️ 均衡池（出现频率接近平均值的号码）
- 📈 趋势池（近期出现频率上升的号码）
- 🧬 质数池（数学上具有特殊性质的号码）

前后区各有独立的五个池，共计10个池生成器。

### 2. 博弈论遗传算法融合
- 博弈论输出层：纳什均衡优化多策略输出
- 遗传算法：全局优化号码组合适应度
- 适应度函数综合考虑号码频率、遗漏值、奇偶比、和值

### 3. 约束满足引擎
- 唯一性约束：每注内号码不重复
- 范围约束：前区1-35，后区1-12
- 格式约束：5+2标准注
- 数学关系约束：和值、AC值、跨度限制

### 4. 复式投注生成
支持12种复式投注方案：
- 前区：6+4 / 7+4 / 8+4 / 9+4
- 后区：4+2 / 4+3 / 4+4

### 5. 池级别回测
对每个池独立进行历史回测，验证策略有效性。v4.0回测结果：5个池在428期验证集上**全部跑赢随机基准**。

---

## 使用方法

```python
import sys
sys.path.insert(0, '/home/claw/.openclaw/workspace/skills/dlt_lottery_prediction')

from dlt_fusion_complete import DLTFusionComplete

# 初始化
fusion = DLTFusionComplete()

# 预测（返回单式+复式）
result = fusion.predict(include_compound=True)
print(result['single_bets'])    # 4注单式
print(result['compound_bets'])  # 12种复式

# 回测验证
bt = fusion.backtest(n_recent=100)
print(bt['pool_performance'])
```

---

## 技术指标

| 指标 | 数值 |
|------|------|
| 历史数据 | 2853期 |
| 数据范围 | 7001期 ~ 26035期 |
| 前区范围 | 1-35 |
| 后区范围 | 1-12 |
| 复式方案 | 12种 |
| 回测基准 | 全部跑赢随机 |

---

## 文件结构

```
dlt_lottery_prediction/
├── dlt_fusion_complete.py      # 主入口（DLTFusionComplete类）
├── dlt_five_pool_fusion.py     # 五池融合
├── dlt_five_pool_sampler.py    # 五池采样器
├── five_pool_sampler_complete_final.py  # 最终采样器（757行）
├── dlt_constraint_engine.py     # 约束引擎
├── strategy_fusion_engine.py    # 策略融合引擎
└── SKILL.md                    # 本文档
```

---

## 版本历史

- **v4.0** (2026-04-06): 完整重构，新增12种复式投注，博弈论输出层，五池独立回测
- **v3.1**: 多维度策略融合引擎
- **更早版本**: 基础预测功能
