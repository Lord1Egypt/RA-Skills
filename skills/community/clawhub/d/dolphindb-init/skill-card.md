## Description: <br>
Initializes a DolphinDB Python environment by finding an existing DolphinDB SDK installation or installing the SDK into an available Python environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before DolphinDB operations to locate or prepare a Python interpreter with the DolphinDB SDK, then call DolphinDB scripts through a consistent shell interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install an unpinned DolphinDB Python package. <br>
Mitigation: Run it in a dedicated virtual or conda environment and pin the DolphinDB package version when reproducibility or supply-chain control is required. <br>
Risk: The loader evaluates generated shell exports while selecting a Python interpreter. <br>
Mitigation: Review the target interpreter and generated environment values before sourcing the loader in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/dolphindb-init) <br>
- [Source skill definition](artifact/SKILL.md) <br>
- [Environment loader script](artifact/scripts/load_dolphindb_env.sh) <br>
- [Environment detection script](artifact/scripts/detect_dolphindb_env.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides shell functions and environment variables for selecting the DolphinDB Python interpreter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
