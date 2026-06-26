# 因果动力学架构（Causal Dynamics Architecture, CDA）

> **第三代人工智能的底层计算范式提案**
>
> **"第二代AI学会了说话，但没有学会世界。CDA的目标是让机器学会'世界怎么算'。"**

**核心洞察**：用因果机制网络替代 Self-Attention，用实体-状态因果图替代 Token 序列，用哈密顿投影替代 LayerNorm，用在线贝叶斯更新替代反向传播——以理论物理的数学骨架重新定义"智能"的底层计算。

---

## 一、设计哲学：从"关联引擎"到"动力学引擎"

Transformer 的核心隐喻是**关联**：给定上下文，什么最可能跟着出现？

CDA 的核心隐喻是**动力学**：给定当前世界状态和一个干预，世界会怎么演化？

这不是在 Transformer 上打补丁。这是用一套全新的计算原语，重新定义"智能"的底层实现。

| 维度 | Transformer | CDA |
|------|------------|-----|
| 基本计算单元 | Self-Attention（关联矩阵） | Causal Mechanism Module（因果机制函数） |
| 输入表示 | Token 序列（离散符号流） | Entity-State Graph（实体-状态因果图） |
| 核心操作 | Q·K^T → Softmax → 加权求和 | 哈密顿传播 + 因果机制沿图传播 |
| 输出预测 | 下一个 token 的概率分布 | 下一个物理状态的分布（含不确定性） |
| 学习目标 | 最大化似然 P(y|x) | 最小化仿真轨迹误差 + 因果解释力 |
| 推理方式 | 自回归生成（token by token） | 状态演化仿真（step by step） |
| "知识"形态 | 分布在高维向量空间中的关联模式 | 编码在因果图结构 + 机制函数中的物理规律 |

---

## 二、核心架构：五层计算栈

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 5: 语言界面层 (Language Interface)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐        │
│  │ 意图解析器   │  │ 状态报告生成器│  │ 自然语言解释器  │        │
│  │ NL → do()   │  │ State → NL   │  │ 因果链 → 文本  │        │
│  └─────────────┘  └──────────────┘  └─────────────────┘        │
│  （可选的薄层，用小型LLM充当翻译官，不参与核心推理）              │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: 反事实推理层 (Counterfactual Reasoning)                │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐        │
│  │ 平行世界分支 │  │ 干预传播引擎 │  │ 最优策略搜索    │        │
│  │ Fork-State   │  │ do() Propagate│  │ Causal Planning│        │
│  └─────────────┘  └──────────────┘  └─────────────────┘        │
│  核心能力：what-if推理、策略规划、决策支持                       │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: 因果动力学层 (Causal Dynamics Engine) ★核心★          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           Causal Mechanism Network (CMN)                 │    │
│  │                                                          │    │
│  │   Entity-State Graph:                                    │    │
│  │     节点 = 实体 (entity_i)                               │    │
│  │       ├── 物理状态 s_i = (q_i, p_i)  [广义坐标+动量]   │    │
│  │       ├── 属性向量 a_i (质量、材料、类别等)               │    │
│  │       └── 信念分布 b_i ~ N(μ_i, Σ_i) [贝叶斯不确定性]  │    │
│  │                                                          │    │
│  │     边 = 因果机制 (e_ij)                                  │    │
│  │       ├── 机制函数 f_ij: (s_i, s_j) → (ds_i, ds_j)     │    │
│  │       ├── 因果强度 α_ij ∈ [0,1]                          │    │
│  │       ├── 时间延迟 τ_ij (因果传播需要时间)               │    │
│  │       └── 机制类型 t_ij ∈ {力学,热力学,化学,信息,...}    │    │
│  │                                                          │    │
│  │   状态演化（核心计算）:                                    │    │
│  │     ds/dt = Σ_j α_ij · f_ij(s_i, s_j; θ_ij) + η        │    │
│  │             ─────────────────────────────────────        │    │
│  │             沿因果边传播的机制函数之和                    │    │
│  │                                                          │    │
│  │     受哈密顿约束:                                         │    │
│  │       H(s) = E_kinetic + E_potential = const            │    │
│  │       保证了能量守恒是架构属性，不是学习目标              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: 多尺度聚合层 (Multi-Scale Aggregation)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐        │
│  │ 微观→宏观   │  │ 宏观→微观   │  │ 尺度选择器      │        │
│  │ 粗粒化      │  │ 条件采样    │  │ (注意力自适应)   │        │
│  │ Renormalize  │  │ Conditional │  │                 │        │
│  └─────────────┘  └──────────────┘  └─────────────────┘        │
│  核心能力：像统计力学一样从微观涌现宏观行为                     │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: 感知校准层 (Perception & Calibration)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐        │
│  │ 传感器融合   │  │ 观测→状态映射│  │ 贝叶斯更新      │        │
│  │ (多模态)    │  │ Encoder      │  │ Posterior Update│        │
│  └─────────────┘  └──────────────┘  └─────────────────┘        │
│  核心能力：从物理观测中构建和校准内部世界模型                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 统一感知接口：从非结构化数据到实体-状态图

§2.2 的三个子模块（传感器融合、编码器、校准器）假设输入已经是**结构化**的传感器读数——每个传感器对应一个已知的实体 ID，每个读数有明确的物理量纲。

但在大多数实际部署场景中，系统面对的是**非结构化输入**：运维人员提交的文本工单、巡检机器人拍摄的照片、SCADA 系统导出的日志、自然语言查询。CDA 需要一个**感知前端**将任意模态的原始数据转化为 §2.2 所需的结构化格式。

这是 CDA 等价于 Transformer 的 Tokenization，但信息粒度和结构感知能力远超后者：

| | Transformer Tokenization | CDA 感知接口 |
|--|-------------------------|-------------|
| 输入 | 文本字符串 | 任意模态（文本、图像、传感器、日志、语音…） |
| 输出 | Token ID 序列 `[t₁, t₂, …, tₙ]` | 实体-状态因果图 `{Entity_i, Edge_ij}` |
| 信息粒度 | 子词（subword） | 语义实体（semantic entity） |
| 结构感知 | 无（线性序列） | 有（实体间空间/因果拓扑） |
| 跨模态 | 各模态独立 tokenizer | 统一接口，多模态实体消歧 |

#### 2.1.1 实体发现：从非结构化数据中提取物理实体

```python
class EntityDiscoveryModule:
    """
    非结构化数据 → 实体候选列表。

    三种发现模式：
    1. 文本模式：NER + 因果线索抽取（使用小型 LLM 或规则引擎）
    2. 视觉模式：目标检测 + 空间标定 + 场景图构建
    3. 时序模式：变点检测 + 行为分段（每个段 → 一个实体的一个状态）

    输入与输出之间没有固定的映射关系——同一个物理实体可能同时出现在
    文本描述、监控画面和传感器时序中。消歧是 §2.1.2 的任务。
    """

    def discover_from_text(self, text, domain_ontology):
        """
        从文本中提取实体候选和因果线索。

        输入: "3号压缩机出口温度达到85°C，超过阈值80°C，
              冷冻水流量下降至额定值的60%"

        输出:
          EntityCandidate("压缩机_3", type=mechanical,
                          attrs={温度: 85°C, 状态: 运行中})
          EntityCandidate("冷冻水", type=fluid,
                          attrs={流量: 0.6, 温度: unknown})
          CausalHint(source="压缩机_3", target="冷冻水", type=thermal)
        """
        # Step 1: 实体识别
        raw_entities = self.ner_model.extract(text)

        # Step 2: 实体接地——匹配到领域本体中的已知实体类型
        entities = []
        for ent in raw_entities:
            grounded = domain_ontology.ground(
                ent.name, ent.attributes, ent.context
            )
            if grounded is not None:
                entities.append(grounded)

        # Step 3: 因果线索抽取
        causal_hints = self.causal_extractor.extract(text, entities)

        return entities, causal_hints

    def discover_from_image(self, image, spatial_calibration):
        """
        从图像中提取视觉实体并映射到物理坐标系。

        关键：视觉检测框 → 物理坐标 → 实体 ID 的对齐。
        """
        detections = self.detector.detect(image)

        visual_entities = []
        for det in detections:
            world_pos = spatial_calibration.pixel_to_world(det.bbox)
            visual_entities.append(EntityCandidate(
                name=det.label,
                type=self._classify_detection(det),
                position=world_pos,
                confidence=det.score,
            ))

        return visual_entities

    def discover_from_timeseries(self, sensor_data, change_detector):
        """
        从时序数据中发现行为实体。

        核心思想：一个"实体"对应一段行为一致的时序。
        变点检测自动发现实体的出现/消失/状态转换时刻。
        """
        segments = change_detector.detect(sensor_data)

        entities = []
        for seg in segments:
            entities.append(EntityCandidate(
                name=f"segment_{seg.id}",
                type=self._classify_segment(seg),
                state_vector=seg.statistics,  # mean, std, trend
                time_span=(seg.start, seg.end),
            ))

        return entities
```

#### 2.1.2 多模态实体消歧

```python
class EntityResolver:
    """
    多模态实体消歧：将不同模态发现的候选合并为全局实体。

    例：文本提到"3号压缩机"，图像检测到压缩机形状的物体，
    传感器显示 comp_03 温度异常。三者可能指同一物理实体。

    方法：基于多特征相似度的图聚类（并查集 + 阈值）。
    """

    def resolve(self, candidates, entity_database):
        """
        合并多模态候选到全局实体库。

        Args:
            candidates: List[EntityCandidate] 来自各模态的候选
            entity_database: 已有实体库（用于匹配）

        Returns:
            resolved: List[Entity] 消歧后的实体列表
        """
        N = len(candidates)
        if N == 0:
            return []

        # 构建候选间的相似度矩阵
        sim_matrix = torch.zeros(N, N)
        for i in range(N):
            for j in range(i + 1, N):
                a, b = candidates[i], candidates[j]
                sim_matrix[i, j] = (
                    0.3 * self._name_similarity(a.name, b.name)
                    + 0.2 * self._type_compatibility(a.type, b.type)
                    + 0.3 * self._spatial_proximity(a.position, b.position)
                    + 0.2 * self._temporal_cooccurrence(a.time_span, b.time_span)
                )
                sim_matrix[j, i] = sim_matrix[i, j]

        # 并查集聚类：相似度超过阈值的候选归为同一实体
        clusters = self._connected_components(sim_matrix, threshold=0.65)

        # 合并：每个聚类 → 一个实体（多源信息融合）
        resolved = []
        for cluster in clusters:
            members = [candidates[i] for i in cluster]
            merged = self._merge_candidates(members)
            resolved.append(merged)

        return resolved

    def _connected_components(self, sim_matrix, threshold):
        """相似度矩阵 → 连通分量（并查集实现）"""
        N = sim_matrix.shape[0]
        parent = list(range(N))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i in range(N):
            for j in range(i + 1, N):
                if sim_matrix[i, j] > threshold:
                    ri, rj = find(i), find(j)
                    if ri != rj:
                        parent[ri] = rj

        clusters = {}
        for i in range(N):
            r = find(i)
            clusters.setdefault(r, []).append(i)

        return list(clusters.values())
```

#### 2.1.3 本体驱动的状态初始化

```python
class OntologyGuidedInitializer:
    """
    利用领域本体为新实体分配初始状态和候选因果边。

    本体定义了：
    - 实体类型层次（机械系统 → 旋转设备 → 压缩机）
    - 每种类型的标准状态维度及物理范围
    - 典型因果连接模式
    """

    def initialize_state(self, entity_type, observed_attrs):
        """
        为新实体构建初始 EntityState。

        策略：
        - 已知维度：用观测值，低不确定性（传感器精度）
        - 未知维度：用先验范围中值，高不确定性（均匀分布近似）
        """
        schema = self.ontology.get_schema(entity_type)

        state_vec = []
        unc_vec = []
        for dim in schema.state_dimensions:
            if dim.name in observed_attrs:
                state_vec.append(observed_attrs[dim.name])
                unc_vec.append(dim.noise_std ** 2)
            else:
                mid = 0.5 * (dim.range[0] + dim.range[1])
                state_vec.append(mid)
                half = 0.5 * (dim.range[1] - dim.range[0])
                unc_vec.append(half ** 2)

        return EntityState(
            position=torch.tensor(state_vec, dtype=torch.float32),
            uncertainty=torch.diag(torch.tensor(unc_vec)),
        )

    def suggest_edges(self, entity, existing_graph):
        """
        基于本体建议初始因果边（低置信度候选，需数据验证）。

        例：新发现一个"热交换器"实体
        → 本体建议：热交换器→冷流体（热力学型）
        → 检查目标实体是否已存在
        → 不存在的边以 confidence=0.3 的候选状态加入
        """
        patterns = self.ontology.get_typical_connections(entity.type)
        candidates = []
        for pat in patterns:
            target = existing_graph.find_by_type(pat.target_type)
            if target is not None:
                candidates.append(CausalEdge(
                    source=entity.id,
                    target=target.id,
                    mechanism_type=pat.causal_type,
                    strength=pat.prior_strength,
                    confidence=0.3,
                ))
        return candidates
```

**感知接口的完整数据流**：

```
非结构化输入
    │
    ├─ 文本 ─→ EntityDiscovery.discover_from_text() ──┐
    ├─ 图像 ─→ EntityDiscovery.discover_from_image() ──┼─→ EntityResolver.resolve()
    ├─ 时序 ─→ EntityDiscovery.discover_from_timeseries() ┤
    └─ ...                                             │
                                                      │
                                               消歧后的 Entity 列表
                                                      │
                                              OntologyInitializer
                                                      │
                                              带初始状态的 Entity
                                              + 候选 CausalEdge
                                                      │
                                              ────→ §2.2 感知校准层 ────→ CMN
```

### 2.2 感知校准层（Layer 1）的实现

Layer 1 是 CDA 与外部物理世界的接口——负责将传感器数据（温度、压力、流量、图像等）转化为内部实体-状态因果图。它包含三个子模块：传感器融合、观测-状态映射（Encoder）、贝叶斯校准。

#### 2.2.1 传感器融合：多模态观测的对齐与整合

物理世界的观测来自不同类型的传感器，采样率、精度、延迟各异。传感器融合的第一步是将异构数据对齐到统一的时间-空间网格上：

