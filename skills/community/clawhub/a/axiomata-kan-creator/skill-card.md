## Description: <br>
Axiomata KAN Creator creates Python scaffolds, configuration, and command guidance for Kolmogorov-Arnold Network-style model concepts used in monitoring, evaluation, control, and agent-system pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold KAN-style model directories, configuration files, and PyTorch model code for agent monitoring, evaluation, validation, temporal, or research workflows. Users should validate the generated model behavior before relying on KAN, B-spline, or NaN-free claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated models may not match the advertised B-spline KAN behavior or NaN-free guarantees. <br>
Mitigation: Inspect the generated Python and independently validate training stability, architecture, and model behavior before use. <br>
Risk: The generator writes files and directories with limited path and overwrite controls. <br>
Mitigation: Run it only in a dedicated workspace, use simple slug-style names, and pass an explicit safe output directory. <br>
Risk: The release was flagged suspicious by the authoritative clawscan security summary. <br>
Mitigation: Review the artifact before installing or executing it and avoid relying on generated code in production without separate security and correctness checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiomata-kan-creator) <br>
- [KAN Creator Reference](artifact/references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance plus generated Python and JSON files produced by shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local model directories containing config.json, generated Python model code, data folders, and usage guidance; requires Python and PyTorch.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
