## Description:

Generates Baidu amis low-code JSON Schema configurations for enterprise admin pages, including CRUD views, forms, dialogs, wizards, dashboards, interaction patterns, mobile adaptation, and validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumacoder](https://clawhub.ai/user/lumacoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn admin UI requirements into amis JSON schemas and starter templates for CRUD pages, forms, search screens, dialogs, dashboards, and multi-step workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated amis schemas can include API paths, form submissions, login persistence, POST/PUT/DELETE actions, and reload behavior that affect real backend data.

Mitigation: Review API URLs, methods, submitted fields, auth-related storage, destructive actions, and reload targets before connecting generated schemas to production services.

Risk: Starter templates use placeholder API paths and field names that may not match the consuming application's backend contract.

Mitigation: Replace placeholder endpoints and fields, then run the bundled validator and application-specific tests before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lumacoder/skills/amis-json-skills)
- [Baidu amis repository](https://github.com/baidu/amis)

## Skill Output:

**Output Type(s):** [JSON, Code, Configuration, Guidance]

**Output Format:** [Markdown and JSON schema snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference bundled templates and validation results for amis Page, Form, CRUD, Dialog, Button, and Wizard schemas.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
