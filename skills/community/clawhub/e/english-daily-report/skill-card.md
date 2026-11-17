## Description:

Generates a daily English-learning report with a news-style summary, Chinese translation, vocabulary notes, PDF output, and TTS audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaofangzheng](https://clawhub.ai/user/zhaofangzheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language learners use this skill to create a daily English study package from real news or clearly labeled study material, including text, PDF, and audio outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a local file-overwrite weakness in the PDF generation script.

Mitigation: Review the script before running it, restrict write access to the OpenClaw uploads directory, and harden date handling and temporary-file creation before production use.

Risk: The security summary says network and TTS privacy disclosure is incomplete.

Mitigation: Treat web fetching and TTS as external-service interactions and avoid sending sensitive content through those features unless the operator has approved the providers.

Risk: The security guidance warns against untrusted date values until the PDF script is hardened.

Mitigation: Use trusted ISO-style dates only, or add input validation and mktemp-based temporary files before accepting arbitrary user-supplied dates.

## Reference(s):

- [Example English Daily Report](references/example-report.md)
- [ClawHub skill page](https://clawhub.ai/zhaofangzheng/skills/english-daily-report)
- [Publisher profile](https://clawhub.ai/user/zhaofangzheng)
- [Google Chrome](https://www.google.com/chrome/)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report content with shell commands for PDF generation and TTS audio creation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report text and guides creation of PDF and MP3 files under the OpenClaw uploads directory.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
