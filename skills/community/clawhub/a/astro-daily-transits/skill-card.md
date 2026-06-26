## Description: <br>
Astro Daily Transits calculates daily planetary transits over a natal chart and produces bilingual text forecasts, JSON transit data, and rendered PNG chart images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dynamicsalex](https://clawhub.ai/user/dynamicsalex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate astrology transit forecasts for a supplied birth date, birth time, city, and target date. It can return a text reading, structured JSON for downstream analysis, or a chart image with the forecast panel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reports that the renderer may automatically install Pillow when it is missing. <br>
Mitigation: Review before installing and preinstall Pillow from a trusted, pinned source instead of relying on automatic installation. <br>
Risk: Generated charts can include a bundled donation QR shortlink. <br>
Mitigation: Inspect or disable the bundled QR frame before sharing generated images if that link is not desired. <br>
Risk: Forecast inputs and outputs can expose personal birth details, location, name, and forecast content. <br>
Mitigation: Avoid sharing generated JSON or images when those personal details should remain private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dynamicsalex/skills/astro-daily-transits) <br>
- [Declared skill homepage](https://github.com/dynamicsAlex/astro-daily-transits) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, image files, shell commands, guidance] <br>
**Output Format:** [Plain text forecast, structured JSON, or PNG chart generated through Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Russian and English output, optional AI-supplied conclusion text, and target dates in the past, present, or future.] <br>

## Skill Version(s): <br>
5.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
