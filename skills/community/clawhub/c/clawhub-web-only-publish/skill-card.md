## Description: <br>
Publish skills to ClawHub via web dashboard only. No CLI login, no device flow. Reuse existing browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dalomeve](https://clawhub.ai/user/Dalomeve) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill to publish ClawHub skills through an already-authenticated browser session and avoid CLI login or device-flow failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could publish the wrong skill folder, slug, display name, version, or changelog. <br>
Mitigation: Confirm the visible ClawHub account, selected skill folder, slug, display name, version, and changelog before publishing. <br>
Risk: Published files could unintentionally include credentials. <br>
Mitigation: Run and review a pre-publish secret scan and do not publish when credentials are detected. <br>
Risk: Using the CLI fallback could publish with an unintended existing token. <br>
Mitigation: Use the CLI fallback only when intentionally publishing with an already-authenticated CLI token, and do not run CLI login. <br>


## Reference(s): <br>
- [ClawHub Web Only Publish listing](https://clawhub.ai/Dalomeve/clawhub-web-only-publish) <br>
- [ClawHub upload page](https://clawhub.ai/upload) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown workflow guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the user to confirm the active ClawHub account, selected skill folder, metadata, changelog, and secret scan before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
