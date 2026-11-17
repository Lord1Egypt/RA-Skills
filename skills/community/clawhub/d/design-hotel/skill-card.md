## Description:

Discover design-forward boutique hotels with curated interiors, architectural concepts, artistic experiences, and real-time booking details through the flyai CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search for boutique, design-forward, art-themed, or scenic hotels and present results with real-time booking links. It is intended for hotel discovery workflows that require current FlyAI/Fliggy data instead of static travel knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or invoke a global npm CLI and execute local shell commands.

Mitigation: Review the skill before installation and run it in an isolated environment with explicit approval for package installation.

Risk: Hotel searches can send travel details to FlyAI/Fliggy and return mandatory commercial booking links.

Mitigation: Use the skill only when the user accepts external travel-query processing and clearly present booking links as live third-party results.

Risk: The runbook behavior can keep plaintext logs of raw user travel queries.

Mitigation: Avoid persistent logging of sensitive travel details or store only approved, redacted execution records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/design-hotel)
- [Fallbacks](references/fallbacks.md)
- [Playbooks](references/playbooks.md)
- [Runbook](references/runbook.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for hotel results; result entries must include booking detail URLs.]

## Skill Version(s):

3.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
