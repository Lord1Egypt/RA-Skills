## Description:

Provides a May 2026 AI large model weekly report with Bilibili video links and study notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to surface a concise LLM weekly-report reference with Bilibili source links and related study notes. When executed, it also writes an entry to local knowledge storage, so it should be used only where persistent local writes are intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes to persistent local knowledge storage through an unaudited external Python module path.

Mitigation: Install and invoke it only when persistent local writes are intended, and review the local learn module before use.

Risk: Caller-provided text may be stored without validation or deletion controls.

Mitigation: Validate or limit stored inputs, disclose the persistent write behavior, and provide a way to delete saved entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/auto-llm-4712)
- [Bilibili source BV1d2Vh6EE1t](https://www.bilibili.com/video/BV1d2Vh6EE1t)
- [Bilibili MoE expert parallel all-to-all video](https://www.bilibili.com/video/BV1W314BfEHr)
- [Bilibili OpenCLI personal assistant WebUI video](https://www.bilibili.com/video/BV1DNG86eEr3)
- [Bilibili GRPO KL divergence video](https://www.bilibili.com/video/BV1rsAXe7EZs)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown-style skill content and local knowledge-base entry metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Execution returns a boolean status after attempting to store the provided or default report text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
