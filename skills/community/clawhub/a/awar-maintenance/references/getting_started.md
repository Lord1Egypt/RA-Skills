# 入门指南

> 机器人世界模型与动作模型 (World-Action Model) 领域快速入门

---

## 一、领域概述

### 1.1 什么是 World Model？

**World Model (世界模型)** 是智能体对外部环境的内部表征与预测系统。类比人类认知：

> 当你计划伸手拿水杯时，你的大脑会隐式地预测：杯子位置、移动路径、水会如何流出、重力如何影响等。这种预测能力就是"世界模型"。

**在机器人中的定义**:
$$
\hat{s}_{t+1} = f(s_t, a_t; \theta)
$$

其中 $s_t$ 是环境状态，$a_t$ 是动作，$f$ 是学习到的世界模型。

### 1.2 World Model vs Action Model

| 组件 | 核心问题 | 输出 | 代表方法 |
|------|----------|------|----------|
| **World Model** | "环境会如何变化？" | 未来状态预测 | Dreamer, GAIA-1 |
| **Action Model/Policy** | "我应该做什么？" | 动作序列 | ACT, Diffusion Policy |
| **VLA** | "理解+预测+执行" | 动作 | RT-2, OpenVLA |

### 1.3 为什么现在火起来？

**三大驱动力**:

1. **LLM 的成功**: GPT/ViT 的预训练-微调范式启发机器人领域
2. **数据规模**: Open X-Embodiment 等大数据集出现
3. **算力提升**: GPU/TPU 足够训练百亿参数模型

**里程碑时间线**:

```
2021 ─── RT-1: 视觉-动作多任务学习
   │
2022 ─── DreamerV3: 通用世界模型，统一RL+IL
   │
2023 ─── RT-2: VLA概念，零样本泛化
   │
2024 ─── OpenVLA: 开源VLA
   │
2024 ─── Pi0: Physical Intelligence 基础模型
```

---

## 二、核心概念图谱

```
                          ┌─────────────────────────────────────┐
                          │       Robot World-Action Model      │
                          └─────────────────────────────────────┘
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
          ▼                               ▼                               ▼
   ┌─────────────┐                ┌─────────────┐                ┌─────────────┐
   │   World     │                │   VLA /     │                │   Action    │
   │   Model     │                │   Foundational│              │   Controller│
   └─────────────┘                └─────────────┘                └─────────────┘
          │                               │                               │
          ▼                               ▼                               ▼
  环境动态预测                      理解+泛化                        高频执行
  长程规划能力                      零样本迁移                      精确控制
```

---

## 三、技术流派

### 3.1 Model-Based RL 派 (World Model)

**核心思想**: 先学习环境模型，再进行规划

```
数据收集 → 学习 World Model → 想象力 Rollout → 策略优化
              ↓
        Dreamer / PlaNet / RSSM
```

**优势**: 数据效率高、可解释性强
**挑战**: 累计误差、长程预测不稳定

### 3.2 End-to-End 派 (VLA)

**核心思想**: 端到端学习感知-动作映射

```
感知 → 理解 → 动作 (单网络)
  ↑__________________↓ (闭环)
```

**优势**: 表达能力强、自动特征学习
**挑战**: 需要大量数据、解释性差

### 3.3 Diffusion 派 (Action)

**核心思想**: 用扩散模型建模多模态动作分布

```
观测 + 噪声 → 去噪网络 → 干净动作
                ↑
         条件: 视觉/语言
```

**优势**: 自然处理多峰分布、训练稳定
**挑战**: 推理延迟较高

---

## 四、关键论文清单

### 4.1 必读经典

| 论文 | 年份 | 引用 | 推荐理由 |
|------|------|------|----------|
| **RT-2** | 2023 | 2000+ | VLA 开山之作 |
| **DreamerV3** | 2023 | 800+ | 统一世界模型 |
| **ACT** | 2023 | 500+ | Action Chunking |
| **Diffusion Policy** | 2023 | 400+ | 扩散动作生成 |

### 4.2 按流派推荐

**World Model 流**:
1. Dreamer 系列 (Vriend et al., 2023)
2. PlaNet (Hafner et al., 2019)
3. MuZero (Schrittwieser et al., 2020)

**VLA 流**:
1. RT-2 (Brohan et al., 2023)
2. OpenVLA (Zhao et al., 2024)
3. Pi0 (Physical Intelligence, 2024)

**Diffusion 流**:
1. Diffusion Policy (Chi et al., 2023)
2. 3D Diffusion Policy (Ze et al., 2024)
3. UniDiffuser (Bao et al., 2023)

