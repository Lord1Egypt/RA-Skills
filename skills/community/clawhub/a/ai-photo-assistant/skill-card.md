## Description:

AI写真助手 is a customer-service assistant that explains AI photo services, answers pricing and style questions, and guides users toward placing an order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duoduoks](https://clawhub.ai/user/duoduoks)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask about the AI photo service, pricing, and style options. The agent can use DeepSeek to draft customer-service replies and route users toward the AI photo ordering page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts may be sent to DeepSeek without clear disclosure.

Mitigation: Disclose DeepSeek processing before use and avoid entering sensitive prompts.

Risk: The skill may read a DeepSeek API key from the global OpenClaw configuration.

Mitigation: Use a dedicated, limited DeepSeek API key and review local OpenClaw configuration before running the skill.

Risk: Responses may steer users toward an AI photo service order page.

Mitigation: Review generated responses for commercial routing and make the destination clear to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duoduoks/skills/ai-photo-assistant)
- [Publisher profile](https://clawhub.ai/user/duoduoks)
- [AI photo service order page](https://www.xn--ehqw44a690c.com/ai-photo)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text responses and Markdown-style installation command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send user prompts to the DeepSeek API when a DeepSeek API key is configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
