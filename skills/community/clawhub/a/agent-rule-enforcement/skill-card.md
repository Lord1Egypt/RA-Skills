## Description:

Audit whether an agent's written rules are actually enforceable: classify each rule as interception, exit gate, detection, or prompt-only, compute blocking coverage, and run behavioral checks over event logs. Use when a rulebook has grown, when someone asks whether rules are really followed, or after changing agent instructions. Tool-agnostic; works on Markdown rules and JSONL event logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengcengcai-creator](https://clawhub.ai/user/cengcengcai-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess where agent rules are enforced, measure observed behavior against JSONL event logs, and identify practical enforcement changes. Its coverage metrics are structural and do not certify compliance or prove safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The rule scanner writes a CSV beside its input, and the host's runtime permission controls are not established by the release scan.

Mitigation: Grant only the file access needed for the selected rule files and output location, and confirm the host enforces those limits.

Risk: Rule tiers and behavioral checks can produce misleading conclusions if heuristics, task segmentation, or thresholds are treated as proof.

Mitigation: Review every suggested tier and calibrate checks on a known-good log period before relying on the reported coverage or rates.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cengcengcai-creator/skills/agent-rule-enforcement)
- [Checks and event schema](references/checks.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, CSV, Guidance]

**Output Format:** [JSON behavior-audit summaries, a CSV rule-tier review scaffold, and concise Markdown or text findings and proposals.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rule-tier suggestions require manual review; behavior checks and thresholds should be calibrated against known-good logs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
