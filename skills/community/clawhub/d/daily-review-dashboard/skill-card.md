## Description:

Manage Steven's daily subjective review dashboard by reading, updating, and displaying daily reviews, issue tracking, sentiment tags, and next-day plans in review_egg/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j97feng-beep](https://clawhub.ai/user/j97feng-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to maintain a local subjective daily trading review dashboard for Steven, including raw review notes, structured summaries, issue tracking, sentiment tags, holdings snapshots, and next-day plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill updates several persistent local review files and embedded dashboard data, so an incorrect update could make records inconsistent.

Mitigation: Review generated file changes before accepting new daily review updates, especially JSONL, CSV, summary JSON, issue tracker JSON, and dashboard HTML changes.

Risk: Subjective review notes and objective trade records may be confused if data is copied across systems.

Mitigation: Keep subjective review data under review_egg/ and objective trading ledger data under trade/, matching the skill's documented separation rule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j97feng-beep/skills/daily-review-dashboard)
- [Publisher profile](https://clawhub.ai/user/j97feng-beep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions with file edits, JSON/JSONL and CSV updates, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent local updates under review_egg/ and dashboard data embedded in HTML JavaScript.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
