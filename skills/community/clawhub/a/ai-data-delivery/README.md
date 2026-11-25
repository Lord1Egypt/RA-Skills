# AI Data Delivery · 0.3.10

**Turn a database schema into a source-linked semantic model that another Agent can read offline.**

[简体中文](README.zh-CN.md) · [Releases](https://github.com/franklinxkk/ai-data-delivery/releases) · [Security](SECURITY.md)

## Import a schema and read the result

Extract the ZIP and enter the directory containing `requirements.txt` and `scripts/`. Use Python 3.10 or later. On Windows you can substitute `py -3` or your virtual environment's Python. Install the pinned dependencies once.

```bash
python -m pip install -r requirements.txt
```

To check the installation, run `python scripts/smoke.py`. It imports synthetic tables and reads the exported package in a temporary directory. Use the commands below to keep a model you can edit.

Run the example in a fresh project directory. The import reads the supplied synthetic SQL as text and saves physical drafts. The export writes a new ZIP. The third command reads that ZIP in a separate process. These commands run locally without a server or model key.

```bash
python -X utf8 scripts/knowledge.py --project "./work/transport" import --file "examples/semantic-workbench/transport.sql" --seed-draft
python -X utf8 scripts/knowledge.py --project "./work/transport" export --out "./work/transport.zip" --draft
python -X utf8 scripts/semantic_read.py --package "./work/transport.zip" verify
```

In the first receipt, `result.result.seeded.counts` contains `{"dataset": 2, "field": 5, "relation": 1}`. The reader returns the following excerpt.

```json
{"status": "verified", "draft": true, "asset_count": 8, "complete": false}
```

The package passed integrity checks. All eight definitions are drafts. To inspect the vehicle table, search the package:

```bash
python -X utf8 scripts/semantic_read.py --package "./work/transport.zip" search --query vehicle --kind dataset
```

The example returns one match. Use `matches[0].asset.id` with `sources --id ID` to read the original `CREATE TABLE vehicle` passage. It establishes a reference from `vehicle.company_id` to `company.id`. Ownership and maintenance obligations need separate evidence. For a different schema, substitute your DDL path and use terms from its tables. [Reader commands and paging](references/agent-reader.md)

## Add a business definition

Try asking your Agent, “Which company is responsible for vehicle maintenance, and where does the source say so?” Register the bundled synthetic business notes in the **same project**:

```bash
python -X utf8 scripts/knowledge.py --project "./work/transport" import --file "examples/semantic-workbench/transport-v1.txt"
```

The receipt gives `result.result.batch_id`. The Agent can use `task --batch BATCH_ID` to read the passage “企业负责本企业车辆维护。” (“A company maintains its own vehicles.”). Attach the exact excerpt and its source revision to the business relationship, then inspect its dependencies. Keep that role in draft until authorized review. The previously exported ZIP still contains the earlier revision. Export to a new file to hand off the revised model. [Modeling and scoped export](references/modeling.md)

To review visually, run `python -X utf8 scripts/start.py --project "./work/transport"` and open the printed local URL. Click a table to inspect columns, or choose **New object** to create a business object. **Connect** takes the two endpoints in order and shows the direction before saving. **3D connections** opens the graph around a change. Stop the editor with **Ctrl+C**. To share that view offline, run `python scripts/knowledge.py --project "./work/transport" graph-view --out change.html` and review its included quotations before sharing.

## Common questions

| What happened? | What to do |
| --- | --- |
| Installation must work offline | On a connected machine with matching OS, architecture and Python version, run `python -m pip download --only-binary=:all: -r requirements.txt -d wheels`. Transfer the wheels, then run `python -m pip install --no-index --find-links ./wheels -r requirements.txt` at the destination. |
| The authoring CLI returned `argument_error` | Put global options such as `--project`, `--language zh`, `--revision` and `--progress` before the command. Put `--file`, `--seed-draft` or `--out` after their respective command. `--progress` writes stage events to stderr and keeps one JSON receipt on stdout. |
| The model already exists, or the SQL changed | Reopen the same project. Omit `--seed-draft` on subsequent imports and review the changes. For recurring DDL exports use a stable `--source-key` from first import, or use `--source-id` for a registered source. For GBK text use `import --encoding gb18030 --file FILE`. |
| The write result is uncertain, or another edit changed the project | For a retryable write, supply a unique global `--operation-id` up front. After interruption, run `receipt OPERATION_ID` on the same project. For `status: conflict`, use `state --summary` for the revision, read the affected assets in `state`, compare your input and reapply the reconciled edit with its reviewed revision. |
| Export failed | Use an existing destination directory and a new filename. For `details.code: NOT_PUBLISHABLE`, inspect the listed issues and review the relevant definitions and dependencies. Use `--draft` when the recipient requested a draft. |
| A reader search has no matches, or an ID is unknown | Inspect `fallback.candidates` for available terms on a no-match search. For `error.code: UNKNOWN_ID`, search the supplied snapshot and copy an ID from its matches. |

## Other tasks

| Goal | Entry point |
| --- | --- |
| Find possible joins in a schema with few foreign keys | `knowledge.py --project DIR relation-hints` lists field pairs with their metadata. Check business evidence before saving a relationship. |
| Connect selected SQLite, PostgreSQL or MySQL tables | [Read-only catalog setup](references/readonly-metadata.md) |
| Hand off a particular question or check the impact of a change | [Question handoff and impact](references/question-delivery.md) |
| Exchange definitions with Neo4j or ontology-graph-spec | [Offline interchange](references/neo4j-interop.md) |

The host Agent interprets the materials. This tool stores the model and its sources locally. Production queries, enterprise access control and multi-user administration are outside its scope. Keep a backup when upgrading an existing project. The distribution includes the MIT license in `LICENSE.md`. [Architecture](references/architecture.md) · [License in source](https://github.com/franklinxkk/ai-data-delivery/blob/main/LICENSE) · [Skill instructions](SKILL.md) · [Changelog](CHANGELOG.md)
