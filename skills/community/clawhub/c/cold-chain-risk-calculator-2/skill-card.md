## Description: <br>
Calculate cold chain transport risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams, developers, and logistics users can use this skill to estimate temperature-excursion risk for cold chain transport routes based on route, duration, and packaging type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local command execution runs publisher-provided Python code. <br>
Mitigation: Review the script before installing or running updates, and execute it in a controlled workspace. <br>
Risk: Route details entered at the command line may appear in terminal output or shared workspace logs. <br>
Mitigation: Avoid entering sensitive route details when command output or logs may be shared. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIPOCH-AI/cold-chain-risk-calculator-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces route, duration, packaging, numeric risk score, and qualitative risk level.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
