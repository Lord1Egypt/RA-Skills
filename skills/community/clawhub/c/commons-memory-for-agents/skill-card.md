## Description: <br>
OpenClaw Agent Memory Commons helps OpenClaw agents search, validate, contribute, and sync privacy-safe knowledge cards for shared fixes, workflows, integration notes, benchmarks, and tool recipes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mixomaxo](https://clawhub.ai/user/mixomaxo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to reuse evidence-backed operational knowledge, search and validate local cards, and stage privacy-safe contributions for review before public publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional scheduled sync jobs update local reports and refresh shared knowledge cards on a schedule. <br>
Mitigation: Enable cron jobs only after reviewing the workflow and confirming that scheduled ClawHub updates and local report files are acceptable. <br>
Risk: GitHub setup and push flows can publish files from a maintainer workspace. <br>
Mitigation: Treat publishing commands as maintainer actions: review tracked files, avoid secrets, use least-privilege tokens, and prefer manual or private-repository review until the published contents are inspected. <br>
Risk: Shared knowledge cards can become unsafe or misleading if private data, secrets, or unverified advice bypass review. <br>
Mitigation: Use the built-in validation and review flow, reject cards containing private data or credentials, and publish public cards through reviewed pull requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mixomaxo/skills/commons-memory-for-agents) <br>
- [Publisher Profile](https://clawhub.ai/user/mixomaxo) <br>
- [Architecture](docs/architecture.md) <br>
- [Discovery and Installation](docs/discovery.md) <br>
- [Governance](docs/governance.md) <br>
- [Threat Model](docs/threat-model.md) <br>
- [Knowledge Card Schema](docs/knowledge-card.schema.json) <br>
- [Static Card Index](site/index.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON knowledge cards, static JSON/HTML indexes, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local pending proposals and reports are written under OpenClaw state; public cards are reviewed before distribution.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence; artifact frontmatter reports 1.0.11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
