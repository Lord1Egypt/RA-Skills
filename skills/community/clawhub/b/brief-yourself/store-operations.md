# Store Operations｜Brief Yourself 1.0.1

本文件是 Brief Yourself 1.0.1 的 runtime 操作手册，覆盖全部 14 个正式 1.0.1 操作与 2 个迁移命令。active schema identity 为 `1.0.1`。参数以各命令的 `--help` 为最终依据。

## Directory Layout

```text
.brief-yourself/
├── context.json
├── brief.md
├── evidence/
│   └── index.json
├── views/
├── patches/
│   ├── pending/
│   ├── applied/
│   └── rejected/
└── history/
    ├── changes.jsonl
    └── context-vN.json
```

`context.json` 是 Canonical Store。`brief.md` 是用户可读版本；Skill 负责根据 Canonical Store 更新它。原始证据默认留在原系统，`evidence/index.json` 只保存索引。

## Initialize

```bash
python scripts/context_store.py init \
  --store .brief-yourself \
  --context-id user-controlled-id \
  --preferred-name ExampleUser
```

`init` 不覆盖已有 Store。

新 Store 使用 active schema identity `1.0.1`。旧 `0.2` / `0.3` Store 只允许 `validate` 与 `inspect`；不得直接 `export`。`migrate-v02` 会改写传入路径，因此只能先由用户创建一个明确的副本，再对该副本显式执行：

```bash
python scripts/context_store.py migrate-v02 \
  --store .brief-yourself \
  --confirmed-by user \
  --approve
```

迁移保留原 revision 快照、递增 revision，并记录变更；`validate` 不会静默迁移。该命令只到 `0.3`，不能链式进入 `1.0.1`。从 `0.3` 到 `1.0.1` 只能运行只读的 `preview-migrate-v03`，由用户另行审核和决定物化方式。

## Register Source

`register-source` 是 Evidence Source 的**写入入口，不是读取授权界面**。读取历史、项目、简历、Obsidian 或 Harness Memory 前的授权卡由 `source-consent-and-disclosure.md` 约束；只有在用户已授权读取、并且明确批准把该来源长期登记进 Store 后，才能运行本命令。

长期 Claim 引用新 Evidence Source 前，先把单个、已审核的 Source JSON 登记到 Store：

```bash
python scripts/context_store.py register-source \
  --store .brief-yourself \
  --source source.json \
  --confirmed-by user \
  --approve
```

`source.json` 的字段以 `assets/schemas/personal-context-store-v1.0.1.schema.json` 的 `source` 定义为准：

```json
{
  "id": "source-002",
  "type": "conversation",
  "title": "用户可识别的来源名称",
  "locator": "system-or-user-managed-location",
  "access_scope": "实际读取范围",
  "collected_at": "ISO-8601",
  "consent": "explicit",
  "retention": "source-managed",
  "sensitivity": "private"
}
```

`consent` 固定为 `explicit`；`collected_at` 必须带时区。命令会同时更新 `context.json` 与 `evidence/index.json`、备份旧 revision、递增 revision 并写入审计记录。缺少 `--approve` 时零写入；Source ID 在任一索引中已存在时拒绝覆盖。

## Validate

```bash
python scripts/context_store.py validate --store .brief-yourself
```

验证结构、枚举、全局 ID、来源引用、disclosure、状态和 revision 一致性；不会静默修复或迁移。

## Inspect And Export

```bash
python scripts/context_store.py inspect --store .brief-yourself
python scripts/context_store.py inspect --store .brief-yourself --claim-id claim-001
python scripts/context_store.py export \
  --store .brief-yourself \
  --format markdown \
  --include-private \
  --output brief-export.md
```

`inspect` 默认输出 revision、计数、ID 和待审核 Patch；指定 Claim ID 才输出该 Claim。`export` 只接受 `1.0.1` Store，默认只导出 `public`；加入 `private` 或 `restricted` 必须使用对应 flag。旧 Store 的未知字段不会通过 export 被带出。

## Create View

```bash
python scripts/context_store.py create-view \
  --store .brief-yourself \
  --purpose "为目标岗位诊断并优化简历" \
  --task anti-ai-resume-screener \
  --claim-ids claim-001 claim-004 \
  --tension-ids tension-001 \
  --include-private \
  --archive-in-personal-store \
  --output resume-view.json
```

