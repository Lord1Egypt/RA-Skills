## Description:

Use @ainative/next-sdk to add AI chat to Next.js apps with App Router and Pages Router examples for streaming chat routes, auth middleware, and server-side API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate @ainative/next-sdk into Next.js applications, including chat completion routes, streaming responses, route protection, and server-side SDK calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public chat API can expose server-funded AI usage to abuse or unexpected cost.

Mitigation: Protect or rate-limit /api/chat, add quotas and monitoring, and validate token usage before production use.

Risk: Example request handling accepts chat message bodies without showing validation controls.

Mitigation: Validate request bodies, message roles, message size, and maximum token settings before forwarding requests.

Risk: Chat content is sent to AINative or its upstream model provider.

Mitigation: Disclose this data flow to users and review privacy requirements before enabling the chat workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urbantech/skills/ainative-nextjs-sdk)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes server-side API key usage, Next.js route examples, streaming response setup, auth middleware configuration, and environment variable guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact text mentions npm package v1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
