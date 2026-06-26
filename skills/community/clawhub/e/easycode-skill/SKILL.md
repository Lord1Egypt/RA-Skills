---
name: easycode-skill
description: Use when users ask to generate Java code from database tables with EasyCode-style templates, including parsing db config, remembering last-used generation settings, resolving output paths from base package, and producing a file generation plan/execution.
---

# EasyCode Skill

## Purpose

This skill turns natural-language requests into deterministic EasyCode-style generation inputs and execution steps.

Use this skill when users ask for:
- Generating Java code from one or more DB tables
- MyBatisPlus or custom template-group generation
- Reusing previous DB/package/author/template settings
- Auto-mapping `base_package` to project output paths

## Inputs and Contract

1. Normalize the request to `generate_java_code` schema in [references/function-schema.json](references/function-schema.json).
2. Require explicit table names.
3. Fill missing fields from local state when available.
4. If critical DB fields are still missing, ask only for missing items.
5. When available, pass `generation_config.table_columns` for full field-level rendering parity.
6. If `table_columns` is absent, script attempts JDBC metadata fetch from `db_connection`.

## Workflow

1. Parse user intent.
2. Load recent state from `.easycode-skill/state.json` by running:
   - `python3 scripts/easycode_skill.py state --show`
3. Merge request + state + defaults:
   - default `template_group` is `Custom-V3`.
   - default output root is `src/main/java`.
4. Validate template group against [references/template-groups.md](references/template-groups.md).
5. Preview output plan:
   - `python3 scripts/easycode_skill.py plan --spec '<json>'`
6. Execute generation:
   - `python3 scripts/easycode_skill.py execute --spec '<json>'`
   - add `--overwrite` only when user confirms replacement
   - add `--run-project-format` to run formatter after generation
7. Persist successful config:
   - `python3 scripts/easycode_skill.py state --save --spec '<json>'`
8. Helper commands:
   - `python3 scripts/easycode_skill.py check-driver --db-type mysql`
   - `python3 scripts/easycode_skill.py spec-template --db-type mysql --tables user,order`
   - `python3 scripts/easycode_skill.py interactive` (首次 1~9 步引导，后续仅输入表名)

## Generation Rules

- Path mapping:
  - Convert `base_package` (for example `com.app.admin`) to `src/main/java/com/app/admin`.
  - Append template-level relative package (for example `entity`, `mapper`, `service`, `controller`).
- Template groups:
  - `MyBatisPlus` -> `configs/EasyCodeConfig-mybatispuls.json` (fallback project root file)
  - `Custom-V2` -> `configs/EasyCodeConfig-V2.json` (fallback project root file)
  - `Custom-V3` -> `configs/EasyCodeConfig-V3.json` (fallback project root file)
- JDBC drivers:
  - Preferred lookup is `drivers/drivers-paths.json`.
  - Skill-local jars under `drivers/<db>/` are supported.
  - If still missing, pass `db_connection.driver_jar`.
- Safety:
  - Always show a pre-write file list.
  - If file exists, mark as `overwrite_candidate` and ask for confirmation before replacing.

## Current Renderer Status

- The script uses a Java Velocity bridge to render template `code` with EasyCode global macros (`init/define/autoImport/mybatisSupport`).
- `execute` writes rendered output (not scaffold), and `plan` can include rendered content with `--include-content`.
- If `table_columns` is missing, script auto-fetches metadata through JDBC.
- When no JDBC driver is found locally, pass `db_connection.driver_jar` (and optional `db_connection.driver_class`) or provide `table_columns`.
- Default JDBC type preferences:
  - Number -> `Long`
  - Time/Date/Timestamp -> `Date`
  - Override via `generation_config.type_mapping` when needed.
  - Optional interactive prompt: add `--interactive-type-mapping` to `plan/execute` when `type_mapping` is not specified.
- Optional project formatter:
  - set `generation_config.project_format_command` to custom command(s), or
  - use `--run-project-format` and let script auto-detect `gradlew/mvnw` format tasks.

## Memory Policy

Persist these keys after successful run:
- `db_type`, `url`, `user`
- `author`, `base_package`, `template_group`
- optional `project_root`, `output_root`
- interactive mode also persists `pass`, `driver_jar`, `driver_class`, `type_mapping`, `project_format_command` for next-run defaults.

Do not store plaintext password in state. If password must be cached, store encrypted value from host secret manager.

## Execution Guidance

- Prefer deterministic script calls for plan/state actions.
- For actual rendering, use the project’s EasyCode engine implementation when available.
- If engine invocation is unavailable, still provide a complete plan and clearly report blocked execution step.

## Response Style

When reporting execution:
- Show resolved template group
- Show resolved base output directory
- Show generated/updated file count
- Show blocked items (if any) and exact next action
