## Description: <br>
Deploy web apps and APIs to a public URL with a single command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpbonch](https://clawhub.ai/user/jpbonch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use AgentScale to register for an API key, package the current project, deploy web apps or APIs to a public URL, list services, and check account tier or credits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deploy command packages and uploads the current project archive, which may expose files that should not be deployed. <br>
Mitigation: Run deploy only from the intended project directory, review the project for secrets first, and rely on the documented exclusions only as a baseline. <br>
Risk: The tool uses a locally stored API key and AGENTSCALE_API_URL can redirect API calls carrying that key. <br>
Mitigation: Keep AGENTSCALE_API_URL unset unless the alternate endpoint is deliberately trusted, and install only from a trusted AgentScale npm package source. <br>
Risk: Adding credits or using payment commands can spend money. <br>
Mitigation: Require explicit approval before running payment, credit, or agentspend commands. <br>


## Reference(s): <br>
- [AgentScale on ClawHub](https://clawhub.ai/jpbonch/agentscale) <br>
- [Nixpacks](https://nixpacks.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or read a local AgentScale API key and may upload a compressed project archive.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata; artifact package.json reports 0.1.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