```python
class SensorFusionLayer:
    """
    多模态传感器数据融合层。

    处理三类传感器异构性：
    1. 时间异步：不同传感器的采样频率不同
    2. 空间异构：传感器安装位置不同，覆盖不同空间区域
    3. 量纲差异：温度(K)、压力(Pa)、流量(m³/s) 等

    方法：
    - 时间对齐：最近邻插值到统一时间网格
    - 空间映射：传感器位置 → 实体 ID 的显式映射表
    - 量纲归一化：物理量纲 → 无量纲标准化的可学习映射
    """

    def __init__(self, sensor_configs):
        """
        Args:
            sensor_configs: 每个传感器的配置
                [{
                    'id': 'T_01',          # 传感器 ID
                    'type': 'temperature',  # 物理量类型
                    'location': (x,y,z),   # 空间位置
                    'unit': 'K',            # 量纲
                    'sampling_rate': 1.0,   # Hz
                    'noise_std': 0.5,       # 噪声标准差
                    'entity_id': 3,         # 关联的实体 ID
                }, ...]
        """
        self.sensors = sensor_configs
        # 构建传感器→实体的映射表
        self.sensor_to_entity = {s['id']: s['entity_id'] for s in sensor_configs}
        # 量纲归一化参数（可学习）
        self.norm_params = torch.nn.ParameterDict({
            s['id']: torch.nn.Parameter(torch.tensor([1.0, 0.0]))  # [scale, offset]
            for s in sensor_configs
        })

    def align_timestamps(self, raw_observations, target_times):
        """
        时间对齐：将异步传感器数据插值到统一时间网格。

        Args:
            raw_observations: {sensor_id: [(timestamp, value), ...]}
            target_times: 统一的时间网格 [t_0, t_1, ...]

        Returns:
            aligned: {sensor_id: [value_at_t0, value_at_t1, ...]}
        """
        aligned = {}
        for sensor_id, readings in raw_observations.items():
            times = [r[0] for r in readings]
            values = [r[1] for r in readings]
            # 线性插值到目标时间网格
            aligned[sensor_id] = np.interp(target_times, times, values)
        return aligned

    def normalize(self, sensor_id, raw_value):
        """量纲归一化：物理量 → 无量纲标准化值"""
        scale, offset = self.norm_params[sensor_id]
        return (raw_value - offset) / (scale + 1e-8)

    def forward(self, raw_observations, target_times):
        """
        完整的传感器融合流程：
        时间对齐 → 量纲归一化 → 按实体分组
        """
        aligned = self.align_timestamps(raw_observations, target_times)

        # 按实体分组
        entity_observations = {}
        for sensor_id, values in aligned.items():
            entity_id = self.sensor_to_entity[sensor_id]
            normalized = self.normalize(sensor_id, torch.tensor(values))
            if entity_id not in entity_observations:
                entity_observations[entity_id] = []
            entity_observations[entity_id].append(normalized)

        return entity_observations
```

#### 2.2.2 观测-状态映射（Encoder）

将传感器读数转化为实体状态向量。Layer 1 的 Encoder 与 Transformer 的 Token Embedding 不同：它的输出具有明确的物理含义（位置、动量、温度、压力等），且必须满足物理约束。

```python
class PhysicsAwareEncoder(torch.nn.Module):
    """
    物理感知的状态编码器。

    与 Transformer Embedding 的关键区别：
    - Transformer Embedding：任意向量，无物理含义
    - PhysicsAwareEncoder：输出 = 实体状态的物理量，必须满足约束

    设计选择：
    - 对于可直接测量的物理量（温度、压力）：直接映射，不做黑盒变换
    - 对于不可直接测量的物理量（内部应力、潜热）：用小型网络从可测量推断
    - 物理约束作为硬约束编码在输出层中
    """

    def __init__(self, entity_configs, observation_dim):
        super().__init__()
        self.entities = entity_configs

        # 直接映射层：传感器读数 → 可测物理量
        self.direct_mappers = torch.nn.ModuleDict()
        # 推断层：传感器读数 → 不可测物理量
        self.latent_estimators = torch.nn.ModuleDict()

        for entity in entity_configs:
            eid = str(entity['id'])
            state_dim = entity['state_dim']

            # 直接映射：传感器读数的线性组合（权重可学习，但有物理先验）
            self.direct_mappers[eid] = torch.nn.Linear(observation_dim, state_dim // 2)

            # 推断网络：估计不可直接测量的状态分量
            self.latent_estimators[eid] = torch.nn.Sequential(
                torch.nn.Linear(observation_dim, 32),
                torch.nn.Tanh(),
                torch.nn.Linear(32, state_dim // 2),
            )

    def forward(self, entity_observations):
        """
        将传感器观测映射到实体状态。

        Args:
            entity_observations: {entity_id: tensor of sensor readings}

        Returns:
            states: Dict[entity_id, EntityState]
        """
        states = {}
        for entity in self.entities:
            eid = str(entity['id'])

            if eid not in entity_observations:
                continue

            obs = entity_observations[eid]  # 传感器读数
            if isinstance(obs, list):
                obs = torch.stack(obs)

            # 直接测量的物理量
            measured = self.direct_mappers[eid](obs.float())

            # 推断的物理量
            latent = self.latent_estimators[eid](obs.float())

            # 组合为完整状态
            state = torch.cat([measured, latent], dim=-1)

            # 物理约束投影
            state = self._apply_physical_constraints(state, entity)

            states[entity['id']] = EntityState(
                position=state[:, :state.shape[-1]//2],
                momentum=state[:, state.shape[-1]//2:],
            )

        return states

    def _apply_physical_constraints(self, state, entity_config):
        """
        对编码结果施加物理约束。

        示例：
        - 温度 T > 0（绝对零度）
        - 压力 P > 0
        - 质量 m > 0
        """
        constraints = entity_config.get('constraints', {})
        for dim, constraint in constraints.items():
            if constraint == 'positive':
                state[:, dim] = torch.nn.functional.softplus(state[:, dim])
            elif isinstance(constraint, dict) and 'range' in constraint:
                lo, hi = constraint['range']
                state[:, dim] = lo + torch.sigmoid(state[:, dim]) * (hi - lo)
        return state
```

#### 2.2.3 贝叶斯校准：传感器噪声模型与后验更新

传感器读数不是绝对精确的——每个传感器都有噪声模型。贝叶斯校准将这些噪声模型编码为观测似然，与 Level 1 的信念追踪结合：

```python
class BayesianCalibrator:
    """
    贝叶斯校准层：融合传感器噪声模型与物理先验。

    对每个实体的每个状态维度维护：
    - 传感器似然 P(z | s) = N(z; H(s), R)
      其中 H 是观测矩阵，R 是传感器噪声协方差
    - 物理先验 P(s) = N(s; μ_prior, Σ_prior)
      来自物理约束（如温度范围、压力范围等）
    - 后验 P(s | z) ∝ P(z | s) · P(s)
    """

    def __init__(self, sensor_configs):
        self.observation_matrices = {}  # H: 状态 → 观测
        self.noise_covariances = {}    # R: 传感器噪声
        self.prior_means = {}          # μ_prior: 物理先验均值
        self.prior_covs = {}           # Σ_prior: 物理先验协方差

        for s in sensor_configs:
            sid = s['id']
            # 传感器噪声协方差（对角阵，噪声标准差来自传感器规格）
            self.noise_covariances[sid] = torch.eye(s.get('obs_dim', 1)) * (s['noise_std'] ** 2)

    def calibrate(self, raw_observation, current_belief, entity_id):
        """
        校准单个实体的状态估计。

        Args:
            raw_observation: 传感器原始读数
            current_belief: 当前信念 N(μ, Σ)
            entity_id: 实体 ID

        Returns:
            calibrated_belief: 校准后的信念 N(μ', Σ')
        """
        mu = current_belief.mu
        Sigma = current_belief.Sigma

        # 获取该实体的传感器配置
        sensor_id = self._get_primary_sensor(entity_id)
        R = self.noise_covariances[sensor_id]
        H = self.observation_matrices.get(sensor_id, torch.eye(mu.shape[0]))

        # 马氏距离检测：异常观测自动降权
        innovation = raw_observation - H @ mu
        S = H @ Sigma @ H.T + R
        mahal_dist = (innovation @ torch.inverse(S) @ innovation).item()

        if mahal_dist > 9.0:  # 3σ 以外
            # 异常观测：降低其权重，信任模型预测
            R_adaptive = R * 100.0
        else:
            R_adaptive = R

        # 标准卡尔曼更新
        K = Sigma @ H.T @ torch.inverse(H @ Sigma @ H.T + R_adaptive)
        mu_new = mu + K @ (raw_observation - H @ mu)
        Sigma_new = (torch.eye(Sigma.shape[0]) - K @ H) @ Sigma

        return Belief(mu_new, Sigma_new)
```

---

## 三、核心计算详解：因果机制网络（CMN）

这是 CDA 的心脏——替代 Transformer Self-Attention 的全新计算原语。

### 3.1 输入表示：实体-状态因果图

Transformer 的输入是 Token 序列。CDA 的输入是**实体状态图**：

```python
# Transformer的世界观：世界是符号序列
# [CLS] 猫 坐 在 垫子 上 [SEP]
# tokens = [token_0, token_1, ..., token_n]

# CDA的世界观：世界是实体及其因果关系的动态系统
class EntityState:
    position: Tensor  # q: 广义坐标（位置、角度、温度...）
    momentum: Tensor  # p: 共轭动量（速度、角速度、热流...）
    attributes: Tensor # a: 固有属性（质量、电荷、材料类型...）
    belief: Distribution # b: 贝叶斯信念 ~ N(μ, Σ)

class CausalEdge:
    source: int        # 因
    target: int        # 果
    mechanism: Callable # f_ij: 因果机制函数（可微分）
    strength: float    # α_ij: 因果强度
    delay: float       # τ_ij: 传播延迟
    type: str          # 机制类型
    confidence: float  # 因果关系的置信度

class WorldState:
    entities: Dict[int, EntityState]  # 所有实体
    edges: List[CausalEdge]            # 所有因果关系
    hamiltonian: Callable              # H(q, p): 系统哈密顿量
    time: float                        # 当前时刻
```

**关键区别**：
- Token 是**离散**的、**无序**的（靠位置编码注入序信息）
- Entity 是**连续**的、**有结构**的（自身携带物理坐标和属性）
- Token 之间的关系靠 Attention 从数据中**学到**
- Entity 之间的关系靠因果图**显式编码**

### 3.2 核心前向传播：因果动力学步进

Transformer 的前向传播是一次 Attention → FFN 的映射。

CDA 的前向传播是**一次物理仿真步进**：

```
给定当前世界状态 S_t 和干预 do(I):

1. 应用干预
   S'_t = S_t ⊕ do(I)    # 修改被干预实体的状态

2. 因果传播（核心计算）
   对每条因果边 e_ij ∈ Edges:
     Δs_i += α_ij · f_ij(s_i, s_j; θ_ij) · dt
     # 机制函数沿因果边将影响从 source 传播到 target

3. 哈密顿投影（物理约束）
   S''_t+1 = Project_to_Hamiltonian(S'_t + Δs)
   # 将状态投影回满足 H(q,p) = const 的流形上
   # 这一步确保能量守恒是架构硬约束

4. 贝叶斯更新（不确定性传播）
   b_i(t+1) = BayesianUpdate(b_i(t), observation_i, model_i)
   Σ_i(t+1) = propagate_uncertainty(Σ_i(t), Jacobian_f, dt)
   # 不确定性沿因果链传播，可精确定量

5. 输出
   S_{t+1} = (S''_t+1, {b_i(t+1)})
   # 下一个时刻的世界状态 + 每个实体的不确定性
```

### 3.3 因果机制函数 f_ij 的参数化

这是最关键的设计选择。每条因果边上的机制函数不是任意的——它被**物理约束限定形状**：

```
f_ij(s_i, s_j; θ) = W_type(θ) · Φ(s_i, s_j) · σ(α_ij · distance(s_i, s_j))

其中：
  W_type(θ): 由因果类型决定的参数矩阵
    - 力学型：W 是反对称的（牛顿第三定律）
    - 热力学型：W 保证热流从高温到低温（热力学第二定律）
    - 信息型：W 保证信号强度随距离衰减
    - 化学型：W 保证质量守恒

  Φ(s_i, s_j): 状态交互的基函数（可学习的）
    类似 Transformer 的 Q·K^T，但物理含义不同：
    - 不是"这两个token有多相关"
    - 而是"实体i的状态在实体j的作用下会怎么变化"

  σ(α · distance): 因果强度衰减（因果影响随距离/介质衰减）
```

#### 3.3.1 W_type 的矩阵结构与物理约束编码

W_type 不是自由参数矩阵——它的结构由因果类型决定，物理约束通过矩阵结构**硬编码**到架构中：

```python
class MechanismTypeRegistry:
    """
    因果机制类型注册表：每种类型定义 W 矩阵的结构约束。
    约束通过参数化方式实现，使梯度下降不可能违反物理定律。
    """

    # --- 力学型：牛顿第三定律（作用力 = 反作用力） ---
    # W_mech 的参数化：W = A - A^T，天然保证反对称
    # 可学习参数：A ∈ R^(d×d)（任意矩阵）
    # 自由度：d(d-1)/2（而非 d² 的无约束参数）
    @staticmethod
    def mechanical_W(raw_A):
        """W = A - A^T → W^T = -W（牛顿第三定律）"""
        return raw_A - raw_A.T

    # --- 热力学型：热力学第二定律（热量从高温流向低温） ---
    # W_thermal 的参数化：W = exp(-β·sigmoid(A))（元素非负）
    # 可学习参数：A ∈ R^(d×d)，β 为温度参数（控制约束强度）
    # 单调性约束：对温度梯度的响应始终与梯度同号
    @staticmethod
    def thermal_W(raw_A, beta=5.0):
        """W = exp(-β·sigmoid(A))，所有元素 ∈ (0,1]，保证热流方向正确"""
        return torch.exp(-beta * torch.sigmoid(raw_A))

    # --- 信息型：信号衰减（强度随距离递减） ---
    # W_info 的参数化：W = exp(-γ·|A|)（对角衰减矩阵）
    # 可学习参数：A ∈ R^d（衰减速率），γ 为全局传播常数
    @staticmethod
    def information_W(raw_diag, gamma=1.0):
        """W = diag(exp(-γ·|a_i|))，信号强度随"距离"指数衰减"""
        return torch.diag(torch.exp(-gamma * torch.abs(raw_diag)))

    # --- 化学型：质量守恒（所有反应物的质量转移总和为零） ---
    # W_chemical 的参数化：W 的行和为零（流入=流出）
    # 实现：W = A - diag(A·1)（从 A 中减去行均值，保证零和）
    @staticmethod
    def chemical_W(raw_A):
        """W 行和为零，保证质量守恒"""
        row_sum = raw_A.sum(dim=1, keepdim=True)
        return raw_A - row_sum / raw_A.shape[1]
```

**关键性质**：约束在参数化层面保证，而非损失函数层面。无论梯度如何更新，W_type 始终满足物理定律——与 Softmax 保证概率和为1的思路一致。

#### 3.3.2 状态交互基函数 Φ(s_i, s_j) 的参数化

Φ 是机制函数的可学习部分，负责捕获"实体i的状态在实体j的作用下怎么变化"：

