## Description: <br>
A specialized skill for safely managing and testing OpenClaw configuration changes using a Blue/Green deployment pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshualeecowan33-ui](https://clawhub.ai/user/joshualeecowan33-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to stage, validate, promote, or roll back OpenClaw configuration changes without immediately replacing the primary configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the deployment script can change the live OpenClaw configuration while presenting part of the workflow as validation. <br>
Mitigation: Review openclaw.json.green, run JSON checks manually, keep an independent backup, and run the script only when a live configuration change is intended. <br>


## Reference(s): <br>
- [Blue Green Deployer on ClawHub](https://clawhub.ai/joshualeecowan33-ui/blue-green-deployer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through OpenClaw configuration staging and invokes a shell deployment script.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
