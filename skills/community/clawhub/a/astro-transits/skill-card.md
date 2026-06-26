## Description: <br>
Astrological transit calculator with natal chart support. Daily transits, weekly forecasts, void-of-course Moon, aspects, stations, and ingresses. Uses Swiss Ephemeris. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mizukaizen](https://clawhub.ai/user/mizukaizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate local astrological transit reports, natal chart JSON, weekly forecasts, and void-of-course Moon checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natal chart files can contain birth date, time, timezone, and location coordinates. <br>
Mitigation: Keep saved chart JSON files private and avoid sharing them in prompts, logs, or public repositories. <br>
Risk: Installing Python dependencies directly into a shared environment can affect other projects. <br>
Mitigation: Install pyswisseph in a virtual environment before running the scripts. <br>
Risk: The natal chart save path can overwrite an existing file. <br>
Mitigation: Choose --save paths deliberately and avoid paths used by unrelated files. <br>


## Reference(s): <br>
- [Astro Transits ClawHub listing](https://clawhub.ai/mizukaizen/astro-transits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with shell commands; scripts emit JSON and plain-text transit reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with python3 and pyswisseph; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
