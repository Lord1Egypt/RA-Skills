## Description:

Provides Vue 3, Nuxt 3, Pinia, testing, and performance guidance for agents implementing modern Vue applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to produce Vue 3 Composition API implementations, reusable composables, Pinia stores, Nuxt 3 patterns, Vitest tests, and performance-focused component guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auth examples that persist user state in localStorage could be copied into production in a way that stores full user objects, tokens, or session material in browser storage.

Mitigation: Before production use, replace that pattern with server-managed HttpOnly cookies or an explicit allowlist of non-sensitive UI fields.

## Reference(s):

- [Vue Specialist Code Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Vue and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vue single-file components, TypeScript composables, Pinia stores, Nuxt patterns, Vitest tests, and performance recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
