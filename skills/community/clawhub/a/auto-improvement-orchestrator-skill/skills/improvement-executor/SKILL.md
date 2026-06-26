---
name: improvement-executor
description: "当需要把已批准的改进候选应用到目标文件、回滚之前的变更、或预览变更效果时使用。支持 4 种 action（append/replace/insert_before/update_yaml），每次变更前自动备份。不用于打分（用 improvement-discriminator）或门禁验证（用 improvement-gate）。"
license: MIT
triggers:
  - apply improvement
  - execute candidate
  - rollback change
  - 执行变更
  - 回滚
version: 0.1.0
author: OpenClaw Team
---

# Improvement Executor

Applies accepted candidates with automatic backup and rollback.

## When to Use

- 把已批准的改进候选应用到目标文件（自动创建备份，支持一键回滚）
- 回滚之前的变更（通过 receipt 中的 rollback_pointer 精确恢复）
- 用 `--dry-run` 预览变更效果，确认无误后再真正执行
- 在 orchestrator pipeline 第 4 阶段自动调用
- 需要对 YAML frontmatter 做字段级合并更新时（update_yaml 模式）
- 需要在指定 heading 前插入新内容时（insert_before 模式）
- 批量执行 ranking 中多个候选的变更
- 验证变更是否可逆——每次执行都会产出 receipt，receipt 包含完整的原始内容

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`（executor 不做质量判断）
- **门禁验证** → use `improvement-gate`（executor 只执行，gate 才验证结果）
- **全流程编排** → use `improvement-orchestrator`（orchestrator 统一调度各阶段）
- **评估 skill 结构** → use `improvement-learner`
- 候选尚未通过 discriminator 评分时，不应直接调用 executor
- 不要用 executor 做批量文件重命名或目录结构变更——它只处理单文件内容修改
- 不要在没有 ranking.json 的情况下调用——输入必须是 discriminator 产出的标准格式
- 不要手动编辑 receipt.json——receipt 包含哈希校验，手动修改会导致 rollback 失败

## 4 Action Types

| Action | Description |
|--------|------------|
| `append_markdown_section` | Append a new section to the end of the file |
| `replace_markdown_section` | Replace an existing section by heading match (exact heading text) |
| `insert_before_section` | Insert content before a matched heading |
| `update_yaml_frontmatter` | Merge fields into YAML frontmatter (deep merge, preserves existing keys) |

每种 action 的适用场景：
- **append** — 新增全新 section（如添加 "## Caveats"），不影响已有内容
- **replace** — 重写已有 section 的全部内容，按 heading 精确匹配（大小写敏感）
- **insert_before** — 在指定 section 前插入内容，适合在 "## CLI" 前加 "## Design Notes"
- **update_yaml** — 合并 frontmatter 字段，已有字段会被覆盖，新字段会被添加

## Why Automatic Backup Matters

**Tradeoff: disk space for safety — every apply creates a full copy of the original file.**

之所以每次变更前都做自动备份，原因是：

1. **One bad apply can corrupt the entire skill** — replace_markdown_section 如果匹配到错误的 heading，会覆盖关键内容。没有备份就无法恢复。
2. **Backup 是 rollback 的基础** — receipt 中的 `rollback_pointer` 指向备份文件的绝对路径和原始内容哈希。回滚时先校验哈希，确保备份未被篡改，再恢复。
3. **备份成本极低** — SKILL.md 通常不超过 10KB，备份文件存储在 `.state/backups/` 下，按时间戳命名，不会干扰版本控制。
4. **审计需求** — 备份链构成了完整的变更历史，可以追溯任意时间点的文件状态。

**问题**: 为什么不用 git 替代备份？Because executor 可能在没有 git repo 的环境中运行（例如临时目录中的 skill 测试），且 git commit 粒度太粗——一次 orchestrator run 可能执行多个候选，每个都需要独立的回滚点。

<example>
正确: 先 dry-run 预览，确认无误再执行
$ python3 scripts/rollback.py --receipt receipt.json --dry-run
→ 查看回滚内容，确认后去掉 --dry-run 执行
</example>

<anti-example>
错误: 跳过 discriminator 直接执行
→ executor 只应处理已通过评分的候选，未评分的直接执行可能破坏目标文件
</anti-example>

## CLI

execute.py 是核心入口，接收 ranking artifact 和 candidate ID，输出 result.json。
rollback.py 负责回滚，接收 receipt.json 还原到变更前的状态。
两个命令都支持 `--dry-run` 预览变更而不实际修改文件。
execute.py 会在执行前自动创建备份，备份路径记录在 result.json 的 backup_path 字段中。
建议对高风险变更（replace/update_yaml）始终先跑 --dry-run 确认。
rollback.py 在恢复前会校验备份文件的 SHA256 哈希，防止备份被篡改。

```bash
# Apply a single candidate (requires ranking artifact + candidate ID)
python3 scripts/execute.py --input ranking.json --candidate-id CANDIDATE_ID --output result.json

