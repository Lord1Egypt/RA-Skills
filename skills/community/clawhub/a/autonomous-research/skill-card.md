## Description:

Autonomous Research helps agents conduct independent research by finding sources, evaluating credibility, synthesizing findings, and producing cited reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to plan and execute broad research tasks, evaluate source reliability, synthesize findings, and generate structured reports or briefs with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad autonomous research may send sensitive topics or prompts to external search and website providers.

Mitigation: Use only for topics suitable for external providers, avoid secrets or regulated data, and require confirmation before networked research when appropriate.

Risk: External API and data-flow behavior is under-scoped in the release evidence.

Mitigation: Review the skill before installation and document expected external providers, inputs, and outputs for the deployment environment.

Risk: The npm dependency appears unpinned or unnecessary in the release evidence.

Mitigation: Pin the dependency to an approved version or remove it if it is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobisamaa/skills/autonomous-research)
- [Publisher profile](https://clawhub.ai/user/tobisamaa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, executive briefs, comparative summaries, citation lists, and inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require networked research through external search and website providers.]

## Skill Version(s):

1.0.0 (source: release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
