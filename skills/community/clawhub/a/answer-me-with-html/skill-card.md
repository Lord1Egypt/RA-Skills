## Description:

Turns complex answers into one-page visual HTML explainers and, when requested, explainer videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingyuna](https://clawhub.ai/user/qingyuna)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and developers use this skill to turn explanations, comparisons, and multi-step answers into visual HTML pages. It can also produce narrated explainer videos when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proactive page generation creates local files even when no page was requested.

Mitigation: Confirm when a page is useful and where it will be stored; disable always-on use if unwanted.

Risk: Generated pages may include local code or images that should not be shared.

Mitigation: Review each generated page before sharing it.

Risk: Update actions and background checks can change future behavior or create network activity.

Mitigation: Update only from a trusted publisher or source; disable update checks or browser auto-open if unwanted.

## Reference(s):

- [Answer me with HTML on ClawHub](https://clawhub.ai/qingyuna/skills/answer-me-with-html)
- [Settings and updates](artifact/references/settings.md)
- [Explainer video guidance](artifact/references/video.md)
- [Theme catalog](https://answer-me-with-html.com/themes/)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML files]

**Output Format:** [Markdown draft and standalone HTML page; optional narrated video player]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pages are stored locally and may include code or images.]

## Skill Version(s):

0.5.5 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
