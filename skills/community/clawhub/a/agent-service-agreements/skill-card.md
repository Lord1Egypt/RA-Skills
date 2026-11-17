## Description:

Helps agents define, negotiate, sign, and verify machine-readable service agreements with SLAs, quality thresholds, payment terms, escrow terms, and automated verification criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfleetcommander](https://clawhub.ai/user/alexfleetcommander)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create and review service agreements before delegating or accepting agent work, then verify delivered work against agreed quality thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agreements may be mistaken for automatic payments or legally reviewed contracts.

Mitigation: Treat agreements as coordination records and separately validate legal terms and payment handling before relying on them.

Risk: Agreement store files written in the workspace can influence later delivery verification.

Mitigation: Install in a virtual environment, pin the PyPI package for reproducible review, and keep agreement store files under normal workspace review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexfleetcommander/skills/agent-service-agreements)
- [PyPI Package](https://pypi.org/project/agent-service-agreements/)
- [Service Agreements Whitepaper](https://vibeagentmaking.com/whitepaper/service-agreements/)
- [Vibe Agent Making](https://vibeagentmaking.com)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation, verification, listing, and review of local JSONL agreement records.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
