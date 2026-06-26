## Description: <br>
Standardizes bioinformatics analyses by guiding agents to create reproducible shell-scripted workflows, use established sequencing and enrichment tools, and report results with R Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bioinformatics practitioners and data analysts use this skill to plan and execute sequencing-data workflows such as QC, alignment, quantification, differential analysis, enrichment analysis, and visualization. It emphasizes established tools, scripted steps, organized logs, and reproducible reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated shell scripts, R Markdown, and Conda or Mamba commands can execute local tools and create or update analysis outputs. <br>
Mitigation: Review generated commands before execution, run them in an isolated project directory or environment, and keep raw data read-only. <br>
Risk: Workflow commands may be unsuitable for valuable data or shared systems if paths, environments, or resource assumptions are wrong. <br>
Mitigation: Validate paths, sample metadata, tool versions, and compute settings before running the workflow on important datasets or shared infrastructure. <br>


## Reference(s): <br>
- [Bioinfo Style on ClawHub](https://clawhub.ai/biociao/bioinfo-style) <br>
- [Common bioinformatics tools quick reference](references/tools.md) <br>
- [Analysis script templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell script and R Markdown examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates reproducible workflow steps, command templates, logs, directory structures, and report guidance for local bioinformatics analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
