## Description:

Astro Daily Transits helps an agent calculate daily astrological transits over a natal chart, identify aspects and house activations, and produce bilingual text forecasts, JSON data, and chart images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dynamicsalex](https://clawhub.ai/user/dynamicsalex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate entertainment or educational astrology transit forecasts for a supplied birth date, time, city, and target date. It can return text, structured JSON, and a rendered chart image for agent-assisted interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes the runtime environment and uses a native Windows extension.

Mitigation: Review before installing and run only in an isolated environment where runtime package installation and native extensions are acceptable.

Risk: Generated chart images may include a default QR code and ClawHub URL.

Mitigation: Review generated images before sharing and confirm the embedded link content is acceptable.

Risk: The skill may import interpretation data from a nearby astro-natal-chart skill directory when present.

Mitigation: Run it in a controlled workspace and verify adjacent skill directories before relying on the generated forecast.

Risk: Astrological forecasts are not a scientific basis for high-impact decisions.

Mitigation: Use outputs for entertainment or educational purposes and avoid using them for medical, financial, legal, or similarly consequential decisions.

## Reference(s):

- [Astro Daily Transits ClawHub Page](https://clawhub.ai/dynamicsalex/skills/astro-daily-transits)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [Plain text forecast, JSON transit data, and PNG chart output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Russian and English output; chart output may include a default ClawHub URL and QR code.]

## Skill Version(s):

5.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
