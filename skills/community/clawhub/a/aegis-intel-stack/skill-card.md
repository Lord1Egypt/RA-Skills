## Description: <br>
Provides utility micro-skills for EVM gas snapshots, transaction explanation, health checks, intel manifests, and delta update workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kankinku](https://clawhub.ai/user/kankinku) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run or call a local Aegis utility stack for EVM gas, transaction, manifest, and delta update analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to install dependencies, copy environment configuration, build code, and run a local Node.js service from an external aegis-suite checkout that is not included in the reviewed artifact. <br>
Mitigation: Review package.json, lockfiles, npm scripts, environment requirements, and the local server implementation before running the commands, and execute them only in a trusted project. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kankinku/aegis-intel-stack) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local run commands, API call examples, and generated documentation output paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
