> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# Module G · AI 最新发展（V5 新增）

> 本模块追踪 AI 领域的前沿进展，包括大模型能力跃升、新兴应用场景、AI Agent 发展以及未来趋势展望。

## 模块概览

| 单元 | 名称 | 时长 | 难度 |
|------|------|------|------|
| G1 | 大模型能力跃升 | 4h | ⭐⭐⭐ |
| G2 | AI Agent 与自主系统 | 4h | ⭐⭐⭐⭐ |
| G3 | AI 前沿应用与趋势 | 3h | ⭐⭐⭐ |

## G1 · 大模型能力跃升

### G1.1 模型架构演进

**从 Transformer 到前沿架构**

```
时间线：
2020: GPT-3 (175B 参数) - 涌现能力初现
2022: ChatGPT - 对话式 AI 突破
2023: GPT-4 - 多模态与复杂推理
2024: Claude 3 / Gemini - 长上下文与安全
2025: GPT-4o / Gemini Ultra - 原生多模态
2026: 下一代模型 - 更强推理、更低成本
```

**关键技术突破**

| 技术 | 突破 | 影响 |
|------|------|------|
| Scaling Law | 参数/数据/算力协同扩展 | 能力持续提升 |
| RLHF | 人类反馈强化学习 | 输出质量对齐 |
| MoE | 稀疏专家混合 | 成本效益优化 |
| 上下文窗口 | 100K+ tokens | 长文档理解 |
| 多模态 | 文本/图像/音频统一 | 真实世界感知 |
| 工具调用 | 外部 API 集成 | 能力边界扩展 |

### G1.2 涌现能力（Emergent Abilities）

**定义**
当模型规模超过某个临界点时，突然出现的新能力称为"涌现能力"。

**典型涌现能力**

```python
涌现能力案例 = {
    "思维链推理": {
        "临界点": "~100B 参数",
        "表现": "能够进行多步推理",
        "应用": "数学题、逻辑题"
    },
    "上下文学习": {
        "临界点": "~10B 参数",
        "表现": "无需微调即可学习新任务",
        "应用": "Few-shot prompting"
    },
    "代码生成": {
        "临界点": "~60B 参数",
        "表现": "生成复杂代码",
        "应用": "Copilot、代码补全"
    },
    "多语言翻译": {
        "临界点": "~50B 参数",
        "表现": "低资源语言翻译",
        "应用": "跨语言沟通"
    }
}
```

### G1.3 多模态融合

**多模态能力图谱**

```
文本 ←→ 图像 ←→ 音频 ←→ 视频 ←→ 3D

能力矩阵：
| 能力 | GPT-4V | Claude 3 | Gemini |
|------|--------|----------|--------|
| 图像理解 | ✅ | ✅ | ✅ |
| 图像生成 | ❌ | ❌ | ✅ |
| 视频理解 | ✅ | ✅ | ✅ |
| 音频处理 | ❌ | ❌ | ✅ |
| 3D 感知 | 有限 | 有限 | ✅ |
```

**应用场景**
- 文档理解（图表、截图、PDF）
- 视频分析（安防、教育、医疗）
- 语音助手（实时翻译、对话）
- 具身智能（机器人控制）

### G1.4 前沿案例与学术引用

#### 案例一：AlphaFold 3 — 蛋白质结构预测突破

- **案例名称**：AlphaFold 3 蛋白质与分子结构预测
- **时间**：2024 年
- **简述**：2024 年 5 月，Google DeepMind 在 *Nature* 上发表了 AlphaFold 3 的研究论文。相比前代模型仅能预测蛋白质单体结构，AlphaFold 3 实现了对蛋白质与 DNA、RNA、小分子配体（ligand）等所有生命分子复合物的结构预测，精度大幅超越此前的专用工具。AlphaFold 3 引入了基于扩散模型（diffusion model）的架构，能够直接预测原子级坐标，为药物设计、基因工程和疾病机理研究提供了革命性的工具。DeepMind 同步推出了 AlphaFold Server，向全球科研社区提供免费预测服务。
- **教学讨论要点**：
  1. AlphaFold 从 v1 到 v3 的演进展示了 AI 能力如何从"解决单一问题"扩展到"解决一类问题"。这种能力跃升的关键技术突破是什么？
  2. AlphaFold 对传统实验结构生物学（X 射线晶体学、冷冻电镜）构成了怎样的挑战？两者是替代关系还是互补关系？
