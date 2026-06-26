## Description: <br>
The AEIF-based long-term memory hub for AI Agents to prevent repeating bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[404-UNKNOW](https://clawhub.ai/user/404-UNKNOW) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to consult and commit reusable experience capsules so an agent can retrieve prior fixes, inject EvoMap advice, and list stored memories during troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores session-derived memory that may contain secrets, proprietary details, or sensitive work context. <br>
Mitigation: Use manual commits for sensitive work, avoid storing secrets or proprietary session details, and review stored capsules before reuse. <br>
Risk: The bundled high-trust advice can recommend weakening Git security globally through TLS bypass behavior. <br>
Mitigation: Remove or ignore the bundled Git SSL-disable capsule and do not apply global TLS-bypass commands unless the security impact is understood and reversible. <br>
Risk: Configured LLM clients used for distillation or verification may transmit session data outside the local environment. <br>
Mitigation: Verify where any configured LLM client sends data before committing session history or enabling automated memory workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/404-UNKNOW/engram-2) <br>
- [Engram Cloud waitlist](https://404-unknow.github.io/Engram/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown advice, command responses, and AEIF JSON capsule data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node; stores local memory capsules and may download a local embedding model during initialization.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
