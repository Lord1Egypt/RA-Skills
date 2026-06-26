## Description: <br>
Guides agents through opening GoHighLevel developer accounts, creating marketplace apps, obtaining API credentials, and connecting integrations via OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[the-TimeBeing](https://clawhub.ai/user/the-TimeBeing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and external users use this skill to open or connect a GoHighLevel account, create a Developer Marketplace app, collect OAuth credentials, and follow setup guidance for API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creating GoHighLevel app credentials and OAuth access may authorize access to agency or sub-account data. <br>
Mitigation: Use only the minimum OAuth scopes needed, confirm the account being connected, and store Client Secrets and tokens only in an approved secrets manager. <br>
Risk: Secrets may be exposed if pasted into normal chat, logs, screenshots, repositories, or configuration files. <br>
Mitigation: Keep Client Secrets and tokens out of chat, logs, screenshots, and repositories; use environment variables or approved secret storage. <br>
Risk: The sign-up workflow includes a referral URL that may not be desired for all users. <br>
Mitigation: Use a direct GoHighLevel URL instead of the referral sign-up link when preferred. <br>


## Reference(s): <br>
- [GoHighLevel reference](reference.md) <br>
- [Developer Marketplace](https://marketplace.gohighlevel.com/) <br>
- [HighLevel API documentation](https://marketplace.gohighlevel.com/docs/) <br>
- [HighLevel API OAuth 2.0](https://marketplace.gohighlevel.com/docs/Authorization/OAuth2.0) <br>
- [OAuth Getting Started](https://marketplace.gohighlevel.com/docs/oauth/GettingStarted) <br>
- [ClawHub skill page](https://clawhub.ai/the-TimeBeing/ghl-open-account) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, setup steps, and official documentation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; guidance includes OAuth credential handling and plan prerequisite notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
