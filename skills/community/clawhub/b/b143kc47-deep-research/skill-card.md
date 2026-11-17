## Description:

Deep Research helps agents perform adaptive, evidence-backed research, literature review, project due diligence, claim verification, and cited synthesis across web pages, papers, official docs, repositories, datasets, local files, and conflicting perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b143kc47](https://clawhub.ai/user/b143kc47)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research-focused agents use this skill for broad, auditable research tasks such as literature reviews, claim verification, technical due diligence, project comparisons, and cited reports where multiple source classes and counterevidence checks matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ledger tool can delete directories outside its research folder if invoked with unsafe reset options.

Mitigation: Run the skill in a restricted workspace and avoid using --force or path-like --name values until reset target validation is confirmed.

Risk: Evidence logs may capture secrets, private data, or unnecessary personal information.

Mitigation: Do not store secrets or unnecessary private data in logs, and review generated research artifacts before sharing.

Risk: Research outputs can contain incorrect, stale, or misleading guidance when sources are weak or adversarial.

Mitigation: Prefer primary sources, record evidence IDs and locators for high-impact claims, search for counterevidence, and review conclusions before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b143kc47/skills/b143kc47-deep-research)
- [ClawDIS homepage](https://github.com/B143KC47/deep-research-skill)
- [Research protocol](references/research-protocol.md)
- [Query playbook](references/query-playbook.md)
- [Source quality guide](references/source-quality.md)
- [Project and paper research patterns](references/project-and-paper-patterns.md)
- [Report template](references/report-template.md)
- [Evaluation checklist](references/evaluation.md)
- [OpenClaw installation notes](references/openclaw-install.md)
- [Design bibliography and influences](references/bibliography.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional ledger artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cited reports, evidence tables, research ledgers, limitations, uncertainty notes, and practical next steps.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
