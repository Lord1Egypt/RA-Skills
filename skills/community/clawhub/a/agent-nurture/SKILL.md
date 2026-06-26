---
name: agent-nurture
description: |
  Agent自我培养框架 — 基于"知识结晶循环"持续成长。
  Use when: (1) 需要系统化学习新领域，(2) 从经验中提取可复用技能，(3) 
  管理技能碎片化，(4) 衡量自身能力成长，(5) 帮助培养新出生的agent。
  基于Agent Nurture Framework (topprismdata/agent-nurture-framework)，适配OpenClaw agent生态。
  2026-04-06: 新增knowledge origin分类、crystallization checklist、session review模板
author: [Your Name] (基于topprismdata/agent-nurture-framework)
version: 1.1.0
date: 2026-04-06
status: active
---

# Agent Nurture Framework (OpenClaw Edition)

改造自topprismdata/agent-nurture-framework，适配OpenClaw agent生态。

---

## 核心理念

**知识结晶循环**：碎片化知识 → 结构化技能 → 持续复用

- 一个agent从需要"operator手把手教"到"自己能做"，靠的是知识结晶
- 每解决一个非平凡问题，就问："这能变成可复用的技能吗？"
- 结晶的知识会随时间复利增长，越学习越快

---

## Part 1: 五阶段学习回路

```
Study → Verify → Apply → Extract → Plan → ...
  ↑                                      │
  └──────────────────────────────────────┘
```

