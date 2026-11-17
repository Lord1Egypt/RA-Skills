## Description:

Detects contradictions between multi-agent instruction files, cron prompts, skills, and hooks that can cause inconsistent agent behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[korengast](https://clawhub.ai/user/korengast)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of OpenClaw multi-agent workspaces use this skill to audit agent instructions, cron prompts, skills, and hooks for conflicting rules before inconsistent behavior reaches users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad workspace inspection may expose instruction files, memories, user preferences, cron prompts, skills, and hooks to the invoking agent.

Mitigation: Run the audit only on user-approved agents or workspaces, and review the report before sharing it outside the operating context.

Risk: Reports may quote sensitive or unrelated prompt content while documenting contradictions.

Mitigation: Redact secrets, personal data, and unrelated prompt text from findings before forwarding or publishing the report.

Risk: Proposed fixes can change agent behavior if applied without review.

Mitigation: Require user confirmation for diffs and re-read affected files after every fix to verify the contradiction was resolved.

## Reference(s):

- [Contradiction Detector on ClawHub](https://clawhub.ai/korengast/skills/contradiction-detector)
- [Discovery Procedure](references/discovery.md)
- [Contradiction Patterns](references/contradiction-patterns.md)
- [Reporting and Fixes](references/reporting-and-fixes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown findings with quoted evidence, proposed diffs, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports proposed fixes for user confirmation before changes are applied.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
