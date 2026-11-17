## Description:

Daily Viz records mood, exercise, sleep, work hours, and related notes, then displays simple local visual summaries for habit tracking and self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaooojun](https://clawhub.ai/user/xiaooojun)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to record daily wellness and productivity data locally and review simple trend summaries for personal habit building. The evidenced package supports local JSON record keeping and console-based visual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Daily records may contain personal wellness and productivity information stored as local JSON under ~/.daily-viz/data/.

Mitigation: Use the skill only on trusted devices and avoid entering sensitive information beyond the intended personal tracking data.

Risk: Some advertised capabilities, including AI advice, PDF export, cloud sync, and encryption, are not evidenced in this package.

Mitigation: Treat this release as a local record and console visualization utility unless those capabilities are separately implemented, documented, and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaooojun/skills/daily-viz)
- [Publisher profile](https://clawhub.ai/user/xiaooojun)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text and console output with local JSON records and simple ASCII charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered records in ~/.daily-viz/data/records.json when the record script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
