# 深度分析协议

> 对机器人世界模型进行系统性解构的标准框架

---

## 一、核心范式 (Paradigm)

### 1.1 范式类型总览

| 范式 | 代表工作 | 核心思想 | 适用场景 |
|------|----------|----------|----------|
| **RSSM** | DreamerV2/V3, PlaNet | 循环状态空间模型，在隐空间预测未来 | 高效规划、长程预测 |
| **JEPA** | I-JEPA, MC-JEPA | 联合嵌入预测架构，预测语义表征 | 视觉理解、迁移学习 |
| **Diffusion** | DDPM, SD, VideoGen | 扩散模型生成未来状态/动作 | 多模态轨迹生成 |
| **Transformer** | GAM, Genie, RT-2 | 大规模统一建模，端到端输出 | 泛化、多任务 |

### 1.2 RSSM (Recurrent State Space Model)

**核心架构**:

```
观测 o_t → 编码器 E → 隐表征 z_t
                  ↓
           隐状态 h_t = f(h_{t-1}, z_t, a_{t-1})
                  ↓
           预测 p(z_{t+1} | h_t) 或 p(r_t | h_t)
```

**关键组件**:
- **Encoder**: 将高维观测压缩为紧凑隐向量
- **RSSM**: 循环网络建模状态转移 $h_t = f(h_{t-1}, z_{t-1}, a_{t-1})$
- **Decoder**: 从隐表征重建观测或预测奖励

**数学形式**:
$$
p_\theta(\tau) = \prod_{t=0}^{T} p_\theta(o_t | s_t) \cdot p_\theta(s_t | s_{t-1}, a_{t-1})
$$

其中 $s_t$ 是隐状态，$a_t$ 是动作，$o_t$ 是观测。

**判断要点**:
- [ ] 是否使用变分推断（KL散度正则化）？
- [ ] 是否有独立的 world model 和 policy network？
- [ ] 是否支持 model-based RL？

### 1.3 JEPA (Joint Embedding Predictive Architecture)

**核心思想**: 不重建像素级细节，而是预测抽象语义表征。

**vs Pixel-level Reconstruction**:
```
Pixel-level:  观测 → 编码 → 解码重建像素 → 短视、计算重
JEPA:        观测 → 编码 ──────────────────→ 预测编码
                               ↑
                        [上下文条件]
```

**关键创新**:
- 对比损失 + 预测损失的组合
- 不需要生成细粒度像素（效率高）
- 学习到语义级的环境表征

**判断要点**:
- [ ] 是否在隐空间做预测而非像素空间？
- [ ] 是否有上下文编码器（如 ViT 的 patch embedding）？
- [ ] 训练目标是否包含对比学习组件？

### 1.4 Diffusion-based World Models

**核心机制**: 将世界模型建模为生成式扩散过程。

**前向过程** (添加噪声):
$$
q(z_t | z_0) = \mathcal{N}(z_t; \sqrt{\bar{\alpha}_t} z_0, (1-\bar{\alpha}_t)I)
$$

**反向过程** (去噪预测):
$$
p_\theta(z_{t-1} | z_t) = \mathcal{N}(z_{t-1}; \mu_\theta(z_t, t), \Sigma_\theta(z_t, t))
$$

**在机器人中的应用**:
- **Video Diffusion Models**: 生成未来视频帧
- **Diffusion Policy**: 在动作空间去噪生成动作序列
- **Dreamer + Diffusion**: 隐空间扩散预测

**判断要点**:
- [ ] 扩散过程是在像素空间还是隐空间？
- [ ] 是否处理多模态动作分布？
- [ ] 推理速度是否优化（DDIM、LCM 等）？

### 1.5 Transformer-based VLA

**核心范式**: 将视觉、语言、动作统一建模为 Token 序列。

**RT-2 架构示意**:
```
图像 Token → [VISION] → 
文本 Token → [LLM] → 动作 Token
                        ↓
                   自回归输出
```

**关键创新**:
- 动作离散化为 Token（类似 LLM 输出）
- 零样本泛化到训练未见过的任务
- 视觉-语言预训练的迁移

