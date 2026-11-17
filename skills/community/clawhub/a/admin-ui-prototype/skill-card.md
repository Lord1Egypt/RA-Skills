## Description:

Queries project-specific Arco Design usage patterns and generates Vue 3 admin page prototypes with mock data, scaffold files, and route snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arisefx](https://clawhub.ai/user/arisefx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to query project-specific Arco Design Vue patterns and generate runnable admin UI prototypes for list, form, detail, dashboard, modal, and empty-state pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project scaffolding may modify files under webui/admin-ui and install JavaScript dependencies.

Mitigation: Review generated files and dependency changes before use; pin dependencies or use a reviewed lockfile for stricter supply-chain control.

Risk: Generated delete, upload, and API examples may be unsafe if connected directly to real backends.

Mitigation: Review each placeholder and mock API path, then replace it with validated backend integration, authorization checks, confirmations, and error handling.

Risk: The skill is tailored to Chinese-locale Vue 3 and Arco Design admin UI conventions.

Mitigation: Confirm the generated copy, naming conventions, and UI patterns match the target project before adopting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arisefx/skills/admin-ui-prototype)
- [Skill Definition](artifact/SKILL.md)
- [Component Usage Index](artifact/knowledge/components/README.md)
- [Admin UI Page Conventions](artifact/knowledge/ui-conventions.md)
- [Page Templates](artifact/knowledge/page-templates.md)
- [Preview Project Scaffold](artifact/knowledge/scaffold.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with Vue, TypeScript, LESS, route snippets, file lists, and shell commands when scaffolding or previewing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update files under webui/admin-ui and may run pnpm install during scaffolding.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
