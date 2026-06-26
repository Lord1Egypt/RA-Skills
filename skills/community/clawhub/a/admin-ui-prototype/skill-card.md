## Description: <br>
Query project-specific Arco Design usage patterns and generate Vue 3 admin page prototypes with mock data, scaffold files, and route snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arisefx](https://clawhub.ai/user/arisefx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query project-specific Arco Design conventions and generate runnable Vue 3 admin UI prototypes with mock data, scaffold files, and route snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prototypes can include mock data and placeholder API calls. <br>
Mitigation: Review generated files and replace TODO placeholders with validated production API wiring before using the prototype beyond local review. <br>
Risk: Scaffolding may require package installation or a local development server. <br>
Mitigation: Run pnpm install or pnpm dev only in a trusted workspace where network downloads and a local preview server are acceptable. <br>
Risk: Generated admin UI code may not match an application's security, data, or workflow requirements without review. <br>
Mitigation: Review the generated Vue files, route snippets, and configuration before deployment or integration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arisefx/admin-ui-prototype) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [UI conventions](artifact/knowledge/ui-conventions.md) <br>
- [Page templates](artifact/knowledge/page-templates.md) <br>
- [Scaffold template](artifact/knowledge/scaffold.md) <br>
- [Component documentation index](artifact/knowledge/components/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with Vue, TypeScript, route snippets, and shell commands when scaffolding is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local files under webui/admin-ui and use mock data placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
