## Description: <br>
Entry point for the Elytro wallet skill plus the curated DeFi sub-skills. Start here before loading any individual protocol skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeExplorer29](https://clawhub.ai/user/CodeExplorer29) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill as the starting point for Elytro smart-account wallet workflows and curated DeFi protocol flows such as token swaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The linked CLI and sub-skills may help prepare or execute wallet or DeFi transactions. <br>
Mitigation: Verify the @elytro/cli package and Elytro repository, review each loaded sub-skill separately, and approve wallet actions only after checking transaction details. <br>
Risk: This entry-point skill delegates important behavior to wallet, execution, and protocol-specific sub-skills. <br>
Mitigation: Load only the sub-skills needed for the workflow and review their instructions before using them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/CodeExplorer29/elytro-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
