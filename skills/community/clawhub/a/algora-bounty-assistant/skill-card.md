## Description:

Automatically search for low-competition GitHub bounty tasks with fewer than five comments and generate a concise report with details and estimated difficulty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[santosparra651-arch](https://clawhub.ai/user/santosparra651-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bounty hunters use this skill to search open GitHub issues labeled as bounties, prioritize low-comment opportunities, and review concise difficulty or value signals before choosing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx commands can execute package code that differs from the reviewed artifact.

Mitigation: Install or run a pinned reviewed version, or inspect the package source before execution.

Risk: The included analyze.js file is not part of the documented primary search command.

Mitigation: Treat analyze.js as nonessential and inspect it before intentionally running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/santosparra651-arch/skills/algora-bounty-assistant)
- [Publisher profile](https://clawhub.ai/user/santosparra651-arch)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console report with issue titles, URLs, comment counts, and difficulty or value signals.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an optional maximum comment count argument for the bounty search command.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
