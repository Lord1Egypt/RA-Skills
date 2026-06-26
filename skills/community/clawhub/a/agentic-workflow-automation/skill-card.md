## Description: <br>
Generates reusable multi-step agent workflow blueprints for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to define ordered workflow blueprints with triggers, step contracts, dependencies, and fallback behavior for handoff to automation platforms or internal orchestrators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script reads a user-selected JSON file and writes blueprint output files, and the security guidance notes that --dry-run should not be relied on to prevent file creation or overwrites. <br>
Mitigation: Test with a temporary or dedicated output path and review the chosen input and output locations before running the script. <br>
Risk: Generated workflow blueprints can encode incorrect step ordering, vague contracts, or weak fallback behavior if the input is underspecified. <br>
Mitigation: Review each generated step for a single purpose, explicit ordering, and clear on-failure behavior before using the blueprint in an automation platform. <br>


## Reference(s): <br>
- [Workflow Blueprint Guide](references/workflow-blueprint-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/0x-Professor/agentic-workflow-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, or CSV blueprint files with concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads an optional JSON input file up to 1 MiB and writes the selected output artifact path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