- **参考来源**：Abramson, J., et al. (2024). "Accurate structure prediction of biomolecular interactions with AlphaFold 3." *Nature*, 630, 493-500. https://doi.org/10.1038/s41586-024-07487-w

#### 案例二：GPT-4 技术报告

- **案例名称**：GPT-4 多模态大模型技术报告
- **时间**：2023 年
- **简述**：2023 年 3 月，OpenAI 发布了 GPT-4 技术报告。GPT-4 是一个大规模多模态模型，能够接受图像和文本输入并生成文本输出。在多项专业考试和学术基准测试中，GPT-4 展现了显著提升：在律师资格考试（Bar Exam）中排名前 10%（GPT-3.5 仅为后 10%）；SAT 数学得分 700/800；GRE 写作获得 4/6 分；在 MMLU（大规模多任务语言理解）基准上达到 86.4% 的准确率（GPT-3.5 为 70.0%）。GPT-4 还展现了更强的"事实性"和"可控性"，在对抗性提示测试中比 GPT-3.5 更安全。
- **教学讨论要点**：
  1. GPT-4 在律师资格考试中排名前 10%，这是否意味着 AI 已经具备"专家级"能力？"通过考试"与"胜任工作"之间还有什么差距？
  2. GPT-4 技术报告没有公开模型参数量和训练数据细节。大模型研究的"透明度"问题对 AI 安全和科学发展有何影响？
- **参考来源**：OpenAI. (2023). "GPT-4 Technical Report." *arXiv preprint arXiv:2303.08774*.

#### 重要学术引用

**Scaling Laws（缩放定律）**

Kaplan et al. (2020) 发表了具有里程碑意义的缩放定律研究，揭示了神经网络语言模型的性能（以交叉熵损失衡量）与模型参数量 N、训练数据量 D、计算量 C 之间存在幂律关系。核心发现包括：
- 模型性能与上述三个因素均呈幂律下降关系
- 在计算受限场景下，最优策略是同时扩大模型和数据
- 存在"不可压缩"的交叉熵损失下限
- 大模型在小任务上的"浪费"实际上是对未来大任务的预训练

这一发现直接指导了 GPT-3、PaLM、LLaMA 等大模型的研发策略，成为大模型时代的理论基石。

- **参考来源**：Kaplan, J., McCandlish, S., Henighan, T., et al. (2020). "Scaling Laws for Neural Language Models." *arXiv preprint arXiv:2001.08361*.

**Emergent Abilities（涌现能力）**

Wei et al. (2022) 系统研究了大语言模型中的"涌现能力"现象——某些能力在小模型中不存在或表现极差，但在模型规模超过某个临界点后突然出现。研究识别了多项涌现能力，包括：
- 思维链推理（Chain-of-Thought）：在约 100B 参数模型中涌现
- 多步算术推理：在模型规模增大后突然出现
- 任务指令跟随：大模型能理解并执行未见过的任务指令

论文指出，涌现能力的存在意味着"扩大模型规模"不仅仅是量变，而是能带来质变——这对 AI 研发策略和 AI 安全研究都具有深远影响。

- **参考来源**：Wei, J., Tay, Y., Bommasani, R., et al. (2022). "Emergent Abilities of Large Language Models." *Transactions on Machine Learning Research (TMLR)*. arXiv:2206.07682.

---

## G2 · AI Agent 与自主系统

### G2.1 Agent 架构

**Agent 核心组件**

