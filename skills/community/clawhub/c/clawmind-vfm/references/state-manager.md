# state_manager.py — 接口文档

## 文件位置

`/home/node/.openclaw/workspace/skills/project-manager/scripts/state_manager.py`

## 核心接口

### `push_project(name: str, goal: str, status: str = "active")`
创建或更新项目。

```python
push_project("my-project", "目标描述", "active")
```

### `set_task(task: str, step: int, total: int, next_action: str)`
设置当前任务进度。

```python
set_task("完成任务X", 2, 5, "写测试代码")
```

### `add_log(entry: str)`
追加日志条目。

```python
add_log("心跳 10:00：完成了模块A开发")
```

### `get_state() → dict`
读取完整状态（项目 + 任务 + 日志）。

### `_load(path) / _save(path, data)`
内部状态读写。

## 状态文件

- `state/current_state.json` — 项目/任务/日志
- `state/self_driver.json` — 引擎状态（由 self_driver.py 管理）

## 注意事项

- 项目名唯一，后面的 `push_project` 会覆盖前面的
- 日志自动带时间戳，不需要手动加
- 任务完成记得把 `progress_pct` 设为 100
