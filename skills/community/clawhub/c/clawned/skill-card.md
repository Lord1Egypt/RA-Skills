## Description: <br>
Security agent that inventories installed OpenClaw skills, analyzes them for threats, and syncs results to your Clawned dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jenish-sojitra](https://clawhub.ai/user/jenish-sojitra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inventory installed skills, scan selected skill directories for security issues, and sync results to a Clawned dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync flow sends installed-skill inventory and basic host registration details to Clawned. <br>
Mitigation: Install only if you trust Clawned with that inventory and host metadata. <br>
Risk: The scan command may send selected skill source files to the Clawned server for analysis. <br>
Mitigation: Use scan --path only for skill directories you are comfortable analyzing through the configured Clawned endpoint. <br>
Risk: Cron, watch, or daemon modes perform ongoing monitoring and syncing. <br>
Mitigation: Enable those modes only when continuous monitoring is intended. <br>
Risk: CLAWNED_SERVER controls the endpoint that receives requests. <br>
Mitigation: Keep CLAWNED_SERVER pointed at a trusted endpoint. <br>


## Reference(s): <br>
- [Clawned homepage](https://clawned.io) <br>
- [Clawned skill listing](https://clawhub.ai/jenish-sojitra/clawned) <br>
- [Detection Patterns](references/detection-patterns.md) <br>
- [Threat Model](references/threat-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and JSON responses, with Markdown setup and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and CLAWNED_API_KEY; CLAWNED_SERVER is optional.] <br>

## Skill Version(s): <br>
1.3.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
