---
name: awar-maintenance
description: 机器人世界模型与动作模型（WAM）技术仓库维护Skill；支持搜集、分析、分类并生成图文并茂的AWAR仓库文档；包含科普介绍、深度技术分析、快速上手指南；当用户需要构建机器人AI领域技术仓库或研究VLA/RT-2/Dreamer等前沿工作时使用
---

# AWAR 仓库维护

> Awesome World-Action-Robotics - 机器人世界模型与动作模型技术全景图

## 仓库定位

AWAR (Awesome World-Action-Robotics) 是一个专注于机器人领域**世界模型（World Models）**与**动作模型（Action Models）**的技术仓库。目标是：

- **科普价值**: 让研究者快速入门 WAM 领域
- **技术深度**: 提供深度算法解析与横向对比
- **实用导向**: 每个项目包含快速上手指南与实操建议

---

## 什么是 World-Action Model？

### 核心概念

**World Model (世界模型)** 是智能体对环境动态的内部表征与预测系统。类比人类：当你伸手去拿水杯时，你的大脑会预测杯子会被拿起、倾斜、水会流出——这就是隐式世界模型的作用。

```
感知输入 → 世界模型 → 环境预测 / 动作输出
    ↑___________↓           ↑___________↓
       (闭环反馈)              (执行反馈)
```

**Action Model (动作模型)** 是将决策转化为具体执行动作的策略系统。它接收世界模型的预测作为输入，输出机器人各关节的控制指令。

### 为什么重要？

| 传统方法 | WAM 方法 |
|----------|----------|
| 手工设计奖励函数 | 隐式学习环境动态 |
| 短程规划（<10步） | 长程预测（100+步） |
| 单任务专用 | 跨任务泛化 |
| 仿真难以迁移 | 物理一致性建模 |

---

## 仓库结构

```
Awesome-World-Action-Robotics/
├── README.md                      # 主入口
├── assets/                        # 静态资源
│   ├── getting_started.md         # 入门指南
│   ├── overview.png               # 领域全景图
│   └── benchmark_table.md         # 性能对比总表
├── FOUNDATIONAL_WAMS.md           # 基础大模型（RT-2, OpenVLA, Pi0...）
├── PREDICTIVE_DYNAMICS.md         # 预测动力学（Dreamer, GAIA...）
├── SIMULATION_REAL2SIM.md        # 仿真与Sim2Real
└── ACTION_CONTROLLERS.md          # 动作控制器（ACT, Diffusion Policy...）
```

---

## 工作流程

### Phase 1: 探索与发现

**检索策略** - 使用以下关键词组合进行系统性搜索：

```
# 核心检索词
"World Models for Robotics" "Vision-Language-Action" "VLA Robot"
"Generative World Models" "Predictive Dynamics" "Action Chunking"

# 进阶检索词
"Diffusion Policy Robot" "Robot Foundation Model" "Sim-to-Real"
"Joint Embedding Predictive Architecture" "Latent World Model"
```

**发现来源优先级**:
1. arXiv (cs.RO, cs.LG, cs.AI) - 最新 preprint
2. GitHub Trending - 社区活跃度
3. 顶会论文 (CoRL, RSS, ICRA, NeurIPS, ICLR) - 质量保证
4. 机构博客 (DeepMind, OpenAI, Stanford, MIT) - 深度解读

### Phase 2: 深度解构

按四维度框架分析每个项目，详见 [references/awareness_analysis_framework.md](references/awareness_analysis_framework.md)。

**四维度分析**:

| 维度 | 关键问题 | 输出 |
|------|----------|------|
| **核心范式** | JEPA / RSSM / Diffusion / Transformer? | 架构分类与创新点 |
| **状态表征** | Pixel / Latent / PointCloud? | 表征方式与效率 |
| **动作集成** | Chunking / Diffusion / Tokenization? | 动作生成机制 |
| **物理一致性** | 闭环支持 / 长程稳定 / Sim2Real? | 可靠性评估 |

### Phase 3: 分类归档

根据 [references/classification_standard.md](references/classification_standard.md) 确定分类：

```
Foundational WAMs      → 基础大模型层
Predictive Dynamics    → 环境预测层
Simulation & Real2Sim   → 仿真数据层
Action Controllers     → 动作执行层
```

### Phase 4: 文档生成

按 [references/output_template.md](references/output_template.md) 生成标准化文档，必须包含：

- [x] 核心创新（算法突破点）
- [x] 架构图（项目结构/流程图）
- [x] Quick Start（3步上手指南）
- [x] Benchmark 数据（性能指标）
- [x] 开发者评估（配置难度/硬件适配）

---

## 文档质量标准

### 最低要求

每个项目文档必须包含：
- 一句话核心价值定位
- 架构图或流程图（使用 `assets/` 中的模板）
- 快速上手代码片段（3-5行核心调用）
- 至少一个 Benchmark 数据点

### 推荐做法

- 嵌入项目官方 Demo 视频链接
- 提供竞品对比表格
- 标注关键技术局限
- 添加中文注释（降低入门门槛）

### 禁止事项

- 禁止使用"令人惊叹"、"突破性"等主观词汇
- 禁止仅列名称无实质分析
- 禁止直接复制论文摘要（需改写为技术要点）
- 禁止缺失 Benchmark 数值

---

## 参考资源索引

| 资源 | 用途 |
|------|------|
| [references/getting_started.md](references/getting_started.md) | 领域入门、概念解释、学习路径 |
| [references/awareness_analysis_framework.md](references/awareness_analysis_framework.md) | 深度技术分析协议 |
| [references/classification_standard.md](references/classification_standard.md) | 分类标准与边界定义 |
| [references/output_template.md](references/output_template.md) | 文档输出模板与示例 |
| [assets/](assets/) | 架构图模板、徽章样式 |

---

## 维护规则

### 去重机制

- **同名项目**: 保留信息最完整、最新的记录
- **命名变体**: 建立别名映射（如 RT-2 = Robotic Transformer 2）
- **近似项目**: 分析核心差异点，选择性合并或并列

### 更新机制

- 发现新版本: 更新版本号、发布日期、Benchmark
- 发现新论文: 按发布日期归档，补充对比分析
- 发现停更: 添加 "Last Update" 标记与替代方案

### 贡献规范

- 每个 PR 必须包含至少一个项目的完整文档
- 新增项目需说明分类依据
- 修改现有项目需保持格式一致
