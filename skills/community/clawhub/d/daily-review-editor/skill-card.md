## Description: <br>
将 Digest 候选进一步精选为 Daily Review 日报：合并同一事件、提炼主题、分配栏目、突出重点。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gcdd1993](https://clawhub.ai/user/gcdd1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers or operators who collect Digest candidates use this skill to turn a daily candidate set into a concise Simplified Chinese Markdown Daily Review with six fixed sections, merged duplicate events, prioritized items, and one deeper topic analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated daily reviews may omit context or introduce inaccurate summaries. <br>
Mitigation: Review the generated Markdown, source links, and Chinese summaries before relying on or publishing the review. <br>
Risk: External FreshRSS, note-system, or file-saving workflows could change downstream state if automated around the skill. <br>
Mitigation: Connect downstream workflows only under explicit user control and avoid automatic read-back or syncing without review. <br>


## Reference(s): <br>
- [Daily Review Spec](references/daily-review-spec.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gcdd1993/daily-review-editor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Simplified Chinese Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses six fixed sections in a fixed order and keeps FreshRSS read-back or downstream syncing under explicit user control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
