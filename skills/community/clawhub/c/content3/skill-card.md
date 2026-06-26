## Description: <br>
Content3 API for creating videos, managing content, submitting reviews, and posting to social media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimitriharding](https://clawhub.ai/user/dimitriharding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to work with the Content3 Agent API: generate short-form videos, manage content libraries, submit human reviews, promote approved content, and prepare social media drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may grant broad access to Content3 content, review, product, and social publishing workflows. <br>
Mitigation: Use the narrowest API-key scopes needed, avoid wildcard or full-access keys, and protect ~/.config/content3/api_key. <br>
Risk: Public review links can expose submitted content to anyone with the share URL. <br>
Mitigation: Confirm before creating public review links and disable links when they are no longer needed. <br>
Risk: Publishing social drafts can send generated content to connected social accounts. <br>
Mitigation: Require explicit final human approval before publishing drafts. <br>


## Reference(s): <br>
- [Content3 Developer Documentation](https://content3.app/developers) <br>
- [ClawHub Content3 Skill Page](https://clawhub.ai/dimitriharding/content3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cURL commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Content3 API key and API scopes appropriate to the requested workflow.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
