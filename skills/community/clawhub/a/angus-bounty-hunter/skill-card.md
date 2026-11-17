## Description:

Automated smart contract bug bounty hunting that scans Immunefi and Code4rena targets with Slither static analysis, triages findings with local LLMs, and generates PoC templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipp11](https://clawhub.ai/user/chipp11)

### License/Terms of Use:


## Use Case:

Developers and smart contract security researchers use this skill to scan Solidity bug bounty targets, triage high- and medium-impact Slither findings, and prepare follow-up PoC work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan workflow can run dependency installation steps from untrusted target repositories on the user's machine.

Mitigation: Run scans only in a disposable container or VM with no sensitive host credentials, wallet files, SSH agents, or cloud tokens available; review or disable npm and pip install steps before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chipp11/skills/angus-bounty-hunter)

## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Code, Markdown, Guidance]

**Output Format:** [Markdown with bash commands and scanner output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Slither JSON/text result files and PoC template guidance when used with the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
