## Description:

招投标处理专家 routes pasted bidding tables to local checks for contract consistency, bid comparison, bid deposits, batch compliance, collusion indicators, performance bonds, and full tender compliance, returning line-referenced conclusions when the required inputs are present.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, finance, and compliance reviewers use this skill to paste bidding, contract, deposit, or bond tables and receive local rule-based checks with missing-input notices when the material is incomplete. Its outputs support human review and should not be treated as final legal, procurement, or anti-collusion determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a local usage counter in the user's home directory and stops after the free-use limit.

Mitigation: Review the local counter behavior before installation and run it only in an environment where this local state file is acceptable.

Risk: Compliance and collusion outputs may be mistaken for authoritative legal, procurement, or anti-collusion decisions.

Mitigation: Use the findings as review aids and require qualified human review before taking procurement, legal, or enforcement action.

Risk: Documentation may not consistently match the checks executed by the package.

Mitigation: Validate behavior with representative sample tables and inspect the reported missing-input and unexecuted-check notices before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-bidding-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON results from local Node.js command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include sub-skill routing, missing-input notices, line-referenced findings, and a local free-use counter message.]

## Skill Version(s):

1.0.10 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