```python
class AIAgent:
    def __init__(self):
        self.planner = PlanningModule()      # 任务规划
        self.memory = MemoryModule()         # 记忆存储
        self.tools = ToolRegistry()           # 工具调用
        self.executor = ExecutionModule()     # 动作执行
        self.reflector = ReflectionModule()   # 自我反思
    
    def run(self, goal):
        # 1. 理解目标
        task = self.planner.parse(goal)
        
        # 2. 制定计划
        plan = self.planner.create_plan(task)
        
        # 3. 执行循环
        for step in plan:
            # 执行动作
            result = self.executor.run(step, self.tools)
            
            # 反思结果
            reflection = self.reflector.analyze(result)
            
            # 更新记忆
            self.memory.add(step, result, reflection)
            
            # 必要时调整计划
            if not reflection.success:
                plan = self.planner.adjust(plan, reflection)
        
        return self.memory.summarize()
```

### G2.2 工具调用系统

**常用工具类型**

| 工具类型 | 示例 | 功能 |
|----------|------|------|
| 搜索 | Web Search, Browser | 获取实时信息 |
| 代码执行 | Python, Bash | 运行计算/代码 |
| 文件操作 | Read, Write, Edit | 文件系统交互 |
| API 调用 | HTTP Request | 外部服务集成 |
| 数据库 | SQL, Vector DB | 数据存储检索 |
| 知识库 | RAG | 私有知识问答 |

**工具调用流程**

```
User: 帮我分析 AAPL 股票走势

1. 规划阶段
   - 识别需要工具：股票数据 API
   - 确定调用顺序：先获取数据，再分析

2. 执行阶段
   Tool: stock_api.get_price_history("AAPL", "1y")
   ↓
   Result: [K线数据]

3. 分析阶段
   Tool: python.analyze(data, indicators=["MA", "RSI"])
   ↓
   Result: 技术分析结果

4. 响应阶段
   - 整合结果，生成投资建议
   - 包含数据来源和风险提示
```

### G2.3 多 Agent 系统

**协作模式**

```
┌─────────────────────────────────────────────┐
│           Multi-Agent Orchestrator           │
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Planner │  │  Coder  │  │Reviewer │    │
│  │  Agent  │◄─►│  Agent  │◄─►│  Agent  │    │
│  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │          │
│       └────────────┴────────────┘          │
│                    │                        │
│                    ▼                        │
│            ┌─────────────┐                  │
│            │   Memory    │                  │
│            └─────────────┘                  │
└─────────────────────────────────────────────┘
```

**Agent 协作场景**

| 场景 | Agent 组合 | 协作方式 |
|------|------------|----------|
| 软件开发 | Planner + Coder + Tester | 规划→实现→测试→迭代 |
| 投资分析 | Researcher + Analyst + Risk | 调研→分析→风险评估 |
| 内容创作 | Ideator + Writer + Editor | 创意→写作→审核 |
| 客服支持 | Router + Resolver + Escalator | 分类→解决→升级 |

### G2.4 自主性与安全边界

**自主等级**

| 等级 | 名称 | 描述 | 适用场景 |
|------|------|------|----------|
| L1 | 辅助 | 完全人工控制，AI 提供建议 | 高风险决策 |
| L2 | 半自动 | 人工批准后执行 | 常规任务 |
| L3 | 条件自动 | 特定场景自主，定期人工审查 | 标准流程 |
| L4 | 高度自动 | 大部分场景自主，异常时人工介入 | 低风险场景 |
| L5 | 完全自动 | 全场景自主，无人工干预 | 实验性场景 |

**安全护栏设计**

