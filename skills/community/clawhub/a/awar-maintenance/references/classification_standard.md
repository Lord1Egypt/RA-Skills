# 分类标准与仓库结构

> 机器人世界模型的技术分类体系与边界定义

---

## 一、四类分类详解

### 1.1 Foundational WAMs - 基础世界动作模型

**定位**: 机器人领域的"基础大模型"，提供从感知到动作的端到端能力。

#### 什么是基础模型？

在 NLP 领域，BERT/GPT 被称为"语言基础模型"，因为它们预训练于大规模语料，可以微调到各种下游任务。

在机器人领域，"基础模型"需要：
1. **大规模预训练**: 在海量机器人数据上学习
2. **多任务泛化**: 能执行训练时未见的任务
3. **可微调性**: 易于适配特定机器人/场景

#### 核心特征

| 特征 | 说明 | 量化标准 |
|------|------|----------|
| 预训练数据规模 | 机器人轨迹/视频数量 | >100K 轨迹 |
| 任务泛化能力 | 零样本执行新任务 | >50% 成功率 |
| 视觉理解 | 开放词汇、场景理解 | 超越专用检测 |
| 动作输出 | 通用动作空间 | 支持多种机器人 |

#### 发展时间线

```
2021 ──── RT-1 (Google): 13个任务的视觉-动作模型
   │
2023 ──── RT-2 (Google): VLA概念提出，零样本泛化
   │
2024 ──── OpenVLA: 开源VLA，27B参数
   │
2024 ──── Pi0 (Physical Intelligence): 通用物理技能
   │
2024 ──── HomeRobot (Microsoft): 家庭场景基础模型
```

#### 代表性工作对比

| 项目 | 机构 | 参数 | 数据规模 | 开源 |
|------|------|------|----------|------|
| RT-2 | Google DeepMind | 55B | RT-1数据 | 否 |
| OpenVLA | 洛桑理工+NYU | 27B | Open X-Embodiment | 是 |
| Pi0 | Physical Intelligence | 7B | 私人数据 | 部分 |
| Unitree-X | 宇树科技 | 7B | 机器人数据 | 是 |

---

### 1.2 Predictive Dynamics - 预测动力学

**定位**: 专注于"环境动态建模"的系统，核心是学习"如果我这样做，环境会如何变化"。

#### 与基础模型的区别

```
基础模型问: "我应该做什么动作？"
预测模型问: "如果我做了这个动作，环境会变成什么样？"
```

#### 核心机制

**世界模型的核心方程**:
$$
s_{t+1} = f(s_t, a_t; \theta)
$$

其中 $s_t$ 是环境状态，$a_t$ 是动作，$f$ 是学习到的动态模型。

**预测型 vs 反应型**:

| 类型 | 代表 | 优势 | 劣势 |
|------|------|------|------|
| **反应型** (RT-2) | 直接策略 $a = \pi(s)$ | 快速、简单 | 缺乏长程规划 |
| **预测型** (Dreamer) | 动态模型 $s' = f(s,a)$ | 可规划、长程 | 需要求解器 |

#### 技术演进

```
2019 ──── PlaNet: 隐式世界模型，dreaming规划
   │
2020 ──── DreamerV2: RSSM + KL平衡 + 想象力rollout
   │
2021 ──── DreamerV3: 统一算法，RL+IL+跨域
   │
2023 ──── GAIA-1: 生成式世界模型，视频预测
   │
2024 ──── UniSim: 统一模拟器，视觉-语言-动作
```

#### 与强化学习的关系

Predictive Dynamics 是 Model-Based RL 的核心组件：

```
Model-Based RL Pipeline:
  收集数据 → 学习世界模型 → 规划/策略优化 → 执行
     ↑_______________↓ (dreaming/imagining)
```

---

### 1.3 Simulation & Real2Sim - 仿真与Sim2Real

**定位**: 解决"如何让机器人在仿真中学习，然后迁移到真实世界"。

#### 为什么需要仿真？

| 方面 | 真实机器人 | 仿真环境 |
|------|------------|----------|
| 数据采集速度 | 慢（物理限制） | 快（可并行） |
| 成本 | 高（硬件磨损） | 低（云计算） |
| 安全性 | 有风险 | 无风险 |
| 可控性 | 难复现 | 完全可控 |
| 泛化 | 受限 | 受限（Sim2Real gap） |

#### Sim2Real Gap 的来源

```
Sim2Real Gap = 感知差距 + 动力学差距 + 动作差距

感知差距:
  仿真渲染 ≠ 真实相机
  完美分割 ≠ 噪声检测

动力学差距:
  标称质量 ≠ 真实质量
  理想摩擦 ≠ 现实摩擦

动作差距:
  精确执行 ≠ 死区/延迟
```

#### 核心技术

**1. Domain Randomization (DR)**:
- 在仿真中随机化视觉/物理参数
- 训练一个"泛化"的策略

**2. System Identification (SysID)**:
- 精确测量真实机器人参数
- 使仿真尽可能接近真实

**3. Domain Adaptation**:
- 图像风格迁移（Sim→Real）
- 对抗自适应

#### 代表性工作

| 项目 | 核心方法 | 应用场景 |
|------|----------|----------|
| OmniH2O | 人类视频→机器人 | 通用操作 |
| RoboGen | 生成式仿真 | 多任务学习 |
| RTX | 物理引擎+DR | 灵巧操作 |
| ManiWHERE | 域适应 | 室内场景 |

---

### 1.4 Action Controllers - 动作控制器

**定位**: 专门优化"动作生成质量"的模块，强调高频、实时、精确。

#### 动作控制的层级

