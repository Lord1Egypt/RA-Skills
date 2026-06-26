# 数据模式文档

## 1. 汉字数据源

### 1.1 概述

| 属性 | 值 |
|------|-----|
| 数据文件 | `assets/top_2500_chars_with_words.json`（Skill 内置） |
| 文件大小 | ~499 KB |
| 记录总数 | 2500 条 |
| 格式 | JSON 数组 |
| 编码 | UTF-8 |
| 来源 | 现代汉语大规模语料库词频统计 |

> 数据源直接内置在 Skill 的 `assets/` 目录中，无需外部依赖。

### 1.2 单条记录结构

```typescript
interface CharacterEntry {
  rank_id: number;              // 词频排名，1-2500，唯一标识
  char: string;                 // 单个汉字，如 "的"
  words: string[];              // 组词示例数组，2 个常见词组
  frequency: number;            // 该字在语料库中的词频百分比
  frequency_cumulative: number; // 从第 1 名到该字的累计词频百分比
  literacy_rate: number;        // 该字在数据集中的位置百分比参考值 (0-100)
}
```

### 1.3 字段说明

| 字段 | 类型 | 说明 | 用途 |
|------|------|------|------|
| `rank_id` | number | 1-2500 的唯一排名 | 确定字属于哪个层级 |
| `char` | string | 单个汉字 | 测试时展示给用户 |
| `words` | string[] | 2-5 个常见词组 | 组词辅助理解、学习复习 |
| `frequency` | number | 词频百分比 | 参考信息，不直接参与计算 |
| `frequency_cumulative` | number | 累计词频 | 展示覆盖率统计 |
| `literacy_rate` | number | 0-100 的位置百分比参考 | 辅助判断，不直接参与计算 |

### 1.4 示例数据（摘自 `assets/top_2500_chars_with_words.json`）

```json
[
  {
    "rank_id": 1,
    "char": "的",
    "words": ["好的", "是的"],
    "frequency": 4.8867,
    "frequency_cumulative": 4.8867,
    "literacy_rate": 0.04
  },
  {
    "rank_id": 50,
    "char": "会",
    "words": ["开会", "社会"],
    "frequency": 0.3821,
    "frequency_cumulative": 25.67,
    "literacy_rate": 0.95
  },
  {
    "rank_id": 2500,
    "char": "敞",
    "words": ["敞开", "宽敞"],
    "frequency": 0.0019,
    "frequency_cumulative": 98.5262,
    "literacy_rate": 100.0
  }
]
```

### 1.5 累计词频覆盖率

| 排名区间 | 累计覆盖 | 对应层级 | 典型场景 |
|----------|---------|---------|---------|
| 1-50 | ~25% | L1 核心字 | 最基础日常用字 |
| 1-200 | ~55% | L1+L2 | 基本读懂短句 |
| 1-500 | ~78% | L1-L3 | 阅读简单文章 |
| 1-1000 | ~90% | L1-L4 | 阅读一般文章 |
| 1-1500 | ~95% | L1-L5 | 较流畅阅读 |
| 1-2500 | ~98.5% | L1-L6 | 几乎无障碍阅读 |

### 1.6 按层级分布

| 层级 | 排名区间 | 字数 | 抽样数 | 抽样率 |
|------|---------|------|--------|--------|
| L1 核心字 | 1-50 | 50 | 50 | 100% |
| L2 常用字 | 51-200 | 150 | 50 | 33.3% |
| L3 扩展字 | 201-500 | 300 | 30 | 10.0% |
| L4 进阶字 | 501-1000 | 500 | 25 | 5.0% |
| L5 提高字 | 1001-1500 | 500 | 10 | 2.0% |
| L6 拓展字 | 1501-2500 | 1000 | 10 | 1.0% |

---

## 2. 层级配置

### 2.1 层级配置结构

```typescript
interface LevelConfig {
  level: number;          // 层级编号 1-6
  name: string;           // 层级名称
  rankStart: number;      // 排名区间起始
  rankEnd: number;        // 排名区间终止
  sampleInterval: number; // 抽样间隔（= 权重）
  testCount: number;      // 抽样测试数
  weight: number;         // 加权倍数
  description: string;    // 说明
}
```

### 2.2 熔断配置结构

