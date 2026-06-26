## Description: <br>
Auto-create or reuse a Conda environment for Python projects by scanning dependency files, matching existing environments, and handling CUDA/GPU needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kazuya-ecnu](https://clawhub.ai/user/kazuya-ecnu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up isolated Conda environments for Python projects, reuse compatible existing environments, and install dependencies from common project files. It is especially useful for projects with conflicting Python versions, CUDA/GPU packages, or team environment standardization needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can execute project packaging logic or install untrusted packages. <br>
Mitigation: Review dependency files and run install commands only in an isolated environment you control. <br>
Risk: The skill creates or updates Conda environments and may install packages with pip or conda. <br>
Mitigation: Confirm the target project path, environment name, and proposed commands before execution; avoid modifying the base environment. <br>
Risk: PEP 668 fallback handling may propose pip's --break-system-packages option. <br>
Mitigation: Use that fallback only inside an isolated Conda environment after confirming it will not affect system-managed Python packages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kazuya-ecnu/auto-conda-env) <br>
- [PyTorch CUDA 11.8 wheel index](https://download.pytorch.org/whl/cu118) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and a final environment summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment name, Python version, installed dependencies, environment path, and activation command when setup completes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
