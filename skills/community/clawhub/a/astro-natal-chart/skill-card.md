## Description: <br>
Calculates natal chart data from birth date, time, and place, then produces text, JSON, and 5760x2880 PNG visualizations with bilingual interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dynamicsalex](https://clawhub.ai/user/dynamicsalex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to compute entertainment and educational natal chart data from personal birth details, generate JSON for analysis, and render bilingual chart PNGs. Agents can optionally write a conclusion file that is embedded in the final chart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles names, birth dates, exact times, locations, generated PNGs, and exported JSON that may be personal data. <br>
Mitigation: Use only data the user intends to process, avoid sharing outputs with external AI services without consent, and store generated files outside synced or public folders unless sharing is intended. <br>
Risk: The renderer may install Pillow automatically if it is missing. <br>
Mitigation: Review the environment before running, install dependencies from trusted package indexes, or preinstall Pillow in a controlled environment. <br>
Risk: The release includes and loads a bundled Windows native Swiss Ephemeris extension. <br>
Mitigation: Run only on a Windows x64 host where native binary execution is expected, verify the artifact hash from ClawHub evidence, and keep execution in a user-controlled workspace. <br>
Risk: Astrology output may be mistaken for scientific, medical, or financial guidance. <br>
Mitigation: Treat generated interpretations as entertainment or educational material and do not use them for medical, financial, or other high-stakes decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dynamicsalex/skills/astro-natal-chart) <br>
- [Project homepage declared in skill metadata](https://github.com/dynamicsAlex/astro-natal-chart) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Python 3.14 release](https://www.python.org/downloads/release/python-3145/) <br>
- [Microsoft Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, guidance] <br>
**Output Format:** [Plain text, JSON, and PNG chart files; optional AI conclusion text can be embedded in the PNG.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows x64; requires Python 3.14.x, Microsoft Visual C++ Redistributable, Pillow 12.x, and a bundled Swiss Ephemeris native extension.] <br>

## Skill Version(s): <br>
4.3.7 (source: SKILL.md frontmatter and server release evidence, released 2026-06-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
