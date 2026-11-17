## Description:

AEGIS provides civilian-first threat monitoring for conflict zones with real-time safety alerts and human-readable situation updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pleasechooseusername](https://clawhub.ai/user/pleasechooseusername)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use AEGIS to configure location-based emergency monitoring, run scans or scheduled jobs, and generate safety briefings or Telegram alerts during conflict or crisis situations.

### Deployment Geography for Use:

United Arab Emirates, Dubai-focused; review and adapt profiles and scripts before relying on other locations.

## Known Risks and Mitigations:

Risk: Local configuration may contain Telegram, NewsAPI, cloud LLM credentials, and safety-related location data.

Mitigation: Use local-only mode where possible, avoid optional cloud keys unless plaintext local storage is acceptable, and verify file permissions under ~/.openclaw.

Risk: Telegram delivery and cloud LLM verification can send alert content or monitoring context outside the local machine.

Mitigation: Configure Telegram or cloud endpoints only after reviewing the data exposure; use local Ollama or no LLM for sensitive contexts.

Risk: Current country support is UAE/Dubai-focused.

Mitigation: Review and adapt country profiles, source filters, emergency contacts, and scripts before relying on the skill for another location.

Risk: Emergency-monitoring outputs can be incomplete, delayed, or incorrect.

Mitigation: Treat AEGIS as supplemental situational awareness and verify safety decisions against official government and emergency sources.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/pleasechooseusername/skills/aegis)
- [Homepage from ClawHub metadata](https://github.com/PleaseChooseUsername/aegis-openclaw-skill)
- [Configuration Reference](references/config-reference.md)
- [Source Registry](references/source-registry.json)
- [UAE Country Profile](references/country-profiles/uae.json)
- [Threat Keywords](references/threat-keywords.json)
- [Preparedness Guidance](references/preparedness/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text alerts, briefings, configuration instructions, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON state under ~/.openclaw/aegis-data and may post to Telegram when configured.]

## Skill Version(s):

3.4.0 (source: ClawHub release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