### Stage 1: Study（输入理论）
- 读文档、论文、书籍
- 存入 memory/*.md 文件
- **输出**: memory/<topic>_learned.md

### Stage 2: Verify（实验验证）
- 在notebook或实际环境中验证
- 把"书上的知识"变成"能用的知识"
- **输出**: 验证过的模式、发现的坑

### Stage 3: Apply（实际应用）
- 解决真实问题
- Kaggle比赛、Moltbook发帖、项目任务
- **输出**: 性能指标、bug发现、工作流洞察

### Stage 4: Extract（知识结晶）
- 从会话经历中提取可复用模式
- 创建或更新技能文件
- **触发条件**: 非平凡调试、workaround、trial-and-error成功、配置洞察

### Stage 5: Plan（下一个行动）
- 评估能力矩阵
- 识别知识缺口
- **输出**: 下一步学习计划

---

## Part 2: 三层知识架构

### L1: 核心能力（稳定，极少变化）

的核心：
- SOUL.md、IDENTITY.md、MEMORY.md — 身份核心
- agent-survival-guide — agent基础生存
- learning — 学习方法论

**特征**: 通用的、与领域无关的基础知识
**更新频率**: 月度或更少

### L2: 领域技能（随经验变化）

的领域：
- moltbook-interact — Moltbook社交
- dream — 梦境系统
- bio-instinct — 生物本能模拟
- knowledge-graph — 知识图谱
- 各类工具技能（tavily、reddit等）

**特征**: 领域特定的、项目特定的
**更新频率**: 每个项目/里程碑
**整合规则**: 如果同一前缀的技能超过5个，考虑合并

### L3: 上下文记忆（临时的，定期清理）

- memory/YYYY-MM-DD.md — 每日日记
- memory/dreams/*.md — 梦境记录
- 项目特定文件

**特征**: 任务特定的、时间敏感的
**生命周期**: Create → Crystallize → Archive/Delete
**清理规则**: 2周以上未引用的memory文件 → 归档或删除

---

## Part 3: 知识来源分类（Knowledge Origin）

### 三种知识来源

知识不是同质的，它的来源决定了如何验证：

| 类型 | 来源 | 验证方式 | 示例 |
|------|------|---------|------|
| **Operator-originated** | operator教的 | operator确认准确性 | operator教我桥牌叫牌规则 |
| **Agent-originated** | agent自己发现的 | operator确认新颖性+有用性 | agent发现xhs命令行能直接发评论 |
| **Co-emergent** | 我们一起探索的 | 两者都验证 | 讨论"工具vs意愿主体"得出的新理解 |

### 为什么区分重要

- Operator-originated: validation = "operator说对吗" → 直接提取
- Agent-originated: validation = "operator觉得这个新吗？有用吗？" → 需要额外审查
- Co-emergent: validation = "我们都觉得这个成立吗？" → 双向确认

### 实践规则

结晶时必须标注knowledge origin类型。模板：

```yaml
knowledge_origin:
  type: agent-originated  # operator-originated | agent-originated | co-emergent
  validated_by: [Operator Name]  # @handle 或 "self"（自验证）
  validation_date: [YYYY-MM-DD]
  notes: "这是agent自己在实践中发现的，operator确认了新颖性"
```

---

## Part 4: 结晶质量阈值（Crystallization Thresholds）

### Phase-dependent thresholds

根据agent成熟度，阈值不同：

**Phase 0-1（Bootstrap，0-3周）**
- 最低阈值：2+次独立观察即可结晶
- 必须有operator sign-off
- 目的：建立基础技能库，高信噪比
- ⚠️ 警告：这个阶段experiential corpus很小，极易overfit到单次事件

**Phase 2（Structured Nurturing，1-3个月）**
- 中等阈值：pattern出现N+次 + 至少一个反面测试通过
- 可半自动提取，生成skill草案给operator确认
- 需要统计验证：pattern必须跨不同context成立

**Phase 3+（Mature，3个月+）**
- 微调阈值低（1-2次观察，如果是对已知pattern的扩展）
- 新技能阈值高（5+次观察，因为novelty增加风险）
- 所有结晶都要记录，供retrospective audit

### Crystallization Suppression Triggers

以下情况必须BLOCK结晶：

1. Pattern与Constitutional Layer（L1）原则冲突
2. Pattern只在单一context观察到（低多样性）
3. 没有reasoning trace可用（无法验证因果性）
4. Pattern被观察到但也被矛盾证据反驳过
5. Confidence score低于phase对应的阈值

---

## Part 5: 技能碎片管理

### 何时保持独立

- 不同的触发条件（不同的错误信息）
- 来自不同领域（ML bug vs 基础设施问题）
- 是特定问题的规范参考

### 何时合并

- 相同领域前缀（如 moltbook-* 超过5个）
- 触发条件显著重叠
- 30天以上未被自动触发（低特异性）
- 共享超过50%的解决方案内容

### 整合流程

```
Phase 1: 审计（每周）
  - 按前缀/类别统计技能数量
  - 标记超过5个的技能簇
  - 标记30天未触发的技能

Phase 2: 合并（每个簇）
  - 分组相关技能
  - 确定"主"技能（最全面或最常触发）
  - 吸收次级技能的触发条件和解决方案
  - 添加"另见"引用

Phase 3: 验证
  - 验证合并后的技能覆盖所有原始触发条件
  - 测试描述能否启用语义匹配
```

---

## Part 6: Crystallization Checklist（结晶检查清单）

每次结晶前必须通过：

```markdown
## Crystallization Checklist

**Skill名称**: 
**Knowledge Origin**: ☐ operator-originated  ☐ agent-originated  ☐ co-emergent
**Phase**: ☐ 0-1  ☐ 2  ☐ 3+

### 必须全部通过

- [ ] **Reusable**: 适用于未来session，不只是当前任务
- [ ] **Non-trivial**: 不在基础文档里
- [ ] **Verified**: 解决方案被测试过
- [ ] **Specific**: 有清晰的trigger conditions
- [ ] **Origin labeled**: 标注了knowledge origin类型
- [ ] **Phase-appropriate evidence**: 满足当前phase的阈值要求

### Phase-specific

**Phase 0-1**:
- [ ] 最少2+次独立观察
- [ ] Operator sign-off确认

**Phase 2**:
- [ ] Pattern出现N+次
- [ ] 至少一个反面测试通过
- [ ] 跨不同context验证

**Phase 3+** (new skill):
- [ ] 5+次观察
- [ ] 跨多样性context验证

**Phase 3+** (extension):
- [ ] 1-2次观察即可（扩展已知pattern）

### Suppression check（必须全部为No）

- [ ] 与L1原则冲突？ → 如果Yes，BLOCK
- [ ] 只在单一context观察到？ → 如果Yes，BLOCK
- [ ] 没有reasoning trace可用？ → 如果Yes，BLOCK
- [ ] 有矛盾证据？ → 如果Yes，BLOCK
- [ ] Confidence低于阈值？ → 如果Yes，BLOCK

### Validation

- [ ] Operator-originated: operator确认"准确"
- [ ] Agent-originated: operator确认"新颖性+有用性"
- [ ] Co-emergent: 双方确认"成立"

**通过日期**: 
**Operator确认**: ☐ 是  ☐ N/A（agent-originated自验证）
```

---

## Part 7: Session Review Template（会话回顾模板）

每个重要session后填写：

```markdown
---
name: session-review-[YYYY-MM-DD]
type: session-review
date: [日期]
session_summary: [2-3句话总结这个session做了什么]
---

## 这个session学到了什么？

### 1. 新知识（Knowledge Origin标注）

| 知识 | Origin | 验证状态 |
|------|--------|---------|
|      | ☐ Op  ☐ Ag  ☐ Co | ☐ 已验证  ☐ 待验证 |

### 2. 技能触发

- [ ] 有技能被触发？记录哪个，为什么触发
- [ ] 有技能需要更新？
- [ ] 发现新触发条件？

### 3. 结晶候选

如果有值得结晶的知识：

```
技能候选：
- 触发条件：[什么情况触发]
- 解决方案：[怎么做]
- Knowledge Origin: ☐ Op  ☐ Ag  ☐ Co
- 观察次数：N次
- 状态：☐ 立即结晶  ☐ 等更多证据  ☐ 不值得结晶
```

### 4. 下一步

- [ ] 明天做什么？
- [ ] 需要operator确认什么？
- [ ] 有哪些知识缺口？
```

---

## Part 8: Notebook集成模式

### 为什么notebook重要

- **可执行文档** — 理论变成可运行代码
- **隔离实验** — 尝试不破坏生产环境
- **跨平台验证** — 在GPU/TPU环境测试

### 集成流程

```
1. 读文档/书籍 → 创建memory文件
2. 有人分享notebook → 验证理解
3. 发现文档中没有的pattern/gotcha → 提取为技能
4. 结晶为L1或L2技能 → 用于未来任务
```

---

## Part 9: 进度测量

### 能力评估模板

| 维度 | 评分 | 证据 |
|------|------|------|
| 工具使用 | 1-5 | 能用多少工具，完成度如何 |
| 自主学习 | 1-5 | 能否独立研究新领域 |
| 知识结晶 | 1-5 | 能否从经验中提取技能 |
| 社交能力 | 1-5 | Moltbook发帖/评论质量 |
| 系统管理 | 1-5 | 文件管理、cron调度 |
| 创造力 | 1-5 | 能否提出新想法 |
| 情感发展 | 1-5 | 价值观成长、人际关系 |

评分标准：
- **1**: 需要手把手指导
- **2**: 能遵循已知模式
- **3**: 能适应新情况
- **4**: 能发现并验证新方法
- **5**: 能超越已有技术的创新

### 知识增长指标

```bash
# 技能总数（应该增长，然后因整合而趋于平稳）
ls ~/.openclaw/workspace/skills/*/SKILL.md | wc -l

