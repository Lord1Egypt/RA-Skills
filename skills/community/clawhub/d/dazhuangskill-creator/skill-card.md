## Description:

Creates, reshapes, evaluates, packages, and optimizes agent skills, including scaffolding new skills, refining existing ones, designing evaluations, and improving trigger descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazhuangjammy](https://clawhub.ai/user/dazhuangjammy)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create or refactor agent skill directories, choose a lightweight validation path, run evaluation loops when warranted, optimize triggering behavior, and package skills for handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The toolkit can run Claude CLI subprocesses using the existing local Claude Code session.

Mitigation: Run it only in trusted workspaces, review generated commands before execution, and avoid providing secrets in evaluation prompts or artifacts.

Risk: Evaluation workflows can write temporary `.claude/commands` files.

Mitigation: Use an isolated project for evaluations and inspect or remove temporary command files after a run.

Risk: The local HTML review viewer can open evaluation outputs in a browser and may use a local port.

Mitigation: Use trusted evaluation outputs, prefer static/headless review when appropriate, and avoid running the viewer on an occupied port.

Risk: Packaging workflows create distributable skill archives from local directories.

Mitigation: Inspect skill directories for symlinks and unintended files before packaging or sharing archives.

## Reference(s):

- [Skill README](README.md)
- [Skill Architecture Guide](references/skill-architecture.md)
- [Evaluation Loop](references/eval-loop.md)
- [Description Optimization](references/description-optimization.md)
- [Packaging and Delivery](references/package-and-present.md)
- [Schema Reference](references/schemas.md)
- [Claude.ai Runtime Notes](references/runtime-claude-ai.md)
- [Cowork Runtime Notes](references/runtime-cowork.md)
- [A-E Skill Creator Benchmark Report](测评报告/5 个类型性能对比/benchmark_report.md)
- [Capability Archetype Benchmark Report](测评报告/5 个能力原型对比/benchmark_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command snippets, generated or modified files, JSON/YAML configuration, and packaged skill archives when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local validation, evaluation, optimization, packaging, and review-viewer workflows when the requested task calls for them.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
