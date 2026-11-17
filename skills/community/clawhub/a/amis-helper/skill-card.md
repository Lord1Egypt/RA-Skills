## Description:

amis-helper helps developers generate and check Baidu amis 6.x JSON Schema for back-office CRUD pages, dialogs, forms, imports, exports, API response adaptation, and component refresh flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthoyx](https://clawhub.ai/user/anthoyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft production-oriented amis admin-page JSON and avoid known configuration pitfalls in CRUD lists, dialog actions, form controls, API data sources, imports, exports, and selectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated amis JSON may include data-changing delete, import, export, or binding actions once connected to real APIs.

Mitigation: Review every generated endpoint, request body, authentication-bearing download, and destructive action before wiring it to production services.

Risk: The artifact is scoped to amis 6.x and its rules were tested primarily against amis 6.13.0, so behavior may differ in other amis runtimes.

Mitigation: Validate generated configurations in the target amis version, and separately test amis-editor, mobile H5, or SSR usage before adopting the output there.

Risk: Placeholder endpoints, API adaptors, and environment-derived variables can be copied into generated JSON without matching the target backend.

Mitigation: Replace placeholders, confirm response adaptors and status handling, and inspect environment variable references before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anthoyx/skills/amis-helper)
- [META.md](artifact/META.md)
- [CRUD specification](artifact/references/crud.md)
- [Dialog and action chain rules](artifact/references/dialog-actions.md)
- [Form control rules](artifact/references/form-controls.md)
- [API and data source rules](artifact/references/data-source.md)
- [Self-check checklist](artifact/references/self-check.md)
- [Examples index](artifact/examples/INDEX.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with amis JSON Schema snippets and reusable JSON configuration fragments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated configurations should be reviewed before deployment, especially API URLs, data-changing actions, imports, exports, downloads, and environment-derived variables.]

## Skill Version(s):

1.2.10 (source: frontmatter, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
