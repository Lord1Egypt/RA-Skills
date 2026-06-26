# HEARTBEAT Item 12 — Config Change Force Sync

Add this to the AMaster's HEARTBEAT.md checklist:

```markdown
12. ⭐ 配置变更同步（含版本冲突管理 v1.4）
    ┌─ 前置检查 ───────────────────────────────────────────
    │ a. 循环检测: 检查 journal 最近 5 条，连续 3 条相同版本 → 报警跳过
    │ b. 分发锁: 上轮 prepared < 2min → 跳过；>= 2min → 超时处理；>= 10min → abandoned
    │ c. 自身升级: 影响范围含 "agent-config-sync" → 走 isolated 流程
    ├─ 版本检测 ───────────────────────────────────────────
    │ d. 哨兵对比: .current != .last_sync → 有新版本
    │ e. 回滚检测: current < last_sync → 回滚操作，走 revert 流程
    │ f. 批量窗口: batch_mode=true → 等待 batch_window_sec，合并后分发
    ├─ 分发准备 ───────────────────────────────────────────
    │ g. 读 CHANGELOG 最新版本 (含 depends_on / 协同依赖字段)
    │ h. 动态获取 agent 列表 (registry)
    │ i. 生成 SHA256 签名 + TTL 过期时间
    │ j. PREPARE journal 记录 (含版本链信息)
    ├─ 分发执行 ───────────────────────────────────────────
    │ k. 逐个 agent: sessions_send 优先, pending_sync 回退
    │ l. 离线检测: 若 agent 已离线 > 1h → 生成累积追赶包
    │ m. COMMIT journal: 全部 done → committed; 部分 done → prepared
    └─ 收尾 ───────────────────────────────────────────────
    │ n. 更新 .last_sync_version
    │ o. 清理超过 TTL 的过期 prepared 记录 → abandoned
    │ p. 失败不阻断 heartbeat
```

## Structured CHANGELOG Format

每条版本条目必须使用标准 Markdown 锚点，方便语义化解析和增量读取。

### 格式规范

```markdown
# 系统变更日志

## v3.2 (2026-05-16)
**变更类型**: 🖥️ 系统代码
**影响范围**: 量化交易系统, 价格对比
**变更人**: AMaster
**紧急程度**: normal
**前置依赖**: v3.1
**协同依赖**: (无)

### 修改
- 优化回测引擎参数计算逻辑
- 修复价格对比时间戳偏移问题

### 新增
- 添加自动止损阈值配置

### 废弃
- （暂无）

## v3.1 (2026-05-15)
**变更类型**: 🖥️ 系统代码 / 🤖 Agent配置
**影响范围**: all agents
**变更人**: AMaster
**紧急程度**: high
**前置依赖**: v3.0
**协同依赖**: (无)

### 修改
- 所有 agent TOOLS.md 新增 sessions_yield
- 更新 AMaster SOUL.md 协同规则

### 新增
- （暂无）

### 废弃
- （暂无）
```

### 读取策略 (P0-3)

同步时**只发送最新版本的数据**，而非全量 CHANGELOG：

```python
def read_latest_changelog_section(changelog_path):
    """Read only the most recent version's section from CHANGELOG.md"""
    with open(changelog_path) as f:
        content = f.read()

    # Split by ## headers and take the first version section
    sections = re.split(r'(?=^## v\d)', content, flags=re.MULTILINE)
    if len(sections) > 1:
        return sections[1].strip()  # First version section after title
    return None
```

### 版本号格式

- 遵循 `v<MAJOR>.<MINOR>[.<PATCH>]`
- 例如: `v1.0`, `v3.2`, `v5.1.3`
- 变化规则:
  - MAJOR: 整体架构变更
  - MINOR: 功能新增/修改
  - PATCH: 修复/补丁

### 可选字段（v1.4 新增）