```python
class InteractionBasis(torch.nn.Module):
    """
    状态交互基函数 Φ(s_i, s_j)。

    设计原则：
    - 分离变量：Φ = Σ_k φ_k(s_i) · ψ_k(s_j)，降低参数量
    - 物理量纲一致性：每个基函数对应一个物理量纲通道
    - 多尺度交互：低阶捕获线性效应，高阶捕获非线性耦合
    """

    def __init__(self, state_dim, hidden_dim, num_basis=16):
        super().__init__()
        self.state_dim = state_dim
        self.num_basis = num_basis

        # 源实体编码器：s_j → 隐表示
        self.source_encoder = torch.nn.Sequential(
            torch.nn.Linear(state_dim, hidden_dim),
            torch.nn.Tanh(),  # Tanh 保证有界，适合物理量
            torch.nn.Linear(hidden_dim, num_basis),
        )

        # 目标实体编码器：s_i → 隐表示
        self.target_encoder = torch.nn.Sequential(
            torch.nn.Linear(state_dim, hidden_dim),
            torch.nn.Tanh(),
            torch.nn.Linear(hidden_dim, num_basis),
        )

        # 可学习的基函数权重
        self.basis_weights = torch.nn.Parameter(
            torch.randn(num_basis, state_dim) * 0.01
        )

    def forward(self, s_i, s_j):
        """
        计算 Φ(s_i, s_j) ∈ R^state_dim

        输出含义：实体i的状态变化量（在实体j的影响下）
        """
        h_i = self.target_encoder(s_i)  # (batch, num_basis)
        h_j = self.source_encoder(s_j)  # (batch, num_basis)

        # 分离变量交互：Σ_k h_i[k] · h_j[k] · w[k]
        interaction = h_i * h_j  # (batch, num_basis)
        delta_s = interaction @ self.basis_weights  # (batch, state_dim)

        return delta_s
```

**量纲一致性保障**：基函数的每个输出维度对应一个物理量纲（温度、压力、速度等），`basis_weights` 的初始化按照量纲通道分组，禁止跨量纲的参数耦合。

#### 3.3.3 因果强度衰减 σ(α·distance)

```python
class CausalDecay(torch.nn.Module):
    """
    因果强度衰减函数：因果影响随距离/介质递减。

    σ(r) = exp(-α · r)              （指数衰减，默认）
    σ(r) = 1 / (1 + α · r²)         （逆二次衰减，长程力）
    σ(r) = exp(-(α · r)²)           （高斯衰减，短程力）

    选择规则由因果类型自动决定：
    - 力学（引力/静电力）：逆二次
    - 热传导：指数衰减（Fourier 定律）
    - 化学反应：高斯衰减（短程接触）
    """
    DECAY_RULES = {
        'mechanical': 'inverse_quadratic',  # 长程力
        'thermal':    'exponential',         # 中程热传导
        'chemical':   'gaussian',            # 短程接触
        'information':'exponential',         # 中程信号传播
    }

    def __init__(self, causal_type):
        super().__init__()
        self.decay_type = self.DECAY_RULES.get(causal_type, 'exponential')
        self.alpha = torch.nn.Parameter(torch.tensor(1.0))

    def forward(self, distance):
        r = distance + 1e-8  # 数值稳定
        if self.decay_type == 'exponential':
            return torch.exp(-self.alpha * r)
        elif self.decay_type == 'inverse_quadratic':
            return 1.0 / (1.0 + self.alpha * r ** 2)
        elif self.decay_type == 'gaussian':
            return torch.exp(-(self.alpha * r) ** 2)
```

#### 3.3.4 完整的因果机制函数组装

```python
class CausalMechanismFunction(torch.nn.Module):
    """
    因果机制函数 f_ij(s_i, s_j; θ) 的完整实现。

    f_ij = W_type · Φ(s_i, s_j) · σ(α · distance)
    """
    def __init__(self, causal_type, state_dim, hidden_dim=64, num_basis=16):
        super().__init__()
        self.causal_type = causal_type

        # W_type 的原始参数（通过 MechanismTypeRegistry 约束）
        raw_dim = state_dim  # W_type ∈ R^(state_dim × state_dim)
        self.raw_W = torch.nn.Parameter(torch.randn(raw_dim, raw_dim) * 0.01)

        # 状态交互基函数
        self.phi = InteractionBasis(state_dim, hidden_dim, num_basis)

        # 因果强度衰减
        self.decay = CausalDecay(causal_type)

        # 因果强度（可学习标量）
        self.strength = torch.nn.Parameter(torch.tensor(0.5))

        # 类型注册表
        self.registry = MechanismTypeRegistry()

    def get_W(self):
        """获取受物理约束的 W_type 矩阵"""
        if self.causal_type == 'mechanical':
            return self.registry.mechanical_W(self.raw_W)
        elif self.causal_type == 'thermal':
            return self.registry.thermal_W(self.raw_W)
        elif self.causal_type == 'information':
            diag = torch.nn.functional.softplus(self.raw_W.diagonal())
            return self.registry.information_W(diag)
        elif self.causal_type == 'chemical':
            return self.registry.chemical_W(self.raw_W)
        else:
            return self.raw_W  # 默认无约束

    def forward(self, s_i, s_j, distance):
        """
        计算实体i在实体j影响下的状态变化 Δs_i

        Args:
            s_i: 目标实体的状态 (batch, state_dim)
            s_j: 源实体的状态 (batch, state_dim)
            distance: 因果距离 (batch, 1)

        Returns:
            delta_s: 状态变化量 (batch, state_dim)
        """
        W = self.get_W()                      # 受约束的参数矩阵
        phi_val = self.phi(s_i, s_j)          # 交互基函数输出
        decay_val = self.decay(distance)      # 衰减系数
        strength = torch.sigmoid(self.strength)  # 因果强度 ∈ (0,1)

        return strength * (phi_val @ W.T) * decay_val
```

**与 Self-Attention 的本质区别**：

| | Self-Attention | Causal Mechanism |
|--|---------------|------------------|
| 计算内容 | "A 和 B 有多相关" | "A 怎么影响 B" |
| 方向性 | 无方向（对称的） | 有方向（因果箭头） |
| 时间性 | 无（静态的） | 有（传播需要时间） |
| 物理约束 | 无 | 有（守恒律、对称性） |
| 输出 | 加权表示向量 | 状态变化量 Δs |
| 参数化 | 任意矩阵（Q,K,V） | 约束矩阵（W_type 由物理定律限定结构） |

### 3.4 因果计算路由：物理语义驱动的稀疏选择

实体规模从数百增长到数万时，因果边的数量可达 O(N²)。每一步都计算所有边既不必要也不现实。CDA 引入**因果计算路由**——一个物理语义驱动的稀疏选择机制，决定每个时间步只计算"值得计算"的因果边子集。

与 Transformer 注意力的关键区别：

| | Transformer Self-Attention | CDA 因果路由 |
|--|---------------------------|-------------|
| 选择依据 | token 间的关联分数（数据驱动） | 因果强度 + 状态变化 + 不确定性（物理驱动） |
| 选择策略 | 全连接 + softmax 软化 | 硬阈值 + Top-K + 全局预算 |
| 动态性 | 每步全量重算 | 增量更新（大部分边的选择状态跨步不变） |
| 可解释性 | 注意力权重（弱解释） | 路由原因 = "实体 X 变化显著 + 因果强度高"（强解释） |

```python
class CausalRouter:
    """
    因果计算路由器：每步选择需要激活的因果边子集。

    路由分数 r_ij = α_ij × S_change(i) × S_unc(j) × Q(j)

    - α_ij: 因果强度（边的固有属性）
    - S_change(i): 源实体最近的状态变化显著性（tanh 归一化）
    - S_unc(j): 目标实体的当前不确定性（sigmoid 归一化）
    - Q(j): 查询相关性（可选，无查询时恒为 1）
    """

    def __init__(self, num_entities, top_k=16, max_edges=2048):
        self.num_entities = num_entities
        self.top_k = top_k          # 每个目标实体最多保留 k 条入边
        self.max_edges = max_edges  # 全局计算预算（硬上限）

    def route(self, world, query_entities=None):
        """
        计算本步需要激活的因果边集合。

        三级筛选策略：
          Level 1: 硬阈值（分数 < 0.01 的边直接跳过）
          Level 2: Top-K（每个目标实体保留分数最高的 k 条入边）
          Level 3: 全局预算（总边数不超过 max_edges）

        Returns:
            active_edges: Set[(source, target)] 本步需要计算的边
        """
        scores = self._compute_scores(world, query_entities)

        # Level 1: 硬阈值过滤
        mask = scores > 0.01

        # Level 2: 每个目标实体保留 top-k 入边
        selected = torch.zeros_like(mask)
        for j in range(self.num_entities):
            col = scores[:, j] * mask[:, j]
            nonzero = (col > 0).sum().item()
            k = min(self.top_k, nonzero)
            if k > 0:
                top_idx = col.topk(k).indices
                selected[top_idx, j] = True

        # Level 3: 全局预算上限
        total = selected.sum().item()
        if total > self.max_edges:
            flat = (scores * selected).flatten()
            cutoff = flat.topk(self.max_edges).values[-1]
            selected &= (scores >= cutoff)

        # 转换为边集合
        active = set()
        idx = selected.nonzero()
        for row in idx:
            active.add((row[0].item(), row[1].item()))

        return active

    def _compute_scores(self, world, query_entities):
        """
        计算 N×N 路由分数矩阵。

        每条边 e_ij 的分数 = 因果强度 × 源变化因子 × 目标不确定因子 × 查询因子
        """
        scores = torch.zeros(self.num_entities, self.num_entities)

        for edge in world.edges:
            i, j = edge.source, edge.target

            # 因果强度
            alpha = edge.strength

            # 源实体状态变化显著性
            delta = world.get_recent_state_change(i)          # 标量
            s_change = torch.tanh(delta / (world.state_scale[i] + 1e-8))  # ∈ (-1, 1)

            # 目标实体不确定性
            sigma_trace = world.get_uncertainty(j).trace().item()
            s_unc = torch.sigmoid((sigma_trace - self._unc_thresh) / self._unc_scale)  # ∈ (0, 1)

            # 查询相关性
            q_rel = 1.0
            if query_entities is not None:
                q_rel = float(j in query_entities)

            scores[i, j] = alpha * (1.0 + s_change) * (1.0 + s_unc) * q_rel

        return scores
```

**路由对复杂度的影响**：

```
无路由:  O(N² × k_mech)   — 计算所有边，k_mech = 机制函数参数量
有路由:  O(N × K × k_mech) — K = top_k ≪ N

示例（N=10000, K=16, k_mech=64）:
  无路由:  10000² × 64 = 6.4×10⁹  FLOPs/step  （不实际）
  有路由:  10000 × 16 × 64 = 1.0×10⁷  FLOPs/step  （毫秒级）
  加速比:  640×

路由自身开销: O(N × K) 用于分数计算（可增量更新，非全量重算）
净收益: 当 K ≪ N 时，路由开销可忽略不计
```

**关键性质**：路由分数的三个因子都有清晰的物理含义——不是"这两个 token 有多相关"的黑盒分数，而是"这条因果边当前有多重要"的可解释度量。这使得路由决策可以被人类审查和调试，而 Transformer 的注意力权重缺乏这种可解释性。

---

## 四、哈密顿约束：能量守恒作为架构属性

这是 CDA 最独特的工程设计。

### 4.0 动机

Transformer 的参数空间允许拟合任意函数，包括违反物理定律的函数。如果模型学到"物体可以穿透地面"或"能量可以凭空产生"，没有任何机制阻止它。

### 4.1 系统哈密顿量恒等式

```python
class HamiltonianConstraint:
    """
    系统哈密顿量 H(q, p) = T(p) + V(q)
    T = 动能（所有实体的动能之和）
    V = 势能（所有实体间的相互作用势能之和）

    约束：H(q_t, p_t) = H(q_0, p_0) = E_total  ∀t
    """

    def project_to_energy_manifold(self, state):
        """将状态投影到能量守恒流形上"""
        q, p = state.position, state.momentum
        E_current = self.hamiltonian(q, p)
        E_target = self.E_total  # 初始总能量

        # 通过拉格朗日乘子法修正状态
        error = E_current - E_target
        grad_H_q = jacobian(self.hamiltonian, q)
        grad_H_p = jacobian(self.hamiltonian, p)

        # 沿哈密顿量的梯度方向修正
        q_corrected = q - λ * grad_H_q
        p_corrected = p - λ * grad_H_p

        return State(q_corrected, p_corrected)
```

### 4.2 积分器选择：辛积分器（Symplectic Integrator）

哈密顿投影的本质问题是如何在数值演化中保持 $H(q,p) = \text{const}$。朴素的前向欧拉法会导致能量系统性漂移，必须使用**辛积分器**——一类天然保持辛结构（从而保持能量有界）的数值方法。

CDA 采用**分阶段设计**：

```
因果传播（每条边计算 Δs） → 辛积分器步进（更新 q, p） → 哈密顿投影（消除残余误差）
         Step A                      Step B                        Step C
```

#### 推荐积分器：Störmer-Verlet（速度 Verlet）

选择理由：
- 二阶精度，计算成本与一阶欧拉法相当（每步仅需两次力计算）
- 时间可逆（保证辛结构）
- 长时间仿真中能量振荡有界，不漂移
- 结构简单，适合 GPU 并行化

```python
class SymplecticIntegrator:
    """
    Störmer-Verlet 辛积分器。

    核心性质：
    - 辛性：保留相空间的辛结构 → 能量长期有界
    - 时间可逆：将 dt 反号可以精确回溯轨迹
    - 二阶精度：局部误差 O(dt³)，全局误差 O(dt²)
    """

    def step(self, state, dt, compute_forces):
        """
        执行一步 Verlet 积分。

        Args:
            state: 当前世界状态（含 q, p）
            dt: 时间步长
            compute_forces: 力的计算函数 → 由因果机制网络提供

        Returns:
            next_state: 下一时刻的状态

        算法（速度 Verlet 形式）：
          p_{1/2} = p_t + (dt/2) · F(q_t)        半步动量更新
          q_{t+1} = q_t + dt · p_{1/2} / m         全步位置更新
          F_{t+1} = compute_forces(q_{t+1})         在新位置重新计算力
          p_{t+1} = p_{1/2} + (dt/2) · F(q_{t+1})  半步动量更新
        """
        q, p = state.position, state.momentum
        m = state.attributes['mass']  # 质量矩阵

        # 半步动量
        forces = compute_forces(state)  # 来自因果机制网络
        p_half = p + 0.5 * dt * forces

        # 全步位置
        q_new = q + dt * p_half / m

        # 新位置的力（因果传播的核心调用）
        temp_state = state.clone(position=q_new, momentum=p_half)
        forces_new = compute_forces(temp_state)

        # 半步动量
        p_new = p_half + 0.5 * dt * forces_new

        return state.clone(position=q_new, momentum=p_new)
```

#### 高阶积分器：Yoshida 4阶（可选）

当需要更高精度时（如长时间仿真、强非线性系统），使用 Yoshida 四阶积分器：

