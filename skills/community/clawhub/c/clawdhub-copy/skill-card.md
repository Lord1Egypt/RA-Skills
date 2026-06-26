## Description: <br>
Use the ClawdHub CLI to search, install, update, list, and publish agent skills from clawdhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jk50505k](https://clawhub.ai/user/jk50505k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to work with ClawdHub skills through CLI commands for search, install, update, list, authentication, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to install, force-update, bulk-update, or publish skills through the ClawdHub CLI. <br>
Mitigation: Require explicit approval before install, update, update --all, --force, --no-input, login, or publish commands. <br>
Risk: Unpinned or bulk updates can change installed skill behavior unexpectedly. <br>
Mitigation: Prefer pinned versions from trusted publishers and review the target directory before changes are applied. <br>


## Reference(s): <br>
- [Clawdhub Copy release page](https://clawhub.ai/jk50505k/clawdhub-copy) <br>
- [ClawdHub registry](https://clawdhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawdHub CLI commands for install, update, list, login, and publish operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
