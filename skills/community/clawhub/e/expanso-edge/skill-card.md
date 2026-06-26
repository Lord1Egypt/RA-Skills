## Description: <br>
Data processing pipelines for OpenClaw. Deploy skills from the Expanso marketplace to transform, analyze, and process data locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install Expanso Edge, connect it to Expanso Cloud, and deploy marketplace data-processing pipelines that run locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote installer scripts and a cloud-connected local runtime can gain local execution authority. <br>
Mitigation: Install only if you trust Expanso's installer domain, cloud service, and marketplace pipeline source; review or verify installer scripts before running them and run Edge with least local privilege. <br>
Risk: Bootstrap token exposure could compromise Edge node registration or connection setup. <br>
Mitigation: Protect the bootstrap token, avoid logging or sharing it, and rotate it if exposure is suspected. <br>
Risk: Pipeline behavior depends on the deployed Expanso skill and may affect sensitive local data. <br>
Mitigation: Review each deployed pipeline before use and avoid sensitive data until its behavior is understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-edge) <br>
- [Expanso Skills Marketplace](https://skills.expanso.io) <br>
- [Expanso Cloud](https://cloud.expanso.io) <br>
- [Expanso documentation](https://docs.expanso.io) <br>
- [Expanso Edge installer](https://get.expanso.io/edge/install.sh) <br>
- [Expanso CLI installer](https://get.expanso.io/cli/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus EXPANSO_EDGE_BOOTSTRAP_URL and EXPANSO_EDGE_BOOTSTRAP_TOKEN.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
