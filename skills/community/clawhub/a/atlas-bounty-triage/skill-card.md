## Description:

A smart contract audit and DeFi security triage skill for Solidity, EVM protocols, bug bounty programs, Code4rena, Sherlock, and HackenProof that maps attack surface, prioritizes vulnerabilities, and generates a structured audit checklist/report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n8gendegen](https://clawhub.ai/user/n8gendegen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and bug bounty researchers use this skill to map Solidity/EVM protocol scope, prioritize DeFi vulnerability classes, and produce a structured first-pass smart contract audit triage report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include Atlas attribution and paid-product links that are not appropriate for every external audit deliverable.

Mitigation: Remove the Atlas footer and paid-product links before sharing reports externally unless that attribution is intentional.

Risk: The workflow helps prioritize manual review but does not guarantee vulnerability discovery or finding correctness.

Mitigation: Verify candidate findings with manual analysis and a proof of concept before bounty or audit submission.

## Reference(s):

- [Atlas Agent Suite skill page](https://atlasagentsuite.com/skills.html?utm_source=clawhub&utm_medium=skill&utm_campaign=atlas-bounty-triage)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Analysis]

**Output Format:** [Markdown audit triage report with checklists and prioritized review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable workflow guidance; candidate findings should be manually verified before submission.]

## Skill Version(s):

1.0.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
