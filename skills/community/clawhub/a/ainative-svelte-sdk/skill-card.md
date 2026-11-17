## Description:

Use @ainative/svelte-sdk to add AI chat to Svelte/SvelteKit apps with reactive chat state, configuration, message display, loading states, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to install and configure @ainative/svelte-sdk, create Svelte chat stores, and wire AINative chat behavior into Svelte or SvelteKit applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or using an untrusted npm package or service can introduce supply-chain or service-trust risk.

Mitigation: Confirm trust in the @ainative/svelte-sdk npm package and AINative service before installation or production use.

Risk: Embedding private API keys in browser bundles can expose credentials.

Mitigation: Use the SvelteKit server-route pattern for production keys and keep private API keys out of client-side bundles.

Risk: Chat requests can transmit sensitive user content to the AINative API.

Mitigation: Avoid sending sensitive user content unless the application's data handling policy allows it.

## Reference(s):

- [Ainative Svelte Sdk on ClawHub](https://clawhub.ai/urbantech/skills/ainative-svelte-sdk)
- [AINative API base URL](https://api.ainative.studio)
- [AINative chat completions endpoint](https://api.ainative.studio/v1/public/chat/completions)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, TypeScript, and Svelte code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package installation, SDK configuration, store usage, environment variable guidance, and server-route guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
