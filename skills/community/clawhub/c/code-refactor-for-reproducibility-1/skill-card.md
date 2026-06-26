## Description: <br>
Use when refactoring research code for publication, adding documentation to existing analysis scripts, creating reproducible computational workflows, or preparing code for sharing with collaborators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research software engineers use this skill to refactor analysis scripts into reproducible, publication-ready workflows with clearer documentation, environment specifications, validation steps, and explicit assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated files and refactoring output may overwrite or expose local research project details if run directly in a working repository. <br>
Mitigation: Run the skill in a sandbox or disposable working directory, choose a fresh output directory, and review generated files before sharing. <br>
Risk: Environment setup may install dependencies that need project-specific review. <br>
Mitigation: Inspect requirements.txt and any generated environment files before installing dependencies. <br>
Risk: Generated reproducibility metadata may include hostname or package inventory. <br>
Mitigation: Review reproducibility_info.json before publishing or sharing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/code-refactor-for-reproducibility-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, and generated project files or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local files for reproducible project structure, environment setup, tests, documentation, and reproducibility metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
