## Description:

Given a keyword, this skill searches TikTok and Instagram Reels for viral videos, transcribes them, identifies verbal, textual, and visual hooks, and returns a reference table for content calendars, scripts, or research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External content strategists, creators, and agent workflows use this skill to find high-performing short-form video references for a topic, extract transcripts when available, and turn each reference into hook analysis that can feed calendars, scripts, or content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public social-media URLs, handles, metrics, and transcript-derived analysis may be sent to external scraping or transcription services.

Mitigation: Use the skill only for public social-media research and avoid submitting sensitive or private material unless the user accepts those external-service disclosures.

Risk: Reports may be posted back in Telegram and saved locally under informes/.

Mitigation: For sensitive research, instruct the agent not to save or share externally unless that output is required.

Risk: Scraping or transcription failures can lead to unverified metrics or incomplete hook analysis.

Mitigation: Follow the skill's verification gate: do not invent metrics, mark affected rows as unverified, and request a capture or rerun when the scraper or transcript source fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/analizador-referencias-virales-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, files, API calls, guidance]

**Output Format:** [Markdown table and saved Markdown report, with optional structured records for downstream calendar workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include video URLs, public social-media handles, view counts, hook labels, transcript excerpts, and explicit unverified markers when scraping or transcription does not run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
