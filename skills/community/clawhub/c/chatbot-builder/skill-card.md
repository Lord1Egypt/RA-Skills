## Description: <br>
Chatbot Builder helps agents create, train, and deploy AI chatbots using user-provided data across website, Slack, Discord, WhatsApp, and Telegram channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to scaffold chatbot workflows, train them on documents or web content, and deploy them to common chat and web channels. It is suited for support, automation, and conversational assistant setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Training data can contain secrets, private documents, or regulated information. <br>
Mitigation: Use test data first, avoid training on secrets or private documents unless necessary, and confirm where data is stored and how it can be deleted. <br>
Risk: API keys and channel credentials may be exposed or over-scoped during deployment. <br>
Mitigation: Use scoped credentials for model providers and chat channels, and verify any chatbot.sh implementation before installing or running it. <br>
Risk: Conversation memory and analytics may retain user interactions. <br>
Mitigation: Review retention, deletion, and access controls for memory and analytics before connecting real users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/chatbot-builder) <br>
- [Publisher profile](https://clawhub.ai/user/Sunshine-del-ux) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve chatbot training data, API credentials, channel credentials, conversation memory, and analytics configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
