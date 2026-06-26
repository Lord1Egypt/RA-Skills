---
name: cognitive-topology
description: Agent认知拓扑引擎。自动将复杂任务分裂为多个独立分支，并行执行后汇总整合。触发场景：(1)复杂问题需要多角度分析 (2)多独立子任务需要并行执行 (3)需要清晰追踪思维分支 (4)用户说"分叉"、"分支分析"、"多线程"时。使用 sessions_spawn 创建分支，分支结果写入 L2 文件，Main Session 读取并整合。
---

# Cognitive Topology

把复杂任务的「一条直线」变成「多分支并行」。

## 何时触发

当任务符合以下任一条件时，自动启用本技能：
- 需要同时分析 N 个不同方向/角度
- 任务可拆分为相互独立的子任务
- 问题复杂，需要递归分解
- 用户明确说「分叉」「分支」「多角度」

## 核心工作流

### Step 1: Fork - 创建分支

使用 `sessions_spawn` 创建独立分支：

```
sessions_spawn(
  mode="session",
  runtime="subagent",
  task="<具体分支任务>",
  label="ct-<序号>-<简短描述>"
)
```

每个分支有独立 Session ID，互不干扰。

### Step 2: Branch - 分支执行

- 分支 Agent 独立执行自己的任务
- 完成后将结论写入标准 L2 文件：`~/.openclaw/workspace/cognitive-topology/branches/<branch_id>_L2.md`
- L2 格式：## 结论\n\n<具体结论>\n\n## 依据\n\n<分析依据>

### Step 3: Integrate - 整合

Main Session 等待所有分支完成，读取所有 L2 文件，生成 synthesis：

```bash
cat ~/.openclaw/workspace/cognitive-topology/branches/*_L2.md
```

## 目录结构

```
~/.openclaw/workspace/cognitive-topology/
├── branches/              # 分支工作目录
│   ├── ct-1_anal_ai_L2.md  # 分支1的L2
│   ├── ct-2_anal_chip_L2.md # 分支2的L2
│   └── ...
├── topology_latest.json    # 当前拓扑状态
└── synthesis.md            # 整合结果
```

## 关键约束

- 分支只写 L2，不读自己的 L2
- Main Session 读所有 L2，不直接读分支的 Session 历史
- 分支间不直接通信
- 跨分支信息通过 Main Session 的 synthesis 传播

## 简化实现说明

无 UI，星空图用文本树替代：

```markdown
🌐 认知拓扑
├── branch-1 [分析AI板块]
│   └── ✅ 已完成
├── branch-2 [分析半导体]
│   └── ⏳ 进行中
└── branch-3 [分析新能源]
    └── ⏳ 待启动
```

## 典型场景示例

**场景：分析 A 股三个方向的机会**

Main Session 收到任务后：
1. 判断需要分裂为3个独立分支
2. 同时 spawn 3 个分支 Agent
3. 分支1分析AI板块 → 写 L2
4. 分支2分析半导体 → 写 L2
5. 分支3分析新能源 → 写 L2
6. Main 汇总 L2 → 生成 synthesis → 回复用户
