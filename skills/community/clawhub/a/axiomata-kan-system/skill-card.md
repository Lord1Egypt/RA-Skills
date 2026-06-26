## Description: <br>
Axioma KAN System helps OpenClaw agents create KAN concepts, train PyTorch KAN models, assemble KAN pipelines, integrate temporal memory, monitor KAN health, and manage auto-evolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage the lifecycle of Kolmogorov-Arnold Network components for OpenClaw-style agent systems, including creation, training, pipeline assembly, health checks, and retraining recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Training and creation scripts can write or overwrite generated model artifacts and related files in local agent directories. <br>
Mitigation: Run the skill only in a disposable or purpose-built Axioma-style environment, and inspect target paths before creating concepts, training individual KANs, or using train-all workflows. <br>
Risk: The skill documentation includes admin-style operations such as sudo, service, cron, and auto-evolution guidance. <br>
Mitigation: Do not run sudo, service, cron, training, or auto-evolution commands until the paths, services, and expected file changes have been reviewed. <br>
Risk: Hard-coded model locations may not match the current workstation and may affect valuable existing model files if reused unchanged. <br>
Mitigation: Adjust model directories for the intended environment and keep backups of existing model artifacts before executing bundled scripts. <br>


## Reference(s): <br>
- [Axioma KAN System ClawHub release](https://clawhub.ai/kofna3369/axiomata-kan-system) <br>
- [kofna3369 ClawHub publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; bundled scripts can generate JSON configuration files, Python model/training files, model artifacts, and console health reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts may create or overwrite KAN directories, pipeline JSON, and PyTorch model files on local disk.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
