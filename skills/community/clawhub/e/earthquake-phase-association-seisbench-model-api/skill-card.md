## Description:

This skill guides agents in using the SeisBench model API to install SeisBench, load pretrained seismic models, and apply annotation or classification workflows to waveform streams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and geoscience engineers use this skill to apply SeisBench pretrained models to seismic waveform streams for phase picking, earthquake detection, waveform denoising, and depth estimation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation and pretrained weight downloads can introduce supply-chain or reproducibility risk.

Mitigation: Install SeisBench from a trusted Python package index inside a dedicated virtual environment, pin SeisBench and dependencies when reproducibility matters, and account for first-use model weight downloads and caching.

Risk: Very small waveform amplitudes can lead to numerical instability or misleading normalized outputs.

Mitigation: Normalize waveform data deliberately and rescale extremely small values before passing them to SeisBench models when needed.

Risk: Model outputs such as picks, detections, denoised waveforms, or depth estimates can be misleading if treated as final seismic interpretation without review.

Mitigation: Review model outputs against domain expectations and treat continuous waveform streams as potentially containing more than one P-wave or S-wave event.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SeisBench installation guidance, API usage examples, pretrained model loading guidance, performance tips, and waveform handling best practices.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
