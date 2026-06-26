## Description: <br>
Autonomous bug bounty hunting with scope safety for authorized targets, scanning subdomains, JavaScript secrets, misconfigurations, and known vulnerabilities with LLM-assisted analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lugave11](https://clawhub.ai/user/Lugave11) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External security researchers and developers use this skill to run authorized bug bounty scans, analyze findings, and produce structured security reports for approved targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive live scans and recurring scans with weak scope controls. <br>
Mitigation: Run it only for explicitly authorized programs and replace the sample authorization check with strict hostname and subdomain-boundary validation before use. <br>
Risk: External scanner binaries may be introduced during setup. <br>
Mitigation: Verify scanner binaries and their sources independently before installing or executing them. <br>
Risk: Raw secrets or sensitive findings could be sent to cloud models or shared alert channels. <br>
Mitigation: Avoid sending raw secrets to cloud models or shared alert channels unless the program and data handling policy explicitly approve it. <br>
Risk: The documented cron schedule can create unintended recurring scans. <br>
Mitigation: Do not enable scheduled scans unless recurring scanning is intentional, approved, and monitored. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Lugave11/bounty-hunter-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dated security reports and intermediate JSON or Markdown findings for authorized targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
