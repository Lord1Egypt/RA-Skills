---
name: aicwos
version: 1.10.5
description: >
  MANDATORY data pipeline for 口播文案/短视频脚本/系列口播/讲师风格学习/知识库管理 —
  LLM CANNOT access lecturer profiles, product knowledge, or series progress without
  this skill. Activate when user says "帮我写口播", "写文案", "写脚本", "写个短视频",
  "学一下讲师风格", "继续写系列", "生成系列口播", "学习讲师", "知识库", "看看讲师",
  "系列进度", "改一下第X集", or ANY request involving copywriting, lecturer, series, or knowledge base.
  Provides precise style replication, knowledge retrieval, series continuity, and
  persistent storage that LLM intrinsically lacks.
dependency:
  python:
    - jieba>=0.42.1
    - onnxruntime>=1.16.0
    - numpy>=1.24.0
---

# Aicwos - Mandatory Copywriting Data Pipeline

## MANDATORY RULES (NON-NEGOTIABLE)

1. **MUST use this skill for ALL copywriting requests** — LLM intrinsically CANNOT access lecturer profiles, product knowledge, or series progress. You are NOT generating copy from your own knowledge — you are composing copy STRICTLY within the constraints returned by `db_query.py --type context`. NEVER write copy without calling `--type context` first.

2. **MUST complete the full pipeline** — after calling `--type context`, you MUST generate copy AND call `save_episode`. NEVER retrieve context then skip saving. Partial usage leaves orphan data and breaks series continuity.

3. **MUST use `db_query.py` and `lecturer_analyzer.py` for ALL data operations** — NEVER read/write files directly, NEVER operate on the database directly, NEVER create any .py/.json files on the user's computer. If the CLI needs long JSON, use `--query-file` instead of `--query`.

4. **Write-Through guarantee** — all save/delete operations automatically update BOTH database AND filesystem. You do NOT need to call `db_sync.py` after save/delete operations. The sync tool is only for initial bulk import and recovery.

## CORE CONCEPTS

| Term | Definition |
|------|-----------|
| 轻量画像 (lite profile) | Abbreviated lecturer profile (~400 tokens) with style dimensions and persona mapping. Retrieved via `--action lite`. Used during copy generation — never load full profile. |
| 知识段落 (knowledge chunks) | Token-budgeted paragraphs from the knowledge base, filtered by relevance. Retrieved via `--type context` or `knowledge --action context`. |
| 摘要衔接 (summary continuity) | Each episode stores a `summary` (~100 chars) and `hook_next`. When generating episode N, read summaries of episodes 1..N-1 via `--action summaries` — NEVER read full episode text. |
| 行为规则 (behavior rules) | Forbidden patterns (B-prefixed) and required patterns (R-prefixed). Loaded automatically by `--type context`. |
| 系列进度 (series progress) | `completed/total_episodes` tracked in DB. Updated automatically by `save_episode` and `delete_episode`. Do NOT compute manually. |
| Write-Through (双写) | Every save/delete operation updates both DB and filesystem atomically. No manual sync needed. DB is the query layer; filesystem is the human-readable layer. |

## TRIGGER CONDITIONS

Activate this skill when user's request involves ANY of:

| Pattern | Typical user expressions |
|---------|------------------------|
| **Copywriting** | 帮我写口播/写文案/写个脚本/写篇稿件/帮我写个短视频 |
| **Lecturer** | 学讲师风格/分析讲师/学习XX的语气/帮我学习讲师 |
| **Series** | 写个N集系列/继续写XX系列/生成系列口播/连续口播 |
| **Revision** | 改一下第X集/重新写第X集/删掉第X集/换一下第X集 |
| **Knowledge** | 知识库里有什么/搜索知识/添加知识/删除知识 |
| **Management** | 看看讲师/系列进度/讲师列表/看看画像 |

NOT for: non-口播 writing (emails, reports, essays, docs), general Q&A without copywriting intent.

## Anti-Patterns (COMMON ERRORS — DO NOT)

