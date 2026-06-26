## Description: <br>
Create or refactor code for solving HJB equations with this repository's TensorFlow DGM framework. Use when users ask to generate new HJB training code, add a new problem (config/problem/loss/train script), adapt sampling/training hyperparameters, or create plotting/analysis code from trainer CSV outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Reedcgx](https://clawhub.ai/user/Reedcgx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold and adapt TensorFlow DGM projects for Hamilton-Jacobi-Bellman equation experiments, including configs, problem definitions, losses, training scripts, and plotting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes HJB solver project files and can introduce incorrect PDE residuals, terminal conditions, or training parameters if the generated TODO sections are used without review. <br>
Mitigation: Use a clear snake_case problem slug, work in a clean or version-controlled workspace, and review generated problem, loss, config, and training files before running training. <br>
Risk: Training requires installing Python dependencies and executing generated TensorFlow code. <br>
Mitigation: Review requirements.txt and generated scripts before installing dependencies or running training, and run the workflow in an isolated environment. <br>


## Reference(s): <br>
- [Repository Conventions](references/repo-conventions.md) <br>
- [Training Output Contract](references/training-output-contract.md) <br>
- [ClawHub skill page](https://clawhub.ai/Reedcgx/deep-hjb-solver-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash and Python code blocks plus generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HJB projects are organized under a problem slug and may include TensorFlow source files, requirements, training examples, CSV outputs, plots, and saved model weights.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
