## Description:

Remove obvious AI-writing traces from Chinese text in a constrained way while preserving facts, data, structure, and the article's core argument.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and content developers use this skill to clean up Chinese Markdown or plain-text drafts that read too much like AI output while preserving facts, numbers, headings, structure, and core claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or overwrites the documented humanized Markdown and JSON report paths for the chosen slug.

Mitigation: Review the input slug and output paths before running, and keep source drafts under version control or backed up.

Risk: The packaged README references a requirements.txt file that is not present in the artifact.

Mitigation: Verify the runtime environment provides the required skill runtime dependencies before local execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-humanizer-zh)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [Humanized Markdown file plus JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or overwrites disclosed draft output paths for the selected slug.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