| 字段 | 格式 | 说明 |
|------|------|------|
| `**Depends On**: vX.Y` | `vX.Y` | 前置依赖版本。Agent 应用时检查自己当前版本是否 >= 前置版本 |
| `**协同依赖**: [agent_id]` | agent ID 列表 | 需要协同的 Agent。多 Agent 联合变更时，标记依赖关系确保正确处理顺序 |

## Infrastructure files reference

### Version sentinel files
```
memory/.current_system_version  → git-worthy monotonically increasing version
memory/.last_sync_version       → set to current after successful sync
memory/CHANGELOG.md             → structured full change log
memory/.sync_journal.jsonl      → sync atomicity journal
```

### Sync dispatch (updated for v1.1 with journal)

#### Offline Catch-Up (v1.4)

When an agent was offline (missed one or more sync cycles), the Master generates a cumulative catch-up package:

```
离线追赶逻辑 (Master 端):

1. 检查 agent 的 .agent_sync_version (从 agent workspace/memory/ 读取)
2. 对比 .current_system_version:
   - IF agent.agent_sync_version == current → agent is up-to-date
   - IF agent.agent_sync_version < current → agent has fallen behind

3. 计算版本差距:
   gap_versions = 所有 CHANGELOG 条目中，版本 > agent_version 且 <= current_version

4. 追赶策略:
   IF len(gap_versions) == 1:
     → 直接分发该版本
   ELIF len(gap_versions) >= 2 AND depends_on 链完整:
     → 生成累积追赶包: 包含从 agent 最后版本到最新版本的所有变更摘要
     → 单文件分发 (pending_sync_<LATEST>_<SHA>.md)
     → 文件头 前置字段 = agent 当前版本
   ELSE (链断):
     → 按版本顺序依次分发每个 gap_version
     → 按依赖链排序
```

```
离线追赶逻辑 (Agent 端):

启动/恢复时:
  1. 读取自己的 .agent_sync_version
  2. 列出 pending_sync_*.md
  3. 对于所有版本 > .agent_sync_version 的文件:
     a. 若 depends_on 链覆盖 → 使用版本折叠 (一次性跳到最新)
     b. 若链断 → 按版本顺序逐个处理
  4. 每处理一个版本 → 更新 .agent_sync_version
```

#### Dispatch Lock (v1.4)

Before each dispatch cycle, the Master checks for an active dispatch window:

```
前置检查 — 分发锁:
  1. 读取 journal 中最后一条 status=prepared 的记录
  2. 计算 elapsed = now - record.ts
  3. 判断:
     - IF elapsed < 2min → 分发窗口未关闭 → SKIP 本轮分发
     - IF 2min <= elapsed < 10min → 标记为 timeout → 重新分发
     - IF elapsed >= 10min → 标记为 abandoned → 重新分发 (新 journal record)
  4. Loop detection check (见下)
  5. Self-upgrade check (impact range includes agent-config-sync)
  6. Only after ALL checks pass → proceed with dispatch
```

#### Loop Detection (v1.4)

Prevents infinite sync loops when a change triggers re-dispatch of the same version:

```
循环检测逻辑:

1. 读取 journal 最近 5 条记录 (tail -5 .sync_journal.jsonl)
2. 提取每条记录的 to_version
3. 检查: 连续 3 条记录的 to_version 相同
4. 若检测到循环:
   - 写入 WARNING 到 MEMORY.md: "Loop detected for version <VERSION>"
   - Journal 新增记录: {"type":"loop_detected","to":"<VERSION>","ts":"..."}
   - SKIP 本轮分发
   - 要求人工确认后继续
5. 若未检测到循环 → 继续 dispatch 流程
```

Journal loop_detected record format:
```jsonl
{"ts":"2026-05-16T09:00:00Z","type":"loop_detected","to":"v3.2","reason":"3 consecutive identical to_version in journal","status":"blocked"}
```

