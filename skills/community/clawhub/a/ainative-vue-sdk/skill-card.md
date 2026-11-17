## Description:

Use @ainative/vue-sdk to add AI chat to Vue 3 apps with composables for chat, credits, and AINative configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Vue 3 or Nuxt applications use this skill to install @ainative/vue-sdk, configure AINative access, and implement chat, credit balance, and message display flows with Composition API composables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide shows an AINative API key in public frontend configuration, which could risk account or credit abuse.

Mitigation: Use a backend proxy or short-lived restricted client tokens unless AINative explicitly documents that the key is safe to publish in browsers.

Risk: Chat messages are sent to the hosted AINative API.

Mitigation: Add clear user notice for chat data sent to the hosted API before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, TypeScript, and Vue code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on Vue 3 and Nuxt integration examples for the @ainative/vue-sdk package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
