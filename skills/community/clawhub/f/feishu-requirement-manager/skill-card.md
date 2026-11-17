## Description:

Helps an agent manage Feishu Bitable requirements by creating requirements and tasks, splitting work, tracking progress, and handling custom fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoxiaohei2026-tech](https://clawhub.ai/user/maoxiaohei2026-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to organize product or engineering requirements in Feishu Bitable, create linked tasks, assign executors, and review progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store Feishu app_token and table_id values in shared memory.

Mitigation: Confirm that storing these identifiers in shared memory is acceptable for the workspace before first use.

Risk: The skill can guide an agent to create or modify Feishu Bitable tables and records.

Mitigation: Confirm the allowed Feishu app and tables before allowing requirement, task, or project record changes.

## Reference(s):

- [Usage Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/maoxiaohei2026-tech/skills/feishu-requirement-manager)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Markdown]

**Output Format:** [Markdown guidance with JSON-style Feishu Bitable call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create or update Feishu Bitable records and store app_token and table_id values in shared memory.]

## Skill Version(s):

3.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
