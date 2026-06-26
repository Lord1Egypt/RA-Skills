# task-context

查询当前任务上下文，了解任务树结构和最近进展。

## 场景

- 用户问"我的任务怎么样了"
- 需要了解当前在做什么
- 准备生成汇报前先获取上下文

## 操作步骤

### 1. 获取轻量上下文（默认）

```bash
auwomo task context --duration 7d
```

输出包含：
- 活跃结构列表（active_structures）
- 最近记录（recent_records）
- 昨日记录（yesterday_records）
- 树状视图（tree_lines）

### 2. 获取详细上下文（含 description）

```bash
auwomo task context --duration 7d -d
```

加 `-d` 后，每个任务节点会附带 description 字段，帮助理解具体工作内容。

### 3. 获取团队上下文

```bash
auwomo task context --duration 7d --team
```

`--team` 会包含当前用户所有下属的任务。

### 4. 调整时间窗口

```bash
auwomo task context --duration 30d    # 最近 30 天
auwomo task context --duration 2w     # 最近 2 周
```

支持的时间单位：`M`(分钟), `h`(小时), `d`(天), `w`(周), `m`(月), `y`(年)

## 何时使用 `-d`（详细模式）

### 不需要 `-d` 的场景（轻量模式足够）：

- 生成日报、周报（标题 + 树结构已够写汇报）
- 简单状态查询（"我最近做了啥"）
- 检查是否有新记录
- cron 定时汇报触发

### 需要 `-d` 的场景：

- 用户问某个主线/子线具体是做什么的
- 用户要求增删或调整主线/子线结构（需要理解每个的含义才能决策）
- 深入对话：用户对某个任务感兴趣，想了解更多
- 排查 `missing_description` 问题
- 写详细的月度/季度总结

### 原则

轻量模式是默认选择。只在需要理解"这个任务到底是什么"时才用 `-d`。日常记录和汇报不需要加载描述——标题本身已经传达了足够信息。

## 输出解读（JSON 模式）

```bash
auwomo task context --duration 7d --format json
```

关键字段：
- `summary.active_structure_count` — 活跃结构任务数
- `summary.recent_record_count` — 时间窗口内的记录数
- `summary.yesterday_record_count` — 昨日记录数
- `tree_lines` — 缩进树状文本行
- `active_structures[]` — 每个活跃结构的详细信息：
  - `guid`, `summary`, `status` — 基本信息
  - `depth`, `child_count`, `parent_guid` — 树结构
  - `lineage_summary` — 上级脉络
  - `assignee` — 负责人名字（`--team` 时按此分组）
  - `assignee_open_id` — 负责人飞书 open_id
  - `updated_at` — 最后更新时间（RFC3339，用于停滞检测）
  - `description` — 任务描述（仅 `-d` 模式）
- `recent_records[]` — 最近记录的 guid, summary, completed_at, assignee, assignee_open_id, updated_at

> **团队模式**：`--team` 返回包含所有下属的聚合数据。按 `assignee` 或 `assignee_open_id` 分组可得到按人视角。

## 错误处理

- 身份未配置 → 先运行 `auwomo identity whoami` 确认
- lark-cli 不可用 → 检查 `which lark-cli`
- 结果为空 → 可能需要先通过 `task check init` 检查初始化状态