```
任务指令 (自然语言)
    ↓
高层规划 (Task Planning)
    ↓
动作生成 (Action Controller) ← 本类关注
    ↓
关节控制 (Joint Control)
    ↓
电机驱动 (Motor Driver)
```

#### 核心技术对比

| 方法 | 代表工作 | 动作频率 | 多模态 | 适用场景 |
|------|----------|----------|--------|----------|
| **ACT** | ACT (Stanford) | 10-50Hz | 否 | 精确操作 |
| **Diffusion Policy** | Cheng et al. | 5-20Hz | 是 | 复杂轨迹 |
| **Linear Policy** | BC-Zero | 100+Hz | 否 | 快速运动 |
| **GMP** | Grabber | 30Hz | 部分 | 抓取任务 |

#### Action Chunking vs Diffusion

**Action Chunking** (ACT 为代表):
```
观测 → [Transformer] → [a_t, a_{t+1}, ..., a_{t+7}]
         一次预测8步          顺序执行
```
- 优点: 低延迟、可并行解码
- 缺点: 确定性输出、难以处理多峰分布

**Diffusion Policy**:
```
观测 + 噪声 → [去噪网络] → 干净动作序列
                ↑
           条件: 观测嵌入
```
- 优点: 自然处理多峰分布
- 缺点: 推理延迟较高（需要迭代）

---

## 二、分类决策树

```
开始分析新项目

├── Q1: 是否是"端到端动作输出"？
│   ├── 是 (直接输出动作): 
│   │   ├── Q1.1: 是否基于预训练VLM？
│   │   │   ├── 是 → Foundational WAMs (RT-2类)
│   │   │   └── 否 → Q2
│   │   └── Q2: 是否强调泛化/通用性？
│   │       ├── 是 → Foundational WAMs
│   │       └── 否 → Action Controllers
│   └── 否 (输出环境预测):
│       └── Predictive Dynamics
│
├── Q3: 核心功能是否是"仿真/数据生成"？
│   ├── 是 → Simulation & Real2Sim
│   └── 否 → 根据实际能力归类
│
└── Q4: 是否专注"高频动作控制"优化？
    ├── 是 → Action Controllers
    └── 否 → 根据Q1-Q3综合判断
```

---

## 三、仓库目录结构

```
Awesome-World-Action-Robotics/
│
├── README.md                          # 主入口（概览 + 导航）
├── assets/                            # 静态资源
│   ├── getting_started.md             # 入门指南
│   ├── overview.png                   # 领域全景图 (Mermaid)
│   ├── benchmark_table.md             # 性能对比总表
│   └── style_guide.md                 # 文档样式指南
│
├── FOUNDATIONAL_WAMS.md               # 基础世界动作模型
│   ├── README.md                      # 类别概述 + 时间线
│   ├── google/                        # 按机构分类
│   │   ├── rt-1.md
│   │   └── rt-2.md
│   ├── open_source/                  # 开源项目
│   │   ├── openvla.md
│   │   └── homebot.md
│   └── industry/                      # 工业界
│       └── pi0.md
│
├── PREDICTIVE_DYNAMICS.md             # 预测动力学
│   ├── README.md
│   ├── dreamer_family.md              # Dreamer 系列
│   ├── video_prediction.md            # 视频预测派系
│   └── contrastive.md                 # 对比学习派系
│
├── SIMULATION_REAL2SIM.md             # 仿真与Sim2Real
│   ├── README.md
│   ├── domain_randomization.md
│   ├── system_identification.md
│   └── synthetic_data.md
│
└── ACTION_CONTROLLERS.md              # 动作控制器
    ├── README.md
    ├── act.md
    ├── diffusion_policy.md
    └── hybrid.md
```

---

## 四、分类边界与交叉项

### 4.1 边界模糊的案例

| 案例 | 模糊原因 | 推荐分类 |
|------|----------|----------|
| GAIA-1 | 既预测又生成动作 | Predictive Dynamics (主)+ Action Controllers (辅) |
| OpenVLA | 既泛化又需要微调 | Foundational WAMs |
| RoboGen | 仿真+生成+控制 | Simulation & Real2Sim |

### 4.2 多标签使用

对于跨类别的项目，可在文档头部标注主要类别，尾部补充交叉引用：

```markdown
### 项目X

**主要类别**: Predictive Dynamics  
**交叉类别**: Action Controllers  

> 项目X既可以作为世界模型进行规划，也可以作为动作控制器直接执行。
> 相关内容详见 [ACT 对比分析](../ACTION_CONTROLLERS.md#vs-act)

---

## 五、跨类别对比表

| 维度 | Foundational | Predictive | Simulation | Action |
|------|--------------|------------|------------|--------|
| **核心问题** | 泛化能力 | 环境建模 | Sim2Real | 执行精度 |
| **训练范式** | 模仿学习 | RL/IL | DR/SysID | IL |
| **规划能力** | 无/弱 | 强 | 依赖模型 | 无 |
| **推理速度** | 慢 | 中 | - | 快 |
| **硬件要求** | 高 | 中 | 中 | 低 |

---

## 六、维护规范

### 去重机制

```markdown
# 别名映射表

RT-2 = Robotic Transformer 2
OpenVLA = Vision-Language-Action Model
Pi0 = Physical Intelligence 0
ACT = Action Chunking with Transformers
DP = Diffusion Policy
```

### 更新触发条件

- 新论文发布 (arXiv)
- 新版本发布 (GitHub)
- 新基准测试结果
- 项目停更/归档

### 版本追踪

```markdown
### 项目X (v1.0) - 2024-01
### 项目X (v1.2) - 2024-03 ← 更新
```
