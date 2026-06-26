## Description: <br>
Generate safer OpenClaw configuration baselines and audit existing config files for exposure, missing controls, and secret hygiene issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike007jd](https://clawhub.ai/user/mike007jd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate reviewable OpenClaw JSON baseline configurations and audit existing OpenClaw-style configuration files before rollout or after change review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit output can reveal sensitive configuration paths or secret-like value locations. <br>
Mitigation: Run audits only on configurations intended for review and keep audit reports private. <br>
Risk: Generated baselines are starter configurations and do not enforce runtime policy. <br>
Mitigation: Review generated JSON before replacing production configuration and pair it with normal deployment controls. <br>
Risk: The tool reads and writes local configuration files as part of its normal workflow. <br>
Mitigation: Use explicit input and output paths in a controlled workspace. <br>


## Reference(s): <br>
- [Baseline Kit ClawHub Release Page](https://clawhub.ai/mike007jd/baseline-kit) <br>
- [Baseline Kit README](README.md) <br>
- [Baseline Kit Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples; generated artifacts are JSON configuration files and JSON or table audit reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; reads and writes local OpenClaw configuration JSON files] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
