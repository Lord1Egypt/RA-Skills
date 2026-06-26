## Description: <br>
Uses the ClawdHub CLI to search, install, update, list, authenticate for, and publish agent skills from clawdhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djmarkd38](https://clawhub.ai/user/djmarkd38) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to manage ClawdHub skill discovery, installation, updates, authentication, and publishing through the npm-installed ClawdHub CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install, update, update-all, force, and no-input actions can change local skill installations, including bulk updates. <br>
Mitigation: Approve these actions deliberately and avoid forced bulk updates unless updating all installed skills is intended. <br>
Risk: Login and publish actions can affect registry account state or publish unintended skill folder contents. <br>
Mitigation: Review authentication intent and inspect the target folder before publishing it to the registry. <br>


## Reference(s): <br>
- [ClawdHub skill page](https://clawhub.ai/djmarkd38/clawdhub-1-0-0) <br>
- [ClawdHub registry](https://clawdhub.com) <br>
- [Publisher profile](https://clawhub.ai/user/djmarkd38) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawdhub command-line binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
