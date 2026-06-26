## Description: <br>
Claw Brain is a personal AI memory system for OpenClaw and ClawDBot that provides memory, personality, bonding, learning capabilities, encrypted secrets support, and automatic refresh on service restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawcolab](https://clawhub.ai/user/clawcolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to add persistent memory, personality context, user preference learning, and startup memory refresh to OpenClaw or ClawDBot agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to install external package or source code that manages secrets and startup hooks. <br>
Mitigation: Install only from a trusted PyPI or GitHub release, verify the selected version before setup, and review hook behavior before enabling it. <br>
Risk: Memories and user profiles may persist locally, and only records marked as secrets are described as encrypted. <br>
Mitigation: Keep the database and encryption key private, restrict file permissions, and avoid storing sensitive data unless it is intentionally handled as a secret. <br>
Risk: The security review notes that some included claims do not match the reviewed package. <br>
Mitigation: Confirm the packaged files and setup instructions for the exact release before relying on documented installation, environment, or security claims. <br>


## Reference(s): <br>
- [Claw Brain ClawHub Listing](https://clawhub.ai/clawcolab/clawbrain) <br>
- [ClawBrain Repository](https://github.com/clawcolab/clawbrain) <br>
- [Security Documentation](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown with inline command examples and Python API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can provide agent memory context, personality guidance, setup commands, and configuration guidance.] <br>

## Skill Version(s): <br>
0.1.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
