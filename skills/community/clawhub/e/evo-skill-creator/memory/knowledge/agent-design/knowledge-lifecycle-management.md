# 知识文件自动过时检测与生命周期管理

> 学习日期：2026-03-28
> 来源：多源综合研究（行业最佳实践、SM-2/FSRS 算法、Agent 内存管理模式）
> 学习次数：1

## 核心问题

knowledge/ 文件只增不减，长期导致：
1. 上下文膨胀 → 读取时间增加、注意力分散
2. 过时信息误导 → 基于旧知识做出错误决策
3. 信息矛盾 → 新旧知识并存但结论不同

## 元数据标准

### 推荐的 YAML Frontmatter 格式

每个知识文件头部应包含以下元数据：

```yaml
---
created: 2026-03-28        # 首次创建日期
updated: 2026-03-28        # 最后更新日期
last_accessed: 2026-03-28  # 最后被读取/引用的日期
access_count: 1            # 被读取/引用的总次数
study_count: 1             # 学习次数（对应 learn 命令）
category: framework        # 分类：framework / methodology / tool / trend / reference
volatility: medium         # 知识波动性：high（月度变化）/ medium（季度变化）/ low（年度变化）/ stable（基本不变）
confidence: high           # 置信度：high / medium / low
status: active             # 状态：active / stale / archived
---
```

### 元数据字段说明

| 字段 | 用途 | 更新时机 |
|------|------|---------|
| created | 知识溯源 | 创建时设置，不再修改 |
| updated | 判断信息时效性 | 每次修改内容时更新 |
| last_accessed | 遗忘曲线的核心输入 | 每次 go/learn/review 读取此文件时更新 |
| access_count | 衡量知识价值 | 同上 |
| study_count | 追踪学习深度 | learn 命令深入学习此主题时 +1 |
| category | 决定过时策略 | 创建时设置 |
| volatility | 决定 TTL 阈值 | 创建时设置，review 时可调整 |
| confidence | 检索时的权重因子 | 随学习深度和验证提升 |
| status | 是否参与主动检索 | 过时检测机制自动更新 |

## 过时检测机制

### 基于遗忘曲线的衰减模型

核心公式：`R = e^(-t/S)`

- **R**：当前检索价值（0~1）
- **t**：距上次访问的天数
- **S**：稳定性（知识的"半衰期"，随学习次数增加而增长）

### 稳定性（S）计算

借鉴 SM-2 算法的自适应机制：

```
S_initial = 7 天（初次学习后的默认稳定性）
S_new = S_old × EF（每次成功回顾后提升）
EF（易度因子）= 2.5（默认）
```

简化版实现（适用于文件系统级知识管理）：

| study_count | 稳定性 S（天） | 含义 |
|------------|---------------|------|
| 1 | 7 | 首次学习，一周内需要回顾 |
| 2 | 18 | 两次学习，约半个月 |
| 3 | 45 | 三次学习，约一个半月 |
| 4 | 112 | 四次学习，约四个月 |
| 5+ | 280 | 五次以上，约九个月 |

### 过时阈值（结合 volatility）

| volatility | R < 阈值视为 stale | R < 阈值视为需归档 |
|-----------|-------------------|------------------|
| high | R < 0.5（约 0.7S 天） | R < 0.2（约 1.6S 天） |
| medium | R < 0.4（约 0.9S 天） | R < 0.15（约 1.9S 天） |
| low | R < 0.3（约 1.2S 天） | R < 0.1（约 2.3S 天） |
| stable | 不自动过时 | 手动归档 |

### 实际效果示例

一个 `study_count=1, volatility=medium` 的文件：
- S = 7 天
- 6 天后 R ≈ 0.42 → 仍然 active
- 7 天后 R ≈ 0.37 → **标记 stale**
- 13 天后 R ≈ 0.15 → **建议归档**

一个 `study_count=3, volatility=low` 的文件：
- S = 45 天
- 45 天后 R ≈ 0.37 → 仍然 active
- 54 天后 R ≈ 0.30 → **标记 stale**
- 103 天后 R ≈ 0.10 → **建议归档**

## 过时知识的三种处理策略

### 策略 1：标记 Stale（软过时）

**适用场景**：知识可能仍有价值，但需要验证
**操作**：
- status 改为 `stale`
- 仍保留在原位
- 读取时显示警告："此知识已 N 天未更新/访问，可能需要验证"
- 下次 learn 相关主题时自动纳入温故范围

