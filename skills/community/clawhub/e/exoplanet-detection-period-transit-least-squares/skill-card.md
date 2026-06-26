## Description: <br>
Transit Least Squares (TLS) algorithm for detecting exoplanet transits in light curves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to build or review Python workflows that search light curves for transit-shaped exoplanet signals with the transitleastsquares package. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python dependencies may introduce supply-chain or environment risk when installed into a shared environment. <br>
Mitigation: Install dependencies in a virtual environment and verify the provenance of scientific packages before use, especially in controlled environments. <br>
Risk: Transit candidates can be false positives or period aliases if uncertainties, preprocessing, or data gaps are mishandled. <br>
Mitigation: Use flux uncertainties, inspect SDE, SNR, and phase-folded plots, and validate candidate periods before relying on results. <br>


## Reference(s): <br>
- [TLS GitHub Repository](https://github.com/hippke/tls) <br>
- [TLS Tutorials](https://github.com/hippke/tls/tree/master/tutorials) <br>
- [Lightkurve Tutorials](https://lightkurve.github.io/lightkurve/tutorials/index.html) <br>
- [Lightkurve Exoplanet Examples](https://lightkurve.github.io/lightkurve/tutorials/3.1-identifying-transiting-exoplanets.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