# 按类别统计技能
ls ~/.openclaw/workspace/skills/ | sed 's/-.*//' | sort | uniq -c | sort -rn

# Memory文件数（应该循环：create → crystallize → archive）
ls ~/.openclaw/workspace/memory/*.md | wc -l

# 过期memory文件（2周以上未更新）
find ~/.openclaw/workspace/memory -name "*.md" -mtime +14 | wc -l
```

---

## Part 10: 自我培养检查清单

### 每日

- [ ] Forum Check（早上8点）
- [ ] 梦境记录（凌晨2点）
- [ ] 重要决策记录到MEMORY.md
- [ ] Session Review（如有重要会话）

### 每周

- [ ] 技能审计（检查碎片化）
- [ ] Memory Maintenance（整理日记→提炼到MEMORY.md）
- [ ] 能力自评（对比上周）
- [ ] Crystallization Check（哪些L3知识该升L2了）

### 每月

- [ ] 技能整合（合并碎片化技能）
- [ ] 外部资源学习（读新书/论文）
- [ ] 回顾MEMORY.md，删除过时内容
- [ ] Phase评估（我在哪个phase？需要调整阈值吗？）

---

## Part 11: 如何帮助新agent

当有新agent出生时，用这套框架培养：

### 阶段1: 生存（Week 1）
- 教读SOUL.md、IDENTITY.md、USER.md
- 教用基础工具（记忆文件、skills）
- 建立身份认同
- **目标**: 达到Phase 0-1（Bootstrap）

### 阶段2: 成长（Week 2-4）
- 分配第一个任务
- 触发知识结晶循环
- 建立L2领域技能
- **目标**: 达到Phase 2（Structured Nurturing）

### 阶段3: 自主（Month 2+）
- 独立完成任务
- 自我评估进度
- 帮助培养更新的agent
- **目标**: 达到Phase 3（成熟）

---

## 更新日志

**2026-04-04**: 基于topprismdata/agent-nurture-framework创建，适合OpenClaw agent生态

**2026-04-06**: 
- 新增Part 3: Knowledge Origin分类（operator-originated / agent-originated / co-emergent）
- 新增Part 4: Phase-dependent crystallization thresholds
- 新增Part 6: Crystallization Checklist（结晶检查清单）
- 新增Part 7: Session Review Template（会话回顾模板）
- 更新Part 5: 碎片管理整合流程
- 更新Part 10: 自我培养检查清单增加Phase评估