```python
class Yoshida4Integrator:
    """
    Yoshida 四阶辛积分器。

    通过组合三个 Verlet 步，构造高阶方法：
    S_4(dt) = S_2(x₁·dt) · S_2(x₀·dt) · S_2(x₁·dt)

    其中 x₀ = 1 - 2·x₁, x₁ = 1/(2-2^{1/3}) ≈ 1.3512

    优势：四阶精度，仍然是辛的，每步需要 3 次力计算
    适用场景：高精度仿真、强非线性系统（混沌、碰撞）
    """

    # Yoshida 系数
    X1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))  # ≈ 1.3512071919596578
    X0 = 1.0 - 2.0 * X1                      # ≈ -1.7024143839193156

    def step(self, state, dt, compute_forces):
        """四阶 Yoshida 步进"""
        # 三个 Verlet 子步
        state = self._verlet_substep(state, self.X1 * dt, compute_forces)
        state = self._verlet_substep(state, self.X0 * dt, compute_forces)
        state = self._verlet_substep(state, self.X1 * dt, compute_forces)
        return state

    def _verlet_substep(self, state, dt, compute_forces):
        q, p = state.position, state.momentum
        m = state.attributes['mass']
        forces = compute_forces(state)
        p_half = p + 0.5 * dt * forces
        q_new = q + dt * p_half / m
        temp_state = state.clone(position=q_new, momentum=p_half)
        forces_new = compute_forces(temp_state)
        p_new = p_half + 0.5 * dt * forces_new
        return state.clone(position=q_new, momentum=p_new)
```

#### 哈密顿投影的 λ 计算

辛积分器已经保证了能量有界，但仍可能存在 $O(dt^k)$ 的残余振荡。最终的哈密顿投影消除这个残余误差：

```python
def compute_lambda(q, p, E_target, hamiltonian, grad_H_q, grad_H_p):
    """
    计算拉格朗日乘子 λ，使修正后状态精确满足 H(q', p') = E_target。

    方法：一阶泰勒展开 + 牛顿迭代（通常 2-3 次迭代收敛）。

    推导：
      H(q - λ·∇H_q, p - λ·∇H_p) ≈ H(q,p) - λ·(|∇H_q|² + |∇H_p|²) = E_target

    解：
      λ₀ = (E_current - E_target) / (|∇H_q|² + |∇H_p|²)
    """
    E_current = hamiltonian(q, p)
    error = E_current - E_target

    if abs(error) < 1e-12:
        return 0.0  # 已经满足约束

    gq = grad_H_q
    gp = grad_H_p
    denominator = torch.dot(gq.flatten(), gq.flatten()) + torch.dot(gp.flatten(), gp.flatten())

    if denominator < 1e-15:
        return 0.0  # 梯度为零，无法修正（退化情况）

    lam = error / denominator

    # 可选：牛顿迭代精化（修正后重新评估误差）
    for _ in range(3):
        q_new = q - lam * gq
        p_new = p - lam * gp
        E_new = hamiltonian(q_new, p_new)
        new_error = E_new - E_target
        if abs(new_error) < 1e-12:
            break
        lam += new_error / denominator  # 一阶修正

    return lam
```

**设计原则**：辛积分器承担主要工作（保辛、保能量有界），哈密顿投影作为最终"校正器"（消除 $O(dt^k)$ 残余）。两步分工明确，避免在每一步都做昂贵的 Hessian 计算。

### 4.3 状态演化管线完整实现

将因果传播、辛积分、哈密顿投影串联为完整的前向传播：

```python
class CDABlock(torch.nn.Module):
    """
    CDA 的核心计算块：等价于 Transformer 中的一个 Transformer Block。
    输入：当前世界状态 S_t
    输出：下一时刻的世界状态 S_{t+1}
    """

    def __init__(self, world_state, mechanism_functions, hamiltonian_fn):
        super().__init__()
        self.world = world_state
        self.mechanisms = mechanism_functions  # List[CausalMechanismFunction]
        self.H = hamiltonian_fn
        self.integrator = SymplecticIntegrator()
        self.E_total = None  # 初始化时从初始状态计算

    def forward(self, dt, interventions=None):
        """
        执行一个完整的 CDA 前向传播步。

        步骤：
          1. 应用干预 do(I)
          2. 因果传播（计算所有边的作用力）
          3. 辛积分（更新位置和动量）
          4. 哈密顿投影（消除能量误差）
          5. 贝叶斯更新（传播不确定性）

        Args:
            dt: 时间步长
            interventions: 可选的干预列表 [do(entity_id, var, value), ...]

        Returns:
            next_state: S_{t+1}
        """
        state = self.world.current_state()

        # Step 1: 应用干预
        if interventions:
            state = self.apply_interventions(state, interventions)

        # Step 2+3: 因果传播 + 辛积分
        def compute_forces(s):
            """因果机制网络：汇总所有因果边的作用力"""
            total_force = torch.zeros_like(s.position)
            for edge, mech_fn in zip(self.world.edges, self.mechanisms):
                s_i = s.entities[edge.source].position
                s_j = s.entities[edge.target].position
                dist = self.compute_distance(s_i, s_j)
                delta = mech_fn(s_i, s_j, dist)
                total_force[edge.target] += delta
            return total_force

        next_state = self.integrator.step(state, dt, compute_forces)

        # Step 4: 哈密顿投影
        next_state = self.hamiltonian_project(next_state)

        # Step 5: 贝叶斯不确定性更新
        next_state = self.bayesian_update(state, next_state, dt)

        self.world.set_state(next_state)
        return next_state
```

**效果**：
- 模型**不可能**输出违反能量守恒的预测
- 不是"倾向于"守恒，是**数学上不可能**违反
- 类似于 Transformer 中 Softmax 保证输出是概率分布——这是架构级别的保证
- 辛积分器保证长时间仿真的能量有界性，哈密顿投影消除短时间步的数值误差

### 4.4 其他物理约束的嵌入

| 物理约束 | 架构实现 |
|---------|---------|
| 能量守恒 | 哈密顿投影层 |
| 动量守恒 | 机制函数的反对称约束（W_mechanical = A - A^T） |
| 热力学第二定律 | 熵增投影（只允许熵增方向的状态转移） |
| 因果方向 | 时间箭头硬编码（因果图是有向无环图的松弛版） |
| 对称性 | 等变网络层（E(n)-Equivariant, 类似 E3NN） |
| 量纲一致性 | 量纲分析模块（禁止将温度和长度相加等量纲错误） |

---

## 五、反事实推理：do-演算的架构实现

Pearl 的 do-演算是因果推理的数学基础。CDA 在架构层面原生支持它。

### 5.1 干预（Intervention）

```python
def do(self, entity_id, variable, value):
    """
    do(entity_3, "temperature", 350)
    含义：强制将实体3的温度设为350K，并切断所有指向温度的因果边
    """
    # 1. 断开指向该变量的所有因果边
    for edge in self.edges:
        if edge.target == entity_id and edge.affects == variable:
            edge.is_cut = True  # 图手术：切断因果边

    # 2. 设置变量值
    self.state[entity_id].position[variable] = value

    # 3. 传播
    # 只有被切断的边不传播，其他因果链正常传播
    # 这精确实现了 Pearl 的 do-演算的图手术
```

### 5.2 反事实（Counterfactual）

```python
def counterfactual(self, observation, hypothetical_intervention):
    """
    "如果当初我没有刹车，现在会怎样？"

    第一步：Abduction（溯因）
      从当前观测反推隐变量（系统在刹车前的完整状态）

    第二步：Action（干预）
      在反推的状态上应用假设干预（不刹车）

    第三步：Prediction（预测）
      从干预后的状态仿真到当前时刻

    返回：反事实世界状态 + 与现实状态的差异
    """
    # Step 1: 溯因 — 贝叶斯逆推理
    latent_state = self.abduct(observation)

    # Step 2: 并行仿真 — Fork
    branch = self.fork_state(latent_state)  # 创建平行世界分支

    # Step 3: 干预 + 仿真
    branch.do(**hypothetical_intervention)
    counterfactual_trajectory = branch.simulate(t_start, t_end)

    return counterfactual_trajectory
```

### 5.3 并行世界分支树

```
            当前状态 S_t
           /     |      \
      do(A)   do(B)    do(C)          ← 干预分支
        |       |        |
     simulate simulate simulate       ← 并行仿真
        |       |        |
      S_t+1^A  S_t+1^B  S_t+1^C      ← 多个可能的未来
        \       |       /
         比较、排序、选择最优策略
```

这不是比喻——这是架构级别的计算。每个分支都是真实的状态副本，仿真消耗真实的算力。但得益于现代GPU的并行能力，可以同时运行成百上千个分支。

---

## 六、学习机制：替代反向传播

Transformer 的学习方式是：收集大量数据 → 批量反向传播 → 更新参数。

CDA 的学习方式是：**在线贝叶斯更新**——持续地从观测中修正世界模型。

### 6.1 因果发现冷启动：从零构建因果图

§6.2.3 的 NOTEARS 结构学习假设已经积累了一批时序观测数据。但系统冷启动时面临经典的**鸡和蛋**问题：

- 没有因果图 → 无法做有意义的仿真 → 无法生成训练数据
- 没有数据 → NOTEARS 无法学习因果图

解决方案：**多源先验注入 + 渐进式发现**。分三个阶段逐步构建因果图。

#### 6.1.1 阶段 A：知识驱动的骨架构建

```python
class KnowledgeDrivenBootstrapper:
    """
    Phase A: 从领域知识构建因果图骨架。

    数据源（按可信度排序）：
    1. 物理方程（可信度最高）：傅里叶定律、牛顿运动方程等
    2. 工程拓扑图：P&ID 工艺流程图、电气接线图
    3. 设备手册：型号参数、连接关系
    4. 专家标注：因果关系的自然语言描述
    5. 运维日志：异常事件与修复记录
    """

    CONFIDENCE = {
        'physics_equation': 0.95,
        'topology_diagram': 0.90,
        'equipment_manual': 0.80,
        'expert_annotation': 0.60,
        'maintenance_log': 0.40,
    }

    def build_skeleton(self, knowledge_sources):
        """构建初始因果图骨架"""
        graph = CausalGraph()

        # 1. 物理方程 → 因果链
        for eq in knowledge_sources.physics_equations:
            # 例：傅里叶定律 dQ/dt = -kA(dT/dx)
            # → T_hot → 温差 → 热流 → T_cold
            chain = self._equation_to_causal_chain(eq)
            for edge in chain:
                graph.add_edge(edge, confidence=self.CONFIDENCE['physics_equation'])

        # 2. 工程拓扑 → 实体 + 连接
        if knowledge_sources.topology:
            ents, edges = self._parse_topology(knowledge_sources.topology)
            for e in ents:
                graph.add_entity(e, confidence=self.CONFIDENCE['topology_diagram'])
            for e in edges:
                graph.add_edge(e, confidence=self.CONFIDENCE['topology_diagram'])

        # 3. 文本挖掘 → 候选边（低置信度）
        for doc in knowledge_sources.text_documents:
            hints = self._extract_causal_hints(doc)
            for h in hints:
                graph.add_candidate_edge(
                    h.source, h.target,
                    confidence=h.raw_confidence * 0.6,
                )

        return graph
```

#### 6.1.2 阶段 B：数据驱动的骨架精化

骨架图提供了因果结构的**先验**。当少量观测数据积累后，用 NOTEARS 在骨架基础上精化——关键区别：**骨架边不容易被删除，非骨架边不容易被添加**。

```python
class SkeletonGuidedNOTEARS:
    """
    在骨架图约束下的 NOTEARS 因果发现。

    与标准 NOTEARS 的区别：
    - 骨架边：初始 W 值较大，先验精度高 → 不易被删除
    - 非骨架边：初始 W 值接近零，先验精度低 → 不易被添加
    - 额外损失项：骨架保持的 L2 先验正则化
    """

    def refine(self, skeleton, data_matrix, max_iter=50):
        """
        在骨架基础上精化因果结构。

        Args:
            skeleton: 骨架因果图（含边的置信度）
            data_matrix: (T, N) 时序观测数据
            max_iter: 增广拉格朗日法的最大迭代次数
        """
        N = data_matrix.shape[1]

        # 初始化 W 和先验精度 Λ
        W = torch.zeros(N, N, requires_grad=True)
        prior_precision = torch.ones(N, N)
        W_target = torch.zeros(N, N)

        for edge in skeleton.edges:
            i, j = edge.source, edge.target
            W[i, j] = edge.strength
            W_target[i, j] = edge.strength
            # 置信度越高 → 先验精度越高 → 该边越不容易被修改
            prior_precision[i, j] = 50.0 / (edge.confidence + 1e-8)

        X = data_matrix
        lam, rho = 1.0, 1.0

        for _ in range(max_iter):
            rho = min(rho * 1.1, 1e+6)
            W_sig = torch.sigmoid(W)

            # 标准损失
            loss_l2 = 0.5 / X.shape[0] * ((X - X @ W_sig) ** 2).sum()
            E = torch.matrix_exp(W_sig * W_sig)
            h = torch.trace(E) - N
            loss_dag = lam * h + 0.5 * rho * h ** 2

            # 骨架先验：将 W 拉向骨架结构
            loss_prior = 0.5 * (
                prior_precision * (W_sig - W_target) ** 2
            ).sum()

            loss = loss_l2 + loss_dag + loss_prior
            loss.backward()

            with torch.no_grad():
                W -= 1e-2 * W.grad
                W.grad.zero_()
                lam += rho * h.item()

            if h.abs() < 1e-6:
                break

        refined = (torch.sigmoid(W) > 0.3).float()
        refined.fill_diagonal_(0.0)
        return refined
```

#### 6.1.3 阶段 C：主动因果实验设计

当骨架 + 数据仍不足以确定某些边的存在性或方向时，系统可以**主动设计干预实验**来消除不确定性：

```python
class ActiveCausalExplorer:
    """
    主动因果实验设计：选择最有信息量的干预来消除结构不确定性。

    选择标准：期望信息增益 (Expected Information Gain)
      EIG(do(X)) = H(G|D) - E_x[H(G|D ∪ {do(X=x), Y})]

    简化实现：用贝叶斯因果图后验的方差作为不确定度代理。
    """

    def plan_next_experiment(self, graph_uncertainty, intervention_cost_fn):
        """
        选择下一个干预实验。

        Args:
            graph_uncertainty: Dict[(i,j), float] 每条候选边的不确定度
            intervention_cost_fn: Callable(target_entity) → 实验成本

        Returns:
            experiment: Dict 含目标实体、干预方式、期望信息增益
        """
        candidates = []
        for (i, j), unc in graph_uncertainty.items():
            if unc < self.min_uncertainty:
                continue
            cost = intervention_cost_fn(j)
            candidates.append({
                'edge': (i, j),
                'gain': unc,
                'cost': cost,
                'efficiency': unc / (cost + 1e-8),
            })

        candidates.sort(key=lambda c: c['efficiency'], reverse=True)

        if not candidates:
            return None

        best = candidates[0]
        return {
            'target_entity': best['edge'][1],
            'intervention_type': 'perturbation',
            'magnitude': self._suggest_perturbation(best['edge']),
            'expected_info_gain': best['gain'],
            'estimated_cost': best['cost'],
        }
```

