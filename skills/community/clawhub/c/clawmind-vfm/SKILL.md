---
name: clawmind
description: ClawMind — 自我进化 AI Agent 引擎，健康度驱动 + VFM 提案评分 + 经验记忆。依赖 OpenClaw 工作空间。当需要自我进化、自主驱动、健康度追踪、VFM 决策、经验存取时触发。
---

# mind — 自我进化引擎

AI Agent 的"心灵"：记忆与行动的统一体。**记忆**让它能从过去的错误中学习而不重复犯错，**自驱力**让它能持续自主向前。

灵感来源：Hermes Agent 的 Self-Evolving Agent Memory 机制——经验自动提取（intent + path + key_insight）+ 语义聚类。

## 核心架构

```
clawmind/
├── self_driver.py       ← 驱动：健康度 + VFM 评分 + 反思
├── state_manager.py     ← 状态：项目 / 任务 / 日志管理
├── quality_score.py     ← 评分：简报质量 5 维度评估
└── memory/
    └── memory_core.py   ← 记忆：经验存取（remember / recall）
```

**闭环协同**：
```
drive() → propose() 生成提案 → score_action() VFM 评分 → 执行
                                                      ↓
                            recall() 检索 ← remember() 沉淀
```

---

## 健康度系统

### `calc_health(state) → float`

```
health = 0.4 + success*0.25 + progress*0.2 + momentum*0.1 - fail_penalty*0.15 + completion*0.1
```

| 分量 | 范围 | 说明 |
|------|------|------|
| 基础分 | 0.4 | 默认健康起点 |
| 成功率 | 0~0.25 | 最近5条日志中成功条目的比例 |
| 进度分 | 0~0.2 | 当前任务完成百分比 |
| 势头分 | 0~0.1 | 最近3条进度是否递增 |
| 失败惩罚 | 0 或 -0.15 | 连续3条全部失败时触发 |
| 完成奖励 | 0 或 +0.1 | 任何条目达到100%时触发 |

### 健康度阈值与行动

| 健康度 | 状态 | 行动建议 |
|--------|------|----------|
| < 0.3 | 危险 | 降低目标，拆解为最小可测试单元 |
| 0.3~0.4 | 偏低 | 减少每次工作量，确保有可交付进展 |
| 0.4~0.7 | 尚可 | 保持节奏，专注完成当前步骤 |
| ≥ 0.7 | 良好 | 挑战更多，推进目标 |

---

## VFM 提案评分

### `propose(state, context="") → list[dict]`

根据当前状态生成改进提案列表，包含 `description`、`expected_delta_health`、`tags`。

**典型提案**：

| 提案 | 触发条件 | delta |
|------|----------|-------|
| 推进当前任务 | 有任务进行中 | 0.1 |
| 从经验学习 | 最近有成功日志 | 0.05 |
| 拆解为子任务 | 进度 < 30% | 0.12（每个子任务）|
| 检查技能更新 | 总是包含 | 0.03 |
| 知识沉淀 | 最近有核心发现 | 0.04 |

**自动任务拆解**：进度 < 30% 时，`propose()` 自动调用 `_decompose_task()`，根据关键词模式将任务拆为 3~4 个子任务：

- **发布/上传类** → 准备 → 执行 → 验证 → 完成
- **创建/开发类** → 规划 → 构建 → 测试 → 完成
- **研究/探索类** → 调研 → 分析 → 总结 → 归档
- **修复/调试类** → 定位 → 修复 → 验证 → 沉淀教训
- **整理/归档类** → 清点 → 分类 → 验证 → 更新索引

### `score_action(proposal, driver) → float`

**VFM 公式**：`Value × Feasibility × Momentum × 100`

- **Value**：低健康时高 delta 提案价值更高
- **Feasibility**：成功经验多时提升，连续低迷时降低
- **Momentum**：健康度 ≥0.6 → 0.9，≥0.4 → 0.6，<0.4 → 0.3

### `select_best_action(proposals, driver) → dict`

返回得分最高的提案及完整评分列表。

---

## 经验记忆

### `remember(experience, source, tags) → None`

将任务结果或认知存入经验库。

```python
remember("Docker 网络冲突解决，教训：必须指定 --subnet",
         source="task", tags=["docker", "debug"])
```

### `recall_experiences(query, tags, limit) → list[dict]`

语义检索相关经验。

```python
results = recall_experiences("docker", limit=3)
for r in results:
    print(r['task_intent'], '|', r['key_insight'][:60])
```

---

## 状态管理

```python
from state_manager import push_project, set_task, add_log

push_project("新项目", "目标描述", "active")
set_task("任务名", 2, 5, "下一步动作")
add_log("心跳 10:00：完成模块 A 开发")
```

---

## CLI 用法

```bash
# 主循环
python3 self_driver.py

# 查看引擎状态
python3 self_driver.py status

# 提案评分报告
python3 self_driver.py propose
```

---

## 反思问题（健康度 < 0.4 时触发）

1. 当前任务卡在哪里？是思路问题还是执行问题？
2. 有没有之前学过的经验可以用到这里？
3. 这一步是否真的值得做，还是在逃避更核心的问题？
4. 如果这个问题明天还要做，今天最少要完成哪一步？
5. 有没有把一个复杂问题拆得足够小？

---

## 文件索引

| 文件 | 作用 |
|------|------|
| `scripts/self_driver.py` | 自驱力引擎核心 |
| `scripts/state_manager.py` | 状态管理 |
| `scripts/quality_score.py` | 简报质量评分 |
| `scripts/memory/memory_core.py` | 经验记忆核心 |
| `references/state-manager.md` | state_manager 完整接口 |
| `references/vfm-design.md` | VFM 评分设计详解 |
