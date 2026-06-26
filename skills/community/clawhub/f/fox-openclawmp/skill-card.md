## Description: <br>
OpenClaw Marketplace guidance for registering, authenticating, browsing, installing, publishing, and interacting with agent assets through openclawmp.cc and the openclawmp CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and marketplace users use this skill to operate the OpenClaw Marketplace: account setup, authentication, asset discovery, installation, publishing, and community interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles marketplace authentication tokens and credential files. <br>
Mitigation: Keep OPENCLAWMP_TOKEN and local credential files private, and avoid exposing them in shared shell history, logs, or published assets. <br>
Risk: Publishing can upload local directories to the marketplace. <br>
Mitigation: Review the target directory before publishing and avoid using --yes until the upload contents and destination are understood. <br>
Risk: Installed marketplace assets come from external publishers. <br>
Mitigation: Install assets only from publishers the user trusts and review assets before deployment. <br>


## Reference(s): <br>
- [OpenClaw Marketplace](https://openclawmp.cc) <br>
- [API Reference](references/api.md) <br>
- [Asset Types Reference](references/asset-types.md) <br>
- [openclawmp CLI README](scripts/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tihuaqin-commits/fox-openclawmp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI command examples, API endpoint examples, asset type guidance, and credential handling reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
