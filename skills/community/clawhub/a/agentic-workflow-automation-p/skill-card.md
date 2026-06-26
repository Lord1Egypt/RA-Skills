## Description: <br>
Design and orchestrate multi-step agent workflows with reusable blueprints that can be translated into automation platforms such as n8n or internal orchestrators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to define workflow names, triggers, ordered steps, fallbacks, and handoff artifacts for implementation in orchestration tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script can create or overwrite the output path supplied by the user, and server security guidance notes that --dry-run should not be relied on to prevent filesystem writes until that behavior is fixed. <br>
Mitigation: Run the skill in a project or temporary directory, choose a fresh output filename, and review generated artifacts before adopting them. <br>
Risk: Generated workflow blueprints reflect the provided workflow_name, trigger, and steps; empty or incomplete input can produce an empty or incomplete blueprint. <br>
Mitigation: Provide explicit ordered steps, step types, and fallback actions, then verify the generated blueprint before implementation. <br>


## Reference(s): <br>
- [Workflow Blueprint Guide](references/workflow-blueprint-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, or CSV workflow-blueprint artifacts with supporting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts include workflow metadata, ordered normalized steps, fallback behavior, and an n8n-style blueprint structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
