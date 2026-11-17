## Description:

Log, query, import, and chart baby care events as a private CSV-based replacement for baby tracking apps such as Huckleberry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinzokov](https://clawhub.ai/user/martinzokov)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill to maintain a private local baby log, answer natural-language queries about care events, import Huckleberry CSV exports, and generate growth or weight charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive baby identity, care, and health records are stored as local plaintext CSV, JSON, HTML, and PNG files.

Mitigation: Use a private data directory on a trusted single-user device, avoid synced or shared folders, and restrict file permissions.

Risk: CSV imports or exports may be unsafe when opened in spreadsheet tools.

Mitigation: Treat CSV files as untrusted, review unusual imports with dry-run first, and inspect exports before opening them in spreadsheets.

Risk: Approximate percentile data may be mistaken for precise medical guidance.

Mitigation: Use official WHO LMS data for percentile claims and treat charts as tracking aids rather than medical advice.

## Reference(s):

- [Baby Tracker Schema Reference](references/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/martinzokov/skills/baby-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Plain text or Markdown with shell commands, plus optional JSON, CSV, HTML, and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated local files can contain sensitive baby identity, care, and health records.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
