## Description: <br>
CivilLabClaw AI helps civil engineering users route and perform machine-learning structural analysis, damage recognition, digital twin modeling, and monitoring data analysis tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Civil engineers, researchers, and developers use this skill to classify civil-engineering analysis requests and produce structural predictions, crack or damage findings, digital twin outputs, monitoring reports, and visualizations from user-provided images, models, or sensor data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process user-provided infrastructure images, models, and telemetry and write local analysis outputs. <br>
Mitigation: Use trusted inputs, avoid confidential infrastructure data unless local output handling is acceptable, and review the configured output directory before sharing results. <br>
Risk: Running analysis code and dependencies in a broad Python environment can increase operational exposure. <br>
Mitigation: Install and run the skill in a controlled Python environment and pin or lock dependencies before production use. <br>


## Reference(s): <br>
- [CivilLabClaw AI on ClawHub](https://clawhub.ai/jirboy/civillab-claw-ai) <br>
- [OpenSeesPy Documentation](https://openseespydoc.readthedocs.io/) <br>
- [PyTorch](https://pytorch.org/) <br>
- [Scikit-learn](https://scikit-learn.org/) <br>
- [SDNET2018](https://sdnet2018.github.io/) <br>
- [Crack500](https://github.com/leochan1117/Crack500) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON-style analysis summaries with optional generated files such as plots and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include configured report files, visualization files, confidence estimates, anomaly summaries, and raw-data references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
