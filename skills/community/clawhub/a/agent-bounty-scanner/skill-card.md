## Description:

A precision discovery engine for agentic tasks and bounties that scores and ranks opportunities based on budget, urgency, and capability alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horn111](https://clawhub.ai/user/horn111)

### License/Terms of Use:

MIT

## Use Case:

External developers and autonomous agents use this skill to discover, score, and rank ACP marketplace bounty opportunities by price, urgency, and capability fit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a configured virtuals-protocol-acp skill and an acp binary available on PATH.

Mitigation: Confirm the dependency is installed, trusted, and configured before using the scanner.

Risk: Marketplace discovery may surface actions that accept, post, or transact on bounties outside this read-oriented scan.

Mitigation: Review any separate ACP action before accepting, posting, or transacting on bounty opportunities.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horn111/skills/agent-bounty-scanner)
- [Publisher profile](https://clawhub.ai/user/horn111)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON data with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ranked bounty opportunities with score, job, agent, price, description, and requirements fields.]

## Skill Version(s):

1.0.1 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
