## Description: <br>
Axioma Guard checks OpenClaw skill names against the Clawdex service and can produce terminal guidance for suspicious results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Advanced OpenClaw users can use this skill to look up skill names in a reputation service before installation or review. It is best treated as advisory security guidance rather than a complete scanner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill overstates its scanning capability. <br>
Mitigation: Treat results as a limited skill-name reputation lookup and continue normal code review and security scanning before installation. <br>
Risk: The security evidence notes under-disclosed network behavior. <br>
Mitigation: Install only if sharing skill names with Clawdex and possible Merlin API submissions is acceptable for the environment. <br>
Risk: The security guidance says status output should not be treated as proof that services are reachable. <br>
Mitigation: Verify network connectivity and endpoint behavior separately before relying on reported status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiomaguard-en) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with status messages and generated guidance] <br>
**Output Parameters:** [1D; accepts a skill name for targeted checks or local skill directory names for scans] <br>
**Other Properties Related to Output:** [May call external Clawdex and Merlin endpoints during checks and vaccine generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
