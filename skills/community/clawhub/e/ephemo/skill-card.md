## Description: <br>
Publish files and folders to the web instantly. Static hosting for HTML sites and UI assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sandrakottos](https://clawhub.ai/user/sandrakottos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish static web directories and UI assets to a live shareable URL. It supports anonymous temporary deployments and authenticated account-backed site management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish a local folder to a public URL. <br>
Mitigation: Confirm the exact directory before use and remove secrets or private files from the deployment contents. <br>
Risk: Saved Ephemo credentials can make a deployment permanent and account-backed. <br>
Mitigation: Review whether `~/.ephemo_credentials` exists before relying on anonymous temporary behavior, and keep the credential file out of source control. <br>


## Reference(s): <br>
- [Ephemo homepage](https://ephemo.online) <br>
- [ClawHub release page](https://clawhub.ai/sandrakottos/ephemo) <br>
- [Publisher profile](https://clawhub.ai/user/sandrakottos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and URL handoff text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment commands, live URL handoff guidance, claim-code instructions when applicable, and credential-file handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
