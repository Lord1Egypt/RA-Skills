## Description: <br>
Connect to Echo AI, the customer interaction platform, to list assistants, retrieve knowledge bases, and chat with AI-powered Echos built by businesses and creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darthdens](https://clawhub.ai/user/darthdens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent discover Echo AI assistants, inspect assistant knowledge bases, and, with confirmation, send chat messages to an Echo assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Echo AI API key to access assistants and chat endpoints. <br>
Mitigation: Use an assistant-scoped API key when possible and keep ECHO_API_KEY out of prompts, chat messages, and logs. <br>
Risk: Chat calls can send user-provided content to Echo AI and consume Echo owner credits. <br>
Mitigation: Prefer assistant details and FAQs for zero-credit answers, and require explicit user confirmation before each credit-consuming chat call. <br>
Risk: Assistant responses may include incorrect or unsuitable customer-facing guidance. <br>
Mitigation: Review responses before relying on them for business, sales, support, or customer communications. <br>


## Reference(s): <br>
- [Echo AI](https://echoai.so) <br>
- [Echo API Documentation](https://echoai.so/help) <br>
- [Echo AI API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/darthdens/echo-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/darthdens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples and HTTP request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ECHO_API_KEY; chat calls require explicit confirmation and may consume Echo owner credits.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
