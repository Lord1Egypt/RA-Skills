# 地动仪气候模型 Dizhenyi Climate Model v3.0

> 基于米兰科维奇轨道理论 + 分数阶能量平衡方程（FEBE）的跨尺度气候预测框架

## 🌍 项目概述

"地动仪"气候模型是一套开源气候预测框架，通过将地球轨道参数的微小变化通过多圈层非线性反馈机制放大，预测从百年到十万年尺度的气候演化。

### 核心创新

1. **"感知-放大"物理范式** — 受东汉张衡候风地动仪启发
2. **FEBE 分数阶方程** — 精确刻画气候系统记忆效应
3. **La2004 轨道解** — Laskar 天文解的相位校准实现
4. **双向校准** — 20年真实数据 + 10万年古气候代理验证
5. **IPCC ECS 校准** — 与 AR6 报告气候敏感度一致

## 📊 模型能力

| 功能 | 时间尺度 | 精度 | 状态 |
|------|----------|------|------|
| 长期气候预测 | 10³–10⁵ 年 | ~5%（轨道） | ✅ 已验证 |
| 近期气候推演 | 至 2100 年 | IPCC AR6 级 | ✅ 已验证 |
| 极端事件预警 | 事件驱动 | 三阶指标 | ✅ 已验证 |
| 东亚季风预测 | 2025–2100 | 校准 RMSE=0.04 | ✅ 已验证 |
| RCP 情景对比 | 2025–2100 | IPCC AR6 级 | ✅ 已验证 |
| 古气候回溯 | 100 万年 | > 90% 周期匹配 | ✅ 已验证 |
| 冰期推迟测试 | ~10 万年 | 与文献一致 | ✅ 已验证 |

## 📁 目录结构

```
dizhendongyi-climate/
├── SKILL.md              技能说明（OpenClaw 技能格式）
├── README.md             项目文档
├── requirements.txt      Python 依赖
├── references/
│   ├── core_theory.md    核心理论框架
│   ├── extreme_events.md 极端事件预警体系
│   ├── orbital_data.md   轨道参数公式
│   └── verification.md   验证案例
└── scripts/
    ├── orbital_forcing.py      轨道强迫计算
    ├── febe_solver.py          FEBE 方程求解
    ├── climate_predictor.py    综合预测主程序
    ├── east_asian_monsoon.py   东亚季风预测
    └── scenario_comparison.py  RCP 情景对比
```

## 🚀 快速开始

```bash
# 安装依赖
pip install numpy

# 长期预测
python3 scripts/climate_predictor.py long

# 近期推演
python3 scripts/climate_predictor.py near rcp85 2025 2100

# EASM 预测
python3 scripts/east_asian_monsoon.py 2025 2075

# 情景对比
python3 scripts/scenario_comparison.py
```

## 📖 核心方程

### 轨道强迫

$$Q_{65}(t) = Q_{65,0} + A_{\psi}\psi(t) + A_{\epsilon}(\epsilon(t)-\epsilon_0)$$

### FEBE

$$\Delta T(t) = \lambda_{eq} F_{total}(t) [1 - E_{h,1}(-(t/\tau)^h)]$$

### EASM

$$EASM(t) = \alpha F_{orb}(t) + \beta \Delta T_{CO2}(t) + \gamma$$

## ⚠️ 免责声明

本模型用于科学研究和学术探讨。预测结果仅供参考，不构成任何气候政策建议。

## 📜 许可证

MIT License

## 👥 作者

Figo Cheung, Figo AI Team

## 🔗 关联

- [论文](papers/基于"地动仪"框架的地球系统非线性气候演化机制与东亚季风预测.md)
- [冰期推演报告](papers/地动仪气候模型推演报告：RCP8.5情景下下一冰期能否被推迟.md)
