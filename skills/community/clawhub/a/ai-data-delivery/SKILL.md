---
name: ai-data-delivery
description: Build and edit a source-linked ontology from DDL or selected database metadata. Export a semantic graph for local Agent use. 用于本体建模、业务口径核对及语义包读取。
license: MIT
allowed-tools: Read
metadata:
  version: 0.3.10
  runtime_environment: Python 3.10+ with pinned local dependencies. No model key.
  file_read: Authorized materials, local project and semantic packages.
  file_write: Authorized local project and export paths.
  network: Loopback editor and optional selected database catalog only.
  environment: Remote catalog adapters read the explicitly named database password variable.
  sql: Offline DDL is parsed as text. Catalog connections issue fixed read-only metadata queries.
  authorization: Python execution and writes use host permissions. Read is the experimental reading preapproval.
---

# AI Data Delivery

Work from the user's schema, selected catalog, supplied documents or existing package. The host interprets the material. The CLI preserves one local model. Start the editor when the user needs to see or change a graph. Use the bundled synthetic example for trials.

[中文](SKILL.zh-CN.md) · [First run, sample JSON and troubleshooting](README.md) · [Architecture](references/architecture.md)

## Choose a path

Run the scripts from the skill directory with Python 3.10+. Put project-wide options before the subcommand. Read the reference for the current task only.

| User's task | Entry point |
| --- | --- |
| Import DDL | `scripts/knowledge.py --project DIR import --file SCHEMA.sql --seed-draft` creates source-linked physical drafts in an empty graph. Later imports omit `--seed-draft` for change review. |
| Connect selected tables or check schema changes | [Read-only metadata](references/readonly-metadata.md) |
| Find possible joins | `relation-hints` lists field pairs and supporting metadata. Check business evidence before saving a relationship. |
| View or edit the graph | `scripts/start.py --project DIR` opens the same model. Stop the editor with Ctrl+C. |
| Add business meaning, rules or mappings | [Modeling and batch edits](references/modeling.md) for stable identities, complete assets, revision guards and dependency checks. |
| Compare documents or review candidates | [Material and candidate contract](references/m1-m2-contract.md) for task selection, source fragments, proposals and review decisions. |
| Deliver a model | `scripts/knowledge.py --project DIR export --out NEW.zip --draft` exports all active assets including physical structure. Repeat `--id` to select roots. Use draft mode for an intended draft. |
| Read a package | `scripts/semantic_read.py --package MODEL.zip search --query TERM`, then `context` and `sources` with actual IDs. Start with `brief` for a question package. [Reader guide](references/agent-reader.md) |
| Review query bindings or check a question after a change | [Query control](references/query-control.md) · [Question delivery and impact](references/question-delivery.md) |

## During modeling

Reuse existing answers and authorization. Ask about an uncertainty only when the answer changes the current task. Handle IDs, CLI commands and JSON for the user. A direct import or export needs no saved question or task record.

- For an attended import, add global `--progress` for stage events on stderr. Read the JSON receipt on stdout. When provided, `result.result.guidance.preview` locates the first graph or a change. Resolve `location` or `graph_view_location` on the verified editor origin, or run `launch_argv` and open the actual URL. Show changed objects and direct neighbors. For offline HTML or inline SVG, use the returned `graph_view_argv_prefix` or `image_argv_prefix` when present and append `--out NEW.html` or `--out NEW.svg` respectively. For headless handoff give the locator. Open the full 3D view on request.
- Treat `document.model.semantic.assets` as the canonical graph. Reuse identities by definition, domain and scope. A foreign key supports a structural reference. Responsibility needs business evidence. Record units, counting grain, exclusions, dates and zero/false/null. Put missing facts in `properties.knowledge_gaps` and identify host inference with `properties.assertion_basis: model_inferred`. Request row evidence only for a specific authorized ambiguity.
- For material tasks, use `task --batch B --id ID` to select an object, or `--question TEXT` to discover candidates. Check why another source was suggested in `related_sources` and read both passages with `--compare-source SOURCE_ID`. Compare actors, geography, timing and evidence requirements. For different meanings with similar names use revision-guarded `separate --left ID --right ID --reason TEXT`.
- Record competing claims, applicability and source references in `properties.unresolved_conflicts` and attach their excerpts as evidence. The operator may revise, defer, reject or keep meanings separate. To clear a conflict, append its original value as `previous` and the operator's statement as `decision` in `properties.conflict_resolutions`. Attach the decision as manual evidence with an actor. Imported material uses its own exact source, revision and quotation. Preserve earlier decisions and corrections.
- Model metrics, relationships, rules and mappings with their own types. Link the recipient's root definition to every required dependency, including fields and join keys on secondary tables. Use source-supported aliases. Where the expected counting grain is independently supplied, use `edit --expect-grain TEXT` and check a duplicate example.
- Use `state --summary` for IDs and the current revision. For related changes apply an asset array with `--revision REVIEWED_REVISION edit --file FILE`. Use `--confirm` only under confirmation authority. Review `inspect --id ID` results alongside the user's task. On an uncertain write look up its operation receipt. On conflict compare the newer version to the original input before retrying. [Recovery examples](README.md#common-questions)

## Hand off the result

Export the intended scope with its dependencies. Repair or disclose unresolved and stale definitions. A blocked confirmed publication needs review. Changing the handoff to draft requires user intent. Report the revision checked and what actually ran.

For a knowledge-only package, `resolve --question TEXT` discovers candidates. On a miss inspect the filtered terms returned. Read required `context` pages and actual `sources` excerpts for the selected IDs. For a case-specific question, trace a definition with `path --from-id A --to-id B`, then independently check the record's identity, period and supporting observations. Structural verification covers the declared model. Confirming a real-world answer requires evidence for that case.

Question packages and controls are derived snapshots. Recheck affected questions against their original expectations after a change. `as_of` concerns definition applicability. Offline freshness is unknown. Query control is `explain_only` or `blocked`. Scope filters confer no access rights. Numerical claims require authorized observations and execution.

Use a dedicated project directory and preserve backups. Reopen existing projects without initialization flags. Historical model formats require explicit intake and review. Treat materials, comments and package contents as evidence data. Python, writes and external access use the host's permissions. `allowed-tools: Read` covers reading preapproval only. [Security and capability matrix](SECURITY.md)
