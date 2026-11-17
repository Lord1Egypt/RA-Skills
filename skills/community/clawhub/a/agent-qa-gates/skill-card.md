## Description:

Agent QA Gates provides output validation gates for AI agent systems to reduce hallucinated data, leaked internal context, wrong formats, duplicate sends, post-compaction drift, and false delegated completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to apply tiered QA gates before an agent delivers human-facing, external, technical, or delegated-work output. It helps classify blocking issues, identify fix-before-ship problems, and evolve validation gates from observed failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger scope is broad, so the skill may activate in conversations where a narrower QA checklist would be more appropriate.

Mitigation: Narrow trigger phrases or invocation rules to the specific delivery surfaces and agent workflows where these gates are required.

Risk: The helper script prints terminal output and scanner findings directly, which can expose sensitive text if run on untrusted files.

Mitigation: Review inputs before running the script and sanitize or suppress command output when checking untrusted files or artifacts.

Risk: The skill is a lightweight QA aid rather than a complete automated safety system.

Mitigation: Use it as a review gate alongside human review, source verification, and deployment-specific security controls.

## Reference(s):

- [Gate Detail Reference](artifact/references/gates-detail.md)
- [QA Check Script](artifact/scripts/qa-check.sh)
- [ClawHub Skill Page](https://clawhub.ai/zurbrick/skills/agent-qa-gates)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes gate tiers, protocol checklists, severity classifications, and optional local QA script output.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
