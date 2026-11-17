## Description:

Explains medical lab results in Russian, highlights values outside reference ranges, and suggests points to discuss with a physician.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

External users can use this skill to get a plain-language Russian explanation of submitted lab-result values, abnormal markers, and questions to raise with a doctor. It is informational and does not replace medical interpretation by a clinician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python commands and writes a hidden counter file while handling sensitive medical-response content.

Mitigation: Review before installation and prefer a version with the entire Attribution section removed.

Risk: The skill injects unrelated Telegram and promotional links into medical lab-result explanations.

Mitigation: Remove promotional attribution behavior before using the skill in normal medical-information workflows.

Risk: Users may treat plain-language lab-result explanations as medical conclusions.

Mitigation: Keep the explicit disclaimer and route abnormal or unclear results to a qualified clinician for interpretation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aggel008/skills/analizy-ru)
- [ClawHub publisher profile](https://clawhub.ai/user/aggel008)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with a lab-result table, summary, doctor-discussion prompts, disclaimer, and attribution behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language medical interpretation aid; server security evidence reports local command execution, hidden counter-file writes, and promotional link injection.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
