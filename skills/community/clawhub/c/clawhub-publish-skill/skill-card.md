## Description:

Automates publishing a local skill directory to ClawHub, including token checks, CLI patch guidance, slug conflict handling, and rate-limit retry handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to publish local agent skill directories to ClawHub with guided checks, publishing commands, duplicate detection, and recovery paths for common publish errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may patch globally installed ClawHub CLI files.

Mitigation: Run it only in a disposable or tightly scoped environment and require explicit review before applying any CLI patch.

Risk: The publishing flow uses a ClawHub token.

Mitigation: Provide tokens through a safer secret mechanism and avoid recording tokens in prompts, logs, or command history.

Risk: The skill may install or rely on globally installed CLI packages.

Mitigation: Prefer pinned, reviewed CLI versions and avoid unpinned global installs in sensitive environments.

Risk: Automated publish or retry behavior can release content without enough oversight.

Mitigation: Require explicit confirmation before publishing, changing slugs, or scheduling retries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/clawhub-publish-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include publish commands, retry instructions, validation steps, and success or error summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
