## Description: <br>
Design and simulate adaptive clinical trials with interim analyses, sample size re-estimation, and early stopping rules, evaluating Type I error control, power, and expected sample size via Monte Carlo simulation before trial initiation. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, clinical trial designers, and biostatistics reviewers use this skill to configure and run local simulations of adaptive clinical-trial designs before trial initiation. It supports planning analyses for interim looks, sample-size re-estimation, early stopping, and operating-characteristic review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulation outputs can be mistaken for validated clinical-trial decisions. <br>
Mitigation: Treat outputs as research support only and require review by qualified biostatistics and regulatory experts before using them for clinical-trial decisions. <br>
Risk: Dependency versions can affect numerical behavior or security posture. <br>
Mitigation: Install in an isolated Python environment and pin and review NumPy, SciPy, and Matplotlib versions before serious use. <br>
Risk: The configured output path may overwrite existing files. <br>
Mitigation: Choose output paths deliberately and review generated files before relying on them. <br>


## Reference(s): <br>
- [Adaptive Trial Simulator on ClawHub](https://clawhub.ai/AIPOCH-AI/adaptive-trial-simulator) <br>
- [AIPOCH-AI publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON simulation result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write simulation results to a user-selected output path and may generate charts when visualization is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
