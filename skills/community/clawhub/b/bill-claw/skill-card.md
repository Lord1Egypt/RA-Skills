## Description: <br>
BillClaw helps an agent manage a local personal-finance ledger through a Python CLI backed by SQLite, including transaction entry, querying, guarded deletion and category merging, reports with chart PNGs, CSV export, and a local Flask dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[520MianXiangDuiXiang520](https://clawhub.ai/user/520MianXiangDuiXiang520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use BillClaw to manage local bookkeeping workflows: add and query income or expense records, maintain categories, preview and confirm destructive updates, generate financial reports, export CSV data, and open a local dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages a local personal-finance ledger and may produce private CSV or PNG report files. <br>
Mitigation: Keep database backups, treat exports and generated charts as private, and delete report files only after explicit user approval. <br>
Risk: Deletion and category-merge operations can change or remove ledger records. <br>
Mitigation: Use the documented preview step first and run the confirm command only after the user explicitly approves the listed records. <br>
Risk: The optional dashboard exposes ledger data through a local Flask web server. <br>
Mitigation: Keep the dashboard bound to 127.0.0.1, stop it when finished, and avoid exposing the port to a network. <br>
Risk: Unpinned dependency ranges can reduce install reproducibility. <br>
Mitigation: Prefer pinned dependencies or a lockfile before deployment in a managed environment. <br>


## Reference(s): <br>
- [BillClaw ClawHub release page](https://clawhub.ai/520MianXiangDuiXiang520/bill-claw) <br>
- [BillClaw skill instructions](artifact/SKILL.md) <br>
- [BillClaw setup guide](artifact/SETUP.md) <br>
- [Bundled dashboard vendor dependencies](artifact/scripts/static/vendor/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Concise user-facing text or Markdown with inline shell commands; the CLI returns one-line JSON and can create PNG chart reports or CSV exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite ledger by default at db/expenses.db; BILLCLAW_DB_PATH can override the database path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
