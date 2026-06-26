## Description: <br>
General workflows and best practices for planning exoplanet detection and characterization pipelines from light curve data, including method selection and troubleshooting detection issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to plan light-curve workflows for exoplanet detection, select period-search methods, and troubleshoot candidate validation issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scientific thresholds, dependencies, or linked methods may be outdated or unsuitable for a specific research decision. <br>
Mitigation: Verify thresholds, dependencies, and linked methods against current library documentation and domain literature before relying on results. <br>
Risk: Over-aggressive preprocessing, missing flux uncertainties, or period aliasing can weaken or misidentify transit signals. <br>
Mitigation: Use conservative preprocessing, include flux uncertainties, inspect each preprocessing step, and validate candidates with signal metrics, phase-folded plots, odd-even checks, and data-gap review. <br>


## Reference(s): <br>
- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html) <br>
- [Transit Least Squares GitHub](https://github.com/hippke/tls) <br>
- [Transit Least Squares Tutorials](https://github.com/hippke/tls/tree/master/tutorials) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only; does not execute analysis or access credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
