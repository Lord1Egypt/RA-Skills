## Description:

Content-strategy diagnosis for Chinese creator work that helps an agent judge whether a topic, draft, or content plan should become a short video, post, article, or live session and return a concrete next action before writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, content strategists, and agents use this skill to diagnose Chinese-language content ideas, plans, and drafts before writing. It identifies the main bottleneck, recommends the best-fit format and platform, checks material density and goal linkage, and ends with one concrete next move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged defaults and templates are Chinese-oriented, which may produce an unsuitable language or framing for other audiences.

Mitigation: Ask the agent explicitly to respond in the required language and adapt the diagnosis to the target audience.

Risk: The skill provides strategic content guidance that may be incomplete when the user's topic, goal, platform, or source material is thin.

Mitigation: Require the agent to state missing information and stop at diagnosis rather than pretending certainty.

## Reference(s):

- [Content Strategy Diagnosis ClawHub Page](https://clawhub.ai/cellinlab/skills/cell-content-strategy-diagnosis)
- [ClawHub Metadata Homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/content-strategy-diagnosis)
- [Workflow Reference](references/workflow.md)
- [Diagnostic Lens Reference](references/diagnostic-lens.md)
- [Diagnosis Template](assets/diagnosis-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnosis report, typically in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, persistence, credential handling, or hidden data access according to release security evidence.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