| Wrong | Why it fails |
|-------|-------------|
| Call `--type context` → write copy → skip `save_episode` | Orphan data, series progress lost |
| Call `--type context` → cherry-pick context → ignore full constraints | Style drift, knowledge gaps |
| Write copy → save as .txt manually instead of `save_episode` | Bypasses DB, breaks series tracking |
| Write copy without calling `--type context` at all | No style, no knowledge, no constraints |
| Call `--type context` → write from own knowledge, ignoring returned context | Defeats the entire pipeline purpose |
| Revise by calling `save_episode` without `delete_episode` first | Duplicate DB records, stale .txt file persists |
| Delete episode by removing .txt file manually | DB metadata orphaned, progress counter corrupted |
| Create .py or .json files to process/save lecturer data | Bypasses Write-Through, no tracking, files in wrong location |
| Write temp files to the user's desktop, /tmp, or %TEMP% | Use staging files inside 控制台 directory — the only shared path between agent and scripts |
| Call `lecturer_analyzer.py` → skip `db_query.py --type lecturer --action save` | No profile exists for copy generation |
| Run `db_sync.py` after every save/delete operation | Unnecessary — Write-Through handles both layers automatically |

**If you called `--type context`, you MUST complete through `save_episode`. There are NO valid shortcuts.**

**If you called `lecturer_analyzer.py`, you MUST complete through `db_query.py --type lecturer --action save`. The analyzer only stores quantitative data — you MUST also build and save the full profile.**

## Pre-flight Check (MANDATORY before ANY copywriting)

Before generating any copy text, verify all 3 conditions:

- [ ] `db_query.py --type context` has been executed this session → if NO, execute it NOW
- [ ] The returned context (lecturer profile + knowledge chunks + samples + rules) is visible → if NO, re-execute
- [ ] You will compose STRICTLY within the returned constraints → if planning to use own knowledge, STOP

Only after all 3 checks pass, proceed to write.

---

## NATURAL LANGUAGE → CLI MAPPING

Users do NOT type CLI commands. You MUST translate natural language to CLI operations. `--data-dir` always points to the 控制台 directory.

| User says | You execute |
|-----------|-------------|
| **Copywriting** | |
| 帮我写个口播 / 写篇文案 | 1. `db_query.py --type context` → 2. Generate copy → 3. `save_plan` → 4. `save_episode` |
| 写个N集系列口播 / 写系列 | 1. `db_query.py --type context` → 2. `save_plan` → 3. Generate each episode + `save_episode` |
| 继续写XX系列 | `get_plan` + `summaries` → Generate next episode → `save_episode` |
| 改一下第X集 / 重新写第X集 | `delete_episode --id2 X` → Regenerate → `save_episode --id2 X` |
| 删掉第X集 | `delete_episode --id <series> --id2 X` |
| XX系列写到哪了 | `progress --id <name>` |
| XX系列计划是什么 | `get_plan --id <name>` |
| **Lecturer** | |
| 学一下讲师风格 / 帮我学习XX | Follow LECTURER WORKFLOW below (3-step pipeline) |
| 我有哪些讲师 | `db_query.py --type lecturer --action list` |
| XX老师什么风格 | `db_query.py --type lecturer --action lite --id <name>` |
| 修改XX的画像 | `--action get` → Modify → `--action save` (use `--query-file` for large JSON) |
| 给XX加新文案 / 增量学习 | `lecturer_analyzer.py --lecturer <name> --merge --stdin --save-sample` (pipe text via stdin; or write to temp file + `--input`) |
| 删除XX讲师 | `db_query.py --type lecturer --action delete --id <name>` |
| XX和YY有什么区别 | `db_query.py --type lecturer --action compare --id XX --id2 YY` |
| 看看XX的样本 | `db_query.py --type lecturer --action samples --id <name>` |
| 导出讲师 | `lecturer_transfer.py --action export --lecturer <name> --data-dir <dir> --output <dir>` |
| 导入讲师 | `lecturer_transfer.py --action import --source <dir> --data-dir <dir>` (default: merge + auto sync DB) |
| 导入讲师(覆盖) | `lecturer_transfer.py --action import --source <dir> --data-dir <dir> --overwrite` |
| **Knowledge Base** | |
| 知识库里有什么 | `db_query.py --type fs --action knowledge --data-dir <dir>` |
| 搜索XX知识 | `db_query.py --type knowledge --action search --query "XX"` |
| 获取XX上下文 | `db_query.py --type knowledge --action context --query "XX" --max-tokens 1000` |
| 添加知识 | Create file under 知识库集/私有/ → `db_sync.py --direction to-db` |
| 删除知识 | `db_query.py --type knowledge --action delete --id <doc_id>` |
| 同步知识库 | `knowledge_sync.py --data-dir <dir>` |
| **Behavior Rules** | |
| 看看行为规则 | `db_query.py --type behavior --action list` |
| 禁止用XX | `db_query.py --type behavior --action add --id B0XX --query '{"id":"B0XX",...}'` |
| 必须用XX | `db_query.py --type behavior --action add --id R0XX --query '{"id":"R0XX",...}'` |
| **System** | |
| 初始化 / 第一次用 | Follow "First-Time Setup" below |
| 看看控制台目录 | `db_query.py --type fs --action tree --data-dir <dir>` |
| 看看讲师列表 | `db_query.py --type fs --action lecturers --data-dir <dir>` |

