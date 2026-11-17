## Description:

Autonomously optimises OpenClaw skills using a benchmark-driven loop that scores outputs, identifies weak patterns, proposes targeted SKILL.md changes, re-tests, and keeps or discards changes based on measured improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wealthvisionai-source](https://clawhub.ai/user/wealthvisionai-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use Autooptimise to benchmark an OpenClaw skill, review quality scores, and evaluate one targeted improvement at a time before accepting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can test another skill and change that skill's behavior after approval.

Mitigation: Invoke it with an explicit target skill and review every proposed diff before approving changes.

Risk: Unattended scheduled use on sensitive skills could surface or approve changes without enough review.

Mitigation: Avoid unattended HEARTBEAT use on sensitive skills and run it only from trusted source versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wealthvisionai-source/skills/autooptimise)
- [README](artifact/README.md)
- [Runner instructions](artifact/runner/run_experiment.md)
- [Scoring rubric](artifact/benchmark/scorer.md)
- [Benchmark tasks](artifact/benchmark/tasks.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, unified diffs, JSON judge scores, and experiment log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create runner/experiment_log.md and modify a target SKILL.md only after explicit human approval.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog, released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
