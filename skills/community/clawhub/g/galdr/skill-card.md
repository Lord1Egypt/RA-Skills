## Description: <br>
Galdr helps OpenClaw agents turn YouTube URLs or local audio files into grounded, time-ordered listening-experience prompts backed by listener-state traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sellemain](https://clawhub.ai/user/sellemain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use Galdr to analyze songs or music videos from URLs or local audio and assemble evidence-backed ARC prompts for listening-experience prose, comparison, or frame extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Galdr can fetch remote media and retain downloaded or derived local analysis artifacts. <br>
Mitigation: Use trusted URLs and a trusted Galdr binary, then review or clean the Galdr output directory when retained media or derived artifacts are not desired. <br>
Risk: Metric-backed prose can overstate what audio structure proves about private emotional intent. <br>
Mitigation: Treat listener-state metrics as evidence for structural changes, review generated prose against the trace, and avoid claims the structure does not support. <br>
Risk: Fetching or analyzing copyrighted media may be inappropriate without the right context or permissions. <br>
Mitigation: Use the skill only with media the operator is authorized to access or analyze. <br>


## Reference(s): <br>
- [Galdr on ClawHub](https://clawhub.ai/sellemain/galdr) <br>
- [Galdr package on PyPI](https://pypi.org/project/galdr/) <br>
- [Galdr project repository](https://github.com/sellemain/galdr) <br>
- [Metric reference](references/metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated prompt or text outputs from the Galdr CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local analysis artifacts and time-ordered metric traces produced by the Galdr CLI.] <br>

## Skill Version(s): <br>
0.5.1 (source: evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
