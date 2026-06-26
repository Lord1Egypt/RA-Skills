## Description: <br>
Provides a least-privilege interface for managing user data, personas, memory, and configuration snapshots in MyVector/MySQL with input validation and secret redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use VectorClaw to install and operate a self-hosted MyVector/MySQL memory database for user profiles, interaction history, preferences, moods, relationships, agent learnings, and retrieval-time knowledge graph context. The skill is intended for controlled deployments where administrators can enforce opt-in consent, retention, deletion, backups, and least-privilege database access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VectorClaw can persist broad sensitive user profiles, inferred facts, mood data, relationships, and agent reasoning logs. <br>
Mitigation: Require explicit per-user opt-in before enabling storage or auto-extraction, keep auto-extraction in dry-run or human-review mode until validated, disable or remove thought_stream chain-of-thought logging, and honor deletion requests through the provided rollback workflow. <br>
Risk: Database credentials and schema migrations can expose data or damage a production database if handled casually. <br>
Mitigation: Use a dedicated least-privilege MySQL user, protect and rotate credentials, run migrations only after backups, and test migrations, retention, and deletion behavior on non-production data first. <br>
Risk: Auto-extracted or graph-derived memories may be inaccurate or overly sensitive. <br>
Mitigation: Review extracted memories before they affect agent behavior, use human verification flags for promoted facts, and prefer dry-run consolidation before committing graph edges. <br>


## Reference(s): <br>
- [VectorClaw ClawHub Page](https://clawhub.ai/paradoxfuzzle/custom-mysql) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CAPABILITIES.md](artifact/CAPABILITIES.md) <br>
- [SETUP_GUIDE.md](artifact/SETUP_GUIDE.md) <br>
- [changelog.md](artifact/changelog.md) <br>
- [rollback_user.sql](artifact/rollback_user.sql) <br>
- [MyVector](https://github.com/askdba/myvector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and SQL command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose database reads and writes, setup steps, migrations, retention actions, and deletion workflows that require operator review and environment-specific credentials.] <br>

## Skill Version(s): <br>
5.0.1 (source: server release metadata and SKILL.md version section, released 2026-05-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