```typescript
interface FuseConfig {
  consecutiveUnknownLimit: number;  // 连续不认识触发阈值 (默认 5)
  errorRateLimit: number;           // 错误率触发阈值 (默认 0.8)
  minTestCountForErrorRate: number; // 错误率计算最小样本 (默认 5)
}
```

### 2.3 约束规则

1. 各层级 `rankStart` 到 `rankEnd` 必须连续无重叠
2. 第一层 `rankStart` = 1，最后一层 `rankEnd` = 2500
3. 各层 `testCount` 总和 = 175 (`TOTAL_TEST_COUNT`)
4. `weight` = `sampleInterval` = 层级总字数 / 抽样数
5. 可使用 `scripts/validate_level_config.py` 验证一致性
6. 测试序列使用 `scripts/generate_test_sequence.py` 即时生成

---

## 3. 测试记录结构

### 3.1 完整测试记录

```typescript
interface TestRecord {
  id: string;                    // 唯一标识（UUID v4）
  timestamp: number;             // 测试时间戳 (Date.now())
  totalVocabulary: number;       // 估算认字量
  totalTested: number;           // 实际测试字数（含提前终止）
  totalKnown: number;            // 认识的字数
  totalUnknown: number;          // 不认识的字数
  accuracy: number;              // 正确率 (0-1)
  fuseTriggered: boolean;        // 是否触发熔断
  fuseLevel: number | null;      // 熔断触发的层级编号
  fuseReason: string;            // 熔断原因描述
  levelResults: LevelResult[];   // 各层级详细结果（6 条）
  unknownChars: UnknownChar[];   // 所有不认识的字汇总
  userAge: number;               // 被测儿童年龄
}
```

### 3.2 层级结果

```typescript
interface LevelResult {
  level: number;              // 层级编号 (1-6)
  name: string;               // 层级名称（核心字/常用字/...）
  tested: number;             // 实际测试字数
  known: number;              // 认识的字数
  unknown: number;            // 不认识的字数
  knownRate: number;          // 认识率 (0-1)
  estimatedKnown: number;     // 估算该层认识数 = known × weight
  weight: number;             // 层级权重
  fuseTriggered: boolean;     // 是否在该层级触发熔断
  fuseReason: string;         // 熔断原因（若触发）
  unknownChars: UnknownChar[];// 该层级不认识的字
}
```

### 3.3 不认识的字

```typescript
interface UnknownChar {
  char: string;               // 汉字
  rank_id: number;            // 词频排名
  level: number;              // 所属层级
  words: string[];            // 组词示例
}
```

### 3.4 计算规则

```
totalVocabulary = Σ levelResults[i].estimatedKnown
               = Σ (levelResults[i].known × levelResults[i].weight)

accuracy = totalKnown / totalTested  (totalTested > 0)

// 熔断后的层级：
//   tested = 已测数, known = 已知数, 剩余视为 unknown
// 跳过的层级（熔断后更高层级）：
//   tested = 0, known = 0, unknown = 0, estimatedKnown = 0
```

---

## 4. 年龄参考数据

```typescript
interface AgeLiteracyReference {
  age: string;        // 年龄段描述
  expected: string;   // 预期认字量范围
  stage: string;      // 发展阶段名称
}

const AGE_LITERACY_REFERENCE = [
  { age: '3-4岁',  expected: '50-200',   stage: '启蒙期' },
  { age: '4-5岁',  expected: '200-500',  stage: '兴趣培养期' },
  { age: '5-6岁',  expected: '500-800',  stage: '入学准备期' },
  { age: '6-7岁',  expected: '800-1200', stage: '一年级水平' },
  { age: '7-8岁',  expected: '1200-1600',stage: '二年级水平' },
  { age: '8-9岁',  expected: '1600-2000',stage: '三年级水平' },
  { age: '9-10岁', expected: '2000-2500',stage: '四年级水平' },
  { age: '10-12岁',expected: '2500+',    stage: '五年级及以上水平' },
];
```

**使用规则**：
- 根据 `userAge` 查找对应区间
- 将 `totalVocabulary` 与 `expected` 范围对比
- 高于上限 → "超出预期，非常优秀"
- 范围内 → "发展正常，继续保持"  
- 低于下限 → "继续加油，保持兴趣最重要"
- **始终正向鼓励**
