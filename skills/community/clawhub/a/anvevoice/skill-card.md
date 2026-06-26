## Description: <br>
Add AI voice assistants to your website. Engage visitors with natural voice conversations, capture leads, automate support, and boost conversions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ANVEAI](https://clawhub.ai/user/ANVEAI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, website owners, support teams, and marketing teams use this skill to create, configure, deploy, and analyze AnveVoice website voice assistants for customer support, lead capture, engagement, and visitor analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive visitor voice data, transcripts, contact leads, analytics, recordings, billing information, and credential-management data. <br>
Mitigation: Install only when the publisher and remote service are trusted, use the narrowest API-key scope available, and avoid billing or credential tools unless they are needed. <br>
Risk: Embedding a voice widget can collect website visitor voice recordings, transcripts, browser metadata, and contact information. <br>
Mitigation: Confirm user consent, privacy-policy disclosure, retention settings, and applicable GDPR, CCPA, HIPAA, or other compliance requirements before deployment. <br>
Risk: Delete and revoke actions can change or remove bots, knowledge sources, or credentials. <br>
Mitigation: Require manual confirmation before delete, revoke, or broad account-administration actions. <br>
Risk: Over-broad API keys increase the impact of misuse or accidental disclosure. <br>
Mitigation: Use scoped keys for the intended task, keep keys in environment variables, rotate keys regularly, and revoke unused keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ANVEAI/anvevoice) <br>
- [AnveVoice Website](https://anvevoice.com) <br>
- [AnveVoice Documentation](https://anvevoice.com/help) <br>
- [AnveVoice Developer/API Keys](https://anvevoice.com/developer) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [Create Bot Example](artifact/examples/create-bot.md) <br>
- [Analytics Example](artifact/examples/analytics.md) <br>
- [List Bots Example](artifact/examples/list-bots.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples, shell commands, and HTML embed snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ANVEVOICE_API_KEY and may return sensitive account, visitor, conversation, analytics, recording, billing, and credential-management data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
