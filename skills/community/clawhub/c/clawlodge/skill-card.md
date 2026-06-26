## Description: <br>
ClawLodge helps agents search, inspect, download, install, and publish OpenClaw workspaces through the clawlodge CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memepilot](https://clawhub.ai/user/memepilot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to find reusable OpenClaw workspaces, compare releases, download or install artifacts, and publish local workspaces after explicit user intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Download and install guidance can introduce external workspace artifacts into the local environment. <br>
Mitigation: Verify the clawlodge-cli npm package source, inspect candidate packages with show or get before download or install, and stage downloaded artifacts in temporary paths before applying changes. <br>
Risk: Publish, comment, favorite, report, and login flows can involve credentials or public write actions. <br>
Mitigation: Require explicit user confirmation for write actions, avoid exposing personal access tokens in logs, and use whoami and pack checks before publishing. <br>
Risk: The CLI may send anonymous command-level telemetry. <br>
Mitigation: Inspect telemetry state with clawlodge config get telemetry and disable it with clawlodge config set telemetry off or CLAWLODGE_TELEMETRY=off when anonymous usage sharing is not desired. <br>


## Reference(s): <br>
- [ClawLodge skill page](https://clawhub.ai/memepilot/clawlodge) <br>
- [ClawLodge registry](https://clawlodge.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected slugs, versions, local zip paths, agent names, workspace paths, and telemetry settings when relevant.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