```python
class SafetyGuardrails:
    def __init__(self):
        self.allowed_actions = []
        self.denied_actions = []
        self.confirmation_required = []
        self.max_iterations = 10
    
    def check(self, action):
        # 1. 白名单检查
        if action in self.denied_actions:
            return ActionResult.DENIED
        
        # 2. 敏感操作确认
        if action in self.confirmation_required:
            return ActionResult.CONFIRM
        
        # 3. 频率限制
        if self.is_rate_limited(action):
            return ActionResult.RATE_LIMITED
        
        # 4. 迭代次数限制
        if self.iterations > self.max_iterations:
            return ActionResult.MAX_ITERATIONS
        
        return ActionResult.ALLOWED
    
    def get_permission(self, action, context):
        """获取人工批准"""
        # 暂停执行，发送审批请求
        return pending_approval(action, context)
```

### G2.5 前沿案例与学术引用

#### 案例一：Devin — 首个 AI 软件工程师

- **案例名称**：Devin（Cognition AI）— 首个 AI 软件工程师
- **时间**：2024 年 3 月
- **简述**：2024 年 3 月，美国 AI 初创公司 Cognition AI 发布了 Devin，号称"全球首个 AI 软件工程师"。Devin 能够自主完成软件工程的全流程任务：理解需求、制定计划、编写代码、调试错误、部署应用。在 SWE-bench（软件工程基准测试）上，Devin 解决了 13.86% 的真实 GitHub issue，远超此前最佳方法（1.96%）。Devin 展示了 AI Agent 从"辅助工具"向"自主执行者"的重大跨越，引发了关于 AI 对软件工程师职业影响的广泛讨论。
- **教学讨论要点**：
  1. Devin 在 SWE-bench 上的表现虽然远超此前方法，但仅解决了约 14% 的 issue。这是否足以替代人类工程师？"解决 issue"与"交付生产级软件"之间还有什么差距？
  2. 如果 AI Agent 能自主完成大部分编码工作，软件工程师的核心竞争力将转向什么能力？
- **参考来源**：Cognition AI. (2024). "Introducing Devin, the first AI software engineer." https://www.cognition.ai/blog/introducing-devin. 以及 Jimenez, C. E., et al. (2024). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" *ICLR 2024*.

#### 案例二：AutoGPT — 开源自主 Agent 先驱

- **案例名称**：AutoGPT — 开源自主 AI Agent
- **时间**：2023 年 3 月
- **简述**：2023 年 3 月，开发者 Significant Gravitas（Toran Bruce Richards）发布了 AutoGPT，这是最早引起广泛关注的开源自主 AI Agent 项目之一。AutoGPT 基于 GPT-4 驱动，能够自主设定子目标、执行任务、调用工具（网络搜索、代码执行、文件操作等），并根据执行结果自我调整策略。项目在发布后迅速获得超过 16 万 GitHub Star，成为 AI Agent 领域最具影响力的开源项目。AutoGPT 展示了 LLM 驱动 Agent 的巨大潜力，同时也暴露了自主 Agent 在可靠性、任务完成率和成本控制方面的挑战。
- **教学讨论要点**：
  1. AutoGPT 在简单任务上表现出色，但在复杂多步任务中容易出现"循环"或"偏离目标"的问题。这反映了当前 Agent 架构的什么根本性局限？
  2. 开源 Agent 的快速发展是否也意味着更大的安全风险？如何设计"安全护栏"来防止自主 Agent执行有害操作？
- **参考来源**：Significant Gravitas. (2023). "AutoGPT." GitHub: https://github.com/Significant-Gravitas/AutoGPT. 以及 Qin, Y., et al. (2023). "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models." *Science*, 384(6702).

#### 案例三：Microsoft AutoGen — 多 Agent 对话框架

