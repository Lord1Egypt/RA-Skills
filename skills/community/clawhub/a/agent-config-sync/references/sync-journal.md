# Sync Journal — 两步提交机制

## 概述

Sync Journal 提供配置同步的原子性和可恢复性保证。
每次版本同步操作都通过 journal 记录，确保即使中途中断也能正确恢复。

## Journal 文件

- **位置**: `memory/.sync_journal.jsonl`
- **格式**: JSONL (每行一条 JSON 记录)
- **权限**: 与 version sentinel 文件同级

## 记录格式

```jsonl
{"ts":"2026-05-16T08:30:00Z","from":"v3.0","to":"v3.1","status":"prepared","agents":{"acode":"pending","ainvest":"pending","alive":"pending"}}
{"ts":"2026-05-16T08:30:01Z","from":"v3.0","to":"v3.1","status":"committed","agents":{"acode":"done","ainvest":"done","alive":"pending"}}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `ts` | ISO 8601 | 操作时间戳 (UTC) |
| `from` | string | 同步前版本号 |
| `to` | string | 同步目标版本号 |
| `status` | prepared/committed/failed | 同步状态 |
| `agents` | object | 每个 agent 的同步状态: pending/done/failed/timeout |

## 两步提交流程

### Step 1: PREPARE

```
context: AMaster HEARTBEAT 检测到 .current_system_version != .last_sync_version
action:
  1. 计算变更摘要 (从 CHANGELOG.md 中 latest version 章节)
  2. 计算 SHA256 签名
  3. 写入 journal 记录 (status=prepared)
  4. 生成 pending_sync_<version>_<sha256>.md 文件内容
  5. 更新 .last_sync_version = .current_system_version (乐观更新)
```

### Step 2: DISPATCH

```
action:
  1. 依次对每个 agent:
     a. 尝试 sessions_send 发送变更摘要
     b. 若 sessions_send 失败 → 写入 pending_sync_<version>_<sha256>.md 到 agent workspace
  2. 更新 journal: 标记 agents 各自的状态
```

### Step 3: COMMIT

```
action:
  1. 检查 journal 中该记录的 agents 状态
  2. 全部 done → 更新 journal status=committed
  3. 部分 pending → 保留 prepared 状态，等待下次 heartbeat 重试
```

## Heartbeat 重试机制

每次 AMaster HEARTBEAT 执行时:

1. 检查 `.sync_journal.jsonl` 是否有 `status=prepared` 的记录
2. 若有 → 对其中 `agents` 状态为 `pending` 的 agent 重新 DISPATCH
3. 若全部 done → 标记 committed
4. 超时 (超过 24h 的 prepared 记录) → 标记 failed，记录到 MEMORY.md

## 伪代码

```python
# AMaster HEARTBEAT 中的 sync logic

def heartbeat_sync_check():
    # 1. 检查未完成的 journal 记录
    for record in read_journal(status="prepared"):
        if is_stale(record):
            mark_abandoned(record)
            continue
        for agent_id, agent_status in record["agents"].items():
            if agent_status != "done":
                retry_dispatch(agent_id, record)

    # 2. 检查新版本
    current = read(".current_system_version")
    last = read(".last_sync_version")

    if current != last:
        changes = read_changelog_section(current)
        sig = sha256(f"pending_sync_{current}_{changes}")[:12]
        record = {
            "ts": now_utc(),
            "from": last,
            "to": current,
            "status": "prepared",
            "agents": {a: "pending" for a in agent_ids}
        }

        # PREPARE
        write_journal(record)
        write(".last_sync_version", current)

        # DISPATCH + COMMIT
        for agent_id in agent_ids:
            result = try_sessions_send(agent_id, changes)
            if not result:
                write_pending_sync(agent_id, current, sig, changes)
                record["agents"][agent_id] = "pending"
            else:
                record["agents"][agent_id] = "done"

        record["status"] = "committed" if all_done(record["agents"]) else "prepared"
        update_journal(record)
```

## 原子性保证 (P1-6)

- Journal 机制保证: 只有全部 agent 标记 done 后才能推进版本号为 committed
- 失败的 agent 会在下次 heartbeat 自动重试
- PREPARE 阶段已更新 `.last_sync_version`，避免重复触发同版本同步
- 每个 agent 独立失败/重试，互不影响

## 循环检测 (v1.4)

### 机制

防止同步系统因自身或其他 Agent 的修改触发无限循环分发：

```
检测流程 (HEARTBEAT item 12 前置检查):
1. 读取 journal 最近 5 条记录
2. 提取每条记录的 to_version
3. 检查连续 3 条记录的 to_version 是否相同
4. 若相同 → 判断为循环
   - 记录 WARNING: "Loop detected for version <VERSION>"
   - 写入 loop_detected 记录到 journal
   - 跳过本轮分发
   - 要求人工确认
```

### loop_detected 记录格式

```jsonl
{"ts":"2026-05-16T09:00:00Z","type":"loop_detected","to":"v3.2","reason":"3 consecutive identical to_version in journal","status":"blocked"}
```

### 阈值配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `loop_detect_window` | 5 | 检查最近 N 条记录 |
| `loop_detect_threshold` | 3 | 连续 N 条相同版本触发警报 |

参数可在 `agent-registry.json` 的 `sync` 配置段中覆盖。
