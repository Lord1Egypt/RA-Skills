# Calculus Concept Visualizer - 微积分概念可视化助手

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/version-1.0.0-green" alt="Version">
  <img src="https://img.shields.io/badge/author-代国兴-orange" alt="Author">
  <img src="https://img.shields.io/badge/edu-高等数学-purple" alt="Education">
</p>

## 📚 简介

**Calculus Concept Visualizer** 是一个专门为**高等数学**和**考研数学**学习设计的 OpenClaw Skill。它基于**多表征转换理论**和**支架式教学**理念，通过动态可视化、认知诊断和即时检测，解决学生在微积分核心概念理解中的困难。

### 🎯 核心解决的问题

| 痛点 | 解决方案 |
|------|----------|
| **抽象性** - ε-δ 定义难以理解 | GeoGebra 交互式演示（双向滑块） |
| **静态性** - 静态图示无法展示变化过程 | 动态动画 + 学生操控 |
| **被动性** - "以为懂了实际没懂" | 即时诊断 + 认知冲突 |
| **孤立性** - 概念间缺乏连接 | 多表征转换 + 知识图谱 |

---

## 🚀 功能特性

### 1. 动态可视化生成
- ✅ **ε-δ 极限定义**: 可拖动的 ε/δ 滑块，实时验证条件
- ✅ **导数几何意义**: 割线→切线的演变动画
- ✅ **黎曼和构造**: 动态展示积分思想
- ✅ **泰勒展开**: 逐步逼近可视化

### 2. 认知误区诊断
内置 **20+ 种常见误区模式**:
- 🔴 **高危**: 极限=函数值、ε-δ 逻辑颠倒、连续=可导
- 🟡 **中危**: 单侧极限混淆、积分=绝对面积
- 🟢 **低危**: 符号表述不严谨

### 3. 渐进式检测
每概念配套 **3 道检测题**:
1. **识别层** (30%) - 概念辨析
2. **应用层** (40%) - 计算/证明
3. **迁移层** (30%) - 变式/创新

### 4. 分步推导动画
- ε-δ 证明的 5 步严谨推导
- 链式法则的极限推导
- 微积分基本定理证明
- 泰勒公式系数推导

---

## 📦 安装

### 前置要求
- OpenClaw >= 2026.3.20
- Python >= 3.8
- 可选: GeoGebra Classic 6 (用于本地打开 .ggb 文件)

### 安装步骤

```bash
# 1. 安装 OpenClaw
pip install openclaw

# 2. 安装本 Skill
openclaw skills install daigxok/calculus-concept-visualizer

# 3. 验证安装
openclaw skills list | grep calculus-concept-visualizer
```

### 手动安装（开发模式）

```bash
# 1. 克隆仓库
git clone https://github.com/daigxok/calculus-concept-visualizer.git

# 2. 链接到 OpenClaw
openclaw skills link ./calculus-concept-visualizer

# 3. 运行测试
python tests/test_skill.py
```

---

## 🎮 使用方法

### 基础概念可视化

```bash
# ε-δ 极限定义演示
openclaw run calculus-concept-visualizer --concept limit --focus epsilon_delta

# 导数几何意义
openclaw run calculus-concept-visualizer --concept derivative --visualization secant_to_tangent

# 黎曼和动态构建
openclaw run calculus-concept-visualizer --concept integral --method riemann_sum
```

### 针对性诊断教学

```bash
# 诊断学生误区
openclaw run calculus-concept-visualizer --diagnose "极限就是代入计算" --concept limit

# 生成干预方案
openclaw run calculus-concept-visualizer --intervention limit_equals_value

# 生成检测题组
openclaw run calculus-concept-visualizer --quiz limit --difficulty 0.7
```

### 分步推导展示

```bash
# ε-δ 证明推导
openclaw run calculus-concept-visualizer --derive epsilon_delta_proof --function "3x-1" --a 2 --L 5

# 链式法则推导
openclaw run calculus-concept-visualizer --derive chain_rule

# 微积分基本定理证明
openclaw run calculus-concept-visualizer --derive ftc_proof
```

### 交互式对话（推荐）

```bash
# 启动 OpenClaw 对话
openclaw chat

# 然后输入:
"请帮我理解极限的 ε-δ 定义"
"如何纠正学生认为'连续必可导'的错误？"
"生成一道检测泰勒展开理解的迁移题"
```

---

## 🏗️ 技术架构

```
calculus-concept-visualizer/
├── SKILL.md                    # Skill 元数据
├── hermes.config.yaml          # Hermes Agent 配置
├── prompts/
│   ├── system.md               # 系统角色定义
│   ├── concept-explainer.md    # 概念解释模板
│   └── misconception-detector.md # 误区诊断模板
├── tools/
│   ├── generate_geogebra.py    # GeoGebra 配置生成
│   ├── plot_interactive.py     # Python 可视化
│   ├── diagnose_misconception.py # 认知诊断
│   ├── generate_quiz.py        # 检测题生成
│   └── step_builder.py         # 分步推导构建
└── tests/
    └── test_skill.py           # 测试套件
```

### 核心依赖
- `numpy` / `matplotlib` - 数值计算与可视化
- `plotly` - 交互式图表（可选）
- `sympy` - 符号数学（可选）

---

## 📚 教学原理

本 Skill 基于以下教育理论设计：

### 1. APOS 理论 (Dubinsky)
- **Action**: 通过交互操作体验数学过程
- **Process**: 内化动态变化的心智模型
- **Object**: 将过程封装为可操作的数学对象
- **Schema**: 构建概念网络与关联

### 2. 多表征转换理论 (Lesh)
强调概念必须在不同表征间灵活转换：
- 现实情境 → 口语描述 → 图像 → 符号

### 3. 支架式教学 (Vygotsky)
提供临时支持结构，随能力提升逐步撤除：
```
教师演示 → 师生互动 → 学生独立
```

---

## 🎓 适用场景

| 场景 | 功能应用 |
|------|----------|
| **课前预习** | 概念可视化建立直观认知 |
| **课堂演示** | 动态展示抽象定义 |
| **课后复习** | 误区诊断 + 针对性练习 |
| **考研辅导** | 深度理解命题逻辑 |
| **错题分析** | 定位概念理解偏差 |
| **教学研究** | 认知诊断数据收集 |

---

## 👨‍💻 作者信息

- **作者**: 代国兴
- **机构**: 高等数学智慧课程研究团队
- **邮箱**: daigx@example.edu.cn
- **GitHub**: [@daigxok](https://github.com/daigxok)
- **ClawHub**: [daigxok/calculus-concept-visualizer](https://clawhub.ai/daigxok/calculus-concept-visualizer)

### 相关项目
- [calculus-problem-generator](https://clawhub.ai/daigxok/calculus-problem-generator) - 考研数学题型生成
- [calculus-resource-harvester](https://clawhub.ai/daigxok/calculus-resource-harvester) - 数学资源采集

---

## 📄 许可证

MIT License - 开放教育资源，欢迎教学使用与改进。

```
Copyright (c) 2026 代国兴

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
```

---

## 🙏 致谢

- OpenClaw 团队提供的优秀 Agent 框架
- GeoGebra 提供的动态数学可视化工具
- 高等数学教育研究领域的理论支持

---

<p align="center">
  <b>让微积分学习从抽象走向直观，从被动走向主动</b>
</p>
