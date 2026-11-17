## Description:

Scans Solidity Hardhat projects with Slither, tests, coverage, and heuristics, then documents or applies fixes until configured severity gates are clear or the sprint limit is reached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jengajojo](https://clawhub.ai/user/jengajojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-contract engineers use this skill before deployment, after refactors, or in CI to scan Solidity contracts, analyze severity-ranked findings, document patch rationale, and apply limited automated fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically rewrite smart-contract source files without clear user control.

Mitigation: Run it only in a clean disposable branch or sandbox and manually review every generated diff before keeping changes.

Risk: The skill runs project-local build, test, Slither, and coverage commands in the target repository.

Mitigation: Do not run it on untrusted projects or production worktrees with secrets in the environment.

Risk: The artifact presents its workflow as mandatory, which can overstate its authority over project completion decisions.

Mitigation: Treat the skill output as advisory and keep human security review and project approval gates in place.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jengajojo/skills/auto-bug-finder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON sprint data, patch Markdown, and console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes auto-bug-finder/FINAL-REPORT.md, sprint-results.json, and patch docs; may modify the configured Solidity contract file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