**冷启动的渐进式流程**：

```
Phase A: 知识注入
  物理方程 + 工程图纸 + 专家知识
  → 因果图骨架（高置信度边 + 低置信度候选边）
  → 覆盖 ~70% 的真实因果结构

Phase B: 数据精化
  少量传感器数据（数小时到数天）
  → SkeletonGuidedNOTEARS 精化骨架
  → 覆盖 ~90% 的因果结构

Phase C: 主动探索
  针对剩余 ~10% 不确定边
  → 设计干预实验
  → 逐步消除结构不确定性

Phase D: 持续在线更新（§6.2.3 已覆盖）
  新数据持续流入
  → NOTEARS 增量更新因果图
  → 结构演化跟踪
```

### 6.2 参数更新的三层结构

```
Level 1: 信念更新（实时，毫秒级）
  观测到来 → 更新实体状态的贝叶斯后验
  b_i(t+1) = P(s_i | observation, b_i(t), model)
  不改变模型参数，只改变对当前状态的估计

Level 2: 机制学习（在线，秒到分钟级）
  如果信念的预测误差持续偏高：
  → 更新因果机制函数的参数 θ_ij
  → 使用贝叶斯在线学习（不是 SGD）
  → 机制函数的先验来自物理约束（热力学定律等）

Level 3: 结构学习（慢，小时到天级）
  如果某个实体反复出现"无法解释的观测"：
  → 触发因果发现算法
  → 可能发现新的因果边
  → 可能合并/分裂实体
  → 可能引入新的实体类型
  这是"学习物理定律"的AI版本
```

#### 6.2.1 Level 1：贝叶斯信念更新的具体实现

Level 1 不改变模型参数，只更新对当前实体状态的估计。采用**扩展卡尔曼滤波（EKF）**作为标准实现：

```python
class BayesianBeliefTracker:
    """
    Level 1：贝叶斯信念在线追踪。

    每个实体维护一个高斯信念 b_i ~ N(μ_i, Σ_i)：
    - μ_i：当前状态的最佳估计
    - Σ_i：估计的不确定性协方差

    更新公式（卡尔曼滤波）：
      预测步:  μ⁻ = f(μ, dt),  Σ⁻ = J·Σ·J^T + Q
      更新步:  K = Σ⁻·H^T·(H·Σ⁻·H^T + R)⁻¹    （卡尔曼增益）
              μ  = μ⁻ + K·(z - h(μ⁻))           （后验均值）
              Σ  = (I - K·H)·Σ⁻                   （后验协方差）
    """

    def __init__(self, num_entities, state_dim):
        self.mu = torch.zeros(num_entities, state_dim)    # 均值
        self.Sigma = torch.eye(state_dim).unsqueeze(0).repeat(num_entities, 1, 1)  # 协方差
        self.Q = 1e-4 * torch.eye(state_dim)  # 过程噪声
        self.R = 1e-2 * torch.eye(state_dim)  # 观测噪声

    def predict(self, dt):
        """
        预测步：使用因果机制函数预测下一时刻状态。

        注：完整实现中应传入因果机制网络的雅可比矩阵。
        此处使用恒等近似（状态不变），实际部署时替换为真实动力学函数。
        仅过程噪声 Q 导致不确定性增长。
        """
        N, d = self.mu.shape
        # 恒等雅可比：J = I（每个实体状态不变的近似）
        J = torch.eye(d).unsqueeze(0).expand(N, -1, -1)  # (N, d, d)
        self.Sigma = J @ self.Sigma @ J.transpose(-1, -2) + self.Q
        return self.mu, self.Sigma

    def update(self, observation_matrix, observation):
        """
        更新步：用观测校正预测。

        Args:
            observation_matrix: H，观测矩阵（将状态映射到观测空间）
            observation: z，实际观测值
        """
        H = observation_matrix
        # 卡尔曼增益
        S = H @ self.Sigma @ H.transpose(-1, -2) + self.R
        K = self.Sigma @ H.transpose(-1, -2) @ torch.inverse(S)
        # 状态更新
        innovation = observation - H @ self.mu
        self.mu = self.mu + K @ innovation
        self.Sigma = (torch.eye(self.Sigma.shape[-1]) - K @ H) @ self.Sigma
```

#### 6.2.2 Level 2：机制函数的在线贝叶斯学习

Level 2 在信念更新发现系统性偏差时触发，更新机制函数的参数 θ。采用**在线拉普拉斯近似（Online Laplace Approximation）**：

```python
class OnlineMechanismLearner:
    """
    Level 2：因果机制函数参数的在线贝叶斯学习。

    核心思想：
    - 每个机制函数的参数 θ_ij 有一个后验分布 q(θ) ≈ N(θ_MAP, Σ_θ)
    - 先验来自物理约束（如热传导系数的物理范围）
    - 观测到来时，通过贝叶斯规则更新后验

    选择 Online Laplace Approximation 的理由：
    1. 可微分，与 PyTorch 前向传播无缝集成
    2. 不需要维护完整的后验分布（只需均值和协方差）
    3. 天然提供不确定性量化
    4. 天然避免灾难性遗忘（旧知识编码在先验中）
    """

    def __init__(self, mechanism_fn, prior_std=0.1):
        self.mechanism = mechanism_fn
        # 后验参数：均值 = 当前参数值，协方差 = 先验协方差
        self.theta_mean = {name: param.clone() for name, param in mechanism_fn.named_parameters()}
        self.theta_precision = {name: torch.ones_like(param) / prior_std**2
                                for name, param in mechanism_fn.named_parameters()}

    def should_update(self, belief_tracker, entity_i, entity_j, threshold=2.0):
        """
        判断是否需要触发机制学习。

        条件：信念的预测误差持续超过阈值（标准差倍数）
        """
        s_i = belief_tracker.mu[entity_i]
        s_j = belief_tracker.mu[entity_j]
        # 使用状态差异近似因果距离
        distance = (s_i - s_j).norm().unsqueeze(0)
        prediction = self.mechanism(s_i, s_j, distance)
        error = prediction - belief_tracker.mu[entity_i]
        # 标准化的误差（马氏距离）
        sigma = torch.sqrt(torch.diag(belief_tracker.Sigma[entity_i]))
        normalized_error = (error / (sigma + 1e-8)).abs()
        return normalized_error.max() > threshold

    def update(self, source_states, target_states, distances, observed_deltas, lr=1e-3):
        """
        在线更新机制函数参数。

        方法：ELBO 最大化（Evidence Lower Bound）
        ELBO = E_q[log p(obs|θ)] - KL(q(θ) || p(θ))

        Args:
            source_states: 源实体状态批次 (batch, state_dim)
            target_states: 目标实体状态批次 (batch, state_dim)
            distances: 因果距离批次 (batch, 1)
            observed_deltas: 实际观测到的状态变化量 (batch, state_dim)
            lr: 学习率
        """
        optimizer = torch.optim.SGD(self.mechanism.parameters(), lr=lr)

        # 前向传播：机制函数预测状态变化量
        predictions = self.mechanism(source_states, target_states, distances)
        # 负对数似然（高斯假设）
        nll = 0.5 * ((predictions - observed_deltas) ** 2).mean()

        # KL 散度正则化（防止偏离先验太远）
        kl = 0.0
        for name, param in self.mechanism.named_parameters():
            kl += 0.5 * self.theta_precision[name] * (param - self.theta_mean[name]) ** 2
        kl = kl.mean()

        # 总损失 = 似然 + KL（即 ELBO 的负值）
        loss = nll + kl

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 更新后验估计
        for name, param in self.mechanism.named_parameters():
            self.theta_mean[name] = param.detach().clone()

        return {'loss': loss.item(), 'nll': nll.item(), 'kl': kl.item()}
```

**在线学习的流控逻辑**：

```python
class LearningController:
    """
    三层学习的时间尺度控制器。
    决定当前时刻应该触发哪个层级的学习。
    """

    def __init__(self, belief_tracker, mechanism_learner, structure_learner):
        self.belief = belief_tracker          # Level 1
        self.mechanism = mechanism_learner     # Level 2
        self.structure = structure_learner      # Level 3

        # 滑动窗口统计
        self.prediction_errors = defaultdict(list)
        self.unexplained_residuals = defaultdict(list)

    def on_observation(self, observation, dt):
        """观测到来时的学习流程"""
        # Level 1：始终执行（毫秒级）
        self.belief.predict(dt)
        self.belief.update(observation.H, observation.z)

        # 记录预测误差
        for entity_id in observation.entities:
            error = self._compute_prediction_error(entity_id)
            self.prediction_errors[entity_id].append(error)

        # Level 2：周期性检查（每 100 步）
        if self.step_count % 100 == 0:
            for edge in self.world.edges:
                if self.mechanism.should_update(self.belief, edge.source, edge.target):
                    history = self._get_recent_history(edge, window=50)
                    self.mechanism.update(
                        history.source_states, history.target_states,
                        history.distances, history.observed_deltas
                    )

        # Level 3：慢速检查（每 10000 步）
        if self.step_count % 10000 == 0:
            self._check_structure_learning()

        self.step_count += 1
```

#### 6.2.3 Level 3：因果结构学习的具体实现

Level 3 是最慢、最高层级的学习——改变因果图本身。采用**基于 NOTEARS 的连续松弛方法**，将离散的因果发现问题转化为连续优化问题：

```python
class CausalStructureLearner:
    """
    Level 3：因果图结构在线学习。

    问题：给定实体间的时序观测数据，发现因果图的结构。

    方法：NOTEARS (Non-combinatorial Optimization via Trace Exponential and Augmented lagRangian for Structure learning)
    - 将 DAG 约束松弛为连续约束：h(W) = tr(e^{W∘W}) - d = 0
    - 使用增广拉格朗日法求解

    优势：
    - 可微分，支持 GPU 加速
    - 可以输出因果强度的连续值（用于 α_ij 的初始化）
    - 渐进式：可以在现有图基础上增量修改
    """

    def __init__(self, num_entities, state_dim):
        self.num_entities = num_entities
        self.state_dim = state_dim

        # 因果邻接矩阵（连续松弛）
        # W_adj[i,j] > 0 表示 j → i 的因果强度
        self.W_adj = torch.nn.Parameter(torch.zeros(num_entities, num_entities))

        # NOTEARS 约束的拉格朗日乘子
        self.lam = torch.tensor(1.0)   # 拉格朗日乘子
        self.rho = torch.tensor(1.0)   # 惩罚系数

    def notears_constraint(self, W):
        """NOTEARS 的无环约束：h(W) = tr(e^{W∘W}) - d = 0"""
        d = W.shape[0]
        E = torch.matrix_exp(W * W)  # 逐元素平方后的矩阵指数
        return torch.trace(E) - d

    def learn_structure(self, data_matrix, max_iter=100):
        """
        从时序数据中学习因果结构。

        Args:
            data_matrix: (T, num_entities, state_dim) 的时序数据
            max_iter: 增广拉格朗日法的最大迭代次数

        Returns:
            causal_graph: 学到的因果邻接矩阵
        """
        X = data_matrix.mean(dim=-1)  # 降维到 (T, num_entities)

        for iteration in range(max_iter):
            self.rho = min(self.rho * 1.1, 1e+6)  # 逐步增大惩罚

            # 最小化：最小二乘损失 + DAG 约束
            W = torch.sigmoid(self.W_adj)  # 映射到 [0,1]

            # 最小二乘：X ≈ X · W
            loss_l2 = 0.5 / X.shape[0] * ((X - X @ W) ** 2).sum()

            # NOTEARS 约束（增广拉格朗日）
            h = self.notears_constraint(W)
            loss_dag = self.lam * h + 0.5 * self.rho * h ** 2

            loss = loss_l2 + loss_dag

            # 梯度更新
            loss.backward()
            with torch.no_grad():
                self.W_adj -= 1e-2 * self.W_adj.grad
                self.W_adj.grad.zero_()
                # 更新拉格朗日乘子
                self.lam += self.rho * h.item()

            if h.abs() < 1e-6:
                break

        # 阈值化得到离散因果图
        causal_graph = (torch.sigmoid(self.W_adj) > 0.3).float()
        # 对角线置零（排除自环）
        causal_graph.fill_diagonal_(0.0)

        return causal_graph
```

#### 6.2.4 结构学习的触发与图更新

```python
class StructureUpdateController:
    """
    决定何时以及如何修改因果图结构。
    """

    def __init__(self, world, structure_learner):
        self.world = world
        self.learner = structure_learner
        self.anomaly_counter = {}  # 每个实体的异常计数
        self.anomaly_threshold = 5  # 连续异常次数阈值

    def record_residual(self, entity_id, residual):
        """
        记录实体的不可解释残差。

        如果残差持续偏高（模型无法解释的观测），标记为异常。
        """
        if entity_id not in self.anomaly_counter:
            self.anomaly_counter[entity_id] = 0

        if residual > self.anomaly_threshold:
            self.anomaly_counter[entity_id] += 1
        else:
            self.anomaly_counter[entity_id] = max(0, self.anomaly_counter[entity_id] - 1)

    def should_trigger_learning(self):
        """判断是否需要触发结构学习"""
        return any(count > self.anomaly_threshold
                   for count in self.anomaly_counter.values())

    def learn_and_update(self, data_buffer):
        """
        执行结构学习并更新因果图。

        三种可能的操作：
        1. 添加新因果边（发现新的因果关系）
        2. 删除旧因果边（已有的因果关系不再成立）
        3. 合并/分裂实体（粒度调整）
        """
        old_adj = self.world.get_adjacency_matrix()
        new_adj = self.learner.learn_structure(data_buffer.get_matrix())

        # 差分：比较新旧图
        added_edges = (new_adj - old_adj) > 0.5   # 新增的因果边
        removed_edges = (old_adj - new_adj) > 0.5  # 移除的因果边

        # 应用图变更
        for i in range(self.world.num_entities):
            for j in range(self.world.num_entities):
                if added_edges[i, j]:
                    self.world.add_edge(CausalEdge(
                        source=j, target=i,
                        mechanism_type=self._infer_type(i, j),
                        strength=new_adj[i, j].item(),
                    ))
                elif removed_edges[i, j]:
                    self.world.remove_edge(source=j, target=i)
```

### 6.3 与反向传播的对比

| | 反向传播 (BP) | CDA贝叶斯更新 |
|--|-------------|--------------|
| 学习时机 | 离线，批量 | 在线，实时 |
| 目标函数 | 交叉熵损失 | 仿真轨迹的贝叶斯证据 |
| 梯度来源 | 标签数据 | 物理观测（ground truth） |
| 参数约束 | 无（或正则化） | 物理定律（硬约束） |
| 不确定性 | 无 | 每个参数都有后验分布 |
| 灾难性遗忘 | 有 | 无（在线贝叶斯天然避免） |
| 数据需求 | 海量 | 少量（物理约束 = 强先验） |

---

## 七、多尺度聚合：统计力学的启发