默认只包含 `public`，且不在 Personal Store 归档。`--include-private` 与 `--include-restricted` 必须对应用户对当前用途的明确授权；`--archive-in-personal-store` 控制本地归档，`--allow-downstream-persistence` 单独允许下游保存。Domain/Core 全量选择仅为兼容入口，脚本会给出 warning，应优先使用精确 ID。

`principal.type` 与 `audience[].type` 在 1.0 runtime 中只接受 `agent`；team、organization、shared 或未知类型一律拒绝。`confirmed` / `corrected` 条目默认可进入 View；`unreviewed` / `unresolved` 必须由用户显式同意并加入 `--include-unreviewed`。非公开 Tension / Unknown 与 Claim 一样，必须提供覆盖完整 audience 和 purpose 的 disclosure。

默认 `expires_at` 为创建时间后 7 天。可用带时区的 `--expires-at` 指定未来期限；1.0 runtime 不提供永不过期入口。

验证用途、权限和有效期：

```bash
python scripts/context_store.py validate-view \
  --view resume-view.json \
  --store .brief-yourself \
  --task anti-ai-resume-screener \
  --allowed-use "current resume task only"
```

过期、用途不符、敏感级别越权或权限结构无效时返回失败。

## Filesystem And Resource Limits

JSON / JSONL 输入单文件上限为 4 MiB；迁移预览的 JSON 深度上限为 64、节点上限为 100,000，purge 的结构递归深度上限为 64。超过上限会 fail closed 并返回 exit `2`。Store 的受控目录和文件不得是 symlink 或 Windows reparse point；每次受控写入、替换或删除前都会重新检查路径祖先和 resolved containment。该检查不替代操作系统权限，也不把 single-writer runtime 变成并发数据库。

## Stage Patch

```bash
python scripts/context_store.py stage-patch \
  --store .brief-yourself \
  --patch resume-patch.json
```

Stage 只写入 `patches/pending/`，不修改 `context.json`。

## Apply Patch

```bash
python scripts/context_store.py apply-patch \
  --store .brief-yourself \
  --patch-id patch-001 \
  --confirmed-by user \
  --approve
```

只有在用户已经审查具体 Patch 后运行。脚本会：

1. 验证父版本和 Proposal；
2. 备份当前 `context.json` 到 `history/context-vN.json`；
3. 原子写入新版本；
4. 追加 `history/changes.jsonl`；
5. 把 Patch 移入 `patches/applied/`。

缺少 `--approve`、父版本冲突、Core 门槛不足或存在未确认 Proposal 时拒绝执行。

拒绝待审核 Patch：

```bash
python scripts/context_store.py reject-patch \
  --store .brief-yourself \
  --patch-id patch-001 \
  --confirmed-by user \
  --reason "本轮不写回"
```

Patch 会移入 `patches/rejected/`，其中所有 Proposal 的 `user_decision` 会统一记录为 `rejected`，Canonical Context 不变。

## Retire And Purge

`retire` 是经 Patch 执行的逻辑失效，保留历史。`purge` 是不可逆遗忘，只处理当前 Store 内能通过精确 ID 定位的副本。

第一步必须预览：

```bash
python scripts/context_store.py purge-plan \
  --store .brief-yourself \
  --claim-id claim-001
```

确认 `operations` 和外部不可控副本后，使用同一精确目标及返回的 `plan_token`：

```bash
python scripts/context_store.py purge \
  --store .brief-yourself \
  --claim-id claim-001 \
  --plan-token <token-from-purge-plan> \
  --confirmed-by user \
  --approve
```

目标必须且只能是 `--claim-id`、`--source-id`、`--view-id`、`--patch-id` 之一。Store 在预览后发生变化会导致 token 失效。工具会检查 `context.json`、`views/`、`patches/`、`history/` 和 `evidence/index.json`，但无法删除原始来源系统、Store 外导出文件或无法仅凭 ID 定位的语义副本；这些限制必须展示给用户。

## Recovery

脚本不提供自动回滚命令。需要恢复时，让用户选择明确的 `history/context-vN.json`，先预览差异，再复制为新版本；不要覆盖历史版本或回退 revision 数字。
