## Description: <br>
Displays API credit balances for Anthropic, OpenAI, OpenRouter, Mistral, and Groq with health bars, optional API checks, and manual sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FranciscoBuiltDat](https://clawhub.ai/user/FranciscoBuiltDat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to check API credit balances, manually sync balances, record top-ups, and view low-credit status across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local config.json can contain balance metadata that a user may consider sensitive. <br>
Mitigation: Protect config.json with local file permissions, delete it when no longer needed, and avoid sharing the skill workspace with untrusted users. <br>
Risk: Auto-check mode makes outbound requests to provider APIs using environment-provided credentials. <br>
Mitigation: Use manual sync for no-network operation, prefer narrow-scope provider credentials, and keep API keys in environment variables or a secure secret store. <br>
Risk: Credit balances may be stale when manual sync is not updated or provider API checks fail. <br>
Mitigation: Confirm critical balance or purchasing decisions in the provider console and refresh balances before relying on low-credit alerts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/FranciscoBuiltDat/api-credits-lite) <br>
- [README](README.md) <br>
- [Security Policy](SECURITY.md) <br>
- [OpenRouter Key API](https://openrouter.ai/api/v1/auth/key) <br>
- [Vercel Billing API](https://api.vercel.com/v1/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style conversational text with health-bar output and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update local config.json and may make optional provider API calls when credentials are supplied.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact/package.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