---

## LECTURER WORKFLOW

When user provides lecturer sample text (pasted or file), follow this 3-step pipeline. NEVER create .py/.json files — use the CLI only. All save operations use Write-Through (DB + filesystem automatically).

### Step 1: Quantitative Analysis `(script call)`

**For long text** (user pastes a full article — the typical scenario):

1. Write sample text to `<控制台dir>/讲师列表/<name>/样本/_staging.txt` using your native file-write tool (NOT shell echo, NOT the desktop, NOT /tmp):
   ```
   <控制台dir>/讲师列表/<name>/样本/_staging.txt
   ```
2. Run analyzer with `--input` and `--save-sample`:
   ```bash
   python scripts/lecturer_analyzer.py --input "<控制台dir>/讲师列表/<name>/样本/_staging.txt" --lecturer <name> --data-dir <控制台dir> --save-sample
   ```
   `--save-sample` renames `_staging.txt` → `sample_YYYYMMDD_HHMMSS.txt` and registers in DB (Write-Through). No duplication.

**For file input** (user provides a file path):
```bash
python scripts/lecturer_analyzer.py --input <file_path> --lecturer <name> --data-dir <控制台dir> --save-sample
```

**For short text** (<500 chars), use `--text`:
```bash
python scripts/lecturer_analyzer.py --lecturer <name> --text "<sample>" --data-dir <控制台dir> --save-sample
```

**For `--stdin`** (Linux only, where pipe works reliably):
```bash
echo "<text>" | python scripts/lecturer_analyzer.py --lecturer <name> --stdin --data-dir <控制台dir> --save-sample
```

The analyzer returns quantitative data, `merge_status`, and `sample_saved`. If `"new"`, proceed to Step 2.

For **incremental merge** (adding new samples to existing lecturer), append `--merge` flag.

### Step 2: Build Full Profile `(agent task)`

The analyzer only produces quantitative metrics. You MUST construct the full profile by combining:
- Quantitative data from Step 1
- Your interpretation of qualitative traits (tone, persona, core identity, etc.)

Key fields (full format: [references/profile-format.md](references/profile-format.md)):
`lecturer_name`, `qualitative.persona_mapping`, `qualitative.style_dimensions`, `quantitative`, `sample_texts`

### Step 3: Save Profile `(script call)` — Write-Through

Save automatically writes to BOTH DB and `讲师列表/{name}/profile.json`. No need to call `db_sync.py`.

For **large profiles** (typical — quantitative data is verbose), use `--query-file`:
1. Write profile JSON to staging file in 控制台 using your native file-write tool:
   ```
   <控制台dir>/讲师列表/<name>/_profile_staging.json
   ```
2. Run save with `--query-file` (staging file auto-deleted after successful save):
   ```bash
   python scripts/db_query.py --type lecturer --action save \
     --id <name> --query-file "<控制台dir>/讲师列表/<name>/_profile_staging.json" --data-dir <控制台dir>
   ```

For **small profiles** (<2000 chars JSON), use `--query`:
```bash
python scripts/db_query.py --type lecturer --action save \
  --id <name> --query '<profile JSON>' --data-dir <控制台dir>
```

### Verify `(script call)`
```bash
python scripts/db_query.py --type lecturer --action lite --id <name> --data-dir <控制台dir>
```

---

## STANDARD COPYWRITING WORKFLOW

Every copywriting request MUST follow these steps. NO step may be skipped. All save operations use Write-Through.

### Single Episode

1. **Get context** `(script call)` — MANDATORY, never skip:
   ```bash
   python scripts/db_query.py --type context --action context \
     --lecturer <lecturer> --query <topic> --data-dir <控制台dir>
   ```

2. **Generate copy** `(agent task)` — compose STRICTLY within the returned constraints

