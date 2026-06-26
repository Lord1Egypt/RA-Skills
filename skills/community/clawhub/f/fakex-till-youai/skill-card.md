## Description: <br>
Generate X post drafts from a daily AI digest, collect the user's style and profile preferences, let the user choose drafts and posting times, and either auto-publish with the user's own X API credentials or stop at a copy-and-paste workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zimmw](https://clawhub.ai/user/zimmw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI beginners, builders, and creators who already have a daily AI digest use this skill to turn digest items into X post drafts, select the drafts they like, choose posting times, and publish manually or with their own X API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic mode can publish posts to X using the user's credentials. <br>
Mitigation: Use half automatic mode when direct posting authority is not desired, and review final post text and scheduled times before automatic publication. <br>
Risk: Automatic posting requires X API credentials, which are sensitive secrets. <br>
Mitigation: Use dedicated or least-privileged credentials where possible, and avoid pasting secrets into shared chats or logs. <br>
Risk: Draft quality and attribution depend on the upstream digest and available source links. <br>
Mitigation: Review generated drafts and source links before posting, and provide a digest or source links when they are missing. <br>


## Reference(s): <br>
- [follow-builders companion workflow](https://github.com/zarazhangrui/follow-builders) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown conversation with draft post text, schedule details, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration or schedule files when the user chooses automatic posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