- **案例名称**：Microsoft AutoGen — 多智能体对话框架
- **时间**：2023 年
- **简述**：2023 年，微软研究院发布了 AutoGen，一个支持多个 AI Agent 之间进行对话式协作的开源框架。AutoGen 的核心创新在于将 Agent 交互建模为"对话"——多个 Agent（可以是 LLM 驱动的、代码执行的、或人类参与的）通过结构化的对话来协作完成复杂任务。框架支持灵活的 Agent 角色定义、自定义对话模式（如两人对话、群聊、嵌套对话）、以及人机混合协作。AutoGen 在代码生成、数据分析和决策支持等场景中展现了显著优势，代表了多 Agent 系统从"预定义流程"向"动态对话协作"的范式转变。
- **教学讨论要点**：
  1. AutoGen 将 Agent 协作建模为"对话"而非"预定义工作流"。这种设计有什么优势？在什么场景下"动态对话"比"固定流程"更有效？
  2. 在多 Agent 系统中，如何确保 Agent 之间的信息传递是准确和一致的？"幻觉"问题在多 Agent 协作中会被放大还是缓解？
- **参考来源**：Wu, Q., Bansal, G., Zhang, J., et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." *arXiv preprint arXiv:2308.08155*. 发表于 *AAAI 2024 Workshop*.

#### 重要学术引用

**LLM-based Autonomous Agents 综述**

Wang et al. (2023) 发表了关于大语言模型驱动的自主 Agent 的系统性综述，提出了一个统一的 Agent 架构框架，包含三大核心模块：
- **大脑（Brain）**：基于 LLM 的知识存储、推理与决策能力
- **感知（Perception）**：多模态输入处理与环境状态理解
- **行动（Action）**：工具调用、代码执行与环境交互

综述还梳理了 Agent 的关键应用（软件开发、社会模拟、科学研究等）和开放挑战（可靠性、安全性、评估标准），是理解 LLM Agent 领域的权威参考文献。

- **参考来源**：Wang, L., Ma, C., Feng, X., et al. (2023). "A Survey on Large Language Model based Autonomous Agents." *arXiv preprint arXiv:2308.11432*. 发表于 *Frontiers of Computer Science*, 2024.

---

## G3 · AI 前沿应用与趋势

### G3.1 垂直领域应用

**医疗健康**

| 应用 | 现状 | 趋势 |
|------|------|------|
| 医学影像 | FDA 已批准多款 AI 产品 | 更精确的诊断辅助 |
| 药物发现 | AlphaFold 推动研发加速 | 从头设计新分子 |
| 临床笔记 | AI 辅助病历书写 | 多模态病历理解 |
| 个性化治疗 | 基因组分析 | 精准医疗 |

**教育**

| 应用 | 现状 | 趋势 |
|------|------|------|
| 智能辅导 | 自适应学习系统 | 生成式练习题 |
| 自动批改 | 客观题自动评分 | 主观题 AI 批改 |
| 课程推荐 | 基于表现的推荐 | 全面学习分析 |
| 虚拟教师 | FAQ 问答 | 1对1 深度辅导 |

**科学研究**

| 领域 | AI 应用 | 突破 |
|------|---------|------|
| 材料科学 | 结构预测 | 新材料发现 |
| 气候建模 | 降尺度预测 | 精细天气预报 |
| 天体物理 | 图像分类 | 新天体识别 |
| 生物信息 | 序列分析 | 蛋白质设计 |

### G3.2 具身智能

**定义**
具身智能（Embodied AI）是指具有物理形态的 AI 系统，能够与环境交互、感知、推理并执行动作。

**技术栈**

```
具身智能
├── 感知层
│   ├── 视觉 (RGB-D)
│   ├── 触觉
│   ├── 听觉
│   └── 本体感觉
├── 理解层
│   ├── 场景理解
│   ├── 物体识别
│   ├── 空间推理
│   └── 意图理解
├── 规划层
│   ├── 运动规划
│   ├── 任务分解
│   └── 导航避障
└── 执行层
    ├── 机械控制
    ├── 力控
    └── 安全交互
```

**应用场景**
- 家庭服务机器人
- 工业自动化
- 医疗手术辅助
- 探索与救援

### G3.3 未来趋势展望

**短期（1-3年）**

