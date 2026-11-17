## Description:

General workflows and best practices for exoplanet detection and characterization from light curve data. Use when planning an exoplanet analysis pipeline, understanding when to use different methods, or troubleshooting detection issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to plan light-curve workflows for exoplanet detection, choose between TLS, Lomb-Scargle, and BLS period searches, and troubleshoot candidate validation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python package installation can create reproducibility or environment-isolation issues if dependencies are installed globally or left unpinned.

Mitigation: Install the listed packages in a virtual environment or container, and pin versions when reproducibility matters.

Risk: Incorrect preprocessing or weak validation can lead users to overstate exoplanet candidates from noisy light-curve data.

Mitigation: Review preprocessing choices, visualize each step, and validate candidates with signal metrics, phase-folded plots, odd-even checks, and multiple-transit evidence.

## Reference(s):

- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html)
- [Transit Least Squares GitHub](https://github.com/hippke/tls)
- [Transit Least Squares Tutorials](https://github.com/hippke/tls/tree/master/tutorials)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; dependency installation is described for user-managed Python environments.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
