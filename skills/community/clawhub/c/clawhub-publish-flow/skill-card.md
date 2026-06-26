## Description: <br>
Publish or update an OpenClaw skill on ClawHub using the local authenticated ClawHub session and direct API upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish or update reviewed local OpenClaw skill folders on ClawHub, including remote inspection, version and changelog selection, upload, and post-release verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish helper can upload an entire local skill folder to a public registry using the user's saved ClawHub token. <br>
Mitigation: Use it only for deliberate ClawHub releases from a clean skill directory, and inspect the exact outbound files before upload. <br>
Risk: Local-only files, secrets, logs, build output, test data, or machine-specific configuration may be included if they remain in the skill folder. <br>
Mitigation: Remove secrets, .env files, logs, runtime artifacts, hidden local config, and test data before publishing; stop and fix the package if any local-only content is present. <br>
Risk: A mistaken slug, owner, or version could update the wrong public release. <br>
Mitigation: Confirm the target slug and version with ClawHub first, inspect existing remote state before updates, and verify the final release after upload. <br>


## Reference(s): <br>
- [Release Checklist](references/release-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/G-Hanasq/clawhub-publish-flow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown operational report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes skill identity, local path, prior and target versions, upload result, verification result, final URL, and risks or follow-ups.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