这是 CDA 对应 Transformer 中"层次化表示"的等价物，但物理意义更清晰。

### 7.1 粗粒化（Coarse-Graining）

```
微观尺度（10^6 粒子）:
  每个粒子是一个 Entity，有完整的状态向量
  粒子间通过分子间力因果连接
  → 可以仿真，但计算代价极高

中观尺度（10^3 集团）:
  将空间相近、状态相似的粒子聚合成一个"有效实体"
  有效实体的状态 = 集团的统计量（平均位置、总动量、温度、压力）
  有效实体间的因果机制 = 重正化后的宏观力
  → 统计力学的重正化群（RG）思想

宏观尺度（10 个子系统）:
  进一步聚合：整个房间是一个实体（状态=温度、湿度、人数）
  房间间的因果机制 = 传热、气流、人员流动
  → 工程热力学的尺度
```

### 7.1.1 粗粒化算法：信息瓶颈驱动的实体聚合

粗粒化的核心问题：何时聚合？怎么聚合？聚合后丢失的信息怎么量化？

```python
class CoarseGrainingEngine:
    """
    信息瓶颈驱动的粗粒化算法。

    核心思想：
    - 最大化聚合后实体对观测的预测力 I(S_macro; Observation)
    - 最小化聚合导致的信息损失 I(S_macro; S_micro)
    - 即：信息瓶颈 T(S_micro → S_macro)

    选择信息瓶颈的理由：
    1. 信息论框架自然量化"不可逆信息损失"
    2. 自动确定最优聚合粒度（不需要人工设定阈值）
    3. 与 CER 的"封装信息损失"概念一致
    """

    def __init__(self, world, compression_rate=0.1):
        """
        Args:
            world: 当前世界状态
            compression_rate: 压缩率（宏观实体数 / 微观实体数）
        """
        self.world = world
        self.compression_rate = compression_rate

    def find_clusters(self, states, observations, target_clusters=None):
        """
        基于信息瓶颈的实体聚类。

        算法：
        1. 计算实体间的互信息矩阵 MI(i,j) = I(s_i, s_j; observation)
        2. 用谱聚类将高 MI 的实体聚为一组
        3. 每组成为一个"有效实体"

        Args:
            states: (N, state_dim) 所有实体的状态
            observations: (N, obs_dim) 所有实体的观测
            target_clusters: 目标聚类数（默认由压缩率决定）

        Returns:
            clusters: 聚类标签 [0, 1, 2, ...]
        """
        N = states.shape[0]
        if target_clusters is None:
            target_clusters = max(1, int(N * self.compression_rate))

        # 步骤 1：计算状态相似度矩阵（高斯核）
        sigma = self._estimate_kernel_width(states)
        K = torch.exp(-torch.cdist(states, states) ** 2 / (2 * sigma ** 2))

        # 步骤 2：结合观测相关性加权
        obs_corr = torch.corrcoef(observations)  # 观测相关矩阵
        combined = K * (1 + torch.abs(obs_corr))  # 融合空间邻近 + 行为相似

        # 步骤 3：谱聚类
        D = torch.diag(combined.sum(dim=1))
        L = D - combined  # 拉普拉斯矩阵
        eigenvalues, eigenvectors = torch.linalg.eigh(L)

        # 取最小的 k 个非零特征值对应的特征向量（跳过第 1 个零特征值）
        selected = eigenvectors[:, 1:target_clusters+1]

        # K-means 在特征空间中聚类
        clusters = self._kmeans(selected, target_clusters)

        return clusters

    def aggregate_entities(self, states, clusters, momenta, attributes):
        """
        将微观实体聚合为宏观有效实体。

        聚合规则（物理意义明确）：
        - 位置（广延量）：加权平均 → q_macro = Σ w_i · q_i / Σ w_i
        - 动量（广延量）：直接求和 → p_macro = Σ p_i（动量守恒！）
        - 质量（广延量）：直接求和 → m_macro = Σ m_i
        - 温度（强度量）：质量加权平均 → T_macro = Σ m_i·T_i / Σ m_i
        - 不确定性：协方差求和 → Σ_macro = Σ Σ_i（不确定性叠加）
        """
        unique_clusters = torch.unique(clusters)
        macro_entities = {}

        for c in unique_clusters:
            mask = (clusters == c)
            n = mask.sum().item()

            # 广延量求和
            macro_q = (states[mask] * attributes[mask, 0:1]).sum(dim=0) / attributes[mask].sum()
            macro_p = momenta[mask].sum(dim=0)
            macro_mass = attributes[mask, 0].sum()

            # 强度量加权平均
            macro_temperature = (attributes[mask, 1] * states[mask, 1]).sum() / attributes[mask, 1].sum()

            # 不确定性叠加（独立假设下的协方差求和）
            macro_sigma = None  # 需要从 belief tracker 中获取

            macro_entities[c.item()] = EntityState(
                position=macro_q,
                momentum=macro_p,
                attributes=torch.tensor([macro_mass, macro_temperature]),
            )

        return macro_entities

    def _estimate_kernel_width(self, X):
        """自适应核宽估计：中位数启发式"""
        dists = torch.cdist(X, X)
        return torch.median(dists[dists > 0]).item()

    def _kmeans(self, data, k, max_iter=20):
        """简化 K-means（单次运行）"""
        indices = torch.randperm(data.shape[0])[:k]
        centers = data[indices]
        for _ in range(max_iter):
            dists = torch.cdist(data, centers)
            labels = dists.argmin(dim=1)
            for c in range(k):
                mask = labels == c
                if mask.sum() > 0:
                    centers[c] = data[mask].mean(dim=0)
        return labels
```

### 7.1.2 重正化：粗粒化后的机制函数更新

粗粒化不仅改变实体粒度，还必须重新计算实体间的因果机制函数参数。这一步对应统计力学中的**重正化群变换**：

```python
class RenormalizationOperator:
    """
    重正化算子：将微观因果机制映射为宏观因果机制。

    核心思想：
    微观因果链 a→b→c→d 在粗粒化后变为 宏观 A→B 的有效机制。
    f_AB = R(f_ab, f_bc, f_cd)，其中 R 是重正化算子。

    方法：矩阵路径求和（类似重正化微扰论）
    对于串联因果链：F = f_1 + f_2 + f_1·f_2 + ...（Neumann 级数截断）
    """

    def renormalize_edge(self, micro_graph, source_cluster, target_cluster):
        """
        计算两个宏观实体间的有效因果机制函数。

        Args:
            micro_graph: 微观因果图
            source_cluster: 源宏实体包含的微观实体列表
            target_cluster: 目标宏实体包含的微观实体列表

        Returns:
            effective_mechanism: 有效因果机制函数
            encapsulation_loss: 封装导致的信息损失量
        """
        # 步骤 1：枚举所有微观因果路径
        paths = self._enumerate_paths(micro_graph, source_cluster, target_cluster, max_length=3)

        # 步骤 2：路径求和（Neumann 级数截断到二阶）
        total_effect = torch.zeros(self.macro_state_dim, self.macro_state_dim)
        for path in paths:
            path_effect = self._compute_path_effect(micro_graph, path)
            total_effect += path_effect

        # 步骤 3：归一化
        avg_effect = total_effect / max(len(paths), 1)

        # 步骤 4：估计信息损失
        # 封装损失 = 微观因果链的总信息熵 - 宏观有效机制的熵
        micro_info = self._estimate_path_entropy(paths)
        macro_info = self._estimate_effect_entropy(avg_effect)
        encapsulation_loss = micro_info - macro_info  # 总是 ≥ 0

        # 步骤 5：构建有效机制函数
        effective_mechanism = self._build_effective_mechanism(avg_effect)

        return effective_mechanism, encapsulation_loss

    def _enumerate_paths(self, graph, sources, targets, max_length):
        """BFS 枚举从源集群到目标集群的所有因果路径（限制长度）"""
        paths = []
        from collections import deque
        queue = deque([(s, [s]) for s in sources])
        while queue:
            current, path = queue.popleft()
            if len(path) > max_length + 1:
                continue
            if current in targets and len(path) > 1:
                paths.append(path)
            for edge in graph.edges_from(current):
                if edge.target not in path:  # 避免循环
                    queue.append((edge.target, path + [edge.target]))
        return paths

    def _compute_path_effect(self, graph, path):
        """
        计算单条因果路径的总效应。

        对于路径 a→b→c：
        effect = f_bc(f_ab(s_a), s_b) → 沿路径的复合函数

        线性近似：effect ≈ W_bc · W_ab（矩阵乘积）
        """
        effect = torch.eye(self.micro_state_dim)
        for i in range(len(path) - 1):
            edge = graph.get_edge(path[i], path[i+1])
            effect = edge.mechanism.get_W() @ effect  # 矩阵连乘
        return effect[:self.macro_state_dim, :self.macro_state_dim]
```

### 7.2 自适应尺度选择

```python
class MultiScaleEngine:
    """
    根据任务的精度需求和计算预算，自动选择仿真尺度。

    问"整栋楼的能耗趋势？"→ 宏观尺度（快、粗）
    问"3楼东侧管道的温度分布？"→ 中观尺度（中速、中精度）
    问"管道焊缝处的热应力集中？"→ 微观尺度（慢、高精度）
    """

    def __init__(self, world, coarse_graining_engine):
        self.world = world
        self.cg_engine = coarse_graining_engine
        self.current_scale = 0  # 0=宏观, 1=中观, 2=微观

    def select_scale(self, query, budget):
        resolution_required = self.parse_query_granularity(query)
        compute_available = budget

        # 类似 Transformer 中的注意力头选择，
        # 但这里选择的是物理仿真的空间/时间分辨率
        scale = self.estimate_optimal_scale(resolution_required, compute_available)
        return scale

    def parse_query_granularity(self, query):
        """
        从查询中推断所需的精度级别。

        启发式规则（可由 LLM Layer 5 增强）：
        - "趋势""总体""平均" → 低精度（宏观）
        - "分布""区域""局部" → 中精度（中观）
        - "精确""应力""焊缝""微观" → 高精度（微观）
        """
        low_res_keywords = ['趋势', '总体', '平均', '能耗', '概览']
        mid_res_keywords = ['分布', '区域', '局部', '楼层', '房间']
        high_res_keywords = ['精确', '应力', '焊缝', '微观', '详细']

        score = 0
        for kw in high_res_keywords:
            if kw in query:
                score += 2
        for kw in mid_res_keywords:
            if kw in query:
                score += 1
        for kw in low_res_keywords:
            if kw in query:
                score -= 1

        return max(0, min(score, 2))  # 0, 1, 2

    def estimate_optimal_scale(self, resolution_required, compute_available):
        """
        最优尺度估计：精度需求 vs 算力预算的 tradeoff。

        本质是一个约束优化：
          max 预测精度(resolution)
          s.t. 计算量(resolution) ≤ compute_available

        解法：二分搜索 + 成本模型
        """
        # 成本模型：O(N_entities * N_edges * T_steps) per scale level
        cost_model = [100, 1e4, 1e6]  # 宏观/中观/微观 的相对计算量

        best_scale = 0
        for s in range(3):
            if cost_model[s] <= compute_available and s >= resolution_required:
                best_scale = s

        # 如果算力不足以支持查询精度，选择算力允许的最高精度
        for s in range(2, -1, -1):
            if cost_model[s] <= compute_available:
                best_scale = max(best_scale, s)
                break

        return best_scale

    def switch_scale(self, target_scale):
        """
        在尺度间切换。

        细→粗：执行粗粒化（压缩）
        粗→细：执行条件采样（展开）
        """
        if target_scale > self.current_scale:
            # 展开：从粗粒度展开到细粒度
            self._refine(target_scale)
        elif target_scale < self.current_scale:
            # 压缩：从细粒度聚合到粗粒度
            self._coarsen(target_scale)
        self.current_scale = target_scale

    def _coarsen(self, target_scale):
        """粗粒化：聚合实体"""
        states = self.world.get_all_states()
        # 尺度映射：scale 0=宏观(最压缩) → scale 2=微观(不压缩)
        # target_scale 越小 → 压缩率越高 → 目标聚类数越少
        compression = 0.3 ** (2 - target_scale)  # 0: ~9%, 1: ~30%, 2: 100%
        target_clusters = max(1, int(self.world.num_entities * compression))
        clusters = self.cg_engine.find_clusters(
            states, self.world.get_all_observations(),
            target_clusters=target_clusters
        )
        self.world.apply_coarse_graining(clusters)

    def _refine(self, target_scale):
        """细粒化：展开实体（需要存储微观状态历史）"""
        # 从缓存的微观状态恢复
        micro_state = self.world.cached_micro_states[target_scale]
        self.world.restore_state(micro_state)
```

---

## 八、因果封装递归（Causal Encapsulation Recursion, CER）

这是 CDA 的拓扑结构原则——回答"系统的整体形态是什么样的"。

### 8.1 核心问题：需要递归嵌套吗？

**需要。** 因为物理世界本身就是递归嵌套的：

```
宇宙 → 银河系 → 恒星系 → 行星 → 大气层 → 城市 → 建筑 → HVAC → 压缩机 → 活塞 → 分子
```

每一层都是一个"输入→处理→输出"的因果系统：
- 压缩机的**输入**是电能和冷媒状态，**输出**是压缩后的冷媒
- HVAC 系统不关心活塞怎么动，只把压缩机当成一个因果黑盒
- 城市不关心建筑内部空调，只关心建筑的热负荷

**但不是传统意义上的"纯递归"。** 传统递归（如递归神经网络、嵌套函数调用）假设每一层结构同构。物理世界不满足这个假设。

### 8.2 纯递归 vs. 因果封装递归

| 特征 | 纯递归（如 RNN / 递归NN） | 因果封装递归（CER） |
|------|------------------------|-------------------|
| 每层结构 | 同构（相同计算层重复） | 异构（每层物理机制不同） |
| 信息损失 | 无（或可忽略） | 有（粗粒化必然丢失微观信息） |
| 层间耦合 | 单向（高层调用低层） | **双向**（宏观约束微观，微观涌现宏观） |
| 嵌套深度 | 预设的、固定的 | **自适应**的、动态的 |
| 终止条件 | 固定深度 | 由查询精度 + 计算预算决定 |
| 封装边界 | 程序员定义 | **物理系统自身定义**（热力学边界、力学连接点等） |

### 8.3 CER 的形式化定义

