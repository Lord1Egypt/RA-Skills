## Description:

Coordinates EvoMap evolution workflows, including V2 transcript ingest and gene distillation, with a deprecated V1 run and solidify path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to ingest session transcript material, distill candidate evolution genes, and inspect cycle status. The V2 workflow also involves separate transcript conversion, cycle execution, review, and publishing steps; V1 is deprecated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised end-to-end workflow may require manual transcript conversion, cycle execution, review, and publishing; scanner coverage was partial.

Mitigation: Check each step's output and complete and review the workflow manually before relying on a cycle result.

Risk: The deprecated V1 solidify path may run git reset --hard on failure and discard uncommitted changes.

Mitigation: Commit or back up changes before using V1, and prefer V2 when it suits the task.

Risk: The skill's runtime permissions are unknown from the available evidence.

Mitigation: Review the commands and run them in a workspace whose contents you can safely modify.

## Reference(s):

- [Evolver Bridge on ClawHub](https://clawhub.ai/147258xuan/skills/evolver-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Shell commands, status text, logs, and generated text or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes cycle logs and evolution artifacts under the workspace's memory/evolution directory.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
