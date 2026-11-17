## Description:

Provides guidance for using the Transit Least Squares algorithm to detect exoplanet transits in light curves with the transitleastsquares Python package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to guide exoplanet transit searches, refine candidate periods, interpret TLS SDE and SNR outputs, and plan follow-up searches for additional planets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed scientific package dependencies can affect shared or production environments.

Mitigation: Install dependencies in an isolated virtual environment and pin reviewed package versions before operational use.

Risk: Transit detections can be false positives or period aliases when light curve quality, gaps, or preprocessing choices are poor.

Mitigation: Use flux uncertainties, inspect SDE and SNR, check possible half-period or double-period aliases, and visually validate phase-folded light curves.

## Reference(s):

- [TLS GitHub Repository](https://github.com/hippke/tls)
- [TLS Tutorials](https://github.com/hippke/tls/tree/master/tutorials)
- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html)
- [Lightkurve Exoplanet Examples](https://lightkurve.github.io/lightkurve/tutorials/3.1-identifying-transiting-exoplanets.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No generated files by default; outputs guide dependency installation, TLS analysis steps, parameter choices, and result interpretation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
