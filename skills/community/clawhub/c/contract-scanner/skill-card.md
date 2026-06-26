## Description: <br>
Advertises smart-contract security scanning for honeypot detection, tax analysis, ownership checks, and risk scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbrc20](https://clawhub.ai/user/alexbrc20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to ask an agent for smart-contract risk checks before reviewing or trading tokens. Because the included scanner returns simulated results, its output should be treated as a prompt for manual review rather than trading or security advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill advertises real smart-contract safety checks while the included scanner returns hard-coded low-risk results. <br>
Mitigation: Treat outputs as incomplete demo results, review the implementation before installation, and do not rely on its output for trading or security decisions. <br>
Risk: The artifact declares an Etherscan API key requirement even though the included scanner does not perform documented real analysis. <br>
Mitigation: Do not provide an Etherscan API key unless the publisher replaces the mock logic with real documented analysis and removes definitive trading advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexbrc20/contract-scanner) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/alexbrc20) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown usage examples and console-style text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and curl; declares ETHERSCAN_API_KEY as an environment requirement.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
