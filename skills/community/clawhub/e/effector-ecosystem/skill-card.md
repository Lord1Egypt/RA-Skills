## Description:

Use when designing, reviewing, generating, or refactoring React applications built with Effector, effector-react, Farfetched, Atomic Router, @effector/next, patronum, effector-storage, forms, i18n, testing, and related Effector ecosystem tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demark-pro](https://clawhub.ai/user/demark-pro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, review, refactor, and audit React applications that rely on Effector ecosystem state, routing, data fetching, SSR, persistence, forms, i18n, and testing patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples or guidance may introduce geolocation behavior without matching the product audience or consent expectations.

Mitigation: Confirm the project need and user audience before adding geolocation, and keep browser-signal usage explicit and reviewable.

Risk: Locale or i18n examples may not match the target audience.

Mitigation: Adapt locale defaults, supported languages, and fallback behavior to the product's intended users before implementation.

Risk: Persistence examples can be misapplied to sensitive data or unvalidated browser storage.

Mitigation: Do not store secrets in browser storage, and validate persisted external data before it enters Effector state.

Risk: Deep audit mode can surface inferred architecture risks when only static source relationships are visible.

Mitigation: Require file or path evidence for findings, clearly label inferred risks, and pair each finding with a minimal fix and acceptance criterion.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/demark-pro/skills/effector-ecosystem)
- [Source policy](references/00-source-policy.md)
- [Package map](references/01-package-map.md)
- [Effector modeling rules](references/03-effector-modeling.md)
- [Farfetched contracts and remote operations](references/04-farfetched-contracts.md)
- [React UI binding with Effector](references/05-react-ui-binding.md)
- [Routing, forms, persistence, and i18n](references/06-routing-forms-persistence-i18n.md)
- [Testing and tooling](references/07-testing-tooling.md)
- [Anti-patterns](references/08-anti-patterns.md)
- [Review checklist](references/09-review-checklist.md)
- [Ecosystem library notes](references/10-ecosystem-library-notes.md)
- [Next.js with Effector](references/11-nextjs.md)
- [Production audit playbook](references/12-production-audit-playbook.md)
- [Effector documentation](https://effector.dev)
- [Farfetched documentation](https://ff.effector.dev)
- [Atomic Router documentation](https://atomic-router.github.io)
- [@effector/next repository](https://github.com/effector/next)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript code blocks, shell commands, configuration snippets, review findings, and acceptance criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated templates, corrected examples, audit findings, and version-sensitive guidance that should be checked against current package documentation.]

## Skill Version(s):

0.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
