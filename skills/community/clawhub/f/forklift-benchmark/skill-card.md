## Description:

Evaluates forklift embodied-AI task plans by sampling local FK-Bench v2 questions, scoring structured action predictions, and generating reports without requiring an external model API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangpf6698](https://clawhub.ai/user/yangpf6698)

### License/Terms of Use:

Proprietary Skill License Terms; underlying FK-Bench v2 benchmark Apache-2.0

## Use Case:

Developers, benchmark authors, and AI evaluators use this skill to sample Chinese forklift-operation tasks, collect structured action-plan answers from an agent, score those answers, and inspect score reports for embodied-AI evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running protect.py or extend.py with --remove-plaintext intentionally removes local plaintext dataset JSON files inside the skill copy.

Mitigation: Run those maintenance commands only on a disposable or version-controlled copy, and omit --remove-plaintext unless plaintext dataset removal is intended.

Risk: Benchmark scores and generated reports can be mistaken for operational approval of real forklift actions.

Mitigation: Use the outputs as evaluation artifacts only, and require human safety and operational review before applying any forklift action plan outside the benchmark.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangpf6698/skills/forklift-benchmark)
- [README](README.md)
- [Actions DSL](references/actions-dsl.md)
- [Data Schema](references/data-schema.md)
- [Modules and Scenes](references/modules-scenes.md)
- [Scoring](references/scoring.md)
- [Skill Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash commands plus JSON score files and optional PNG/HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against bundled benchmark data and user-provided prediction files; no external API is required for normal sampling, scoring, or visualization.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json and CHANGELOG.md report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
