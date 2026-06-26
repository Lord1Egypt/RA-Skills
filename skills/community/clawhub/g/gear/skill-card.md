## Description: <br>
Use when calculating gear ratios, converting RPM between shafts, computing torque output, analyzing drivetrain configurations, or selecting motors for mechanical systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical users use this skill to calculate gear ratios, convert shaft speeds, estimate torque output, analyze multi-stage drivetrains, and get motor selection guidance for mechanical systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Engineering calculations or motor guidance could be applied as final design decisions without validation. <br>
Mitigation: Treat outputs as calculation aids and review them against project requirements, safety factors, and applicable engineering standards before use. <br>
Risk: The skill executes a local Bash script with embedded Python calculations. <br>
Mitigation: Review the script before running it and execute it only in an environment where local shell execution is acceptable. <br>


## Reference(s): <br>
- [Gear on ClawHub](https://clawhub.ai/bytesagain3/gear) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal calculation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Bash commands call Python 3 to produce calculation summaries and engineering guidance; outputs are calculation aids, not certified design decisions.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
