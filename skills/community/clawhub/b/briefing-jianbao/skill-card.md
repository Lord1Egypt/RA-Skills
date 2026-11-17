## Description:

Briefing-pro turns content from URLs, files, text, or images into one-page slide briefings that can be exported as PNG, PDF, or HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonlinearhuman](https://clawhub.ai/user/nonlinearhuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to convert source material into concise, shareable briefing slides for summaries, insights, and presentation assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted webpage or file content could execute code inside generated briefing pages because the slide templates render user-derived fields through dynamic HTML.

Mitigation: Use only trusted source pages and documents until templates escape all user-derived fields and avoid innerHTML for untrusted content.

Risk: Rendering previews, screenshots, or PDFs from generated HTML can expose the browser environment to hostile content.

Mitigation: Render previews and exports in a restricted browser environment.

Risk: Private URLs or sensitive files may be fetched and parsed while building a briefing.

Mitigation: Avoid submitting confidential sources unless the execution environment and generated outputs are approved for that data.

## Reference(s):

- [Briefing-pro ClawHub listing](https://clawhub.ai/nonlinearhuman/skills/briefing-jianbao)
- [frontend-slides ClawHub skill](https://clawhub.com/skill/frontend-slides)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML, browser screenshot, or print-to-PDF workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce PNG screenshots, PDF exports, or HTML slide files from extracted source content.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