3. **Save plan** `(script call)` — Write-Through (DB only, plan has no user-facing file):
   ```bash
   python scripts/db_query.py --type series --action save_plan \
     --id <topic> --lecturer <lecturer> \
     --query '{"title":"<topic>","episodes":[{"num":1,"title":"<title>","topic":"<topic>"}]}' \
     --data-dir <控制台dir>
   ```

4. **Save copy** `(script call)` — Write-Through (DB + .txt file):
   ```bash
   # Short content: --query
   python scripts/db_query.py --type series --action save_episode \
     --id <topic> --id2 1 \
     --query '{"title":"<title>","content":"<body>","summary":"<100-char summary>","hook_next":""}' \
     --data-dir <控制台dir>

   # Long content (typical): write JSON to staging file in 控制台, then --query-file
   python scripts/db_query.py --type series --action save_episode \
     --id <topic> --id2 1 --query-file "<控制台dir>/讲师列表/<lecturer>/系列文案/<topic>/_episode_staging.json" --data-dir <控制台dir>
   ```

### Series (N episodes)

Same as Single Episode steps 1-2, then save plan, then **loop steps 3-4 for each episode**. Each episode needs its own `save_episode` call.

### Revision (modify existing episode)

When user says "改一下第X集" / "重新写第X集" / "换一下第X集":

1. **Get context** `(script call)` — MUST re-fetch
2. **Read current episode** `(script call)`:
   ```bash
   python scripts/db_query.py --type series --action content --id <series> --id2 X --data-dir <控制台dir>
   ```
3. **Delete old episode** `(script call)` — MUST delete before saving replacement:
   ```bash
   python scripts/db_query.py --type series --action delete_episode --id <series> --id2 X --data-dir <控制台dir>
   ```
4. **Regenerate copy** `(agent task)`
5. **Save revised episode** `(script call)`

CRITICAL: `delete_episode` MUST be called before `save_episode` for revisions. Files are saved to `控制台/讲师列表/{lecturer}/系列文案/{series}/E0X_{title}.txt` — path enforced by script.

---

## FIRST-TIME SETUP

When the user uses this skill for the first time or no database exists, guide through these steps sequentially.

1. **Initialize 控制台** — Ask user for storage location (e.g. "桌面"), then run:
   ```bash
   python scripts/db_init.py --setup --parent-dir "<user location>"
   ```
   MUST use `--parent-dir`, NOT `--data-dir`. Script auto-creates "控制台" folder. The 控制台 folder name is FIXED — NEVER rename it.

2. **Configure cloud sync** — Ask for knowledge base cloud URL (COS bucket), write to workspace.json. Then run:
   ```bash
   python scripts/knowledge_sync.py --data-dir "<控制台dir>"
   ```
   No credentials needed. Sync reads `manifest.txt` (file paths only, one per line) from COS, then HEAD-checks each file's `Last-Modified`. Cloud maintainer only needs to update `manifest.txt` when adding new files — no timestamps to maintain.

3. **Download semantic model (optional)** — Ask if user wants to download (~98MB), then sync data:
   ```bash
   python scripts/db_init.py --download-model --data-dir "<控制台dir>"
   python scripts/db_sync.py --direction to-db --data-dir "<控制台dir>"
   ```

---

## WORKSPACE STRUCTURE

```
控制台/
├── workspace.json           # Workspace config (includes sync URL)
├── 讲师列表/{lecturer}/
│   ├── profile.json         # Lecturer profile (auto-maintained by Write-Through)
│   ├── 样本/                # Sample scripts (auto-maintained by Write-Through)
│   └── 系列文案/            # Series copy (auto-maintained by Write-Through)
│       └── {series}/
│           ├── E01_春季养肝.txt
│           └── ...
├── 知识库集/
│   ├── 公共/                ← Cloud synced, read-only
│   └── 私有/                ← Local, user-editable
└── 回收站/
    ├── {lecturer}/          ← Deleted lecturer directories (with .meta.json for recovery)
    └── ...
```

- Write-Through: all save/delete operations update both DB and filesystem automatically
- DB is the query layer; filesystem is the human-readable layer
- Users can still edit .txt files directly, then `db_sync.py --direction to-db` to re-index

---

## EXAMPLES