### 策略 2：压缩（Summarization Flush）

**适用场景**：知识本身仍然有效，但文件过长
**操作**：
- 将详细内容精炼为摘要（保留关键结论和数据点）
- 原始版本移到 `archive/` 目录
- 摘要版保留在 `knowledge/` 中，标记 `compressed: true`
- 显著减少上下文占用

### 策略 3：归档（Archive）

**适用场景**：知识已过时或长期未使用
**操作**：
- 移到 `memory/archive/` 目录
- 不参与日常检索
- 保留完整内容供未来查阅
- **不删除** — "Archive-Never-Delete" 原则

### 三种策略的选择逻辑

```
if status == stale:
    if volatility in [high, medium]:
        → 下次 learn/scan 时优先验证
        → 验证通过 → 更新 last_accessed, status=active
        → 验证失败 → 归档
    if volatility in [low, stable]:
        → 标记 stale，等待下次被引用时决定

if 需要归档:
    if 文件 > 50 行:
        → 先压缩为摘要，原文归档
    else:
        → 直接归档
```

## 执行时机与自动化

### 被动触发（检索时）

每次 go/learn/review 读取 knowledge/ 文件时：
1. 检查元数据
2. 更新 `last_accessed` 和 `access_count`
3. 如果 status 为 stale，显示警告

### 主动触发（review 命令）

review 命令增加 "memory 健康检查" 步骤：
1. 扫描所有 knowledge/ 文件的元数据
2. 计算每个文件的当前 R 值
3. 列出需要关注的文件：
   - stale 文件清单
   - 建议归档的文件清单
   - 从未被引用的文件（access_count == study_count，说明学了但从没用过）
4. 提出处理建议，让老板确认后执行

### 定期触发（cron）

建议通过 scheduler 定期执行 memory 健康检查：
- 频率：每两周或每月
- 方式：review memory（可作为 review 的子命令）

## 目录结构变更

```
memory/
├── knowledge/          # 活跃知识（status: active 或 stale）
│   └── <domain>/
├── archive/            # 归档知识（不参与日常检索）
│   └── <domain>/
└── ...
```

## 分级免疫机制

并非所有知识都应受衰减影响：

| 类别 | 衰减策略 | 示例 |
|------|---------|------|
| 核心原则 | 免疫（不衰减） | 进化模型、设计哲学 |
| 框架知识 | 慢衰减（volatility=low） | SAGE、DGM 框架 |
| 行业趋势 | 快衰减（volatility=high） | 模型排名、新工具 |
| 工具使用 | 中衰减（volatility=medium） | API 用法、配置方法 |

## 对 evo-skill-creator 的实施建议

### 立即可做

1. **为现有 knowledge/ 文件补充元数据** — 通过 review 命令批量添加 YAML frontmatter
2. **创建 `memory/archive/` 目录结构** — 准备好归档空间
3. **在 review 命令中增加 memory 健康检查** — 可作为 backlog 任务

### 中期规划

4. **在 learn 命令中自动更新元数据** — 每次 learn 读取文件时更新 last_accessed
5. **在 go 命令中检查 stale 知识** — 如果使用了 stale 文件中的知识，提醒验证
6. **为子智能体的 SKILL.md 模板加入 memory 健康检查说明**

### 长期愿景

7. **自动压缩** — 文件超过阈值行数时，自动生成摘要版
8. **跨智能体过时同步** — 如果创建者的知识过时了，自动通知使用了相同知识的子智能体

## 与已有知识的连接

- **SAGE 遗忘曲线** → 本文的衰减模型直接基于 SAGE 的启示
- **上下文工程** → 过时检测是"选择与裁剪"支柱的具体实现
- **多 Agent 协同** → 置信度衰减和内存蒸馏是本文的上层需求
- **自动技能评估** → 过时检测本身可以作为知识管理维度的评估指标

## 参考来源

1. 2026 Agent Lifecycle Management (ALM) 行业实践
2. SM-2 算法（SuperMemo）— 间隔重复调度
3. FSRS (Free Spaced Repetition Scheduler) — 开源 SRS 算法
4. Ebbinghaus 遗忘曲线 — R = e^(-t/S)
5. "Archive-Never-Delete" 原则 — AI Agent 内存管理最佳实践
6. Tiered Memory with TTL — 分层内存 TTL 模式
7. YAML Frontmatter 元数据标准 — Markdown 知识文件管理
