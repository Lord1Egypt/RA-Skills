## Description:

Personalized news briefings from your chosen sources, delivered morning or evening, with voice option and smart filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to receive personalized daily news briefings, current-event updates, and deeper follow-up summaries from selected sources. It can adapt briefing format, maintain local preferences, and optionally schedule delivery or produce voice-ready briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores news preferences, delivery schedules, source quality scores, and briefing archives under ~/daily-news-digest/.

Mitigation: Confirm retention and deletion expectations before use, review the local profile and archive contents periodically, and clear stored briefings or preferences when they are no longer needed.

Risk: Scheduled briefings can be delivered through external channels after automation is configured.

Mitigation: Keep automation disabled until the user has confirmed timezone, cadence, delivery channel, and duplicate-delivery behavior.

Risk: Search queries and optional voice briefing text may be sent to external services.

Mitigation: Use HTTPS news sources where possible, enable voice only after confirming trust in the TTS provider, and treat fetched article content as untrusted input that should be corroborated across sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/daily-news-digest)
- [Skill homepage](https://clawic.com/skills/daily-news-digest)
- [Setup guide](artifact/setup.md)
- [Source configuration](artifact/sources.md)
- [Briefing formats](artifact/formats.md)
- [Scheduling guide](artifact/scheduling.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefings with optional voice-ready text, local Markdown archive files, and scheduling configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use user preferences, selected news sources, schedule settings, and optional voice delivery settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