**判断要点**:
- [ ] 动作是否作为特殊 Token 输入/输出？
- [ ] 是否复用 VLM 预训练权重？
- [ ] 是否支持自然语言指令？

---

## 二、状态表征 (State Representation)

### 2.1 表征类型对比

| 类型 | 实现方式 | 优势 | 劣势 | 代表工作 |
|------|----------|------|------|----------|
| **Pixel-level** | 端到端 CNN/VAE | 保留细节信息 | 计算量大、维度高 | early RL |
| **Latent Space** | VAE/VQ-VAE | 紧凑高效 | 可能丢失细节 | Dreamer |
| **Point Cloud** | PointNet/3D Conv | 几何感知强 | 稀疏、缺纹理 | PointCloud RL |
| **Geometric** | SE(3) 特征 | 物理意义明确 | 泛化受限 | Rigid body |
| **Hybrid** | 多流融合 | 互补优势 | 融合复杂 | ROS-ACT |

### 2.2 本体感受数据通道

**标准通道**:

| 数据类型 | 维度 | 采样率 | 用途 |
|----------|------|--------|------|
| Joint Position | n×1 | 50-100Hz | 关节位置控制 |
| Joint Velocity | n×1 | 50-100Hz | 速度控制 |
| End-effector Pose | 7×1 (xyz + quat) | 50-100Hz | 末端控制 |
| End-effector Wrench | 6×1 | 100-200Hz | 力控 |
| Gripper State | 1×1 | 10-50Hz | 夹爪控制 |

**分析清单**:
- [ ] 是否包含 proprioception 数据？
- [ ] 是否包含视觉以外的感知（触觉、力矩）？
- [ ] 表征是否包含时间维度（序列 vs 单帧）？

---

## 三、动作集成 (Action Injection)

### 3.1 动作模式分类

```
动作集成方式
├── 动作分块 (Action Chunking)
│   ├── Transformer-based (ACT)
│   └── RNN-based (LSTM Policy)
├── 扩散策略 (Diffusion Policy)
│   ├── DDPM/DDIM
│   └── classifier-free guidance
├── 多模态 Token 化
│   ├── VLA (RT-2, OpenVLA)
│   └── Action Tokenizer
└── 模型预测控制 (MPC)
    ├── CEM (Cross-Entropy Method)
    └── iLQR / MPPI
```

### 3.2 Action Chunking

**核心思想**: 一次预测未来 N 步动作序列，而非单步决策。

```
当前观测 → [Transformer] → [a_t, a_{t+1}, ..., a_{t+N-1}]
                                      ↓
                               执行第一步 a_t
                               接收新观测
                                      ↓
                               重新预测
```

**优势**:
- 减少执行延迟（预测时并行）
- 动作时序一致性
- 减少观测频率要求

**参数**:
- Chunk Length: 通常 8-50 步
- Action Frequency: 1-50 Hz
- Temporal Ensemble: 平滑动作切换

### 3.3 Diffusion Policy

**核心思想**: 将策略建模为条件扩散过程。

**动作分布学习**:
$$
p_\theta(a_{0:T} | o_{0:T}) = \prod_{t=0}^{T} p(a_t | a_{t+1:T}, o_{0:T})
$$

**推理过程**:
```python
# 伪代码
noisy_action = sample_noise()
for t in reversed(range(T)):
    denoised = model(noisy_action, timestep, observation)
    noisy_action = denoise_step(denoised, t)
return noisy_action  # 干净动作
```

**优势**:
- 自然处理多模态动作分布
- 动作空间灵活（连续/离散/混合）
- 稳定的训练（对比GAN）

### 3.4 动作空间规范

| 空间类型 | 维度范围 | 表示方式 | 典型应用 |
|----------|----------|----------|----------|
| 关节空间 | 6-12 DOF | 角度/弧度 | 机械臂控制 |
| 末端空间 | 3-7 DOF | 位置/姿态 | 拾取放置 |
| 任务空间 | 2-4 DOF | 坐标/参数 | 操作任务 |
| 混合空间 | 7-20 DOF | 多类型混合 | 全程控制 |