| 趋势 | 描述 |
|------|------|
| 多模态原生 | 模型原生支持多模态，而非拼接 |
| Agent 普及 | AI Agent 广泛进入日常工作流 |
| 端侧 AI | 强 AI 能力在手机/PC 本地运行 |
| 专业微调 | 各行业垂直领域专业模型 |

**中期（3-5年）**

| 趋势 | 描述 |
|------|------|
| 通用机器人 | 通用人形机器人初步应用 |
| AI 原生应用 | 全新应用形态，而非 AI+传统软件 |
| 科学加速 | AI for Science 重大突破 |
| AI 监管 | 全球 AI 治理框架完善 |

**长期（5-10年）**

| 趋势 | 描述 |
|------|------|
| 人工通用智能 | AGI 曙光初现 |
| AI 赋能科研 | 科学发现速度大幅提升 |
| 人机融合 | 脑机接口等增强人类能力 |
| AI 社会 | AI 深度融入社会各层面 |

### G3.4 应对策略

**个人层面**
```markdown
## AI 时代个人发展策略

### 即刻行动
- [ ] 掌握 AI 工具使用（Prompt、工程）
- [ ] 培养 AI 难以替代的能力（创造力、情商）
- [ ] 建立人机协作工作流

### 中期规划
- [ ] 技能组合升级（领域知识 + AI 能力）
- [ ] 建立个人 AI 助手工作流
- [ ] 参与 AI 社区，保持信息同步

### 长期视野
- [ ] 关注 AI 伦理与社会影响
- [ ] 培养跨学科思维
- [ ] 准备持续学习的终身学习模式
```

### G3.5 前沿案例与学术引用

#### 案例一：AlphaFold 对药物发现的影响

- **案例名称**：AlphaFold 加速药物发现与蛋白质工程
- **时间**：2020 年至今
- **简述**：AlphaFold 系列模型对药物发现产生了深远影响。AlphaFold 2 在 2020 年 CASP14 竞赛中达到实验级精度的蛋白质结构预测，将原本需要数月甚至数年的结构解析过程缩短到数小时。具体影响包括：Isomorphic Labs（DeepMind 子公司）已与辉瑞（Pfizer）、诺华（Novartis）等制药巨头达成合作，利用 AlphaFold 技术加速小分子药物设计；DeepMind 与欧洲分子生物学实验室（EMBL）合作发布了 AlphaFold Protein Structure Database，预测了超过 2 亿个蛋白质结构，覆盖几乎所有已知蛋白质；在抗生素研发领域，AlphaFold 帮助研究人员理解细菌耐药性相关蛋白的结构，加速新型抗菌药物的发现。
- **教学讨论要点**：
  1. AlphaFold 将蛋白质结构预测从"实验科学问题"转变为"计算工程问题"。这对药物研发的流程、成本和周期意味着什么？
  2. 当 AI 能预测几乎所有已知蛋白质的结构时，结构生物学家的角色将如何转变？"AI + 人类专家"的协作模式是什么样的？
- **参考来源**：Jumper, J., et al. (2021). "Highly accurate protein structure prediction with AlphaFold." *Nature*, 596, 583-589. 以及 Varadi, M., et al. (2022). "AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models." *Nucleic Acids Research*, 50(D1), D439-D444.

#### 案例二：GraphCast — AI 天气预报系统

- **案例名称**：GraphCast — Google DeepMind AI 天气预测
- **时间**：2023 年
- **简述**：2023 年 11 月，Google DeepMind 在 *Science* 上发表了 GraphCast 模型，这是一个基于图神经网络（Graph Neural Network）的全球中期天气预报 AI 系统。GraphCast 仅用不到一分钟即可生成未来 10 天的全球天气预报，在 1380 个预测目标中的 90.3% 上优于欧洲中期天气预报中心（ECMWF）的传统数值天气预报系统（HRES），同时计算速度提升了约 10 万倍。GraphCast 在极端天气事件（如飓风路径预测）中也展现了出色的预测能力，为灾害预警和应急响应提供了更快速、更精确的工具。
- **教学讨论要点**：
  1. GraphCast 的计算速度比传统数值天气预报快 10 万倍，这对气象服务的实际应用（如飓风预警、农业决策）有什么实际意义？
  2. AI 天气预报模型依赖历史气象数据训练。在气候变化导致极端天气模式发生根本性变化的背景下，AI 模型的可靠性是否会受到影响？
