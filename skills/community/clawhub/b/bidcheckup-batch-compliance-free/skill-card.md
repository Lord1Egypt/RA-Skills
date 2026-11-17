## Description:

一次把多家投标文件的报价算术全部核一遍，不需要付款，也不需要注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement reviewers, bid teams, and agent workflows use this skill to locally check bidder line-item arithmetic, per-bidder verdicts, and missing or unverifiable quote rows before relying on bid materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake arithmetic check output for an official procurement, legal, or scoring decision.

Mitigation: Treat the result as an arithmetic aid only; a qualified human reviewer or evaluation committee should make procurement decisions.

Risk: Incomplete or malformed bidder data can lead to missing-input responses, unchecked bidders, or only partial arithmetic coverage.

Mitigation: Provide structured bidders data with item names, quantities, unit prices, and amounts, then review missing rows, unchecked bidders, and withheld checks before acting.

Risk: Running a local Node script on bid materials exposes those materials to the local execution environment.

Mitigation: Run the skill only in a trusted local environment and only on materials approved for local processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bidcheckup-batch-compliance-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or JSON report with per-bidder verdicts, findings, missing-input messages, and withheld checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution; exits with code 3 when input is insufficient and does not produce a conclusion.]

## Skill Version(s):

1.0.52 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
