## Description: <br>
Auto-create and manage digital product listings on Etsy from existing digital product files using Etsy Open API v3, including listing creation, tagging, pricing, and draft publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Etsy shop operators and developers use this skill to configure OAuth credentials and create draft digital product listings through Etsy Open API v3 for manual review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform Etsy account-changing actions with shop OAuth credentials. <br>
Mitigation: Use a dedicated Etsy app with the narrowest OAuth scopes possible, review every draft listing before publishing, and revoke the app if behavior is unexpected. <br>
Risk: Etsy client secrets, access tokens, and shop IDs are sensitive credentials. <br>
Mitigation: Store credentials only in a secret manager or protected environment variables, and avoid placing tokens in prompts, logs, source files, or shared outputs. <br>
Risk: Automated listing details, pricing, tags, or product claims may be inaccurate or unsuitable for a shop. <br>
Mitigation: Keep created listings in draft state and perform a manual business, policy, and content review before publishing. <br>


## Reference(s): <br>
- [Etsy Developer Documentation](https://developer.etsy.com/documentation/) <br>
- [Etsy Developers](https://www.etsy.com/developers) <br>
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/etsy-autolist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python script usage and Etsy API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Etsy OAuth credentials and shop ID; listing creation is performed as drafts for manual review.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
