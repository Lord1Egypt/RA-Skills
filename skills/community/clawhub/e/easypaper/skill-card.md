## Description: <br>
Generate structured academic papers from metadata using the EasyPaper Python SDK and related repository workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PinkGranite](https://clawhub.ai/user/PinkGranite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research authors use this skill to set up EasyPaper, prepare paper metadata, invoke SDK generation, and locate the final PDF artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing confidential research may use an HTTP Typesetter endpoint if local compilation is unavailable. <br>
Mitigation: Confirm whether EasyPaper runs locally or through an endpoint you control before processing confidential material. <br>
Risk: The workflow depends on third-party Python, LaTeX, and PDF tooling installed in the agent environment. <br>
Mitigation: Install EasyPaper in an isolated Python environment and review the EasyPaper package and linked repository before use. <br>


## Reference(s): <br>
- [EasyPaper Repository](https://github.com/PinkGranite/EasyPaper) <br>
- [EasyPaper Agent Plugin](https://github.com/PinkGranite/EasyPaper/tree/master/plugins/easypaper) <br>
- [End-to-End EasyPaper Command](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/commands/easypaper.md) <br>
- [Paper From Metadata Workflow](https://github.com/PinkGranite/EasyPaper/blob/master/plugins/easypaper/skills/paper-from-metadata/SKILL.md) <br>
- [Metadata Example](https://github.com/PinkGranite/EasyPaper/blob/master/examples/meta.json) <br>
- [Configuration Template](https://github.com/PinkGranite/EasyPaper/blob/master/configs/example.yaml) <br>
- [EasyPaper README](https://github.com/PinkGranite/EasyPaper/blob/master/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report generated PDF paths, status details, word counts, or compile errors.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
