## Description:

Use when the user wants to build, initialize, validate, optimize, or refactor a model-powered assistant, internal tool, automation, evaluator, or workflow from a business scenario or common problem statement, including project-structure refactors or starter skeletons that may separate model setup, prompt config, and orchestration, even if the request also mentions a UI, app shell, or local model service such as Ollama, and it is still unclear whether the solution should stay a single request, add supporting capabilities, or become orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maplemx](https://clawhub.ai/user/maplemx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn broad model-app requests into an Agently-native plan before choosing lower-level capabilities. It helps decide project boundaries, async posture, repo structure, and routing to model setup, prompt management, output control, TriggerFlow, memory, tools, retrieval, or migration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation wording and can steer generic model-app planning requests toward Agently-specific architecture choices.

Mitigation: Install it when Agently-native planning is desired; otherwise prefer framework-neutral guidance until Agently is explicitly requested.

Risk: Planning recommendations can be incomplete or misleading if accepted as implementation instructions without review.

Mitigation: Review generated architecture, capability routing, and validation rules before applying changes to a project.

## Reference(s):

- [Capability Map](references/capability-map.md)
- [Project Framework](references/project-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/maplemx/skills/agently-playbook)
- [Publisher Profile](https://clawhub.ai/user/maplemx)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are planning and routing recommendations for agent workflows; the skill does not execute code or persist changes by itself.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