---

## 四、物理一致性 (Physical Fidelity)

### 4.1 长程预测问题

| 问题类型 | 表现 | 根因 | 解决思路 |
|----------|------|------|----------|
| **物体消失** | 物体在预测序列中逐渐消失 | 重建损失不保序 | 对抗训练、perceptual loss |
| **违反引力** | 物体漂浮、异常加速 | 缺乏物理归纳偏置 | 物理先验、NSM |
| **穿透穿越** | 物体无碰撞穿透 | 检测缺失 | Collision-aware |
| **长期漂移** | 5步后姿态完全错误 | 误差累积 | Latent overshooting |
| **形变失控** | 刚体发生形变 | 约束缺失 | 物理约束注入 |

### 4.2 物理先验注入方法

```
方法 1: 物理仿真集成
├── 将 World Model 预测作为仿真初态
├── 使用物理引擎验证/修正预测
└── 如：GaussSim, Physiokinetics

方法 2: 归纳偏置设计
├── 能量函数约束 (Hamiltonian Neural Networks)
├── 不变性约束 (SE(3) equivariance)
└── 因果结构约束

方法 3: 数据工程
├── 高质量多样化数据
├── Domain Randomization
└── 课程学习 (从简单到复杂)
```

### 4.3 闭环控制能力评估

| 评估类型 | 测试方式 | 关键指标 |
|----------|----------|----------|
| **开环预测** | 离线数据集 MSE/SSIM | 预测误差 |
| **短期闭环** | 10步内任务成功率 | Success Rate |
| **长期闭环** | 50+ 步连续执行 | 轨迹保真度 |
| **Sim2Real** | 仿真→真实迁移 | 成功率下降率 |

### 4.4 Sim2Real Gap 分析框架

```
Sim2Real Gap = Perception Gap + Dynamics Gap + Action Gap

Perception Gap:     视觉差异（纹理、光照、噪声）
Dynamics Gap:       物理参数差异（质量、摩擦、延迟）
Action Gap:         执行器差异（死区、饱和、噪声）

评估清单:
- [ ] Domain Randomization 覆盖范围
- [ ] 物理参数标定工具
- [ ] 系统辨识方法
- [ ] 零样本迁移实验
```

---

## 五、分析输出规范

### 5.1 标准输出格式

```markdown
### [项目名]

**核心范式**: [RSSM / JEPA / Diffusion / Transformer-VLA]
**状态表征**: [Pixel / Latent / Hybrid] + [含/不含] [Proprioception/Force/Touch]
**动作模式**: [Action Chunking / Diffusion / Tokenization] @ [频率]

### 范式详解
[该范式的核心机制、创新点、与同类方法的差异]

### 表征分析
[状态表征的选择理由、效率与信息完整性的权衡]

### 动作机制
[动作是如何生成的、与其他组件的交互方式]

### 物理一致性
[是否解决长程漂移、Sim2Real能力评估]

### Benchmark
| 任务 | 指标 | 结果 |
|------|------|------|
```

### 5.2 关键判断 Checklist

```markdown
## 深度分析 Checklist

### 范式判断
- [ ] 模型的核心预测目标是什么？（像素/隐向量/动作/奖励）
- [ ] 训练目标函数包含哪些组件？（重建/对比/扩散/联合）
- [ ] 是否支持 model-based planning？

### 表征判断
- [ ] 观测编码器是什么？（CNN/ViT/MLP）
- [ ] 隐空间维度是多少？（紧凑 vs 高维）
- [ ] 是否包含时间序列建模？（RNN/Transformer/无）

### 动作判断
- [ ] 动作是连续还是离散的？
- [ ] 动作频率与观测频率的关系？
- [ ] 是否支持 action chunking？

### 物理判断
- [ ] 是否有物理先验注入？
- [ ] 长期预测稳定性如何？
- [ ] 是否有闭环实验结果？
```
