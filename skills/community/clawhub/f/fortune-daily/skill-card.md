## Description:

Fortune Daily generates personalized Chinese horoscope readings by combining Western zodiac signs and Chinese zodiac attributes for daily, weekly, monthly, or specified-date forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vccv2rndrv-cyber](https://clawhub.ai/user/vccv2rndrv-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-assistant operators use this skill to request or schedule personalized horoscope readings across overall, love, career, finance, and health dimensions. It supports one-off queries and opt-in daily push workflows using stored zodiac profile preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain exact birthdays and horoscope profile data in MEMORY.md.

Mitigation: Installers should remove the bundled populated MEMORY.md record, store only the minimum profile data needed, and honor deletion or retention preferences.

Risk: The skill can use stored profile data for scheduled pushes to external channels.

Mitigation: Require explicit user opt-in before scheduled delivery and confirm the destination channel before enabling any recurring push.

Risk: Relationship or wellness horoscope content could be mistaken for professional advice.

Mitigation: Keep readings framed as entertainment and avoid substituting horoscope output for professional mental-health, medical, financial, or relationship support.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vccv2rndrv-cyber/skills/fortune-daily)
- [Zodiac Index](references/zodiac-index.md)
- [Aquarius Reference](references/signs/aquarius.md)
- [Aries Reference](references/signs/aries.md)
- [Cancer Reference](references/signs/cancer.md)
- [Capricorn Reference](references/signs/capricorn.md)
- [Gemini Reference](references/signs/gemini.md)
- [Leo Reference](references/signs/leo.md)
- [Libra Reference](references/signs/libra.md)
- [Pisces Reference](references/signs/pisces.md)
- [Sagittarius Reference](references/signs/sagittarius.md)
- [Scorpio Reference](references/signs/scorpio.md)
- [Taurus Reference](references/signs/taurus.md)
- [Virgo Reference](references/signs/virgo.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown horoscope reading with optional scheduling configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized by birthday, Western zodiac sign, Chinese zodiac attribute, target date or time period, and push preferences when provided.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
