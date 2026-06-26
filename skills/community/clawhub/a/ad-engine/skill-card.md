## Description: <br>
Assemble modular ads from Supabase components and deploy to Facebook Ads Manager via the Marketing API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aces1up](https://clawhub.ai/user/aces1up) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and operators use this skill to assemble Facebook ad variants from Supabase-stored components, preview them, deploy them through the Meta Marketing API, and check live campaign status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a hardcoded Supabase credential in the deployment script. <br>
Mitigation: Review or remove the embedded credential before installation, rotate the database password, and use environment variables or a secrets manager for Supabase access. <br>
Risk: The release evidence reports risky setup behavior around automatic dependency installation. <br>
Mitigation: Move dependencies to a pinned setup step and review packages before running the skill in a production environment. <br>
Risk: Facebook access tokens can authorize ad spend and account changes. <br>
Mitigation: Treat the token as a secret, prefer environment variables or a secrets manager, and validate campaigns with preview or dry-run plus Ads Manager review before enabling deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aces1up/ad-engine) <br>
- [Facebook Ads API setup guide](artifact/FB_SETUP_GUIDE.md) <br>
- [Facebook deployment spec](artifact/FB_DEPLOYMENT_SPEC.md) <br>
- [Ad Engine spec](artifact/AD_ENGINE_SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON preview/status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Facebook credential configuration and make Supabase and Meta Marketing API calls when run with deployment or status commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