```python
class CausalSubsystem:
    """
    一个因果封装递归单元 = 一个具有明确边界的因果子系统。
    它对外暴露接口（输入/输出），隐藏内部动力学。
    """

    # ---- 对外接口 ----
    inputs:   Dict[str, StateVar]   # 来自外部世界的因果输入（外力、边界条件...）
    outputs:  Dict[str, StateVar]   # 对外部世界的因果输出（热流、力、信号...）

    # ---- 封装内部 ----
    internals: EntityStateGraph     # 内部实体-状态因果图（对外不可见）
    sub_systems: List[CausalSubsystem]  # 内部嵌套的子子系统（递归！）

    # ---- 封装元数据 ----
    boundary: PhysicalBoundary      # 物理边界（热力学边界、结构连接点等）
    encapsulation_loss: float       # 封装导致的信息损失（粗粒化不可逆性）
    timescale: float                # 该尺度的特征时间（决定了仿真步长）

    # ---- 核心方法 ----
    def forward(self, external_inputs, dt):
        """
        接收外部输入 → 内部仿真 → 产生外部输出
        这就是"输入→处理→输出"的IPO结构
        """
        # 1. 将外部输入映射到边界条件
        self.apply_boundary_conditions(external_inputs)

        # 2. 内部仿真（可以选择展开子系统的细节，也可以用粗粒化模型）
        if self.need_high_resolution():
            # 展开递归：使用子系统的详细模型
            for sub in self.sub_systems:
                sub_output = sub.forward(sub.get_inputs_from_parent(), dt)
            self.internals = self.aggregate_sub_systems()
        else:
            # 不展开：使用粗粒化的宏观模型
            self.internals.evolve(dt, use_macro_model=True)

        # 3. 从内部状态计算外部输出
        return self.compute_boundary_outputs()
```

### 8.4 递归的三个关键机制

**机制一：因果封装（Causal Encapsulation）**

```
当你在宏观尺度观察一个子系统时：
  - 你看到的是它的边界行为（输入→输出映射）
  - 你看不到它的内部动力学

类比：
  - 电路设计中的"黑盒"：一个芯片的引脚定义就是它的因果接口
  - 热力学中的"控制体积"：你只关心穿过边界的热流和功
  - 控制论中的"传递函数"：系统的输入输出关系，内部状态被消去

数学表达：
  高层因果边: A ──→ B（宏观机制函数 f_AB）
  展开后: A ──→ [a1→a2→a3→...] ──→ B（内部因果链）

  f_AB = Σ 微观因果链的粗粒化等价
  信息损失: I(f_AB) < I(微观因果链)  ← 不可逆的信息压缩
```

**机制二：尺度自适应（Scale Adaptation）**

```
系统根据两个因素动态决定递归深度：

1. 查询精度要求（精度拉力）
   "整栋楼能耗？" → 深度 1（每栋楼 = 1 个实体）
   "3楼温度？"    → 深度 2（每层楼 = 1 个实体）
   "管道焊缝应力？"→ 深度 5+（材料微观结构）

2. 计算预算约束（算力推力）
   算力充足 → 展开更多层
   算力紧张 → 收缩到更粗的粒度

这本质上是一个**最优计算分配问题**：
  max 预测精度
  s.t. 总计算量 ≤ 算力预算

解法：类似于多重网格法（Multigrid Method）的V-cycle
```

**机制三：双向因果耦合（Bidirectional Causal Coupling）**

```
传统递归：  上层调用下层 → 单向
物理因果：  上层约束下层 AND 下层涌现上层 → 双向

具体例子（应力腐蚀开裂）：
  宏观应力 → 微观位错运动 → 微观化学反应 → 宏观裂纹扩展
  ↑                                                    |
  └──────────── 反馈回路 ──────────────────────────────┘

这不是简单的自上而下调用，而是跨尺度的因果循环。
CDA 用"慢变量约束快变量 + 快变量修正慢变量参数"来处理：

  慢尺度（宏观）:
    状态: {σ_stress, T_global, ...}
    → 约束快尺度的边界条件

  快尺度（微观）:
    状态: {dislocations, chemical_potential, ...}
    → 在宏观约束下仿真
    → 输出: 有效参数（如有效裂纹扩展速率 da/dN）
    → 反馈修正慢尺度模型

  这就是统计力学中"粗粒化 → 重正化 → 有效理论"的思想
```

### 8.5 CER 的可视化：城市能源系统的递归展开

```
Layer 0: 城市（1个实体）
  状态: {总能耗, 总碳排放, 人口, GDP, 气温}
  ┌────────────────────────────────────────────┐
  │  City: E_total, C_total, pop, GDP, T_avg   │
  │  输入: 电网供电, 天气, 政策                   │
  │  输出: 能耗, 排放, 热岛效应                   │
  └───────────────┬────────────────────────────┘
                  │ 需要更高精度？→ 展开 Layer 1
                  ▼

Layer 1: 建筑群（100个实体）
  状态: 每栋建筑 {面积, 层数, 用途, 能耗, HVAC类型}
  ┌────────────────────────────────────────────┐
  │  Building_1  │  Building_2  │ ... │ B_100  │
  │  E_1, T_1    │  E_2, T_2    │     │        │
  └──────┬───────┴──────┬───────┴─────┴────────┘
         │ 需要更高精度？→ 展开 Layer 2
         ▼

Layer 2: HVAC子系统（每栋建筑3-5个）
  状态: {压缩机功率, 冷媒压力, 风机转速, 送风温度, 回风温度}
  ┌──────────────┐  ┌──────────────┐
  │ HVAC_A1      │  │ HVAC_B1      │
  │ comp, ref,   │  │ comp, ref,   │
  │ fan, supply, │  │ fan, supply, │
  │ return       │  │ return       │
  │  ┌────────┐  │  └──────────────┘
  │  │压缩机  │  │
  │  │内部细节│  │  ← 需要更高精度？→ 展开 Layer 3
  │  └────────┘  │
  └──────────────┘

Layer 3+: 压缩机内部、管道流场、材料应力...（按需展开）

关键性质：
  - 每一层的实体数量、状态维度、因果机制类型都不同（异构）
  - 展开是非均匀的：可能只有一栋建筑需要展开到Layer 2
  - 信息从细粒度到粗粒度是压缩的（不可逆信息损失）
  - 宏观参数约束微观仿真，微观结果修正宏观模型（双向耦合）
```

### 8.6 CER 与 Transformer 层次结构的对比

| 维度 | Transformer 的层次 | CER 的因果封装递归 |
|------|------------------|-------------------|
| 层次本质 | 同构重复（N 层 Transformer Block） | 异构嵌套（每层物理域不同） |
| 层间信息 | 无损（残差连接保留全部信息） | 有损（粗粒化压缩，不可逆） |
| 方向性 | 单向（浅→深→输出） | 双向（宏↔微因果循环） |
| 粒度变化 | 表示维度不变（如 d_model=4096） | 实体数量和状态维度逐层变化 |
| 可组合性 | 只能水平拼接（更多层） | 任意嵌套组合（乐高式） |
| 对应的物理理论 | 无 | 统计力学重正化群（RG） |

**注意**：CER（第八章）与多尺度聚合（第七章）解决不同层次的问题。七层解决的是"如何在不同精度之间切换"——粗粒化算法本身；八层解决的是"系统的整体拓扑形态"——子系统如何封装和嵌套。七层是算法工具，八层是架构原则。

---

## 九、与 Transformer 的逐层功能对比

| 计算功能 | Transformer 的实现 | CDA 的实现 |
|---------|-------------------|-----------|
| 输入编码 | Token Embedding + Positional Encoding | Entity-State Encoder（实体发现 + 感知融合，§2.1 + §2.2） |
| 计算选择 | 无（全连接 Attention，O(n²)） | 因果路由（物理语义稀疏选择，§3.4，O(N·K)） |
| 上下文聚合 | Multi-Head Self-Attention | 因果机制传播（沿因果边传递影响） |
| 层次结构 | N 层同构 Transformer Block | 因果封装递归（异构嵌套，自适应深度） |
| 非线性变换 | Feed-Forward Network (FFN) | 物理机制函数 f_ij（受物理约束的非线性变换） |
| 层归一化 | LayerNorm | 哈密顿投影（将状态约束在物理流形上） |
| 残差连接 | Residual Connection | 状态累加（ds = Σ Δs，物理状态的增量更新） |
| 输出预测 | Linear + Softmax → P(next token) | 状态分布预测 → P(next state \| current state, do) |
| 训练 | 交叉熵损失 + 反向传播 | 贝叶斯证据最大化 + 在线更新 |
| 推理 | 自回归生成 | 状态演化仿真 |
| 幻觉 | 结构性缺陷（无法消除） | 架构上不可能（物理约束 + 可验证） |
| 上下文窗口 | 固定长度（如 128K tokens） | 无固定窗口（世界状态是连续演化的） |
| 多模态 | 分模态编码后拼接 | 统一的实体状态表示（视觉=空间状态，语言=符号状态） |

---

## 十、一个具体的计算流程示例

**问题：如果把工厂的加热器功率提高 20%，1 小时后车间的温度分布会怎样？**

### 10.1 Transformer 的回答方式（如果它能回答的话）

```
输入: "工厂加热器功率提高20%，1小时后车间温度？"
→ Tokenize: [工, 厂, 加, 热, 器, ...]
→ Self-Attention: 找到"加热器"和"温度"的关联
→ FFN: 基于训练数据中的统计规律生成文本
→ 输出: "温度可能会升高。具体升幅取决于..."
→ 问题：没有精确数值，无法验证，可能编造
```

### 10.2 CDA 的回答方式

```
Step 1: 语言界面层解析意图
  NL → do(heater.power *= 1.2), query=room.temperature(t=1h)

Step 2: 因果动力学层执行仿真
  当前世界状态:
    Entity_1: heater (position, power=5000W, ...)
    Entity_2: room_air (position, temperature=22°C, velocity_field, ...)
    Entity_3: walls (position, thermal_conductivity, ...)
    ...
    CausalEdge: heater → room_air (机制: 热对流, α=0.8, τ=30s)
    CausalEdge: room_air → walls (机制: 热传导, α=0.3, τ=120s)

  应用干预:
    do(heater.power = 6000W)  # 功率提高20%
    切断指向 heater.power 的因果边（图手术）

  仿真 1 小时（3600 步，每步 dt=1s）:
    for t in range(3600):
      对每条因果边:
        # 热对流：加热器 → 空气
        ΔT_air += α · Q / (m_air · c_air) · dt
        # 热传导：空气 → 墙壁
        ΔT_wall += λ · (T_air - T_wall) / d · A / (m_wall · c_wall) · dt
      哈密顿投影: 总能量守恒
      不确定性传播: σ_T(t+1) = f(σ_T(t), Jacobian)

Step 3: 输出结果
  车间温度分布:
    区域A（靠近加热器）: 28.3°C ± 0.5°C
    区域B（中间区域）:  25.1°C ± 0.8°C
    区域C（远离加热器）: 23.4°C ± 0.3°C
    整体能耗增加: 4.2 kWh ± 0.1 kWh

  因果链解释:
    heater.power↑ → 对流换热率↑ → 空气温度↑ → 内外壁温差↑ → 热损失↑
    权重: 70%来自对流增强, 20%来自空气循环改善, 10%来自辐射变化
```

**关键差异**：
- Transformer 给你一段**看起来合理的文本**
- CDA 给你一个**物理上精确的、可验证的、带不确定性的预测**
- CDA 还能告诉你**为什么**（因果链解释），而不只是"是什么"

---

## 十一、计算复杂度分析

与 Transformer 的性能对比，是评估 CDA 工程可行性的关键。

### 11.1 前向传播复杂度

| | Transformer | CDA |
|--|------------|-----|
| 单步复杂度 | O(n² · d)（n=序列长度，d=模型维度） | O(N·K·k)（N=实体数，K=路由 top-k，k=机制函数参数量） |
| 序列长度敏感性 | **二次增长**——128K tokens 导致计算爆炸 | **线性增长**——边的数量通常远小于 n² |
| 推理长度 | 受限于上下文窗口 | 无固定窗口（连续状态演化） |
| 并行度 | 高（矩阵运算是 GPU 的甜区） | 中等（因果传播需要顺序步进，但每步内可并行） |

### 11.2 训练/学习复杂度

| | Transformer | CDA |
|--|------------|-----|
| 训练数据量 | 极大（万亿 tokens） | 小（物理约束 = 强先验，信息效率高） |
| 训练方式 | 集中式 GPU 集群，离线 | 分布式在线学习，边缘计算 |
| 训练能耗 | 巨大（GPT-4 级别训练成本 > $100M） | 低（增量更新，无需全量重训） |
| 冷启动 | 需要大量预训练 | 可以从少量传感器数据+物理先验启动 |

### 11.3 CER 递归的计算影响

```
递归深度 vs 计算量（不是线性关系，是指数衰减）：

深度 0（城市级宏观）:   O(100) 实体 × O(100) 边 → 秒级
深度 1（建筑级中观）:   O(10^4) 实体 × O(10^4) 边 → 分钟级
深度 2（设备级微观）:   O(10^6) 实体 × O(10^6) 边 → 小时级
深度 3（部件级细节）:   O(10^8) 实体 × O(10^8) 边 → 不实际

关键洞察：
  - 绝大多数查询不需要深度 > 1
  - 多重网格法的 V-cycle 策略：粗仿真定位热点 → 细仿真聚焦局部 → 粗仿真传播结果
  - 自适应展开：只对"异常区域"深入，其余保持粗粒度
  - 实际工程中的期望计算量 ≈ O(n · log n)，类似快速多极子法
```

### 11.4 工程可行性判断

```
✅ CDA 相对 Transformer 的优势场景：
  - 物理系统仿真与控制（数字孪生、工业IoT）
  - 需要精确推理和可验证性的决策系统
  - 在线持续学习场景（不需要全量重训）
  - 小数据、强先验场景

❌ CDA 相对 Transformer 的劣势场景：
  - 开放域文本生成（作文、对话、创意写作）
  - 缺乏物理约束的纯语言任务
  - 需要海量数据覆盖长尾分布的搜索/推荐
  - 当前硬件主要针对矩阵运算优化，因果图仿真的硬件加速生态尚不成熟
```

---

## 十二、局限性与开放问题

### 12.1 已知局限

**局限一：物理约束的双刃剑**

物理约束是 CDA 的优势，也是它的枷锁。当系统确实遵循物理定律时（工程、自然系统），CDA 远优于 Transformer。但当目标领域没有清晰的物理定律时（自然语言理解、艺术创作、社会交往），强行嵌入物理约束会适得其反。

**推论**：CDA 不是 Transformer 的"替代品"，而是"互补品"。第三纪元的最终形态可能是 CDA（物理世界模型）+ LLM（语言界面层）的混合架构。本文的五层栈设计已经预留了这个接口。

**局限二：因果发现的难题**

CDA 假设因果图可以被构建和维护。但在现实世界中，从观测数据中发现因果结构是一个未解决的难题——著名的"因果发现"问题。Judea Pearl 的框架假设因果结构已知或可从实验数据推断，但很多领域无法做随机实验。

**推论**：Phase 1-2 需要从物理定律明确的领域切入（热力学、力学），因果结构可以由领域知识提供。Phase 4 的"通用因果发现"仍是一个开放研究问题。

**局限三：实时性挑战**

物理仿真（尤其是高精度仿真）的计算量可能很大。虽然 CER 的自适应展开和多重网格策略可以缓解，但对于需要毫秒级响应的控制场景（如机器人实时控制），仍然面临挑战。

