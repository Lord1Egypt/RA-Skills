## Description: <br>
Extract design primitives from a public website and generate starter token files for your project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arvindrk](https://clawhub.ai/user/arvindrk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to inspect a public website's visual primitives and initialize local design-token files for a project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run npx tooling and install Chromium before extracting design data from a public website. <br>
Mitigation: Use it only with public websites and review the command intent before execution. <br>
Risk: Extracted website data and generated token files may be incomplete or unsuitable for direct use. <br>
Mitigation: Review .extract-design-system and design-system outputs before applying them, and explicitly approve changes to existing app code or styling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arvindrk/extract-design-system) <br>
- [Workflow](artifact/references/workflow.md) <br>
- [Outputs](artifact/references/outputs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated JSON and CSS token files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are starter design-token artifacts for review before integration.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
