## Description:

将 Digest 候选进一步精选为 Daily Review 日报：合并同一事件、提炼主题、分配栏目、突出重点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gcdd1993](https://clawhub.ai/user/gcdd1993)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn preselected digest candidates into a concise Simplified Chinese Daily Review with fixed sections, merged duplicate events, and clear judgments about importance, risks, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly constrains output into six fixed Daily Review sections, which may be unsuitable for loosely structured digests.

Mitigation: Use it when the desired result is a fixed-section Daily Review, and review the final section placement before publishing.

Risk: Users could assume downstream feed or knowledge-base state changes are part of review generation.

Mitigation: Treat the Review document as the output and require explicit user instruction before marking FreshRSS items read or syncing downstream systems.

Risk: English source material can lose important nuance if summarized too tersely.

Mitigation: Include Chinese summaries that cover the event, key facts, core conclusion, and why the source matters.

## Reference(s):

- [Daily Review Spec](references/daily-review-spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Simplified Chinese Markdown daily review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses six fixed sections in a stable order and expects Markdown links with Chinese summaries for English sources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
