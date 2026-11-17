## Description:

Automates a Chinese web-novel workflow that helps generate, format, review, and publish chapters to Fanqie Novel through dependent OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjiahui11](https://clawhub.ai/user/chenjiahui11)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and operators use this skill to move from a story idea or existing chapter files to formatted chapters published under a configured Fanqie Novel author account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish chapters to a real Fanqie account without a strong confirmation boundary.

Mitigation: Review generated chapters manually, test with non-critical works, and verify the target work title before publishing.

Risk: The workflow depends on unpinned external generation and publishing skills.

Mitigation: Pin or verify open-novel-writing, novel-generator, and fanqie-publisher before relying on the workflow.

Risk: The workflow reads local novel chapter files and uses Fanqie author login or session data.

Mitigation: Install only in an environment where those files and session credentials are appropriate for this workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjiahui11/skills/fanqie-novel-auto-publish)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local chapter files and publish externally through a configured Fanqie session.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