```python
# Pseudocode for sync dispatch with journal — v1.4 enhanced
import json, time, hashlib, re, os
from datetime import datetime, timezone, timedelta

TTL_HOURS = 24  # Configurable via agent-registry.json sync.ttl_hours
DISPATCH_TIMEOUT_MIN = 2
DISPATCH_ABANDON_MIN = 10
LOOP_WINDOW = 5
LOOP_THRESHOLD = 3
BATCH_WINDOW_SEC = 300  # Configurable via agent-registry.json sync.batch.window_sec
SELF_PROTECT_BLACKLIST = ["HEARTBEAT.md", "BOOTSTRAP.md", "SKILL.md", "scripts/",
                           "SECURITY.md", "references/"]

def heartbeat_sync_check(agent_ids, memory_dir, workspace_base, agent_workspaces):
    """Enhanced HEARTBEAT item 12 — full sync lifecycle"""

    # ── 0. Retry pending records ──────────────────────────────
    for record in read_journal(status="prepared"):
        elapsed = (now_utc() - parse_ts(record["ts"])).total_seconds()
        if elapsed > TTL_HOURS * 3600:
            # Expired prepared record → mark abandoned
            record["status"] = "abandoned"
            record["reason"] = f"TTL exceeded ({TTL_HOURS}h)"
            update_journal(record)
            continue
        if elapsed < DISPATCH_TIMEOUT_MIN * 60:
            # Dispatch window still open → skip this record
            continue
        # Retry dispatch for still-pending agents
        for agent_id, agent_status in record["agents"].items():
            if agent_status != "done":
                retry_dispatch_agent(agent_id, record, workspace_base,
                                     agent_workspaces)

    # ── 1. Read version sentinels ────────────────────────────
    current_ver = read(f"{memory_dir}/.current_system_version").strip()
    last_ver = read(f"{memory_dir}/.last_sync_version").strip()

    if current_ver == last_ver:
        return  # No changes

    # ── 2. Rollback detection ─────────────────────────────────
    if version_less(current_ver, last_ver):
        handle_rollback(current_ver, last_ver, memory_dir, workspace_base,
                        agent_ids, agent_workspaces)
        return

    # ── 3. Dispatch lock ──────────────────────────────────────
    last_prepared = get_last_journal_entry(status="prepared")
    if last_prepared:
        elapsed = (now_utc() - parse_ts(last_prepared["ts"])).total_seconds()
        if elapsed < DISPATCH_TIMEOUT_MIN * 60:
            # Dispatch window still open — skip this cycle
            return
        elif DISPATCH_TIMEOUT_MIN * 60 <= elapsed < DISPATCH_ABANDON_MIN * 60:
            # Timed out → mark and re-dispatch
            last_prepared["status"] = "timeout"
            update_journal(last_prepared)

    # ── 4. Loop detection ─────────────────────────────────────
    recent = read_journal_last_n(LOOP_WINDOW)
    to_versions = [r["to"] for r in recent if "to" in r]
    if len(to_versions) >= LOOP_THRESHOLD and \
       len(set(to_versions[-LOOP_THRESHOLD:])) == 1:
        loop_ver = to_versions[-1]
        log_warning(f"Loop detected for version {loop_ver}")
        write_journal({
            "ts": now_utc().isoformat(),
            "type": "loop_detected",
            "to": loop_ver,
            "reason": f"{LOOP_THRESHOLD} consecutive identical to_version",
            "status": "blocked"
        })
        return  # Skip this dispatch cycle

    # ── 5. Read CHANGELOG + self-upgrade check ────────────────
    changelog = read(f"{memory_dir}/CHANGELOG.md")
    latest_section = extract_latest_section(changelog, current_ver)

    # Parse impact range from CHANGELOG entry
    impact_range = parse_field(latest_section, "影响范围")
    depends_on = parse_field(latest_section, "前置依赖") or last_ver
    priority = parse_field(latest_section, "紧急程度") or "normal"

    # Check if this change affects agent-config-sync itself
    is_self_upgrade = False
    for blacklisted in SELF_PROTECT_BLACKLIST:
        if blacklisted in impact_range or "agent-config-sync" in impact_range:
            is_self_upgrade = True
            break

    if is_self_upgrade:
        handle_isolated_sync(current_ver, last_ver, latest_section,
                             memory_dir, agent_ids, agent_workspaces)
        return

    # ── 6. Batch mode check ───────────────────────────────────
    batch_mode = get_sync_config("batch.mode") == "auto"
    if batch_mode:
        batch_id = f"batch_{now_utc().strftime('%Y%m%d_%H%M')}"
        # Check if there's already an open batch window
        open_batch = get_last_journal_entry(status="batched", batch_id__startswith="batch_")
        if open_batch:
            elapsed = (now_utc() - parse_ts(open_batch["ts"])).total_seconds()
            if elapsed < BATCH_WINDOW_SEC:
                # Add to existing batch
                open_batch["accumulated_versions"].append(current_ver)
                open_batch["accumulated_changes"].append(latest_section)
                update_journal(open_batch)
                return
            else:
                # Batch window closed → merge and dispatch
                handle_batch_commit(open_batch, memory_dir, workspace_base,
                                    agent_ids, agent_workspaces)

    # ── 7. Generate signature ─────────────────────────────────
    sig = hashlib.sha256(
        f"pending_sync_{current_ver}_{latest_section[:200]}".encode()
    ).hexdigest()[:12]

    # ── 8. PREPARE journal ────────────────────────────────────
    expires_at = (now_utc() + timedelta(hours=TTL_HOURS)).isoformat()
    record = {
        "ts": now_utc().isoformat(),
        "type": "normal",
        "from": last_ver,
        "to": current_ver,
        "depends_on": depends_on,
        "status": "prepared",
        "priority": priority,
        "changelog_section": parse_field(latest_section, "变更类型"),
        "ttl_hours": TTL_HOURS,
        "agents": {}
    }
    # Initialize agent statuses
    for agent_id in agent_ids:
        record["agents"][agent_id] = {"status": "pending", "ts": None}

    append_journal(f"{memory_dir}/.sync_journal.jsonl", record)

    # ── 9. Update last_sync_version optimistically ────────────
    _atomic_write(f"{memory_dir}/.last_sync_version", current_ver)

    # ── 10. DISPATCH to each agent ────────────────────────────
    generated_at = now_utc().isoformat()
    for agent_id in agent_ids:
        agent_ws = agent_workspaces.get(agent_id)
        if not agent_ws:
            record["agents"][agent_id]["status"] = "skipped"
            record["agents"][agent_id]["reason"] = "no_workspace"
            continue

        # Offline catch-up check
        agent_version_file = f"{agent_ws}/memory/.agent_sync_version"
        agent_version = read(agent_version_file).strip() if os.path.exists(agent_version_file) else None

        if agent_version and version_less(agent_version, last_ver):
            # Agent is far behind → generate cumulative catch-up
            content = generate_catchup_content(agent_version, current_ver, changelog, sig)
        else:
            content = format_sync_content(current_ver, latest_section, sig,
                                          generated_at, expires_at, priority,
                                          depends_on)

        try:
            sessions_send(agentId=agent_id, message=content)
            record["agents"][agent_id] = {"status": "done", "ts": now_utc().isoformat()}
        except RuntimeError:
            # Fallback to file
            ws = f"{workspace_base}-{agent_id}"
            filename = f"pending_sync_{current_ver}_{sig}.md"
            write(f"{ws}/{filename}", content)
            record["agents"][agent_id] = {"status": "pending", "ts": None}

    # ── 11. COMMIT ────────────────────────────────────────────
    all_done = all(a["status"] == "done" for a in record["agents"].values())
    record["status"] = "committed" if all_done else "prepared"
    update_last_journal_entry(f"{memory_dir}/.sync_journal.jsonl", record)

    # ── 12. Cleanup expired prepared records ──────────────────
    cleanup_abandoned_records(memory_dir, TTL_HOURS)


def handle_rollback(target_ver, current_ver, memory_dir, workspace_base,
                    agent_ids, agent_workspaces):
    """Handle version rollback: current < last_sync"""
    sig = hashlib.sha256(
        f"revert_sync_{current_ver}_to_{target_ver}".encode()
    ).hexdigest()[:12]

    record = {
        "ts": now_utc().isoformat(),
        "type": "revert",
        "from": current_ver,
        "to": target_ver,
        "status": "prepared",
        "agents": {}
    }

    for agent_id in agent_ids:
        ws = agent_workspaces.get(agent_id)
        if not ws:
            continue
        revert_file = f"{ws}/revert_sync_{current_ver}_to_{target_ver}_{sig}.md"
        content = f"""# Revert Sync — {current_ver} → {target_ver}

**类型**: revert_sync
**回滚到**: {target_ver}
**生成时间**: {now_utc().isoformat()}
**签名**: {sig}

## 操作指令
1. 从 memory/.sync_snapshots/{target_ver}_pre/ 恢复文件
2. 验证 SHA256 checksums (参考 snapshot_manifest.json)
3. 更新 memory/.agent_sync_version = {target_ver}
4. 删除本文件
"""
        write(revert_file, content)
        record["agents"][agent_id] = {"status": "pending", "ts": None}

    append_journal(f"{memory_dir}/.sync_journal.jsonl", record)
    _atomic_write(f"{memory_dir}/.last_sync_version", target_ver)


def handle_isolated_sync(version, last_ver, changelog_section, memory_dir,
                         agent_ids, agent_workspaces):
    """Handle self-upgrade via isolated sync flow"""
    sig = hashlib.sha256(
        f"isolated_sync_{version}_{changelog_section[:200]}".encode()
    ).hexdigest()[:12]

    isolated_file = f"{memory_dir}/isolated_sync_{version}_{sig}.md"
    content = f"""# Isolated Sync — agent-config-sync Self-Upgrade

**类型**: isolated_sync
**版本**: {version}
**生成时间**: {now_utc().isoformat()}
**签名**: {sig}

{changelog_section}

## 重要
此文件不是通过正常 HEARTBEAT 分发，而是要求 Agent 下次启动时在 BOOTSTRAP 检查中主动请求升级。
"""
    write(isolated_file, content)

    # Notify agents via BOOTSTRAP-visible notification (not direct dispatch)
    for agent_id in agent_ids:
        ws = agent_workspaces.get(agent_id)
        if ws and os.path.exists(f"{ws}/BOOTSTRAP.md"):
            note = f"\n⚠️ agent-config-sync 系统需要升级: 见 master memory/isolated_sync_{version}.md\n"
            append(f"{ws}/BOOTSTRAP.md", note)

    write_journal({
        "ts": now_utc().isoformat(),
        "type": "isolated",
        "from": last_ver,
        "to": version,
        "status": "prepared",
        "agents": {a: {"status": "notified", "ts": now_utc().isoformat()}
                   for a in agent_ids}
    })


def handle_batch_commit(batch_record, memory_dir, workspace_base,
                        agent_ids, agent_workspaces):
    """Merge accumulated batch versions into single dispatch"""
    versions = batch_record["accumulated_versions"]
    changes = batch_record["accumulated_changes"]

    # Merge: use highest version, combine all change descriptions
    final_version = max(versions, key=version_sort_key)
    combined_content = "\n\n".join(changes)
    sig = hashlib.sha256(
        f"batch_sync_{final_version}_{combined_content[:200]}".encode()
    ).hexdigest()[:12]

    batch_record["status"] = "committed"
    batch_record["final_version"] = final_version
    batch_record["batch_size"] = len(versions)
    update_journal(batch_record)

    # Dispatch as single cumulative sync
    for agent_id in agent_ids:
        ws = f"{workspace_base}-{agent_id}"
        filename = f"pending_sync_{final_version}_{sig}.md"
        content = format_batch_sync_content(final_version, combined_content, sig)
        write(f"{ws}/{filename}", content)


def generate_catchup_content(agent_version, target_version, full_changelog, sig):
    """Generate cumulative catch-up for an agent that fell behind"""
    gap_entries = extract_version_range(full_changelog, agent_version, target_version)
    combined = "\n\n".join(gap_entries)

    generated_at = now_utc().isoformat()
    expires_at = (now_utc() + timedelta(hours=TTL_HOURS)).isoformat()

    return f"""## 累积追赶包 — {agent_version} → {target_version}

**类型**: pending_sync (cumulative catch-up)
**累积范围**: {agent_version} → {target_version}
**生成时间**: {generated_at}
**过期时间**: {expires_at}
**签名**: {sig}

{combined}

## 操作指令
1. 版本差距: {agent_version} → {target_version} ({len(gap_entries)} versions)
2. 检查 depends_on 链完整性
3. 如链完整 → 直接跳到 {target_version}
4. 如链断 → 按版本顺序处理
5. 更新 memory/.agent_sync_version = {target_version}
"""


# ── Helper functions ──────────────────────────────────────────
def _atomic_write(filepath, content):
    tmp = f"{filepath}.tmp.{os.getpid()}"
    with open(tmp, 'w') as f:
        f.write(content)
    os.fsync(f.fileno()) if hasattr(os, 'fsync') else os.sync()
    os.rename(tmp, filepath)

def version_less(a, b):
    """Compare vX.Y.Z format versions"""
    def parse(v): return tuple(int(x) for x in v.lstrip('v').split('.'))
    return parse(a) < parse(b)

def version_sort_key(v):
    return tuple(int(x) for x in v.lstrip('v').split('.'))

def now_utc():
    return datetime.now(timezone.utc)

def read(filepath):
    with open(filepath) as f:
        return f.read()

def extract_latest_section(changelog, version):
    sections = re.split(r'(?=^## v\d)', changelog, flags=re.MULTILINE)
    for s in sections:
        if s.strip().startswith(f"## {version}"):
            return s.strip()
    return sections[1].strip() if len(sections) > 1 else ""

def extract_version_range(changelog, from_ver, to_ver):
    """Extract all CHANGELOG entries between two versions (exclusive of from_ver)"""
    sections = re.split(r'(?=^## v\d)', changelog, flags=re.MULTILINE)
    entries = []
    for s in sections[1:]:  # skip title
        ver_match = re.match(r'## (v[\d.]+)', s)
        if ver_match:
            v = ver_match.group(1)
            if version_less(from_ver, v) and not version_less(to_ver, v):
                entries.append(s.strip())
    return entries

def parse_field(markdown_section, field_name):
    """Parse a **Field**: value line from a CHANGELOG section"""
    pattern = rf'\*\*{re.escape(field_name)}\*\*:?\s*(.+?)(?:\n|$)'
    m = re.search(pattern, markdown_section, re.IGNORECASE)
    return m.group(1).strip() if m else None

def format_sync_content(version, section, sig, generated_at, expires_at,
                        priority, depends_on):
    return f"""# pending_sync_{version}_{sig}.md

**类型**: pending_sync
**版本**: {version}
**前置**: {depends_on or 'none'}
**生成时间**: {generated_at}
**过期时间**: {expires_at}
**紧急程度**: {priority}
**签名**: {sig}

{section}

## 操作指令
1. 创建前置快照: mkdir -p memory/.sync_snapshots/{version}_pre/
2. 备份受影响文件到快照目录
3. 应用变更
4. 更新 memory/.agent_sync_version = {version}
5. 删除本文件
"""

### Pending_sync fallback paths

Version-named files (cumulative mode):
- `~/.openclaw/workspace-acode/pending_sync_<VERSION>_<SHA>.md`
- `~/.openclaw/workspace-ainvest/pending_sync_<VERSION>_<SHA>.md`
- `~/.openclaw/workspace-alive/pending_sync_<VERSION>_<SHA>.md`

Agent can discover all pending files: `ls pending_sync_*.md`
