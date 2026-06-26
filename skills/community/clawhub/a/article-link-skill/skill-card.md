## Description: <br>
Article Link Skill submits supported paywalled media URLs to pick-read.vip and returns matched or extracted English article text when authorized with an Import Token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1787812757](https://clawhub.ai/user/1787812757) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check supported media, submit article links, monitor extraction jobs, and retrieve English article text through the provided CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends submitted article URLs and an Import Token to pick-read.vip. <br>
Mitigation: Use only with URLs and tokens you are comfortable sharing with that service, and avoid real Import Tokens until the network, token, and privacy behavior is documented clearly. <br>
Risk: The security summary reports that the runtime disables HTTPS certificate checks. <br>
Mitigation: Review before installing and do not use for sensitive tokens until TLS verification behavior is corrected or accepted by the user. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1787812757/article-link-skill) <br>
- [pick-read.vip](https://pick-read.vip) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON results containing article metadata and HTML content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a configured Import Token for most operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
