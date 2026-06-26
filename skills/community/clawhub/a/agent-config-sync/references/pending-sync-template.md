# pending_sync Template

**v1.4**: Enhanced file header with TTL/expiry, depends_on chain, and agent version tracking fields. Backward compatible — new fields are additive.

## Template Content

```markdown
# pending_sync_<VERSION>_<SHA>.md

**类型**: pending_sync
**版本**: <VERSION>
**前置**: <PREVIOUS_VERSION>
**生成时间**: <GENERATED_AT>
**过期时间**: <EXPIRES_AT>  (24h 后)
**紧急程度**: <PRIORITY>
**签名**: <SHA256>

## 变更清单
- [ ] 🖥️ 系统代码变更
- [ ] 🤖 智能体配置变更
- [ ] ⚙️ OpenClaw 系统配置变更
- [ ] 🎯 任务/工作配置变更

## 详情
请读取 `/home/admin/.openclaw/workspace-amaster/memory/CHANGELOG.md` 中 `<VERSION>` 对应的章节。

## 操作指令
1. 创建前置快照: mkdir -p memory/.sync_snapshots/<VERSION>_pre/
2. 备份受影响文件到快照目录
3. 应用变更
4. 更新 memory/.agent_sync_version = <VERSION>
5. 删除本文件
```

## Template Fields

| Field | Required | Format | Example |
|-------|:--------:|--------|---------|
| `**类型**` | ✅ | `pending_sync` / `revert_sync` / `isolated_sync` | pending_sync |
| `**版本**` | ✅ | `vX.Y` | v3.5 |
| `**前置**` | ⬜ | `vX.Y` or `none` | v3.4 |
| `**生成时间**` | ✅ | ISO 8601 with timezone | 2026-05-16T08:30:00+08:00 |
| `**过期时间**` | ✅ | ISO 8601 (24h after generated) | 2026-05-17T08:30:00+08:00 |
| `**紧急程度**` | ✅ | `normal` / `high` / `critical` | high |
| `**签名**` | ✅ | SHA256 first 12 hex chars | a1b2c3d4e5f6 |

## SHA256 Signature

The `<SHA256>` value in the filename and template body is computed as:

```
sha256("pending_sync_<VERSION>_" + 变更摘要)
```

Take the first 12 hex characters as the short signature.

### Purpose
- Receiving agent can verify file integrity
- Prevents tampered or truncated sync notifications
- Short 12-char format keeps filenames manageable

### Verification (in agent-side logic)

```python
import hashlib

def verify_sync_file(filename, expected_version, change_summary):
    expected_sig = hashlib.sha256(
        f"pending_sync_{expected_version}_{change_summary}".encode()
    ).hexdigest()[:12]
    actual_sig = filename.split("_")[-1].replace(".md", "")
    return expected_sig == actual_sig
```

## File Naming Convention

| Pattern | Example |
|---------|---------|
| Version sync | `pending_sync_v3.1_a1b2c3d4e5f6.md` |
| Startup discovery | `ls pending_sync_*.md` to list all pending |
| Revert sync | `revert_sync_v3.3_to_v3.2_a1b2c3d4.md` |
| Isolated sync | `isolated_sync_v1.4_a1b2c3d4.md` |

## Cleanup

Each agent independently deletes its own pending file after processing:

```bash
# Agent-side cleanup after sync applied
rm -f pending_sync_*.md revert_sync_*.md isolated_sync_*.md
```

The file persists as long as the agent hasn't applied the sync. If the same version file is generated twice (e.g., dispatch retry), the content is idempotent — the agent can re-apply safely.

## TTL & Expiry

By default, pending_sync files expire **24 hours** after generation. The agent's BOOTSTRAP/HEARTBEAT checks should:

1. Parse `**过期时间**` from the file header
2. If `now > 过期时间` → delete the expired file, request latest version from Master
3. If `now <= 过期时间` → proceed with sync processing

TTL is configurable via `agent-registry.json` → `sync.ttl_hours` (default: 24).