# Rollback a previous change using its receipt
python3 scripts/rollback.py --receipt receipt.json

# Dry-run: preview what rollback would do without modifying files
python3 scripts/rollback.py --receipt receipt.json --dry-run
```

Each action type maps to a different candidate structure. Examples:

```bash
# append_markdown_section: add a new "## Caveats" section at the end
python3 scripts/execute.py --input ranking.json --candidate-id C001 --output result.json
# candidate C001's action = "append_markdown_section", content = "## Caveats\n..."

# replace_markdown_section: overwrite the "## When to Use" section
python3 scripts/execute.py --input ranking.json --candidate-id C002 --output result.json
# candidate C002's action = "replace_markdown_section", heading = "When to Use"

# insert_before_section: insert content before "## CLI"
python3 scripts/execute.py --input ranking.json --candidate-id C003 --output result.json
# candidate C003's action = "insert_before_section", before_heading = "CLI"

# update_yaml_frontmatter: merge {version: "0.2.0"} into frontmatter
python3 scripts/execute.py --input ranking.json --candidate-id C004 --output result.json
# candidate C004's action = "update_yaml_frontmatter", fields = {version: "0.2.0"}
```

Always preview with --dry-run before executing irreversible changes:

```bash
# Dry-run for execute (not just rollback)
python3 scripts/execute.py \
  --input ranking.json \
  --candidate-id CANDIDATE_ID \
  --dry-run \
  --output preview.json
# preview.json shows the diff without modifying the target file
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Execute | JSON with `rollback_pointer` (original content hash, backup absolute path, timestamp) |
| Rollback | Restored file + confirmation JSON with restore status and hash verification result |
| Dry-run (execute) | JSON diff preview: before/after content, action type, target heading |
| Dry-run (rollback) | JSON showing what would be restored without modifying files |

result.json 的核心字段：
- `status`: success / failure / dry_run
- `action`: 执行的 action 类型（append/replace/insert_before/update_yaml）
- `target_file`: 被修改的文件绝对路径
- `backup_path`: 备份文件路径（用于 rollback）
- `content_hash_before` / `content_hash_after`: 变更前后的 SHA256 哈希
- `rollback_pointer`: 包含恢复所需的全部信息，传给 rollback.py 即可一键恢复

## Related Skills

- **improvement-discriminator**: Scores candidates before execution — executor 的输入是 discriminator 排序后的 ranking
- **improvement-gate**: Validates results after execution — gate 验证 executor 产出的 result.json
- **improvement-orchestrator**: Calls executor as stage 4 — 全流程中 executor 在 evaluator 之后、gate 之前
- **improvement-generator**: Produces the candidates — generator 的输出经 discriminator 评分后成为 executor 的输入
- **improvement-evaluator**: Task-based evaluation — evaluator 在 executor 之前验证候选的可行性
- **improvement-learner**: 6-dim structural scoring — executor 应用变更后，learner 可重新评分验证质量提升
- **benchmark-store**: Pareto front data — executor 变更后 gate 会用 benchmark 数据做回归检测

Pipeline 中的数据流: generator → discriminator → evaluator → **executor** → gate
