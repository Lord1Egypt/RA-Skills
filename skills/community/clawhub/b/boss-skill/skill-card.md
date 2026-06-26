## Description: <br>
Boss orchestrates a BMAD-style software delivery workflow that coordinates product, architecture, design, development, QA, and DevOps agents from requirements through optional deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoVic](https://clawhub.ai/user/echoVic) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan and execute new projects or feature work through a structured Chinese-language workflow that produces requirements, architecture, UI, task, QA, and deployment artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad project and environment changes as part of an automated coding and deployment workflow. <br>
Mitigation: Run it in a clean branch or sandbox and review proposed file, dependency, service, and deployment changes before allowing them to affect production work. <br>
Risk: The --quick mode can skip confirmation points in the workflow. <br>
Mitigation: Avoid --quick for important projects and require explicit review before dependency installs, Docker or service startup, global package installs, or production-affecting commands. <br>
Risk: Deployment steps may affect live services or external infrastructure. <br>
Mitigation: Use --skip-deploy unless deployment is explicitly intended and approved for the target environment. <br>


## Reference(s): <br>
- [Boss Skill README](README.md) <br>
- [Boss Skill Design](DESIGN.md) <br>
- [BMAD Methodology](references/bmad-methodology.md) <br>
- [Artifact Guide](references/artifact-guide.md) <br>
- [Testing Standards](references/testing-standards.md) <br>
- [Quality Gate](references/quality-gate.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chinese-language Markdown artifacts, code changes, shell commands, configuration files, and final delivery summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files and .boss/<feature>/ delivery artifacts; deployment output is optional and controlled by skill arguments.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
