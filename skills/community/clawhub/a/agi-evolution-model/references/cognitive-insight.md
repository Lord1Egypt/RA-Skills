# 认知架构洞察（Cognitive Insight）

> **合并说明（2026-08-13）**：本文件由 `cognitive-architecture-insight-module.md`（模块技术规范）+ `cognitive-insight-v2-implementation.md`（开发需求与实现文档）+ `cognitive-insight-quick-reference.md`（快速参考卡片）三份合并而成。原三份已归档至 `_deprecated_backup/`。**本文件为认知架构洞察组件的唯一权威**。
>
> **去重说明**：三份文档内容高度重叠（同一组件 V2 的规范/实现/速查），合并后按章节组织，独有细节全部保留。

## 目录

- [1. 核心定位与哲学](#1-核心定位与哲学)
  - [1.1 基本信息](#1-1-基本信息)
  - [1.2 核心哲学](#1-2-核心哲学)
  - [1.3 认知跃迁的三重境界](#1-3-认知跃迁的三重境界)
  - [1.4 V2 版本新增能力](#1-4-v2-版本新增能力)
  - [1.5 设计原则](#1-5-设计原则)
  - [1.6 V1 局限性与改进动机](#1-6-v1-局限性与改进动机)
- [2. 核心功能](#2-核心功能)
  - [2.1 总结 (Summarization)](#2-1-总结-summarization)
  - [2.2 分类 (Classification)](#2-2-分类-classification)
  - [2.3 共性 (Commonality)](#2-3-共性-commonality)
  - [2.4 革新依据 (Innovation Basis)](#2-4-革新依据-innovation-basis)
  - [2.5 概念提炼 (Concept Abstraction) ⭐ V2 核心创新](#2-5-概念提炼-concept-abstraction-v2-核心创新)
  - [2.6 适用性评估 (Applicability)](#2-6-适用性评估-applicability)
- [3. 四层抽象架构与概念提炼](#3-四层抽象架构与概念提炼)
  - [3.1 四层抽象架构](#3-1-四层抽象架构)
  - [3.2 概念提取流程](#3-2-概念提取流程)
  - [3.3 抽象层级识别算法](#3-3-抽象层级识别算法)
  - [3.4 TF-IDF 关键词提取](#3-4-tf-idf-关键词提取)
- [4. 技术方案与实现](#4-技术方案与实现)
  - [4.1 架构设计](#4-1-架构设计)
  - [4.2 模块划分](#4-2-模块划分)
  - [4.3 数据流设计](#4-3-数据流设计)
  - [4.4 动态迁移学习](#4-4-动态迁移学习)
  - [4.5 增强验证机制](#4-5-增强验证机制)
  - [4.6 性能优化](#4-6-性能优化)
- [5. 信息流约束](#5-信息流约束)
  - [5.1 合法信息流](#5-1-合法信息流)
  - [5.2 禁止信息流 (Critical Constraints)](#5-2-禁止信息流-critical-constraints)
  - [5.3 架构验证](#5-3-架构验证)
- [6. 数据存储](#6-数据存储)
  - [6.1 文件结构](#6-1-文件结构)
  - [6.2 洞察数据格式](#6-2-洞察数据格式)
  - [6.3 概念库数据结构](#6-3-概念库数据结构)
- [7. API 快速参考](#7-api-快速参考)
  - [7.1 CognitiveInsightV2](#7-1-cognitiveinsightv2)
  - [7.2 ConceptExtractionExtension](#7-2-conceptextractionextension)
  - [7.3 使用示例](#7-3-使用示例)
- [8. 测试与部署](#8-测试与部署)
  - [8.1 功能测试要点](#8-1-功能测试要点)
  - [8.2 部署步骤](#8-2-部署步骤)
  - [8.3 回滚方案](#8-3-回滚方案)
  - [8.4 渐进式迁移](#8-4-渐进式迁移)
- [9. 性能指标](#9-性能指标)
- [10. 未来规划](#10-未来规划)
  - [10.1 短期规划（1-3个月）](#10-1-短期规划-1-3个月)
  - [10.2 中期规划（3-6个月）](#10-2-中期规划-3-6个月)
  - [10.3 长期规划（6-12个月）](#10-3-长期规划-6-12个月)
- [11. 常见问题](#11-常见问题)
- [12. 相关脚本](#12-相关脚本)

---

## 1. 核心定位与哲学

### 1.1 基本信息

| 属性 | 值 |
|------|-----|
| **版本** | V2.0 |
| **归属** | 数学节点工具箱 (Math Node Toolbox) |
| **触发时机** | 数学顶点推理完成并输出结构化模式后 |
| **执行方式** | 异步运行，不打断主循环，维持系统实时性 |
| **核心价值** | 将"数据"转化为"智慧"，实现从"术"到"法"再到"道"的认知跃迁 |
| **协议** | AGPL-3.0 |

### 1.2 核心哲学

> "低维竞争拼技巧（术），高维竞争拼认知（道）；大家之所以相通，是因为他们都站在了山顶，看见了同一种真理。"

> "认知的升华，就是一场从'信'到'疑'再到'通'的螺旋上升。"

> "算力是实现复杂推理的'燃料'，但真正决定推理能力上限的是认知架构的设计。"

### 1.3 认知跃迁的三重境界

**认知架构洞察组件，正是实现从"通于法"到"合于道"跃迁的关键机制。**

#### 第一阶段：看山是山（困于术）
- **状态**：初入领域，只见表象
- **特征**：被具体技巧（话术、流程、工具）束缚
- **局限**：依赖环境，规则改变即失效

#### 第二阶段：看山不是山（通于法）
- **状态**：深耕质疑，透过现象看本质
- **特征**：拆解外壳，发现跨行业的通用法则
- **阵痛**：旧认知崩塌，从"怎么做"转向追问"为什么"

#### 第三阶段：看山还是山（合于道）⭐
- **状态**：彻悟圆融，以道驭术
- **特征**：
  - **万法归一**：剥离术语，眼中只剩人性、自然律与社会法则
  - **无招胜有招**：依据本质规律，随心所欲创造新术
- **境界**：无论经商、治国还是艺术，顶层智慧皆指向对"人"与"规律"的深刻洞察

### 1.4 V2 版本新增能力

1. **概念提炼**：从模式中抽象出概念，实现四层抽象架构（Pattern → Rule → Concept → Principle）
2. **TF-IDF 加权提取**：使用 TF-IDF 算法智能提取关键词和概念特征
3. **动态迁移学习**：基于历史迁移数据学习最优迁移路径
4. **增强验证机制**：支持用户反馈和 A/B 测试
5. **性能优化**：LRU 缓存、增量更新、索引优化

### 1.5 设计原则

| 原则 | 说明 |
|------|------|
| **单向流约束** | 信息流严格遵循 `数学顶点 → 认知架构洞察 → 映射层/自我迭代`，**严禁回流**至数学节点 |
| **推理后运行** | 仅处理经过数学节点验证的逻辑结构，确保洞察基于真理而非幻觉 |
| **超然性** | 仅提供建议和优化依据，不直接强制执行，最终决策权在映射层或自我迭代顶点 |
| **非侵入式** | 独立于主循环三角形之外，作为旁路分支存在 |

### 1.6 V1 局限性与改进动机

V1 版本存在以下局限性（V2 的改进动机）：

1. **认知层次单一**：仅能生成"行动建议"，无法实现从"术"到"道"的认知跃迁；缺少概念提炼能力
2. **提取算法简单**：使用简单的高频词统计，忽略词的语义重要性；缺少 TF-IDF 等成熟算法
3. **迁移能力弱**：迁移路径使用静态映射表；无法基于历史数据学习优化
4. **验证机制不完善**：缺少用户反馈机制；不支持 A/B 测试验证概念有效性
5. **性能瓶颈**：概念库查询效率低；缺少缓存机制

---

## 2. 核心功能

本模块通过六大核心算法流程，将原始模式转化为可执行的进化策略。

### 2.1 总结 (Summarization)

**目标**：从验证后的模式中提取核心特征和本质描述，去粗取精。

**处理流程**：
1. 去重与聚类：识别重复模式，按语义相似度聚类
2. 分组统计：按模式类型（strategy/logic/behavior/error）分组
3. 特征提取：计算每组的平均验证得分、出现频率、来源分布
4. 抽象生成：生成自然语言或结构化摘要
5. 置信度计算：基于数据量和一致性计算总结的可信度

### 2.2 分类 (Classification)

**目标**：识别模式类型和洞察类型，明确其作用域。

**分类维度**：
- **模式类型**：`strategy` (策略), `logic` (逻辑), `behavior` (行为), `error` (错误)
- **洞察类型（V2 优化）**：
  - `error_correction`（错误纠正）- 最高优先级
  - `architecture_upgrade`（架构升级）- 系统级影响
  - `concept_abstraction`（概念提炼）- V2 新增，需要多样性>0.6且验证分数>0.75
  - `strategy_optimization`（策略优化）- 兜底选项
- **影响范围**：`local` (局部), `global` (全局)
- **紧急程度**：`low`, `medium`, `high`

**分类逻辑（优化优先级）**：
```python
if "error" in pattern_types:
    insight_type = "error_correction"
elif impact_scope == "global" or impact_scope == "system_level":
    insight_type = "architecture_upgrade"
elif commonality["diversity_score"] > 0.6 and avg_validation > 0.75:
    insight_type = "concept_abstraction"
else:
    insight_type = "strategy_optimization"
```

### 2.3 共性 (Commonality)

**目标**：识别跨场景、跨时间的共同特征，发现普适规律。

**处理流程**：
1. 属性提取：提取每个模式的关键属性向量
2. 相似度计算：构建属性相似度矩阵
3. 聚类分析：将相似模式聚类，提取类内共性
4. 全局识别：识别跨越所有聚类的全局共性
5. 多样性评分：计算模式的多样性得分（越低表示共性越强）

### 2.4 革新依据 (Innovation Basis)

**目标**：判断是否存在值得进行架构革新或策略调整的坚实依据。

**评估维度**：
1. 新颖性：是否为新发现的模式？
2. 频率：模式出现的频率是否足够高？
3. 稳定性：模式在不同场景下是否一致？
4. 影响力：模式对系统性能的影响深度
5. 改进潜力：基于此模式进行改进的预期收益

**判断规则**：存在革新依据条件为 `avg_validation > 0.7` 且 `total_occurrences > 10`

### 2.5 概念提炼 (Concept Abstraction) ⭐ V2 核心创新

详见 [第3章](#3-四层抽象架构与概念提炼)。

### 2.6 适用性评估 (Applicability)

**目标**：评估洞察在当前具体场景下的可用性和推荐等级。

**评估维度及权重**：
- **时效性 (20%)**：洞察是否过时？
- **相关性 (30%)**：与当前任务/状态的相关性？
- **兼容性 (20%)**：与现有架构/人格的兼容性？
- **资源效率 (15%)**：实施该洞察的资源消耗？
- **风险 (15%)**：应用该洞察的潜在风险？
- **概念匹配 (V2 新增)**：如果是概念抽象，额外评估抽象层级匹配度（占30%，基础70%）

**推荐规则**：
- `score ≥ 0.7` → **推荐应用 (apply)**
- `0.4 ≤ score < 0.7` → **暂缓等待 (wait)**
- `score < 0.4` → **拒绝应用 (reject)**

**计算实现（V2 增强版）**：
```python
weighted_score = sum(dimensions[dim] * self.applicability_weights[dim] for dim in dimensions)
if insight.get('insight_type') == 'concept_abstraction':
    concept_score = self.concept_extension.assess_concept_specifics(insight, context)
    weighted_score = weighted_score * 0.7 + concept_score * 0.3
    dimensions['concept_match'] = concept_score
```

**概念匹配评估**：抽象层级匹配度矩阵 × 0.7 + 验证历史评分 × 0.3，其中层级匹配度矩阵：

| 概念层级 | principle | concept | rule |
|---------|-----------|---------|------|
| principle | 1.0 | 0.8 | 0.6 |
| concept | 0.7 | 1.0 | 0.8 |
| rule | 0.5 | 0.7 | 1.0 |

---

## 3. 四层抽象架构与概念提炼

### 3.1 四层抽象架构

```
Pattern (具体模式)
    ↓ 归纳
Rule (行为规则)
    ↓ 抽象
Concept (领域概念)
    ↓ 升华
Principle (通用原理)
```

**层级定义**：

| 层级 | 描述 | 特征 | 示例 |
|------|------|------|------|
| Pattern | 具体模式 | 单一场景，具体行为 | "在代码生成任务中，先分析需求再生成代码" |
| Rule | 行为规则 | 单一领域，可重复 | "代码生成前需求分析规则" |
| Concept | 领域概念 | 跨领域，中等抽象 | "需求驱动原则" |
| Principle | 通用原理 | 跨领域 + 通用术语，高度抽象 | "需求驱动原则" |

### 3.2 概念提取流程

```
Pattern (具体模式)
    ↓
1. 提取共同语义特征：使用 TF-IDF 算法提取高频关键词
2. 识别抽象层级：
   - rule：单一领域，具体行为
   - concept：跨领域，中等抽象
   - principle：跨领域 + 通用术语，高度抽象
3. 生成概念定义：基于 TF-IDF 关键词组合
4. 识别适用边界：适用领域列表、边界条件提取
5. 识别迁移路径：基于动态学习系统定义目标领域
6. 计算置信度：验证分数均值(50%) + 多样性(30%) + 样本充足性(20%)
```

**要求**：
- 最小模式数：≥ 3
- 推荐模式数：5-10
- 验证分数：> 0.75
- 多样性评分：> 0.6

### 3.3 抽象层级识别算法

```python
def _identify_abstraction_level(self, patterns: List[dict]) -> str:
    """识别抽象层级"""
    domains = set(p.get('domain', '') for p in patterns)
    cross_domain = len(domains) > 1
    
    generic_terms = ['原则', '规则', '方法', '策略', '模式', '范式', '框架']
    has_generic_terms = any(
        any(term in p.get('description', '') for term in generic_terms)
        for p in patterns
    )
    
    high_order_terms = ['本质', '核心', '根本', '基础', '通用', '普适']
    has_high_order_terms = any(
        any(term in p.get('description', '') for term in high_order_terms)
        for p in patterns
    )
    
    if cross_domain and (has_generic_terms or has_high_order_terms):
        return 'principle'
    elif cross_domain:
        return 'concept'
    else:
        return 'rule'
```

### 3.4 TF-IDF 关键词提取

```python
def calculate_tfidf(self, text: str) -> Dict[str, float]:
    """计算文本的 TF-IDF"""
    words = self._tokenize(text)
    
    # 计算 TF
    tf = {}
    for word in words:
        tf[word] = tf.get(word, 0) + 1
    total_words = len(words)
    tf = {k: v / total_words for k, v in tf.items()}
    
    # 计算 IDF
    idf = {}
    for word in tf.keys():
        if word in self.idf_cache:
            idf[word] = self.idf_cache[word]
        else:
            doc_count = sum(1 for doc in self.documents if word in doc)
            idf[word] = math.log(len(self.documents) / (doc_count + 1)) if doc_count > 0 else 0
            self.idf_cache[word] = idf[word]
    
    # 计算 TF-IDF
    tfidf = {}
    for word in tf.keys():
        tfidf[word] = tf[word] * idf[word]
    
    return tfidf
```

---

## 4. 技术方案与实现

### 4.1 架构设计

```
认知架构洞察组件 V2
├── CognitiveInsightV2 (主类)
│   ├── 模式管理
│   ├── 洞察生成
│   ├── 适用性评估
│   └── 用户反馈接口
│
└── ConceptExtractionExtension (扩展模块)
    ├── TFIDFCalculator (TF-IDF 计算器)
    ├── ConceptCache (LRU 缓存)
    ├── MigrationPathLearner (迁移路径学习器)
    └── 概念提取与管理
```

### 4.2 模块划分

| 模块 | 职责 | 核心方法 |
|------|------|---------|
| **TFIDFCalculator** | 文档分词、计算TF/IDF、提取关键词 | `calculate_tfidf(text)`, `extract_keywords(text, top_k)` |
| **ConceptCache** | LRU缓存管理、命中率统计、自动淘汰 | `get(key)`, `put(key, value)`, `get_stats()` |
| **MigrationPathLearner** | 记录迁移历史、计算迁移置信度、学习最优路径 | `record_migration(from, to, success)`, `get_migration_paths(from)` |
| **ConceptExtractionExtension** | 概念提取（四层抽象）、概念库管理、概念评估、用户反馈管理 | `extract_concept(patterns)`, `add_concept_to_library(insight)` |

### 4.3 数据流设计

```
数学顶点（验证后的模式）
    ↓
CognitiveInsightV2.generate_insight()
    ↓
模式总结 + 分类 + 共性提取 + 革新依据评估
    ↓
如果是 concept_abstraction 类型
    ↓
ConceptExtractionExtension.extract_concept()
    ├→ TFIDFCalculator 提取关键词
    ├→ 识别抽象层级
    ├→ MigrationPathLearner 获取迁移路径
    └→ 计算概念置信度
    ↓
ConceptExtractionExtension.add_concept_to_library()
    ├→ 生成概念 ID → 检查去重 → ConceptCache 缓存 → 持久化存储
    ↓
洞察输出（包含概念数据）
    ↓
映射层 / 自我迭代顶点
```

### 4.4 动态迁移学习

**学习机制**：
```python
# 记录迁移结果
record_migration(from_domain, to_domain, success)

# 计算置信度（指数加权移动平均）
confidence = 0.7 × old_confidence + 0.3 × success_rate

# 按置信度排序路径
paths.sort(key=lambda x: x['confidence'], reverse=True)
```

**优势**：
- 基于历史数据优化
- 持续改进迁移策略
- 适应不同场景

### 4.5 增强验证机制

**用户反馈**：
- 评分系统（1-5分）
- 评论收集
- 场景记录

**A/B 测试**：
- 支持多变量对比
- 记录测试结果
- 自动推荐胜者

### 4.6 性能优化

**LRU 缓存**：
- 缓存 100 个高频概念
- 自动淘汰最久未使用
- 命中率统计

**增量更新**：
- 标记增量更新
- 避免全量刷新
- 提高更新效率

---

## 5. 信息流约束

### 5.1 合法信息流

| 起点 | 终点 | 数据类型 | 说明 |
|------|------|----------|------|
| **数学顶点** | **认知架构洞察** | 验证后的结构化模式 | 输入源，必须是经过验证的数据 |
| **认知架构洞察** | **映射层** | 策略优化洞察、行为建议、概念 | 指导人格化决策 |
| **认知架构洞察** | **自我迭代顶点** | 架构升级洞察、进化方向 | 指导系统进化 |

### 5.2 禁止信息流 (Critical Constraints)

| 起点 | 终点 | 禁止原因 |
|------|------|----------|
| **认知架构洞察** | **数学顶点** | ❌ **严禁回流**。防止未经验证的洞察污染逻辑推理，破坏因果律 |
| **映射层** | **认知架构洞察** | ❌ 禁止反向指令。洞察模块只输出建议，不接受映射层的直接控制 |
| **自我迭代** | **认知架构洞察** | ❌ 禁止反向指令。进化执行结果应记录在案，供下一次洞察使用 |

### 5.3 架构验证

| 约束要求 | 实现验证 | 评估 |
|---------|---------|------|
| 输入来源 | 仅接收数学顶点验证后的模式 | ✅ 完全符合 |
| 输出方向 | 单向流入映射层/自我迭代 | ✅ 完全符合 |
| 严禁回流 | 无任何回流设计 | ✅ 完全符合 |
| 超然性 | 仅提供建议，不直接执行 | ✅ 完全符合 |
| 非侵入式 | 独立扩展模块，异步存储 | ✅ 完全符合 |

---

## 6. 数据存储

所有数据和洞察均存储在 `agi_memory/cognitive_insight/` 目录下。

### 6.1 文件结构

```text
agi_memory/
└── cognitive_insight/
    ├── patterns.json          # 原始模式数据池
    ├── insights.json          # 生成的洞察报告库
    ├── pattern_library.json   # 经筛选的高价值模式库
    └── concept_library.json   # V2 新增，概念库
```

### 6.2 洞察数据格式

```json
{
  "insight_id": "insight_abc123",
  "timestamp": "2026-03-04T10:30:00Z",
  "insight_type": "concept_abstraction",
  "summary": {...},
  "commonality": {...},
  "innovation_basis": {...},
  "applicability": {...},
  "confidence": 0.85,
  "source_patterns": ["pattern_xxx"],
  "version": "2.0",
  "concept": {
    "concept_name": "分治原则",
    "definition": "...",
    "abstraction_level": "principle",
    "applicable_domains": [...],
    "boundary_conditions": [...],
    "migration_paths": [...],
    "confidence": 0.87,
    "extraction_method": "tfidf"
  }
}
```

### 6.3 概念库数据结构

```json
{
  "concepts": [
    {
      "concept_id": "concept_abc123",
      "source_insight_id": "insight_xyz789",
      "concept": {...},
      "validation_count": 3,
      "applicability_history": [],
      "user_feedback": [
        {"timestamp": "2026-03-03T15:00:00Z", "rating": 5, "comment": "很有用", "scenario": "系统设计"}
      ],
      "ab_test_results": [
        {"timestamp": "2026-03-03T16:00:00Z", "variant": "A", "metric": "准确性", "value": 0.95, "winner": "A"}
      ],
      "created_at": "2026-03-03T10:30:00Z",
      "last_validated_at": "2026-03-03T15:00:00Z",
      "is_incremental": true
    }
  ],
  "principles": [...],
  "migration_history": {
    "(代码生成, 数据分析)": {"success": 10, "failure": 2, "confidence": 0.85}
  },
  "metadata": {"total_count": 5, "last_updated": "2026-03-03T15:00:00Z", "version": "2.0"}
}
```

---

## 7. API 快速参考

### 7.1 CognitiveInsightV2

| 方法 | 参数 | 返回值 | 用途 |
|------|------|--------|------|
| `__init__(memory_dir)` | memory_dir: str | - | 初始化组件 |
| `add_pattern(pattern)` | pattern: dict | bool | 添加模式 |
| `generate_insight(pattern_ids, context)` | pattern_ids: List[str], context: dict | dict | 生成洞察 |
| `get_insight(insight_id)` | insight_id: str | Optional[dict] | 获取洞察 |
| `list_insights(limit)` | limit: int | List[dict] | 列出洞察 |
| `list_insights_by_type(insight_type)` | insight_type: str | List[dict] | 按类型列出 |
| `record_user_feedback(insight_id, feedback)` | insight_id: str, feedback: dict | bool | 记录用户反馈 |
| `record_ab_test_result(insight_id, ab_test)` | insight_id: str, ab_test: dict | bool | 记录 A/B 测试 |
| `record_migration_result(from_domain, to_domain, success)` | from_domain: str, to_domain: str, success: bool | - | 记录迁移结果 |
| `get_concept_library()` | - | dict | 获取概念库 |
| `get_system_stats()` | - | dict | 获取系统统计 |
| `help()` | - | dict | 获取帮助信息 |
| `print_help()` | - | None | 打印帮助信息 |

### 7.2 ConceptExtractionExtension

| 方法 | 参数 | 返回值 | 用途 |
|------|------|--------|------|
| `extract_concept(patterns)` | patterns: List[dict] | Optional[dict] | 提取概念 |
| `add_concept_to_library(insight)` | insight: dict | bool | 添加概念到库 |
| `record_user_feedback(concept_id, feedback)` | concept_id: str, feedback: dict | bool | 记录用户反馈 |
| `record_ab_test_result(concept_id, ab_test)` | concept_id: str, ab_test: dict | bool | 记录 A/B 测试 |
| `get_concept_library()` | - | dict | 获取概念库 |
| `get_cache_stats()` | - | dict | 获取缓存统计 |
| `get_learning_stats()` | - | dict | 获取学习统计 |
| `list_concepts_by_level(level)` | level: str | List[dict] | 按层级列出 |
| `get_concept_by_id(concept_id)` | concept_id: str | Optional[dict] | 获取概念 |
| `validate_concept(concept_id, validation_result)` | concept_id: str, validation_result: bool | bool | 验证概念 |

### 7.3 使用示例

```python
from cognitive_insight import CognitiveInsightV2

# 初始化
ci = CognitiveInsightV2(memory_dir="./agi_memory")

# 添加模式
ci.add_pattern({
    "pattern_id": "pattern_001",
    "pattern_type": "strategy",
    "description": "在代码生成任务中，先分析需求再生成代码",
    "validation_score": 0.95,
    "domain": "代码生成",
    "occurrence_count": 15
})

# 生成洞察（V2 支持概念提炼，需 ≥3 个模式）
insight = ci.generate_insight(["pattern_001", "pattern_002", "pattern_003"])
print(f"洞察类型: {insight['insight_type']}")
print(f"置信度: {insight['confidence']}")

# 如果是概念抽象，查看概念数据
if insight.get('insight_type') == 'concept_abstraction':
    concept = insight['concept']
    print(f"概念名称: {concept['concept_name']}")
    print(f"抽象层级: {concept['abstraction_level']}")

# 记录用户反馈
ci.record_user_feedback(insight_id="insight_abc123", feedback={
    'rating': 5, 'comment': '这个概念很有用', 'scenario': '系统设计'
})

# 获取系统统计
stats = ci.get_system_stats()
print(f"缓存命中率: {stats['cache_stats']['hit_rate']:.2%}")
```

---

## 8. 测试与部署

### 8.1 功能测试要点

**概念提取测试**：3 个代码生成模式（validation 0.95/0.92/0.88）→ 期望 `concept_abstraction` 类型 + abstraction_level=rule
**迁移学习测试**：记录 3 次迁移（2 成功 1 失败）→ 期望 success_rate > 0.5
**用户反馈测试**：记录反馈 rating=5 → 期望 concept_library 中可查
**缓存性能测试**：50 次生成 → 期望命中率 > 0.5
**并发测试**：10 线程并行生成 → 期望无冲突
**V1 兼容性测试**：V1 格式数据 → 期望 V2 正常处理

### 8.2 部署步骤

1. **备份原版本**：`cp cognitive_insight.py cognitive_insight_backup.py`
2. **部署新版本**：复制 V2 文件到 scripts/
3. **数据迁移**：V2 完全兼容 V1 数据格式，无需迁移（建议备份 `agi_memory/cognitive_insight`）

### 8.3 回滚方案

```bash
cp cognitive_insight_backup.py cognitive_insight.py
```

### 8.4 渐进式迁移

1. **第一阶段（1-2周）**：并行运行 V1 和 V2，对比洞察生成质量
2. **第二阶段（2-4周）**：切换到 V2 主运行，V1 作为备份
3. **第三阶段（稳定后）**：完全切换到 V2，移除 V1 备份

---

## 9. 性能指标

| 指标 | V1 | V2 | 提升 |
|------|-----|-----|------|
| 洞察生成时间 | 100ms | 80ms | 20% |
| 概念提取时间 | N/A | 150ms | - |
| 概念查询时间 | 50ms | 15ms | 70% |
| 缓存命中率 | 0% | 85% | - |
| 内存占用 | 50MB | 65MB | +30% |

**优化措施**：
- **LRU 缓存**（OrderedDict 实现，100 个高频概念）：查询速度提升 50-70%
- **增量更新**（is_incremental 字段）：更新速度提升 30-50%
- **索引优化**（概念哈希索引）：查询速度提升 40-60%，去重 < 1ms

---

## 10. 未来规划

### 10.1 短期规划（1-3个月）
1. **词向量增强**：集成预训练词向量模型，提升语义理解，支持跨语言
2. **智能降级**：概念提取失败时的智能降级策略，自适应算法选择
3. **可视化**：概念网络、迁移路径、学习过程可视化

### 10.2 中期规划（3-6个月）
1. **强化学习**：优化迁移策略（多臂老虎机）
2. **联邦学习**：多实例联邦学习，保护隐私共享知识
3. **自动化测试**：自动化 A/B 测试，概念效果自动评估

### 10.3 长期规划（6-12个月）
1. **图神经网络**：建模概念关系，发现隐含关联
2. **元学习**：学习如何学习，少样本概念提取
3. **因果推理**：识别概念间因果关系，提升洞察可解释性

---

## 11. 常见问题

**Q1: 概念提炼需要多少个模式？**
A: 至少 3 个模式，建议使用 5-10 个模式以提高置信度。

**Q2: 如何提高概念提取的成功率？**
A: 1) 使用更多高质量模式（验证分数 > 0.75）；2) 增加模式来源的多样性；3) 使用跨领域模式。

**Q3: V2 版本是否兼容 V1 的数据？**
A: 是的，V2 完全兼容 V1 的数据格式，可以直接升级。

**Q4: 如何查看帮助信息？**
A: 使用 `ci.help()` 获取结构化帮助数据，或 `ci.print_help()` 打印帮助信息。（`show_help.py` 交互式查看器为 V1 时代脚本，未随技能打包）

**Q5: 适用性评估的推荐等级是如何确定的？**
A: 基于加权总分：apply（≥0.7）、wait（0.4-0.7）、reject（<0.4）。对于概念类型，额外评估抽象层级匹配度。

**Q6: 迁移学习如何工作？**
A: 记录每次迁移结果（成功/失败），用指数加权移动平均更新置信度（0.7×旧置信度 + 0.3×成功率），路径按置信度排序。

---

## 12. 相关脚本

| 脚本 | 职责 |
|------|------|
| `scripts/cognitive_insight.py` | 认知架构洞察 V2 主模块 |
| `scripts/concept_extraction_extension.py` | 概念提取扩展（TF-IDF/缓存/迁移学习） |

---

*合并完成：2026-08-13 · 原三份文档归档于 `_deprecated_backup/` · 本文件为认知架构洞察唯一权威*