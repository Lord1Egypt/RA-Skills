## Description: <br>
Manage paid advertising campaigns across Meta (Facebook and Instagram), Google Ads, X, and Snapchat for Indian businesses, with performance analysis, issue detection, and high-ROI recommendations before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishekj9621](https://clawhub.ai/user/abhishekj9621) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers, founders, and marketing operators use this skill to diagnose campaign performance, evaluate paid-ad metrics, and plan or execute budget, creative, audience, and campaign changes across major ad platforms. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require powerful ad-account credentials that could expose accounts or customer data if pasted into chat. <br>
Mitigation: Use secure OAuth or a secret manager, grant least-privilege access, and avoid sharing access tokens, API secrets, OAuth client files, refresh tokens, or customer lists in chat. <br>
Risk: Campaign changes can spend budget, activate campaigns, pause or delete delivery, or upload audiences. <br>
Mitigation: Require explicit user confirmation before any budget change, campaign activation, pause, deletion, or audience upload. <br>
Risk: Rapid budget scaling or unreviewed optimization recommendations can waste ad spend. <br>
Mitigation: Review recommendations in currency terms and keep sudden changes within the artifact's stated guardrails unless the user explicitly approves a larger change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abhishekj9621/ads-manager-claw) <br>
- [Credential Guides](references/credential-guides.md) <br>
- [Google Ads API Reference](references/google-ads.md) <br>
- [Meta (Facebook & Instagram) Ads API Reference](references/meta.md) <br>
- [Snapchat Ads API Reference](references/snapchat.md) <br>
- [X (Twitter) Ads API Reference](references/x-ads.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured performance summaries, diagnostics, recommendations, expected impact estimates, and API-oriented snippets or commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions should be proposed with explicit user confirmation before spend, activation, pause, deletion, audience upload, or other campaign changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
