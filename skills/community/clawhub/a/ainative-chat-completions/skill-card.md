## Description:

Helps agents build conversational AI with AINative's Chat Completions API across REST, Python SDK, React SDK, and Next.js patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to implement AINative chatbots and AI assistants, including streaming responses, tool calling, credit checks, and SDK-based application patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-side AINative API key examples could expose account credentials.

Mitigation: Use server-side routes or server actions for AINative calls, keep API keys in server-only secrets, and rotate any key that was placed in browser code.

Risk: Chat completion requests may include sensitive personal or regulated data.

Mitigation: Review AINative's handling terms before use and add consent, data minimization, and redaction controls where needed.

## Reference(s):

- [AINative Chat Completions API endpoint](https://api.ainative.studio/v1/public/chat/completions)
- [AINative Credits Balance API endpoint](https://api.ainative.studio/api/v1/public/credits/balance)
- [ClawHub skill page](https://clawhub.ai/urbantech/skills/ainative-chat-completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST, Python, React, and Next.js examples for AINative chat completions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
