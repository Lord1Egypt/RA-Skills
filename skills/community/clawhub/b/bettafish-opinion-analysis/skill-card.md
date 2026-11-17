## Description:

BettaFish is a multi-agent public-opinion analysis skill that gathers live web and social media signals, analyzes sentiment and events, and produces Word, PDF, and interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyico](https://clawhub.ai/user/liyico)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, communications, and research teams use this skill to monitor social media and web coverage, compare public sentiment across sources, and generate formal public-opinion analysis reports for review or presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled document tools use unsafe LibreOffice hooks and shared temporary files that could allow local tampering to affect report generation.

Mitigation: Review before installation and avoid LibreOffice conversion or tracked-change features unless shared /tmp paths and macro validation are fixed.

Risk: Generated HTML reports may fetch third-party scripts.

Mitigation: Open generated HTML reports in a controlled environment and review external script dependencies before sharing or deploying them.

Risk: Untrusted report topics may interact poorly with incomplete output escaping and filename sanitization.

Mitigation: Use trusted report topics until output escaping and filename sanitization are reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyico/skills/bettafish-opinion-analysis)
- [Data Sources Guide](references/data_sources.md)
- [Design Guide](references/design_guide.md)
- [Sentiment Guide](references/sentiment_guide.md)
- [ffmpeg](https://ffmpeg.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Word, PDF, and HTML report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live web research inputs and may generate report files with charts, tables, source lists, and interactive HTML visualizations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
