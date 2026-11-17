## Description:

Guides agents through opening GoHighLevel (GHL) developer accounts, creating marketplace apps, and connecting via OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the-timebeing](https://clawhub.ai/user/the-timebeing)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide GoHighLevel account setup, marketplace app creation, OAuth credential setup, and API access preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers users to an undisclosed referral signup link.

Mitigation: Use GoHighLevel's canonical signup URL or require explicit affiliate disclosure before following the referral link.

Risk: The skill recommends broad GoHighLevel installation permissions by default.

Mitigation: Choose the narrowest installation permissions and OAuth scopes needed for the specific integration.

Risk: The skill guides users through OAuth client setup and credential handling.

Mitigation: Store client secrets and tokens in environment variables or a secrets manager and do not commit them to version control.

## Reference(s):

- [GoHighLevel reference](reference.md)
- [GoHighLevel Developer Marketplace](https://marketplace.gohighlevel.com/)
- [HighLevel API documentation](https://marketplace.gohighlevel.com/docs/)
- [HighLevel OAuth 2.0 documentation](https://marketplace.gohighlevel.com/docs/Authorization/OAuth2.0)
- [HighLevel OAuth getting started](https://marketplace.gohighlevel.com/docs/oauth/GettingStarted)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklists, setup steps, and credential-handling recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not produce executable code; directs users to configure GoHighLevel accounts, apps, redirect URIs, OAuth scopes, and secrets storage.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
