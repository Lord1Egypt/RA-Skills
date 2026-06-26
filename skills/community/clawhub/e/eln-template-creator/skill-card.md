## Description: <br>
Generate standardized experiment templates for Electronic Laboratory Notebooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Laboratory staff, researchers, and developers use this skill to generate structured Markdown experiment-record templates for ELN workflows across general, molecular biology, chemistry, cell culture, and animal-study experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated Markdown to a user-selected output path and could overwrite an important file if that path is chosen carelessly. <br>
Mitigation: Run it from a trusted workspace and choose the output path deliberately before writing generated templates. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/AIPOCH-AI/eln-template-creator) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown templates written to stdout or a selected output file, with shell-command usage examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports template type, output path, title, researcher, date, and project parameters; no additional Python packages are required.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
