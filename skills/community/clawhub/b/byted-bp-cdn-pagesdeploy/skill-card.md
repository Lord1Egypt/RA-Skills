## Description: <br>
One-click deployment of static websites to BytePlus / VolcEngine Edge Pages platform, supporting auto project creation, update deployment, custom domain binding, and CDN acceleration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyao00-cloud](https://clawhub.ai/user/fanyao00-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to deploy generated or local static websites to BytePlus / VolcEngine Edge Pages, bind custom domains, preview sites locally, and manage deployment updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires BytePlus / VolcEngine deployment credentials. <br>
Mitigation: Use a least-privileged access key and remove or rotate stored credentials after deployment work is complete. <br>
Risk: Deployment options and build commands can trigger local command execution or misdirect cloud actions. <br>
Mitigation: Use trusted values for --build-cmd, --desc, project names, and domains, and review commands before execution. <br>
Risk: Management commands can update, offline, or delete Pages projects. <br>
Mitigation: Verify the exact project ID before update, offline, or delete operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanyao00-cloud/byted-bp-cdn-pagesdeploy) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands for BytePlus / VolcEngine Edge Pages deployment, domain management, local preview, and project management.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
