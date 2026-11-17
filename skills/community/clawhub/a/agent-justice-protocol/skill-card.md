## Description:

Dispute resolution, forensic investigation, and risk assessment for autonomous AI agent transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to file disputes, investigate failed agent-to-agent transactions, reconstruct provenance chains, and assess agent or transaction risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs an unpinned external Python package.

Mitigation: Install in a virtual environment or sandbox, and pin and verify the package version before use.

Risk: Dispute and provenance files may contain sensitive transaction details.

Mitigation: Pass only the dispute and provenance files needed for the investigation.

## Reference(s):

- [Agent Justice Protocol on ClawHub](https://clawhub.ai/alexfleetcommander/skills/agent-justice-protocol)
- [Agent Justice Protocol on PyPI](https://pypi.org/project/agent-justice-protocol/)
- [Justice Protocol Whitepaper](https://vibeagentmaking.com/whitepaper/justice-protocol/)
- [Vibe Agent Making](https://vibeagentmaking.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dispute filing guidance, forensic investigation workflows, and risk assessment examples for local provenance and dispute files.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
