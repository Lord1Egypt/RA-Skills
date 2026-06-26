## Description: <br>
Complete WhatsApp automation via Evolution API Go v3, including instances, text and media messages, polls, carousels, groups, contacts, chats, communities, newsletters, and real-time webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[impa365](https://clawhub.ai/user/impa365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and run WhatsApp automation against an Evolution API Go deployment they control, including messaging, group administration, contact checks, profile updates, and webhook-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad WhatsApp messaging and account-control capabilities. <br>
Mitigation: Install only for a WhatsApp and Evolution API deployment you control, and require explicit approval before bulk sends, group changes, privacy changes, full-history sync, or instance deletion. <br>
Risk: Global admin keys can create, delete, reconnect, and inspect instances. <br>
Mitigation: Keep the global admin key separate from routine messaging workflows and prefer least-privilege instance tokens for normal operations. <br>
Risk: Misconfigured upload or webhook targets could expose data or send content to an unintended endpoint. <br>
Mitigation: Verify EVOGO_API_URL and webhook destinations before file uploads or automation runs. <br>
Risk: Unapproved or high-volume messaging can create abuse, consent, and rate-limit issues. <br>
Mitigation: Confirm recipient consent, test with small recipient sets, and use message delays or backoff for larger sends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/impa365/evogo) <br>
- [Evolution API Go](https://github.com/EvolutionAPI/evolution-api) <br>
- [WhatsApp Business Platform Documentation](https://developers.facebook.com/docs/whatsapp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Evolution API URL, global admin key, instance name, and instance API token supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
