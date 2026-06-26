# 编排模式（Orchestration Patterns）

> 来源：codex-orchestration skill

## 何时需要 update_plan

当满足任一条件时使用：
- 超过 2 个步骤
- 并行工作有帮助
- 情况不明确或高风险

原则：
- 3-6 步，最多
- 每步一句话
- 只标记 1 步 `in_progress`
- 完成一步或改变方向时更新

简单任务直接跳过 plan。

---

## 模式 A：三角评审（Fan-out, Read-only）

**适用：** 多角度审视同一产物

```
Orchestrator
  ├── Worker 1: Review (LENS: clarity)
  ├── Worker 2: Review (LENS: correctness)
  └── Worker 3: Review (LENS: risks)
        ↓
  Merge → 单一排名列表，去重，推荐
```

---

## 模式 B：评审 → 修复（Serial Chain）

**适用：** 流水线式清理

```
Reviewer → 问题列表（按影响排序）
    ↓
Implementer → 修复 top items
    ↓
Verifier → 检查结果
```

---

## 模式 C：侦察 → 行动 → 验证（Classic）

**适用：** 缺乏上下文是最大风险

```
Scout → 收集最小上下文
    ↓
Orchestrator → 消化信息，选择方案
    ↓
Implementer → 执行
    ↓
Verifier → 合理检查
```

---

## 模式 D：分片（Fan-out, then Merge）

**适用：** 工作可清晰划分（章节、模块、数据集）

```
Worker A → Section A
Worker B → Section B
Worker C → Section C
    ↓
Merge → 统一一致性
```

---

## 模式 E：研究 → 综合 → 下一步

**适用：** 主要是网络搜索和判断

```
Worker 1..N → 并行收集资料
    ↓
Orchestrator → 综合决策简报
    ↓
Next actions
```

---

## 模式 F：选项冲刺（Options Sprint）

**适用：** 选方向（大纲、方法计划、UI）

```
Worker 1 → Option A
Worker 2 → Option B
Worker 3 → Option C
    ↓
Orchestrator → 选择 + 细化
```

---

## 并行原则

**适合并行的：**
- 侦察和摸底
- 不同角度的评审
- 网络研究
- 长时间运行检查（测试、构建、分析）
- 草稿替代方案

**避免并行的：**
- 多个 worker 编辑同一个产物
- 默认规则：**多读者，一作者**

---

## 主 agent 习惯

- 委托前先自己浏览一下产物
- 指令短、上下文丰富——不要把整个 skill 塞给 worker
- Worker 理解错了 → 重跑，不要争论
- 不转发原始 worker 输出，除非已经很干净

---

*来源：codex-orchestration skill*
