## Description:

Calculates natal charts from birth date, time, and city, then produces bilingual text, JSON chart data, and high-resolution PNG wheel visualizations with optional AI conclusion text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dynamicsalex](https://clawhub.ai/user/dynamicsalex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate educational or entertainment natal chart readings from birth details, including calculated planet, house, and aspect data. Agents can also pass chart JSON through an AI interpretation step and embed that conclusion into the rendered PNG.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill bundles a native Windows extension for Swiss Ephemeris.

Mitigation: Review and run the skill in an isolated Windows environment before trusting generated output or deploying it for broader use.

Risk: The renderer attempts to install Pillow at runtime when the package is missing.

Mitigation: Install Pillow explicitly in a controlled environment before execution and avoid relying on runtime package installation.

Risk: The default chart render embeds a bundled QR/frame image.

Mitigation: Inspect generated PNG files before sharing them, or pass a reviewed frame asset when rendering charts.

Risk: Birth details and optional AI conclusion files can contain personal or sensitive information.

Mitigation: Process only data that users have consented to share, and avoid retaining generated chart data or conclusion files longer than needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dynamicsalex/skills/astro-natal-chart)
- [Publisher profile](https://clawhub.ai/user/dynamicsalex)
- [Astro Natal Chart source repository](https://github.com/dynamicsAlex/astro-natal-chart)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Python 3.14 release](https://www.python.org/downloads/release/python-3145/)
- [Microsoft Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## Skill Output:

**Output Type(s):** [text, JSON, image files, guidance]

**Output Format:** [Plain text, JSON, and PNG image files with optional embedded conclusion text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows x64, CPython 3.14, Pillow 12.x, and a bundled Swiss Ephemeris native extension; chart rendering includes a bundled frame image by default.]

## Skill Version(s):

4.3.7 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
