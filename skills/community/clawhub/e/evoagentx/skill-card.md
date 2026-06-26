## Description: <br>
EvoAgentX - Self-evolving AI agents framework integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to install, inspect, open documentation for, and run EvoAgentX workflows from an agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Core commands depend on an evoagentx.ps1 PowerShell helper that was not included for review. <br>
Mitigation: Inspect the helper script before running it, verify its source, and execute installs in a contained environment. <br>
Risk: The skill may use provider API keys and agent memory when running EvoAgentX workflows. <br>
Mitigation: Use scoped or disposable API keys and avoid sensitive prompts until provider and memory behavior are understood. <br>


## Reference(s): <br>
- [EvoAgentX GitHub Repository](https://github.com/EvoAgentX/EvoAgentX) <br>
- [EvoAgentX Website](https://evoagentx.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/nantes/evoagentx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.12, the evoagentx package, and a provider API key; core commands rely on an evoagentx.ps1 helper that was not included for review.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
