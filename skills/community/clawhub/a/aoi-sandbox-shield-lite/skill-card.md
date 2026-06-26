## Description: <br>
Creates local snapshots of critical OpenClaw config and workspace files, validates JSON configuration shape, and prints audit-friendly JSON without applying changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmonddantesj](https://clawhub.ai/user/edmonddantesj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill before publishing or changing OpenClaw workspaces to snapshot important local files and validate JSON configuration syntax and required keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Snapshot runs can duplicate local OpenClaw config, state, and memory files into timestamped folders. <br>
Mitigation: Review snapshot contents before attaching or sharing them, and delete old snapshots when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edmonddantesj/aoi-sandbox-shield-lite) <br>
- [Support issues](https://github.com/edmonddantesj/aoi-skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON printed to stdout, plus local snapshot folders and manifest files for snapshot runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snapshot mode copies selected local OpenClaw state files into timestamped folders; validation mode reports JSON parse errors and missing required keys.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
