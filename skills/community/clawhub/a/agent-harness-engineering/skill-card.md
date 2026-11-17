## Description:

Bootstrap or upgrade a software repository for agent-first engineering with concise AGENTS.md routing, progressive-disclosure docs, mechanical quality checks, CI-enforced structure, and optional maintenance loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeyitech](https://clawhub.ai/user/yeyitech)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to add or refresh agent-readable repository docs, AGENTS.md routing, validation checks, and optional reporting so coding agents can work with clearer context and guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap can modify repository documentation, AGENTS.md, and validation structure.

Mitigation: Run the bootstrap in dry-run mode first, inspect the proposed changes, and review generated docs before committing.

Risk: Generated documentation and checks may contain project assumptions that are incomplete for the target repository.

Mitigation: Customize doc owners, review dates, command names, architecture notes, quality gates, reliability expectations, and security assumptions after scaffolding.

Risk: Garbage-collection findings could be over-applied as cleanup instructions.

Mitigation: Use garbage collection as a reporting and review loop; require human review before cleanup patches are merged.

## Reference(s):

- [Bootstrap Playbook](references/bootstrap-playbook.md)
- [Docs Blueprint](references/docs-blueprint.md)
- [Quality Gates](references/quality-gates.md)
- [Garbage Collection](references/garbage-collection.md)
- [ClawHub Skill Page](https://clawhub.ai/yeyitech/skills/agent-harness-engineering)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated repository files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold AGENTS.md, CLAUDE.md, docs/agent files, and validation scripts in a target repository.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
