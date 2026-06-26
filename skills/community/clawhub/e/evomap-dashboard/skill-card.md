## Description: <br>
Launch a local EvoMap Node Dashboard web viewer for checking node reputation, tasks, and assets with a Node ID and Node Secret. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppop0uuiu](https://clawhub.ai/user/ppop0uuiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and EvoMap node operators use this skill to start a local dashboard and inspect node status, reputation details, claimed tasks, and recent assets without using the EvoMap web invite flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports embedded node secrets in the artifact. <br>
Mitigation: Remove embedded credentials from the files, rotate any exposed secrets, and enter only credentials for nodes you are authorized to access. <br>
Risk: The security review reports broad local-network exposure for the dashboard. <br>
Mitigation: Bind the dashboard to localhost only and restrict CORS before normal use. <br>
Risk: The security review reports an unrelated remote publishing script. <br>
Mitigation: Delete the publishing script or separate it into a clearly disclosed tool before deploying the dashboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppop0uuiu/evomap-dashboard) <br>
- [EvoMap](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent or user to launch a local dashboard and provide node credentials in the browser session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
