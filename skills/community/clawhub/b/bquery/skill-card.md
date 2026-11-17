## Description:

Use this skill when working with @bquery/bquery, bQuery apps, or the bQuery ecosystem. It helps the agent choose the right bQuery module, write idiomatic code, and use the library across core DOM APIs, reactivity, concurrency workers, Web Components, motion, security, platform helpers, router, store, declarative views, forms, i18n, accessibility, drag-and-drop, media observers, plugins, devtools, testing, Storybook, and SSR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josunlp](https://clawhub.ai/user/josunlp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get bQuery-specific coding guidance for browser-native TypeScript or JavaScript applications. It helps choose appropriate bQuery modules and apply idiomatic patterns for DOM work, reactivity, Web Components, routing, forms, accessibility, testing, SSR, and related frontend tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for generic frontend work where bQuery is not actually relevant.

Mitigation: Verify that the repository uses @bquery/bquery or that the user explicitly wants bQuery-specific guidance before applying it.

Risk: Guidance involving dynamic HTML can introduce unsafe rendering if user-controlled content is injected directly.

Mitigation: Use bQuery security helpers such as sanitization and Trusted Types guidance before rendering untrusted HTML.

Risk: Guidance using the bQuery view module can conflict with strict Content Security Policy settings because it requires unsafe-eval.

Mitigation: Call out the CSP requirement when recommending the view module and choose another bQuery pattern if unsafe-eval is unacceptable.

## Reference(s):

- [bQuery homepage](https://bquery.flausch-code.de/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with TypeScript or JavaScript code examples and shell commands when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden execution, persistence, credential handling, or destructive behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
