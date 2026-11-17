## Description:

Assemble modular ads from Supabase components and deploy to Facebook Ads Manager via the Marketing API. Supports preview, single/batch deploy, and status tracking. Uses ad_components table for A/B testing at scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aces1up](https://clawhub.ai/user/aces1up)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketers use this skill to assemble Facebook and Instagram ad variants from Supabase campaign components, preview them, deploy them through the Facebook Marketing API, and check deployed ad status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a hardcoded Supabase database password.

Mitigation: Rotate or remove the embedded database password before use and provide least-privilege database credentials through a secure environment variable.

Risk: The release evidence reports runtime package installation.

Mitigation: Review and pin dependencies, then run the skill in an isolated virtual environment before connecting production accounts.

Risk: Facebook access tokens can create ads and spend money through the connected ad account.

Mitigation: Treat tokens as high-value secrets, grant only required permissions, use dry-run and paused ads for review, and avoid URL-based token exchange when possible.

## Reference(s):

- [Ad Engine skill page](https://clawhub.ai/aces1up/skills/ad-engine)
- [Ad Engine modular A/B testing system](artifact/AD_ENGINE_SPEC.md)
- [Facebook ads deployment spec](artifact/FB_DEPLOYMENT_SPEC.md)
- [Facebook Ads API setup guide](artifact/FB_SETUP_GUIDE.md)
- [Meta Marketing API documentation](https://developers.facebook.com/docs/marketing-apis)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text and optional JSON from CLI actions, with Markdown setup and deployment guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create Facebook campaign, ad set, creative, and ad records, update Supabase message status, and save local Facebook credential configuration.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
