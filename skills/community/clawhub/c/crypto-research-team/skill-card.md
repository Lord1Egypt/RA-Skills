## Description:

Tracks on-chain activity, market data, and project fundamentals to produce dated crypto research briefs using a coordinated team of specialized agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t3ratech](https://clawhub.ai/user/t3ratech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this agent configuration bundle to coordinate specialized research roles that gather crypto market, on-chain, and project-fundamental signals and turn them into dated research briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill asks for broad research, file, memory, scheduling, event, and MCP authority that is not clearly bounded to its stated crypto research purpose.

Mitigation: Install only in a tightly sandboxed workspace and constrain file writes, schedules, events, memory, and MCP tool access to the expected research workflow.

Risk: The security guidance notes a non-crypto business research role that may be outside the stated crypto research purpose.

Mitigation: Confirm that role is expected for this release or remove it before use.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the skill carefully before installation and run its bundled evaluation set before using it for work.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/t3ratech/skills/crypto-research-team)
- [Publisher profile](https://clawhub.ai/user/t3ratech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated briefs synthesized from coordinated role outputs; no environment variables are required beyond a model provider key.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
