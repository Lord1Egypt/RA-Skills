## Description:

Lomb-Scargle periodogram for finding periodic signals in unevenly sampled time series data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and astronomy researchers use this skill to analyze unevenly sampled light curves, radial velocity data, and other astronomical time series for periodic signals such as stellar rotation, pulsation, eclipsing binaries, and possible exoplanet transit candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are not pinned in the skill instructions.

Mitigation: Install Lightkurve, NumPy, and Matplotlib in a dedicated virtual environment and prefer pinned versions or a reviewed lockfile before operational use.

Risk: Periodogram peaks can reflect harmonics, aliases, or other periodic phenomena rather than a confirmed exoplanet signal.

Mitigation: Review period ranges, inspect harmonics and aliases, and apply transit-specific follow-up methods such as TLS or BLS when evaluating exoplanet candidates.

## Reference(s):

- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html)
- [Lightkurve Periodogram Documentation](https://docs.lightkurve.org/)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, markdown]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis guidance and example commands for using Lightkurve, NumPy, and Matplotlib; it does not itself execute analysis.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