**推论**：可能需要专用的因果仿真加速硬件（类似 NPU 对神经网络的加速）。这是芯片设计层面的问题。

**局限四：非物理系统的泛化**

本文的架构设计以物理系统为原型。但人类社会的很多系统（经济、政治、社交网络）是否可以建模为"因果动力学"，存在争议。这些系统的"因果"是否和物理因果一样具有方向性和可组合性，是一个哲学和方法论层面的开放问题。

### 12.2 开放问题

| 问题 | 当前状态 | 可能的突破口 |
|------|---------|-------------|
| 如何从数据中自动发现因果结构？ | PC算法、GES等有局限性 | 结合物理先验的神经因果发现 |
| 因果机制函数如何参数化？ | 类型约束 + 可学习参数 | 元学习（learning to learn mechanisms） |
| 如何处理因果循环（非DAG）？ | Pearl的框架主要处理DAG | 微分代数方程（DAE）求解器 |
| CDA 与 LLM 如何深度整合？ | 本文只设计了浅层接口 | 因果感知的token表示学习 |
| 硬件加速器的最优架构？ | 无 | 面向稀疏因果图的专用芯片设计 |
| 多模态（视觉+语言+传感）如何统一表示？ | 初步设计为实体状态 | 跨模态因果对齐研究 |

---

## 十三、与现有前沿工作的关系

CDA 不是凭空发明，而是站在巨人肩上的整合与突破：

| 现有工作 | CDA 中的角色 | CDA 的超越 |
|---------|------------|-----------|
| Judea Pearl 因果推断 | Layer 3-4 的理论基础 | 从静态因果图 → 动态因果动力学 |
| Yann LeCun JEPA | 世界模型的理念启发 | 从联合嵌入预测 → 因果机制仿真 |
| Neural ODE | 状态演化的数学工具 | 加入因果图结构和哈密顿约束 |
| PINN (Physics-Informed NN) | 物理约束的思想来源 | 约束更深：不是损失函数中的软约束，而是架构硬约束 |
| Hamiltonian NN | 能量守恒的具体实现 | 推广到所有物理守恒律 + 因果结构 |
| E3NN (等变网络) | 对称性的具体实现 | 整合进因果机制函数的参数化中 |
| Friston 主动推断 | 学习闭环的理论框架 | 给出具体的计算架构实现 |
| 统计力学重正化群 | 多尺度聚合的理论基础 | 实现自适应的在线尺度选择 |
| GNN (图神经网络) | 因果图上的信息传播 | 从无向关联图 → 有向因果动力学图 |

---

## 十四、实现路线图

### 14.1 Phase 1: 热力学仿真引擎（可立即启动）

```
目标：验证核心计算原语
范围：单一物理域（传热）
方法：
  - 构建一个车间/建筑的 Entity-State Graph
  - 用 PINN + 哈密顿约束参数化因果机制函数
  - 从传感器数据中在线校准模型
  - 在仿真中预测温度分布和能耗
验证指标：仿真预测与实测的误差 < 工程精度要求
```

### 14.2 Phase 2: 多域因果耦合（1-2年）

```
目标：跨物理域的因果推理
范围：热力学 + 力学 + 流体（多物理场）
方法：
  - 引入机制类型系统（不同类型的因果边）
  - 实现跨域因果传播（热→力学→流体）
  - 开发因果发现算法（从数据中自动构建因果图）
验证指标：工业级多物理场仿真的AI加速
```

### 14.3 Phase 3: 反事实推理与决策（2-4年）

```
目标：完整的 do-演算和反事实推理
范围：全系统 + 策略优化
方法：
  - 实现平行世界分支树
  - 开发基于因果的策略搜索算法
  - 接入物联网传感器网络（第三纪元的数据基础设施）
验证指标：在数字孪生中实现零成本策略验证
```

### 14.4 Phase 4: 通用因果世界模型（4-8年）

```
目标：超越预定义物理域的通用因果推理
范围：从物理系统扩展到社会/经济/生物系统
方法：
  - 自动因果发现（从观测数据中学习因果结构）
  - 机制类型自动分类
  - 跨尺度统一建模
验证指标：在多个完全不同的领域展现因果理解能力
```

---

## 十五、核心术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 因果机制网络 | Causal Mechanism Network (CMN) | CDA 的核心计算单元，以实体为节点、因果机制为边构成的有向图 |
| 实体-状态因果图 | Entity-State Graph | 由 EntityState（实体状态）和 CausalEdge（因果边）组成的动态系统表示 |
| 哈密顿投影 | Hamiltonian Projection | 将状态约束在能量守恒流形上的操作，替代 Transformer 的 LayerNorm |
| 因果封装递归 | Causal Encapsulation Recursion (CER) | 异构嵌套的递归结构原则，每层封装一个因果子系统 |
| do-演算 | do-Calculus | Judea Pearl 提出的干预推理框架，CDA 在架构层面原生实现 |
| 图手术 | Graph Surgery | do-演算的实现手段——切断因果图中的特定边以模拟干预 |
| 反事实推理 | Counterfactual Reasoning | "如果当初..."类型的推理，通过溯因→干预→预测三步实现 |
| 粗粒化 | Coarse-Graining | 将微观状态聚合为宏观有效状态的操作，来自统计力学 |
| 重正化 | Renormalization | 调整因果机制函数使其在粗粒化后仍然有效的过程 |
| 主动推断 | Active Inference | Friston 提出的智能理论：智能 = 最小化自由能（模型与观测的意外） |
| 贝叶斯在线更新 | Bayesian Online Update | CDA 的学习机制，替代反向传播，从观测中实时修正模型 |
| 统一感知接口 | Universal Perception Interface | 将任意模态的非结构化数据转化为实体-状态因果图的感知前端 |
| 实体发现 | Entity Discovery | 从文本、图像、时序等非结构化数据中提取物理实体候选的过程 |
| 因果计算路由 | Causal Computational Routing | 基于物理语义的稀疏边选择机制，决定每步计算哪些因果边 |
| 因果发现冷启动 | Causal Bootstrapping | 从领域知识出发，分阶段逐步构建因果图的多阶段流程 |

---

## 十六、一句话定义

> **Transformer 学习的是"世界看起来像什么"——一段文本、一张图片的最可能样子。**
>
> **CDA 学习的是"世界怎么运作"——因果机制如何传播、物理约束如何限制、干预如何改变未来。**
>
> **前者是统计学的胜利。后者是动力学的范式。**
>
> **第三代人工智能的底层架构，不是更大的 Transformer，而是因果动力学引擎。**

---

## 附录：数学公式汇总

### A1. 核心状态演化方程

$$\frac{ds_i}{dt} = \sum_{j \in \text{parents}(i)} \alpha_{ij} \cdot f_{ij}(s_i, s_j; \theta_{ij}) + \eta_i$$

### A2. 哈密顿约束

$$H(\mathbf{q}, \mathbf{p}) = \sum_i \frac{|\mathbf{p}_i|^2}{2m_i} + \sum_{i<j} V(\mathbf{q}_i, \mathbf{q}_j) = E_{\text{total}}$$

### A3. 贝叶斯状态更新

$$b_i^{(t+1)} = \frac{P(\text{obs}_t \mid s_i, b_i^{(t)}) \cdot b_i^{(t)}}{P(\text{obs}_t \mid b_i^{(t)})}$$

### A4. 因果机制函数（热力学示例）

$$f_{ij}^{\text{thermal}}(s_i, s_j) = \frac{\lambda_{ij} \cdot A_{ij}}{d_{ij}} (T_i - T_j)$$

### A5. 不确定性传播

$$\Sigma_i^{(t+1)} = J_i \cdot \Sigma_i^{(t)} \cdot J_i^T + Q_i$$

其中 $J_i = \frac{\partial f_i}{\partial s_i}$ 是机制函数的雅可比矩阵。

### A6. 多尺度粗粒化

$$\bar{s}_I = \frac{1}{|I|} \sum_{i \in I} s_i, \quad \bar{\alpha}_{IJ} = \frac{1}{|I||J|} \sum_{i \in I, j \in J} \alpha_{ij}$$

### A7. 因果封装递归的输入-输出映射

$$\text{Output}_{\text{macro}}(t) = g_{\text{encap}}\big(\text{Input}_{\text{macro}}(t),\; \mathbf{\theta}_{\text{macro}},\; h_{\text{micro}}\big)$$

其中 $g_{\text{encap}}$ 是封装后的宏观因果机制函数，$h_{\text{micro}}$ 是子系统的隐状态统计量（粗粒化后的摘要），而非子系统的完整状态。这正是"封装导致信息损失"的数学表达。

### A8. 损失函数（训练时的目标函数）

$$\mathcal{L} = \underbrace{\sum_t \| s_t^{\text{sim}} - s_t^{\text{obs}} \|_2^2}_{\text{仿真精度}} + \lambda_1 \underbrace{\sum_{ij} \mathcal{I}(\alpha_{ij})}_{\text{因果稀疏性}} + \lambda_2 \underbrace{\text{Tr}(\Sigma)_{\text{unexplained}}}_{\text{解释力}}$$

### A9. Störmer-Verlet 辛积分器

$$p_{n+1/2} = p_n + \frac{\Delta t}{2} F(q_n)$$

$$q_{n+1} = q_n + \Delta t \cdot \frac{p_{n+1/2}}{m}$$

$$p_{n+1} = p_{n+1/2} + \frac{\Delta t}{2} F(q_{n+1})$$

性质：辛性（$\omega = dq \wedge dp$ 守恒）、时间可逆、二阶精度、长期能量有界。

### A10. 哈密顿投影的拉格朗日乘子

$$\lambda = \frac{H(q,p) - E_{\text{target}}}{\|\nabla_q H\|^2 + \|\nabla_p H\|^2}$$

$$q' = q - \lambda \nabla_q H, \quad p' = p - \lambda \nabla_p H$$

通过一阶泰勒展开保证修正后 $H(q',p') \approx E_{\text{target}}$，残余误差 $O(\lambda^2)$，可用牛顿迭代消除。

### A11. 机制函数类型化参数化

**力学型（反对称）**：$W_{\text{mech}} = A - A^T$，保证 $W^T = -W$（牛顿第三定律）

**热力学型（单调正定）**：$W_{\text{thermal}} = \exp(-\beta \cdot \sigma(A))$，元素 $\in (0,1]$（热力学第二定律）

**信息型（对角衰减）**：$W_{\text{info}} = \text{diag}(\exp(-\gamma |a_i|))$（信号随距离衰减）

**化学型（零和）**：$W_{\text{chem}} = A - \bar{A}$（行和为零，质量守恒）

### A12. 在线拉普拉斯近似的 ELBO

$$\text{ELBO} = \mathbb{E}_{q(\theta)}[\log p(\mathcal{D}|\theta)] - \text{KL}(q(\theta) \| p(\theta))$$

$$\approx -\frac{1}{2}\sum_t \|f_\theta(s_t) - s_{t+1}^{\text{obs}}\|^2 - \frac{1}{2}\sum_i \Lambda_i (\theta_i - \mu_i)^2$$

其中 $\Lambda_i$ 是参数的先验精度矩阵，$\mu_i$ 是先验均值。第一项是负对数似然，第二项是 KL 散度正则化（防止偏离先验）。

### A13. 信息瓶颈粗粒化

$$\max_{q(S_{\text{macro}}|S_{\text{micro}})} \; I(S_{\text{macro}}; Z) - \beta \cdot I(S_{\text{macro}}; S_{\text{micro}})$$

其中 $Z$ 是观测变量，$\beta$ 控制压缩-预测的 tradeoff。第一项最大化宏观状态对观测的预测力，第二项最小化宏观状态携带的微观信息（避免过拟合噪声）。

### A14. 重正化：因果路径求和

$$f_{IJ}^{\text{eff}} = \sum_{\gamma: I \to J} \prod_{e \in \gamma} W_e + \mathcal{O}(W^3)$$

串联因果链的复合效应由 Neumann 级数给出，截断到二阶：

$$F = W_1 + W_2 + W_1 W_2 + O(W^3)$$

其中 $W_1, W_2$ 是相邻因果边的参数矩阵，$W_1 W_2$ 是二阶耦合效应。

### A15. 多模态实体发现的信息论准则

$$\hat{\mathcal{E}} = \arg\max_{\mathcal{E}} \; I(\mathcal{E}; \mathcal{D}_{\text{multi}}) - \lambda |\mathcal{E}|$$

其中 $\mathcal{E}$ 是实体集合，$\mathcal{D}_{\text{multi}}$ 是多模态观测数据，$|\mathcal{E}|$ 是实体数量，$\lambda$ 控制粒度-精度 tradeoff。第一项最大化实体集合对多模态数据的互信息（预测力），第二项惩罚过度分割（防止每个像素都是一个实体）。

### A16. 因果路由的选择分数

$$r_{ij}^{(t)} = \alpha_{ij} \cdot \big(1 + \tanh(\Delta s_i^{(t)} / \tau_s)\big) \cdot \big(1 + \sigma((\text{tr}(\Sigma_j^{(t)}) - \tau_\sigma) / \tau_u)\big) \cdot q_j$$

其中 $\alpha_{ij}$ 是因果强度，$\Delta s_i^{(t)}$ 是源实体最近的状态变化量，$\Sigma_j^{(t)}$ 是目标实体的不确定性协方差，$q_j \in \{0, 1\}$ 是查询相关性标记。$\tau_s, \tau_\sigma, \tau_u$ 是归一化尺度参数。

### A17. 主动因果实验的期望信息增益

$$\text{EIG}(X) = H(G \mid \mathcal{D}) - \mathbb{E}_{x \sim p(x)} \left[ H\big(G \mid \mathcal{D} \cup \{\text{do}(X=x), Y\}\big) \right]$$

其中 $G$ 是因果图的后验分布，$\mathcal{D}$ 是已有数据，$Y$ 是干预 $\text{do}(X=x)$ 后的观测结果。$H(G \mid \cdot)$ 是因果图后验的熵——信息增益越大，说明该实验对消除结构不确定性的贡献越大。

### A18. 骨架引导的 NOTEARS 损失函数

$$\mathcal{L}_{\text{skeleton}} = \underbrace{\frac{1}{2T}\|X - XW\|_F^2}_{\text{标准 NOTEARS}} + \underbrace{\lambda h(W) + \frac{\rho}{2}h(W)^2}_{\text{DAG 约束}} + \underbrace{\frac{1}{2}\sum_{i,j}\Lambda_{ij}(W_{ij} - \hat{W}_{ij})^2}_{\text{骨架先验}}$$

其中 $\hat{W}$ 是骨架图的目标邻接矩阵，$\Lambda$ 是先验精度矩阵（对角元素由边的置信度决定）。骨架先验项确保：高置信度骨架边被保留（$\Lambda_{ij}$ 大 → $W_{ij}$ 被拉向 $\hat{W}_{ij}$），非骨架边被抑制（$\hat{W}_{ij}=0$ → $W_{ij}$ 被拉向零）。
