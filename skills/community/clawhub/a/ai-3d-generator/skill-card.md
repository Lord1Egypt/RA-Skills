## Description: <br>
Generates detailed parametric 3D models from text descriptions by guiding an agent to produce and run Python/Trimesh code that exports STL files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vonzellu](https://clawhub.ai/user/vonzellu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, makers, and 3D-printing workflows use this skill to turn natural-language model descriptions into Python/Trimesh generation scripts and STL exports. It is intended for prompt-driven creation of parametric objects such as robots, architecture, vehicles, and mechanical forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill is purpose-built for text-to-STL generation, but it asks agents to generate and run local Python code from prompts without enough safety boundaries. <br>
Mitigation: Install only if you are comfortable reviewing or sandboxing generated Python before it runs. Use a disposable workspace or container, restrict output filenames to simple basenames, avoid enabling the cron example unless you intentionally want recurring generation, and verify the hardcoded virtualenv and dependencies before running the scripts. <br>
Risk: The artifact includes hardcoded local paths for virtual environments and STL export locations. <br>
Mitigation: Review and adjust paths in a disposable workspace or container before running generation scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vonzellu/ai-3d-generator) <br>
- [Publisher profile](https://clawhub.ai/user/vonzellu) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with Python and bash examples; generated Python scripts and STL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python/Trimesh workflows and may execute generated code to create STL exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