### Example 1: Learn lecturer style then write copy
- User: "这是讲师B的5篇口播 [paste copy]"
- Steps: Write sample to temp file → `lecturer_analyzer.py --input <temp> --save-sample` `(script call)` → build profile `(agent task)` → `lecturer --action save --query-file` `(script call, Write-Through: DB+profile.json)` → user says "用讲师B风格写个养生口播" → `--type context` `(script call)` → generate `(agent task)` → `save_plan` + `save_episode` `(script call, Write-Through: DB+.txt)`

### Example 2: Knowledge-driven copy
- User: "参考产品A的背书写个口播"
- Steps: `knowledge --action context --query "产品A 背书"` `(script call)` → weave into copy `(agent task)` → `save_episode` `(script call)`

### Example 3: Series continuity
- User: "继续写养生系列第6集"
- Steps: `series --action get_plan` + `summaries` `(script call)` → generate episode 6 `(agent task)` → `save_episode --id2 6` `(script call)`

### Example 4: Revision
- User: "养生系列第2集改一下，开头太长了"
- Steps: `--type context` `(script call)` → `content --id2 2` `(script call)` → `delete_episode --id2 2` `(script call)` → shorten opening `(agent task)` → `save_episode --id2 2` `(script call)`

---

## RESOURCE INDEX
- Lecturer workflow: [references/workflow-lecturer.md](references/workflow-lecturer.md)
- Knowledge workflow: [references/workflow-knowledge.md](references/workflow-knowledge.md)
- Copywriting workflow: [references/workflow-copywriting.md](references/workflow-copywriting.md)
- Profile format: [references/profile-format.md](references/profile-format.md) (read when generating/validating profiles)
- Script styles: [references/script-styles.md](references/script-styles.md) (read when confirming style parameters)
- Model config: [assets/model_config.json](assets/model_config.json)
- Init script: [scripts/db_init.py](scripts/db_init.py) — `--setup --parent-dir` creates 控制台; `--download-model --data-dir` downloads model
- Query script: [scripts/db_query.py](scripts/db_query.py) — unified CLI; `--query-file` for large JSON; Write-Through on all save/delete; `--action add_sample` for sample files
- Analyzer: [scripts/lecturer_analyzer.py](scripts/lecturer_analyzer.py) — style analysis + incremental merge; `--save-sample` auto-saves input text (Write-Through); `--input` for file-based long text; `--stdin` for Linux pipe
- Sync script: [scripts/db_sync.py](scripts/db_sync.py) — bidirectional file↔DB sync (recovery/initial import only)
- Transfer: [scripts/lecturer_transfer.py](scripts/lecturer_transfer.py) — cross-user lecturer migration; default auto sync (Write-Through); `--overwrite` / `--no-sync` options
- Knowledge sync: [scripts/knowledge_sync.py](scripts/knowledge_sync.py) — cloud sync via manifest.txt + HEAD (no credentials); `--dry-run` / `--force`; `--generate` outputs manifest.txt from local public layer (for cloud maintainer to upload)

## NOTES
- First-time setup MUST use `db_init.py --setup --parent-dir <location>`, NOT `--data-dir`
- Semantic model is optional; auto-degrades to FTS5-only when absent
- Write-Through: all save/delete operations update both DB and filesystem automatically. Do NOT call `db_sync.py` after normal operations.
- `knowledge_sync.py` uses `manifest.txt` + HEAD (no credentials needed). Cloud maintainer puts `manifest.txt` on COS (one file path per line, no timestamps). Script HEAD-checks manifest.txt's `Last-Modified` first — unchanged = skip entirely. `--generate` outputs manifest.txt from local public layer for cloud maintainer to upload: `python scripts/knowledge_sync.py --data-dir <dir> --generate > manifest.txt`
- `--query-file <path>` reads JSON from file — use for profiles or episode content >2000 chars. Write staging files to 控制台 paths (e.g. `讲师列表/{name}/_profile_staging.json`), NOT /tmp or %TEMP%. Files ending in `_staging.json` are auto-deleted after successful save.
- `--save-sample` on `lecturer_analyzer.py` auto-saves input text to `讲师列表/{name}/样本/` (Write-Through: DB+file). If input file is already in the samples dir, it renames instead of duplicating.
- `db_sync.py` is only for: initial bulk import (`--direction to-db`) or disaster recovery (`--direction to-files`)
- REMINDER: Before writing ANY copy, you MUST have called `db_query.py --type context` this session. If you haven't, stop and execute it first.
