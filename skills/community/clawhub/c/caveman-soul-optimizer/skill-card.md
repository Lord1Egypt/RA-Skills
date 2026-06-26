## Description: <br>
Compresses OpenClaw agent internal reasoning and planning into a concise style while preserving final-response personality and technical syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricgu8086](https://clawhub.ai/user/ricgu8086) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent developers use this skill to reduce token use in internal planning and logs while keeping final user communication and technical artifacts uncompressed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes an agent's planning style globally, which may conflict with strict hidden-reasoning, logging, or response-format policies. <br>
Mitigation: Install it only in agents where compressed planning text is acceptable, and review outputs in policy-sensitive workflows. <br>
Risk: The README's absolute safety claim could be read as a privacy guarantee beyond the security evidence. <br>
Mitigation: Treat the security evidence as authoritative: the skill is prompt-only with no executable code or credential access found, but it should not be used as a privacy control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ricgu8086/caveman-soul-optimizer) <br>
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) <br>
- [mCo0L/caveman-claw](https://github.com/mCo0L/caveman-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with technical syntax preserved for code, commands, JSON, paths, and documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only behavior; no executable code or credential access found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
