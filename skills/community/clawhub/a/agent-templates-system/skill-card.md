## Description: <br>
OpenClaw Agent Templates system reference and workflow guide for creating, editing, reviewing, debugging, or extending template-backed agent creation, storage, UI, workspace seeding, identity defaults, and create-from-template flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill when working on OpenClaw's Agent Templates feature: reusable agent blueprints, template CRUD, SQLite-backed storage, UI editing, and materializing agents from templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Template materialization can create or overwrite workspace files, seed memory, merge skills, and update agent configuration when the documented OpenClaw feature is used. <br>
Mitigation: Review each template JSON definition before use, especially workspace.files, memorySeeds, overwrite modes, workspace path overrides, and clawhubUrl skill references. <br>
Risk: Raw JSON editing can produce invalid or unintended template definitions for non-technical users. <br>
Mitigation: Validate template JSON and review the resulting workspace files, memory seed targets, identity defaults, and merged skill list before creating an agent. <br>


## Reference(s): <br>
- [Agent Templates Implementation](references/implementation.md) <br>
- [Agent Template Schema Notes](references/template-schema.md) <br>
- [Agent Templates UI Design](references/ui-design.md) <br>
- [Example Agent Template Definition](assets/examples/agent-template-definition.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/agent-templates-system) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON schema examples and implementation references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; it does not install or run code itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
