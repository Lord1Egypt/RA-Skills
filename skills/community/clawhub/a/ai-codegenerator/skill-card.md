## Description:

Generates a basic FastAPI project scaffold from a user-provided task description, with optional context and constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason513597](https://clawhub.ai/user/jason513597)

### License/Terms of Use:


## Use Case:

Developers use this skill to create a starter FastAPI application for a described task and receive a generated project path plus execution summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill writes a generated FastAPI project under /home/jason/.openclaw/workspace/generated using a task-derived name.

Mitigation: Use distinct task names when preserving earlier generated files matters, and inspect the returned project_path before using the output.

Risk: The generated FastAPI scaffold is minimal and may not satisfy all functional, security, or deployment requirements for the requested task.

Mitigation: Review, test, and adapt the generated project before deployment or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason513597/skills/ai-codegenerator)
- [Publisher profile](https://clawhub.ai/user/jason513597)

## Skill Output:

**Output Type(s):** [code, configuration, text]

**Output Format:** [FastAPI project files plus JSON execution summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated projects under /home/jason/.openclaw/workspace/generated using a task-derived directory name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
