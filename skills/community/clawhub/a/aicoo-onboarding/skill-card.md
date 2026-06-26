## Description: <br>
Guides first-time Aicoo users through API key setup, workspace initialization, local context collection, people discovery, share-link creation, and an Aicoo Square post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up Aicoo for the first time, initialize their workspace, sync selected local context, discover people, create a shareable agent link, and publish a Square post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan broad local context and upload selected content to Aicoo during onboarding. <br>
Mitigation: Limit which files are scanned, inspect upload payloads, and exclude secrets or confidential repositories before running API calls. <br>
Risk: The setup flow uses sensitive API credentials and suggests persisting them in shell startup files. <br>
Mitigation: Store API keys only where the user accepts persistence risk, avoid committing credentials, and rotate keys if exposure is suspected. <br>
Risk: Share links, notes access, network connections, and public Square posts can expose user information to others. <br>
Mitigation: Confirm share scope, notes permissions, expiration, sign-in requirement, connection target, and post content before execution. <br>


## Reference(s): <br>
- [Aicoo skill page](https://clawhub.ai/xisen-w/aicoo-onboarding) <br>
- [Aicoo API keys](https://www.aicoo.io/settings/api-keys) <br>
- [First-time setup example](examples/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce user-specific onboarding notes, share-link settings, discovery prompts, and public post drafts.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact metadata lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
