## Description: <br>
Guides agents through preparing, sanitizing, versioning, publishing, verifying, and recording OpenClaw skill releases on ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jini92](https://clawhub.ai/user/jini92) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare OpenClaw skills for ClawHub publication, including language checks, personal information sanitization, version selection, publish commands, and post-publish verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses the operator's ClawHub login to publish skills. <br>
Mitigation: Confirm the authenticated ClawHub account and intended slug before running publish commands. <br>
Risk: The artifact includes a hardcoded personal profile check and local bookkeeping updates. <br>
Mitigation: Replace the profile check with the actual publisher handle and treat memory or Obsidian updates as optional local records. <br>
Risk: The workflow can rewrite skill files while sanitizing language and personal information. <br>
Mitigation: Review file diffs before publishing and require confirmation before overwriting source files. <br>


## Reference(s): <br>
- [ClawHub Publish release page](https://clawhub.ai/jini92/clawhub-publish-mai) <br>
- [ClawHub Pre-Publish Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with checklist items, tables, and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces procedural publishing guidance for an agent; it does not produce structured machine-readable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
