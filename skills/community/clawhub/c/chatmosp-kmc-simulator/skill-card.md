## Description:

Chatmosp Kmc Simulator runs the chatMOSP Kinetic Monte Carlo engine through Wine to execute catalyst surface reaction simulations and produce TOF and coverage outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanyangye](https://clawhub.ai/user/sanyangye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry researchers use this skill to run chatMOSP KMC simulations after parameter preparation, validate expected inputs and outputs, and return coverage and TOF results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unverified external Python wrapper and Windows executable.

Mitigation: Install only from a trusted mosp-for-chatMOSP source and verify the exact kmc_standalone.py and engine/main.exe before running simulations.

Risk: Loosely scoped shell commands and task paths can be risky when supplied from untrusted inputs.

Mitigation: Avoid untrusted task names or paths, review commands before execution, and run the simulator in a contained workspace or sandbox.

## Reference(s):

- [Chatmosp Kmc Simulator on ClawHub](https://clawhub.ai/sanyangye/skills/chatmosp-kmc-simulator)
- [sanyangye ClawHub Publisher Profile](https://clawhub.ai/user/sanyangye)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and references to generated simulation data and plot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce coverage and TOF plots, CSV files, and KMC engine output files when used with the required chatMOSP workspace dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
