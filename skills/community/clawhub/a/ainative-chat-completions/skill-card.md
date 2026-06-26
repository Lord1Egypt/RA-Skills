## Description: <br>
Helps agents build conversational AI with AINative's Chat Completions API, including raw API usage, Python, React, Next.js, streaming, tool calling, and credit tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI application builders use this skill to implement chatbots and assistants with AINative's Chat Completions API, including streaming responses, tool calling, SDK integration, and credit usage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or bearer tokens may be exposed if copied into frontend bundles, logs, or shared prompts. <br>
Mitigation: Keep real credentials server-side or in protected secret storage, and use environment variables for server integrations. <br>
Risk: Chat content is sent to AINative and may include sensitive user or business data. <br>
Mitigation: Send only content appropriate to share with AINative under the user's privacy and compliance requirements. <br>
Risk: Using unfamiliar SDK packages or provider endpoints can introduce supply-chain or trust assumptions. <br>
Mitigation: Verify AINative and its SDK packages are intended providers before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/urbantech/ainative-chat-completions) <br>
- [AINative Chat Completions endpoint](https://api.ainative.studio/v1/public/chat/completions) <br>
- [AINative credits balance endpoint](https://api.ainative.studio/api/v1/public/credits/balance) <br>
- [CHAT_COMPLETION_API_REFERENCE.md](docs/api/CHAT_COMPLETION_API_REFERENCE.md) <br>
- [React useChat hook source](packages/sdks/react/src/hooks/useChat.ts) <br>
- [Next.js SDK source](packages/sdks/nextjs/src/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code examples and command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes REST, Python, React, and Next.js examples for AINative Chat Completions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
