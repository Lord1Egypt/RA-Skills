## Description: <br>
Scan Solidity repositories for Atlas smart-contract vulnerability patterns and generate triage-ready security reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n8gendegen](https://clawhub.ai/user/n8gendegen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External auditors, bounty hunters, DeFi teams, and agent builders use this skill to run a local first-pass Solidity triage scan and prepare candidate vulnerability reports for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner produces heuristic vulnerability candidates rather than verified findings. <br>
Mitigation: Require manual validation, proof-of-concept review, and impact analysis before disclosure, bounty submission, or severity claims. <br>
Risk: Running the scanner reads local Solidity repositories and writes reports to a chosen output directory. <br>
Mitigation: Run it only against repositories intended for analysis and choose the output directory deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n8gendegen/atlas-vuln-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/n8gendegen) <br>
- [Atlas homepage](https://atlasagentsuite.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON scanner logs, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces heuristic flags, confidence labels, candidate finding writeups, and executive summaries that require manual validation before disclosure or severity claims.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