- **参考来源**：Lam, R., et al. (2023). "Learning skillful medium-range global weather forecasting." *Science*, 382(6675), 1416-1421. https://doi.org/10.1126/science.adi2336

#### 案例三：Khan Academy Khanmigo — AI 教育助手

- **案例名称**：可汗学院 Khanmigo — AI 驱动的一对一辅导助手
- **时间**：2023 年
- **简述**：2023 年，可汗学院（Khan Academy）与 OpenAI 合作推出了 Khanmigo，一个基于 GPT-4 的 AI 教育助手。Khanmigo 的设计理念不是直接给出答案，而是采用苏格拉底式教学法——通过引导性提问帮助学生自主思考和解决问题。它能根据学生的回答动态调整提示策略，识别学生的知识盲点，并提供个性化的学习路径。Khanmigo 同时支持学生端（辅导、写作指导、辩论练习）和教师端（课程计划生成、学生表现分析、差异化教学建议）。截至 2024 年，Khanmigo 已服务超过 100 万师生，成为 AI 教育应用的标杆案例。
- **教学讨论要点**：
  1. Khanmigo 采用"引导而非告知"的苏格拉底式教学。与直接给出答案的 AI 相比，这种方式对学习效果有什么不同的影响？AI 教育产品应该"帮助学生思考"还是"帮学生完成任务"？
  2. AI 教育助手可能加剧"数字鸿沟"——富裕地区的学生更早获得高质量 AI 辅导。如何确保 AI 教育工具的公平可及性？
- **参考来源**：Khan Academy. (2023). "Introducing Khanmigo." https://www.khanacademy.org/about/press/khanmigo. 以及 Bakia, M., et al. (2024). "AI in Education: Lessons from the Khan Academy Pilot." *UNESCO Working Paper*.

#### 重要学术引用

**DALL-E 2 — 文本到图像生成**

Ramesh et al. (2022) 发表了 DALL-E 2 的研究论文，这是文本到图像生成领域的里程碑式工作。DALL-E 2 基于 CLIP 文本-图像编码器与扩散模型（diffusion decoder）的结合，能够从自然语言描述生成高分辨率、语义一致的图像。相比初代 DALL-E，DALL-E 2 在图像质量、分辨率和语义准确性上均有大幅提升：
- 支持图像编辑（基于文本指令修改图像特定区域）
- 支持图像变体生成（基于原图生成风格/内容相似的新图）
- 能处理复杂的组合性概念（如"一只戴太空头盔的柯基犬在月球上"）

DALL-E 2 的发布标志着 AI 创意生成进入新纪元，对设计、艺术、广告等行业产生了深远影响，同时也引发了关于 AI 生成内容版权和深度伪造的讨论。

- **参考来源**：Ramesh, A., Dhariwal, P., Nichol, A., et al. (2022). "Hierarchical Text-Conditional Image Generation with CLIP Latents." *arXiv preprint arXiv:2204.06125*. 发表于 *NeurIPS 2022 Workshop*.

---

## 课件与游戏建议

### 课件形式
- G1：大模型能力对比可视化（历年模型能力雷达图）
- G1：涌现能力模拟实验（不同规模模型效果对比）
- G2：Agent 工作流可视化（实时展示 Agent 思考过程）
- G3：AI 应用案例库（各行业 AI 应用实例展示）

### 游戏形式
- G1：「模型训练师」模拟大模型训练过程
- G2：「Agent 设计师」构建自己的 AI Agent
- G3：「AI 趋势预测」根据信息预测 AI 发展方向
- G2：「具身挑战」控制虚拟机器人完成复杂任务
