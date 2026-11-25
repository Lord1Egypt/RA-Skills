## Description:

Generates structured daily work diaries from available conversation records and related materials, then archives them to notes and knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openmsg88](https://clawhub.ai/user/openmsg88)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other knowledge workers use the skill to turn a day's recorded work into a consistent diary, backfill a missing day, and archive entries to their chosen notes and knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a suspicious verdict and a confirmed concern about API keys in command-line arguments.

Mitigation: Review the scripts before use, run them only in a trusted environment, restrict credential access, and rotate credentials if exposure is suspected.

Risk: The security assessment says coverage was partial because two referenced local paths were missing.

Mitigation: Confirm referenced files are present and review the complete skill contents before installation or execution.

## Reference(s):

- [Troubleshooting guide](references/troubleshooting.md)
- [Daily Work Diary on ClawHub](https://clawhub.ai/openmsg88/skills/daily-work-diary)
- [IMA Agent Interface](https://ima.qq.com/agent-interface)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON]

**Output Format:** [Structured Markdown diary with an archive status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed daily template; includes only supported facts and leaves unavailable details out.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
