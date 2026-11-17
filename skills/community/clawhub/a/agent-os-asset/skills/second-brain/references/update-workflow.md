# Update Workflow / 更新流程

English is normative; ZH-CN is paired. / 英文为规范文本；简体中文为配对译文。

## Path Configuration / 路径配置

All runtime output stays outside the installed Skill directory.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 所有运行时输出都保存在已安装 Skill 目录之外。

| Purpose / 用途 | CLI | Environment / 环境变量 | Portable default / 可移植默认值 |
| --- | --- | --- | --- |
| Source vault | `--vault` | `SECOND_BRAIN_VAULT` | `$HOME/Documents/SecondBrain` |
| Index directory | `--out` | `SECOND_BRAIN_INDEX_DIR` | `<state-root>/index` |
| State root | n/a | `SECOND_BRAIN_STATE_DIR` | `$XDG_STATE_HOME/second-brain` or `$HOME/.local/state/second-brain` |
| Routine log | `--log` | `SECOND_BRAIN_LOG` | `<state-root>/logs/routine-update.log` |
| Routine lock | `--lock` | `SECOND_BRAIN_LOCK` | `<state-root>/locks/routine-update.lock` |
| Asset registry | `--asset-index-registry` | `SECOND_BRAIN_ASSET_REGISTRY` | `<state-root>/asset-index-registry.json` |
| Report vault | external workflow | `SECOND_BRAIN_REPORT_VAULT` | `$HOME/Documents/SecondBrainReports` |
| Report index | `query_index.py --index` | `SECOND_BRAIN_REPORT_INDEX` | `<state-root>/report-index/documents.jsonl` |

CLI arguments take precedence for the invoked command. Set environment variables for recurring jobs.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 对当前命令而言，CLI 参数优先。重复任务请设置环境变量。

## Normal Incremental Update / 常规增量更新

Index updates, logs, locks, and registry writes require an explicit update request or approval. A retrieval question alone grants no write authority; use existing results and disclose staleness. / 索引更新、日志、锁和注册表写入需要明确更新请求或批准；单独的检索问题不授予写入权限，应使用现有结果并说明过期状态。

```bash
SKILL_DIR="/path/to/second-brain"
python3 "$SKILL_DIR/scripts/routine_update.py"
```

The default `agent-readable` mode indexes `.agent.md` files and skips raw originals, archived/extracted content, templates, operational root documents, profile notes, hidden/plugin/cache/trash/attachment directories, and PII.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 默认 `agent-readable` 模式索引 `.agent.md` 文件，并跳过原始文件、archived/extracted 内容、模板、根目录操作文档、profile 笔记、hidden/plugin/cache/trash/attachment 目录和 PII。

Runtime output includes:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 运行时输出包括：

- `manifest.json`: compact incremental state and PII exclusions.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: `manifest.json`：紧凑的增量状态与 PII 排除项。
- `documents.jsonl`: queryable structured records.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: `documents.jsonl`：可查询的结构化记录。
- `index-summary.md`: build statistics.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: `index-summary.md`：构建统计。
- `vault-map.md` and `tag-map.md`: navigation summaries.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: `vault-map.md` 和 `tag-map.md`：导航摘要。
- `excluded-pii-paths.txt`: privacy audit list.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: `excluded-pii-paths.txt`：隐私审计列表。

## Rebuild Modes / 重建模式

Use a full rebuild only for initial setup, schema changes, or suspected corruption:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 仅在首次设置、schema 变更或怀疑损坏时执行完整重建：

```bash
python3 "$SKILL_DIR/scripts/routine_update.py" --force
```

Use raw Markdown fallback only when explicitly needed:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 仅在明确需要时使用原始 Markdown fallback：

```bash
python3 "$SKILL_DIR/scripts/routine_update.py" --force --source-mode all-markdown
```

Use Agent Asset manifest mode only after retention and privacy decisions are final and index writing is explicitly approved. The suite root pipeline performs the mandatory fresh audit and scope checks:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 仅在保留与隐私决策最终确定且明确批准索引写入后使用 Agent Asset manifest 模式；套件根 pipeline 执行必需的新一轮审计与范围检查：

```bash
python3 "/path/to/agent-os-asset/scripts/asset_pipeline.py" \
  --root "/path/to/workspace" --scope "." --stage index --execute-index
```

## Optional Remote Summaries / 可选远程摘要

Remote summaries are disabled by default. Enable them only for the current workflow with a dedicated credential, explicit model, and HTTPS endpoint:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 默认禁用远程摘要。仅使用专用凭据、明确 model 和 HTTPS endpoint 为当前 workflow 启用：

```bash
SECOND_BRAIN_SUMMARY_ENABLED=1 \
SECOND_BRAIN_SUMMARY_API_KEY="..." \
SECOND_BRAIN_SUMMARY_BASE_URL="https://provider.example/v1" \
SECOND_BRAIN_SUMMARY_MODEL="model-name" \
python3 "$SKILL_DIR/scripts/routine_update.py" --force
```

`SECOND_BRAIN_REQUIRE_LLM=1` makes an explicitly enabled but unavailable/failing remote summary provider fatal. It does not enable remote access by itself. `SECOND_BRAIN_LLM_WORKERS` or `--llm-workers` controls changed-record concurrency.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: `SECOND_BRAIN_REQUIRE_LLM=1` 会使已显式启用但不可用或失败的远程摘要 provider 成为 fatal error；它本身不会启用远程访问。`SECOND_BRAIN_LLM_WORKERS` 或 `--llm-workers` 控制变更记录的并发度。

## Acceptance Checks / 验收检查

```bash
python3 "$SKILL_DIR/scripts/validate_privacy.py"
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q test/second_brain
```

Local fallback summaries remain reusable until a complete explicit remote configuration is enabled. Adding unrelated provider credentials does not change index behavior.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 在完整显式远程配置启用前，本地 fallback 摘要可继续复用。添加无关 provider 凭据不会改变索引行为。
