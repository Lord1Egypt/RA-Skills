## Description:

Build a transactional HTML email that renders correctly across Gmail, Outlook, and Apple Mail, with a plain-text alternative and dark-mode support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atom00blue](https://clawhub.ai/user/atom00blue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write or edit transactional email HTML and plain-text bodies, including reusable Drin templates with variables, cross-client layout rules, inlined styles, preheaders, bulletproof buttons, and dark-mode support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated email templates can include unsafe or unvalidated link variables such as ctaUrl and unsubscribeUrl.

Mitigation: Use trusted or server-generated values, restrict links to approved HTTPS destinations, and preview templates before sending.

Risk: Raw or unescaped template output can insert unsafe content into email HTML.

Mitigation: Keep raw or unescaped template output limited to pre-sanitized content and prefer escaped interpolation for normal HTML variables.

## Reference(s):

- [React Email](https://react.email)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with HTML, plain-text email, and TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Drin handlebars template variables and email-client compatibility guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