---

## 五、学习路径

### 5.1 入门路径 (3个月)

```
Month 1: 基础
├── 学习 Python + PyTorch
├── 阅读 RL 基础 (Sutton & Barto)
├── 运行一个简单Policy (PPO/SAC)
│
Month 2: World Model
├── 学习 VAE / RNN 基础
├── 阅读 Dreamer 论文
├── 运行 DreamerPytorch 实现
│
Month 3: 前沿
├── RT-2 / OpenVLA 论文精读
├── Diffusion Policy 实践
└── 尝试微调开源模型
```

### 5.2 进阶路径 (6个月)

```
Month 4-5: 深度
├── 深入 RSSM / JEPA 理论
├── 学习 Transformer 架构
├── 复现一个完整项目
│
Month 6: 前沿
├── 追踪最新 arXiv (cs.RO)
├── 关注顶会 (CoRL, RSS, ICRA)
└── 开始贡献 AWAR 仓库
```

---

## 六、实战资源

### 6.1 开源项目

| 项目 | 语言 | 难度 | 推荐度 |
|------|------|------|--------|
| [LeRobot](https://github.com/huggingface/lerobot) | Python | 低 | ⭐⭐⭐⭐⭐ |
| [DMC-GPT](https://github.com/jdenysg/dmc-gpt) | Python | 中 | ⭐⭐⭐⭐ |
| [DiffusionPolicy](https://github.com/columbia-robovision/DiffusionPolicy) | Python | 中 | ⭐⭐⭐⭐ |
| [OpenVLA](https://github.com/openvla/openvla) | Python | 高 | ⭐⭐⭐⭐⭐ |

### 6.2 数据集

| 数据集 | 规模 | 类型 | 用途 |
|--------|------|------|------|
| Open X-Embodiment | 100K+ | 多机器人 | VLA预训练 |
| LIBERO | 460K | 仿真 | 任务规划 |
| CALVIN | 24K | 仿真 | 长程操作 |
| RT-1 | 130K | 真机 | 模仿学习 |

### 6.3 硬件推荐

**入门级**:
- WidowX / LEAP Arm ($500-2000)
- Aloha ($20K，含双手机器人)

**研究级**:
- UR5 / UR10 ($30-50K)
- Franka Panda ($60K)
- Spot + Arm ($100K)

**高性能**:
- Unitree B2 (国产，性能强)
- 宇树 H1 人形 ($100K)

---

## 七、常见问题

### Q1: World Model 和 World Model 在 LLM 领域是一个东西吗？

**不是**。LLM 的 "World Model" 通常指"语言模型对物理世界的知识表征"。本文档的 World Model 特指**机器人领域的动态环境模型**。

### Q2: VLA 和 LLM 有什么关系？

VLA (Vision-Language-Action) 借鉴了 LLM 的成功范式：
- 使用 VLM 预训练权重 (如 CLIP/ViT)
- 复用 LLM 的推理能力
- 但输出是动作而非文本 Token

### Q3: 为什么动作要用 Token 表示？

RT-2 证明：将连续动作离散化为 Token 后，可以利用 LLM 的预训练知识，实现零样本泛化。这是一种"语言-动作对齐"的思想。

### Q4: Sim2Real Gap 是什么？

指仿真环境与真实环境的差异导致的策略迁移失败。常见原因：
- 视觉差异 (渲染 vs 真实相机)
- 物理差异 (理想 vs 真实摩擦/质量)
- 控制差异 (精确 vs 有延迟的执行)

### Q5: Action Chunking vs Diffusion Policy 哪个更好？

**取决于任务**:
- **简单任务、高频控制**: Action Chunking (低延迟)
- **复杂任务、多峰分布**: Diffusion Policy (表达强)

---

## 八、社区与资源

### 8.1 顶会与期刊

- **CoRL** (Conference on Robot Learning) - 领域顶会
- **RSS** (Robotics: Science and Systems) - 理论偏重
- **ICRA/IROS** - 机器人综合会议
- **NeurIPS/ICML/ICLR** - 机器学习顶会

### 8.2 优质博客

- [Google Robotics Blog](https://blog.research.google.com/technology/robotics/)
- [Physical Intelligence Blog](https://www.physicalintelligence.company/)
- [NYU Flightmare](https://nyu-flightmare.github.io/)
- [Stanford HAI](https://hai.stanford.edu/)

### 8.3 开发者社区

- [LeRobot Discord](https://discord.gg/huggingface)
- [Robot Learning Slack](https://robot-learning-slack.gmist.xyz/)
- [r/robotics](https://reddit.com/r/robotics)
