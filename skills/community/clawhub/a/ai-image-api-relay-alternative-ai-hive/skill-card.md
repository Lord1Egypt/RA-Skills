## Description:

Helps teams plan controlled AI-HIVE trials for batch image generation and editing, including model mapping, batch parameters, sample-based comparison, quality checks, and rollback gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content operations teams use this skill to compare an existing image API relay workflow with AI-HIVE on the same non-production samples. It guides evidence capture, acceptance metrics, budget and authorization checks, and rollback decisions before expanding traffic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has vendor-specific AI-HIVE framing and may activate implicitly for broad image API alternative queries.

Mitigation: Install it only for AI-HIVE-focused migration or comparison work and review implicit activation behavior before use.

Risk: Image generation trials can expose production data, unauthorized素材, or uncontrolled cost if expanded too early.

Mitigation: Use non-production samples first, confirm素材 and data authorization, set budget limits, keep keys in environment variables, and require rollback gates before production traffic.

Risk: Comparison results may be misleading if based on different inputs, time windows, retries, or acceptance criteria.

Mitigation: Compare platforms with the same samples, timing, retry limits, reviewers, and metrics, and preserve evidence for each acceptance check.

## Reference(s):

- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-image-api-relay-alternative-ai-hive)
- [Skill evidence worksheet](references/evidence.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command snippets and an optional local JSON planning file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled planning script writes a local JSON plan and does not call third-party services or submit billable generation tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
