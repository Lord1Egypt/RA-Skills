## Description: <br>
Detects periodic signals in unevenly sampled astronomical time-series data with Lomb-Scargle periodograms using Lightkurve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and astronomy analysts use this skill to generate Lightkurve-based guidance and code for detecting periodic variation in light curves, radial velocity data, and other unevenly sampled astronomical time series. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security guidance advises caution around repository trust, authentication context, moderation, publish targets, dry runs, and full-access nested autoreview. <br>
Mitigation: Confirm the repository and auth context before installation, review intended targets before agent execution, use dry-run behavior where available, and disable broad nested autoreview when it exceeds the environment's risk tolerance. <br>
Risk: Periodogram outputs can identify aliases, harmonics, or misleading peaks if period ranges and follow-up checks are chosen poorly. <br>
Mitigation: Review period ranges, compare possible harmonics, inspect aliases, and use follow-up methods such as TLS or BLS when exoplanet transit detection is the goal. <br>


## Reference(s): <br>
- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html) <br>
- [Lightkurve Periodogram Documentation](https://docs.lightkurve.org/) <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/exoplanet-detection-period-lomb-scargle-periodogram) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is oriented around Lightkurve periodogram setup, period range selection, plotting, interpretation, and model fitting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
