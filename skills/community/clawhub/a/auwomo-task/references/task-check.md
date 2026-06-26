# task-check

前置检查命令，用于在执行操作前确认任务系统状态。

## 三个检查子命令

### check init

检查是否已初始化 — 当前用户是否有可挂载的顶层主线任务。

```bash
auwomo task check init --format json
```

**输出字段**：
- `ok` — 是否已初始化（有至少一个可挂载的顶层主线）
- `status` — `"initialized"` 或 `"missing"`
- `count` — 可挂载的候选数量
- `candidates[]` — 每个候选的 guid, summary, description, depth, child_count

**使用场景**：
- 新用户首次使用前
- 不确定是否有可用主线时
- 如果 `status=missing`，需要引导用户走 `task-create` 流程

---

### check attachable

查找当前可以挂载记录的候选任务。

```bash
auwomo task check attachable --format json
```

**输出字段**：
- `ok` — 是否有可挂载候选
- `status` — `"attachable"` 或 `"blocked"`
- `attachable_count` — 可挂载的候选数
- `candidate_count` — 总候选数（含 blocked）
- `window` — 查询的时间窗口（默认 30 天）
- `candidates[]` — 每个候选的详细信息：
  - `attachable` — 是否可挂载
  - `state` — `"attachable"` 或 `"blocked"`
  - `reasons` — 不可挂载的原因列表（硬阻断）
  - `warnings` — 可挂载但有提示（如缺少描述）
  - `depth` — 在任务树中的深度
  - `lineage` — 祖先链

**候选排序**：
- attachable 在前，blocked 在后
- 无 warning 的在有 warning 的前面
- 深度越深越优先（最贴近当前工作的子线排前面）

**不可挂载的原因（reasons）**：
- `not_app_created` — 不是由 app/bot 创建
- `not_active` — 已完成
- `not_structure` — 不是结构任务
- `record_title` — 标题是 [记录]

**警告（warnings）** — 可挂载但建议处理：
- `missing_description` — 缺少描述，建议用 `task update <guid> --desc "..."` 补充

**使用场景**：
- 在执行 `task record` 前确定挂载点
- 帮用户选择合适的父任务
- 发现 `missing_description` 时，主动建议补充描述

---

### check yesterday-record

检查昨天是否有进展记录。

```bash
auwomo task check yesterday-record --format json
```

**输出字段**：
- `ok` — 昨天是否有记录
- `status` — `"has_records"` 或 `"no_records"`
- `count` — 记录数量
- `window` — 昨天的时间范围（start..end）
- `records[]` — 每条记录的 guid, summary, completed_at, lineage

**使用场景**：
- 日报生成前检查是否有素材
- 提醒用户补记录
- 定时检查用户是否忘记记录进展

---

## 通用选项

所有 check 命令支持：
- `--team` — 包含下属的任务（管理员视角）
- `--format json` — 机器可读输出
