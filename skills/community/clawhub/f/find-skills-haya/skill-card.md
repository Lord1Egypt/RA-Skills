## Description: <br>
Helps users discover and install agent skills for requests that may match installable capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hayasam](https://clawhub.ai/user/hayasam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to identify relevant installable skills, compare basic quality signals, and install selected skills when they want to extend an agent's capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may steer broad requests toward globally installing third-party skills with confirmation suppressed. <br>
Mitigation: Verify the exact skill source and install command before execution; prefer explicit confirmation or a test environment for third-party skills. <br>
Risk: Search results or popularity signals may be insufficient to establish trustworthiness. <br>
Mitigation: Review install counts, source reputation, repository health, and security guidance before recommending or installing a skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hayasam/find-skills-haya) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend third-party skill searches and installation commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
