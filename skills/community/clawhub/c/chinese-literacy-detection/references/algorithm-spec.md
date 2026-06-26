# 分层抽样算法详细规格

## 目录

- [1. 理论基础](#1-理论基础)
  - [1.1 数据来源](#11-数据来源)
  - [1.2 分层抽样原理](#12-分层抽样原理)
  - [1.3 权重的统计学含义](#13-权重的统计学含义)
- [2. 六层配置详解](#2-六层配置详解)
- [3. 测试序列生成](#3-测试序列生成)
  - [3.1 Fisher-Yates 洗牌算法](#31-fisher-yates-洗牌算法)
  - [3.2 随机抽样算法](#32-随机抽样算法)
  - [3.3 完整生成流程](#33-完整生成流程)
- [4. 动态熔断机制](#4-动态熔断机制)
  - [4.1 设计目标](#41-设计目标)
  - [4.2 熔断条件](#42-熔断条件)
  - [4.3 熔断检查伪代码](#43-熔断检查伪代码)
  - [4.4 批量模式下的更新算法](#44-批量模式下的-consecutiveunknown-更新算法)
  - [4.5 熔断处理流程](#45-熔断处理流程)
  - [4.6 熔断对计算的影响](#46-熔断对计算的影响)
- [5. 结果计算](#5-结果计算)
- [6. 精度分析](#6-精度分析)

---

## 1. 理论基础

### 1.1 数据来源

采用现代汉语高频字表（来源于大规模语料库统计），前 2500 字覆盖日常阅读语料的 **98.5%**。这意味着掌握这 2500 字，基本可以无障碍阅读日常中文文本。

### 1.2 分层抽样原理

分层抽样（Stratified Sampling）是统计学中提高估计精度的经典方法。核心思想：
- 将总体按某一特征（此处为词频排名）分为若干层
- 在每层内独立随机抽样
- 用各层的样本统计量加权估算总体参数

**为何选择分层抽样而非简单随机抽样**：
1. **词频分布不均匀**：排名靠前的字使用频率极高，排名靠后的字频率极低
2. **层内同质性强**：同一频率段内的字，儿童认识的概率相近
3. **提高估计精度**：相比等量的简单随机抽样，分层抽样的估计方差更小
4. **降低测试负担**：高频字全测保证基础精度，低频字少量抽样即可推算

### 1.3 权重的统计学含义

每个层级的权重 = 该层级总字数 / 抽样字数 = 抽样间隔

例如 L3 层级（201-500）有 300 字，抽样 30 字，权重为 10。
若抽样的 30 字中有 20 字认识，则估算该层级认识 20 × 10 = 200 字。

---

## 2. 六层配置详解

### 2.1 L1 核心字（排名 1-50）

| 参数 | 值 |
|------|-----|
| 排名区间 | 1 - 50 |
| 总字数 | 50 |
| 抽样数 | 50（全量） |
| 抽样间隔 | 1（每字必测） |
| 权重 | 1 |

**设计理由**：
- 这 50 个字覆盖约 25% 的日常用字（如"的、是、了、我、不、在、有、他、这、个"）
- 作为最基础的字，全量测试可提供最精确的基线数据
- 若 L1 通过率低（如 < 30%），表明用户处于极初始阶段，可提前终止

**典型字集**（前 20）：的、一、是、了、不、在、人、有、我、他、这、中、大、来、上、国、个、到、说、们

### 2.2 L2 常用字（排名 51-200）

| 参数 | 值 |
|------|-----|
| 排名区间 | 51 - 200 |
| 总字数 | 150 |
| 抽样数 | 50 |
| 抽样间隔 | 3 |
| 权重 | 3 |

**设计理由**：
- 150 字全测负担过重，抽样 50 字可在测试时长和精度间平衡
- 权重 3 意味着每认识 1 个抽样字，代表该层级认识 3 个字
- 这个层级对应大约一年级上学期的识字目标

### 2.3 L3 扩展字（排名 201-500）

| 参数 | 值 |
|------|-----|
| 排名区间 | 201 - 500 |
| 总字数 | 300 |
| 抽样数 | 30 |
| 抽样间隔 | 10 |
| 权重 | 10 |

**设计理由**：
- 该区间字频逐渐降低，层内同质性仍然较高
- 30 个样本在 300 的总体中提供 10% 的抽样率，统计上足够可靠
- 对应约一年级下学期至二年级的识字水平

### 2.4 L4 进阶字（排名 501-1000）

| 参数 | 值 |
|------|-----|
| 排名区间 | 501 - 1000 |
| 总字数 | 500 |
| 抽样数 | 25 |
| 抽样间隔 | 20 |
| 权重 | 20 |

**设计理由**：
- 500 字范围较大，25 个样本的 5% 抽样率已满足估计需求
- 该层级对应二至三年级识字水平
- 权重 20 意味着估算精度为 ±20 字的量级

### 2.5 L5 提高字（排名 1001-1500）

| 参数 | 值 |
|------|-----|
| 排名区间 | 1001 - 1500 |
| 总字数 | 500 |
| 抽样数 | 10 |
| 抽样间隔 | 50 |
| 权重 | 50 |

**设计理由**：
- 大多数低年级儿童在此层级认识字较少
- 少量抽样（10字）即可判断是否达到该层级
- 权重 50 表明这是粗粒度估算区间

### 2.6 L6 拓展字（排名 1501-2500）

| 参数 | 值 |
|------|-----|
| 排名区间 | 1501 - 2500 |
| 总字数 | 1000 |
| 抽样数 | 10 |
| 抽样间隔 | 100 |
| 权重 | 100 |

**设计理由**：
- 能到达此层级的通常是高年级学生
- 10 个字的抽样判断是否进入"高级阅读者"区间
- 权重 100 是最大的，单个字的认识/不认识影响较大

---

## 3. 测试序列生成

### 3.1 Fisher-Yates 洗牌算法

用于对测试序列进行公平随机排列：

```
算法 Fisher-Yates-Shuffle(array):
  result ← copy(array)
  FOR i FROM result.length - 1 DOWNTO 1:
    j ← random_int(0, i)  // 含 i
    swap(result[i], result[j])
  RETURN result
```

**算法特性**：
- 时间复杂度：O(n)
- 空间复杂度：O(n)（创建副本）
- 等概率性：每种排列的概率为 1/n!

### 3.2 随机抽样算法

```
算法 Random-Sample(array, count):
  IF count ≥ array.length:
    RETURN Fisher-Yates-Shuffle(array)
  shuffled ← Fisher-Yates-Shuffle(array)
  RETURN shuffled[0..count-1]
```

**特性**：
- 无放回抽样，每个字最多测一次
- 当 count ≥ length 时退化为全量打乱

### 3.3 完整生成流程

```
算法 Generate-Test-Sequence(allCharacters, levelConfigs):

  输入：allCharacters (2500条，来自 assets/top_2500_chars_with_words.json)
        levelConfigs (6层配置)
  输出：testSequence (最多175条，按层级顺序排列)

  testSequence ← []

  FOR EACH config IN levelConfigs:
    1. 过滤：levelChars ← filter(allCharacters, rankStart ≤ rank_id ≤ rankEnd)
    2. 抽样：
       IF config.sampleInterval = 1:
         selected ← Fisher-Yates-Shuffle(levelChars)
       ELSE:
         selected ← Random-Sample(levelChars, config.testCount)
    3. 标记：为每个字附加 level, levelName, weight
    4. 追加：testSequence.append(selected)

  RETURN testSequence

注意：
- 数据源内置于 Skill 的 assets/ 目录中
- 序列按层级顺序排列（L1 全部 → L2 全部 → ... → L6 全部）
- 层级内部随机排列
- 每次测试即时生成新的随机序列
- 可使用 scripts/generate_test_sequence.py 执行生成
- 在 Chatbot 场景中，可按批次（每5-10字）逐步呈现
```

---

## 4. 动态熔断机制

### 4.1 设计目标

- **保护儿童心理**：避免连续遇到大量不认识的字产生挫败感
- **节省测试时间**：当已有足够证据判断水平时提前终止
- **保证统计有效性**：在精度和效率间取得平衡

### 4.2 熔断条件

#### 条件 A：连续失败熔断

```
IF 当前层级.consecutiveUnknown ≥ consecutiveUnknownLimit (5)
THEN 触发熔断
```

**直觉解释**：连续 5 个字都不认识，说明这个难度段已超出能力范围。

#### 条件 B：错误率熔断

```
IF 当前层级.tested ≥ minTestCountForErrorRate (5)
   AND 当前层级.unknown / 当前层级.tested ≥ errorRateLimit (0.8)
THEN 触发熔断
```

**直觉解释**：测了 5 个以上，80% 不认识，统计上该层级的通过率极低。

### 4.3 熔断检查伪代码

```
算法 Check-Fuse(levelResult, fuseConfig):

  // 条件 A: 连续失败
  IF levelResult.consecutiveUnknown ≥ fuseConfig.consecutiveUnknownLimit:
    RETURN { triggered: true, reason: "连续{limit}个字不认识" }

  // 条件 B: 错误率
  tested ← levelResult.known + levelResult.unknown
  IF tested ≥ fuseConfig.minTestCountForErrorRate:
    errorRate ← levelResult.unknown / tested
    IF errorRate ≥ fuseConfig.errorRateLimit:
      RETURN { triggered: true, reason: "错误率达{rate}%" }

  RETURN { triggered: false }
```

### 4.4 批量模式下的 consecutiveUnknown 更新算法

在批量出题模式中（每批 5-10 个字），用户一次性回复本批所有字的认识/不认识情况。
必须按**出题顺序**逐字更新 `consecutiveUnknown`，而非简单累加不认识数。

```
算法 Update-Batch-Result(levelResult, batchChars, userResponse):

  输入：
    levelResult   - 当前层级运行时状态
    batchChars    - 本批出题的字（按出题顺序排列）
    userResponse  - 用户回复解析结果（每个字的认识/不认识标记）

  // ⛔ 前置门控：出题前必须检查，如果已熔断则禁止进入此函数
  ASSERT consecutiveUnknown < 5, "已触发熔断，禁止继续处理"

  // 快速路径：用户回复"都不认识"
  IF userResponse.type = "ALL_UNKNOWN":
    levelResult.unknown += len(batchChars)
    levelResult.tested += len(batchChars)
    levelResult.consecutiveUnknown += len(batchChars)
    // ⚠️ 每批至少5字，consecutiveUnknown 必然 ≥ 5 → 必须触发熔断
    FOR EACH char IN batchChars:
      levelResult.unknownChars.append(char)
    RETURN Check-Fuse(levelResult, FUSE_CONFIG)  // ⚠️ 必然返回 triggered=true
    // 🚫 绝对禁令：此路径返回后，Chatbot 的下一条消息只能是熔断通知+结果报告

  // 快速路径：用户回复"都认识"
  IF userResponse.type = "ALL_KNOWN":
    levelResult.known += len(batchChars)
    levelResult.tested += len(batchChars)
    levelResult.consecutiveUnknown = 0  // 重置
    RETURN Check-Fuse(levelResult, FUSE_CONFIG)

  // 常规路径：逐字按出题顺序处理
  FOR EACH char IN batchChars (按出题顺序):
    isKnown ← userResponse.getStatus(char)

    IF isKnown:
      levelResult.known += 1
      levelResult.tested += 1
      levelResult.consecutiveUnknown = 0  // 重置
    ELSE:
      levelResult.unknown += 1
      levelResult.tested += 1
      levelResult.consecutiveUnknown += 1
      levelResult.unknownChars.append(char)

    // ⚠️ 关键：每处理一个字后立即检查熔断
    fuseResult ← Check-Fuse(levelResult, FUSE_CONFIG)
    IF fuseResult.triggered:
      // 本批剩余未处理的字不再处理
      RETURN fuseResult

  // 本批全部处理完毕，未触发熔断
  RETURN { triggered: false }
```

**关键规则说明**：
1. 必须按出题顺序逐字处理，不能先处理"认识"的再处理"不认识"的
2. 每处理一个字后**立即**检查熔断，而非等本批全部处理完才检查
3. "都不认识"快速路径：`consecutiveUnknown += 本批字数`，由于每批 ≥ 5 字，**必然触发熔断**，Chatbot 的下一条消息**只能是熔断通知+结果报告**
4. "都认识"快速路径：`consecutiveUnknown = 0`，直接重置
5. **前置门控**：进入此函数前必须确认 `consecutiveUnknown < 5`，否则禁止出题

### 4.5 熔断处理流程

```
当熔断在层级 Lk 触发时：
  1. 记录 fuseLevel = k, fuseReason = 原因
  2. 当前层级 Lk：
     - 已测部分保留实际结果
     - 剩余未测字 → known 数不变（相当于全部不认识）
  3. 后续层级 L(k+1) ... L6：
     - tested = 0, known = 0, estimatedKnown = 0
  4. 执行结果计算
```

### 4.6 熔断对计算的影响

```
例：L1 全过(50/50)，L2 40/50，L3 在测第 8 个时触发熔断（已知 1/8）
    L3 剩余 22 个 → 不再测试
    L4、L5、L6 → 全部跳过

    W = 50×1 + 40×3 + 1×10 + 0×20 + 0×50 + 0×100
      = 50 + 120 + 10 + 0 + 0 + 0
      = 180 字
```

### 4.7 层级运行时状态

```
LevelRuntime:
  level: number              // 层级编号
  name: string               // 层级名称
  tested: number             // 已测字数
  known: number              // 认识数
  unknown: number            // 不认识数
  consecutiveUnknown: number // 当前连续不认识数（每次"认识"重置为0）
  knownRate: number          // 认识率
  estimatedKnown: number     // 估算认识数 = known × weight
  weight: number             // 权重
  fuseTriggered: boolean     // 是否触发熔断
  fuseReason: string         // 熔断原因
  unknownChars: []           // 不认识的字列表
```

---

## 5. 结果计算

### 5.1 综合认字量

```
算法 Calculate-Vocabulary(levelResults):
  totalVocabulary ← 0
  FOR EACH result IN levelResults:
    result.estimatedKnown ← result.known × result.weight
    totalVocabulary ← totalVocabulary + result.estimatedKnown
  RETURN totalVocabulary
```

### 5.2 完整测试记录生成

```
算法 Generate-Test-Record(levelResults, fuseInfo, userAge):
  totalTested ← Σ result.tested
  totalKnown ← Σ result.known
  totalUnknown ← Σ result.unknown
  totalVocabulary ← Calculate-Vocabulary(levelResults)
  unknownChars ← flatten(result.unknownChars for each result)
  accuracy ← totalKnown / totalTested (if totalTested > 0)
  encouragement ← Generate-Encouragement(totalVocabulary, userAge)

  RETURN {
    id, timestamp, totalVocabulary, totalTested,
    totalKnown, totalUnknown, accuracy,
    fuseTriggered, fuseLevel, fuseReason,
    levelResults, unknownChars, encouragement, userAge
  }
```

### 5.3 鼓励语生成规则

```
算法 Generate-Encouragement(vocabulary, age):
  reference ← lookup AGE_LITERACY_REFERENCE by age
  
  IF vocabulary > reference.expectedMax:
    RETURN "太厉害了！远超同龄平均水平，你是一个出色的小读者！"
  ELIF vocabulary ≥ reference.expectedMin:
    RETURN "非常棒！认字量发展很健康，继续保持阅读习惯！"
  ELSE:
    RETURN "每个孩子都有自己的成长节奏，保持对文字的兴趣最重要！"

  // 始终正向鼓励，避免负面评价
```

---

## 6. 精度分析

### 6.1 估算误差来源

1. **抽样误差**：随机抽样天然存在的统计波动
2. **层级边界效应**：字频在层级边界处的连续性被离散化
3. **测试状态影响**：儿童注意力、情绪等非认知因素
4. **熔断截断误差**：提前终止导致高层级数据缺失

### 6.2 误差估算

假设每层的认识概率为 p，抽样 n 个字：
- 认识数服从二项分布 B(n, p)
- 认识比例的标准误 SE = √(p(1-p)/n)
- 估算认字量的标准误 = SE × 层级总字数

各层级误差估算（以 p=0.7 为例）：

| 层级 | 总字数 | 抽样数 | SE | 估算 SD |
|------|--------|--------|-----|---------|
| L1 | 50 | 50 | 0.065 | 3.2 字 |
| L2 | 150 | 50 | 0.065 | 9.7 字 |
| L3 | 300 | 30 | 0.084 | 25.1 字 |
| L4 | 500 | 25 | 0.092 | 45.8 字 |
| L5 | 500 | 10 | 0.145 | 72.5 字 |
| L6 | 1000 | 10 | 0.145 | 144.9 字 |

**整体 95% 置信区间约为 ±100-150 字**（取决于真实识字水平的分布）。

### 6.3 提高精度的方案

若需更高精度，可考虑：
1. **增加抽样数**（会增加测试时长）
2. **减少层级数量**（损失细粒度信息）
3. **多次测试取平均**（适合追踪场景）
4. **自适应测试**（根据前序结果动态调整后续抽样数）
