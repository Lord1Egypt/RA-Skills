## Description: <br>
Automatically tracks and commits changes to selected OpenClaw configuration and workspace Markdown files using local Git history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AltairCardinal](https://clawhub.ai/user/AltairCardinal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to keep automatic local Git snapshots of selected workspace Markdown files and the OpenClaw configuration file before each prompt is built. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic Git commits can preserve sensitive configuration, memory, profile, or workspace data without per-run approval. <br>
Mitigation: Enable the skill only when local history is intended, narrow the tracked file list, and avoid tracking secrets or private memory/profile data. <br>
Risk: Local Git history may later sync sensitive tracked data if an affected repository has or later receives a remote. <br>
Mitigation: Check repository remotes before enabling the skill and review committed contents before any push or sync. <br>
Risk: The skill auto-initializes Git repositories for the workspace and OpenClaw configuration directory. <br>
Mitigation: Use it only in directories where automatic repository creation is acceptable, or disable and reconfigure it before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AltairCardinal/config-tracker) <br>
- [OpenClaw project homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Local Git commits and console log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configurable tracked-file list and commit message prefix; defaults to a five-second commit cooldown.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
