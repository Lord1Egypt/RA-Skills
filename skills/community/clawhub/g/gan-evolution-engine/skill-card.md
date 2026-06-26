## Description: <br>
GAN Evolution Engine uses a GAN-like loop to generate, evaluate, select, and save evolved variants of AI agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sudabg](https://clawhub.ai/user/sudabg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evolve target agent skills by generating candidate variants, benchmarking fitness, selecting elite variants, and optionally publishing evolution results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill directly executes generated or target-skill code on the host. <br>
Mitigation: Run it only in an isolated workspace or container, review generated variants before use, and avoid mounting sensitive files or secrets. <br>
Risk: The security evidence says the skill reads local credential files and may send target skill code to OpenRouter. <br>
Mitigation: Do not use it on proprietary or secret-bearing skills unless that disclosure path is acceptable, and review OpenRouter and EvoMap credential paths before enabling publishing. <br>


## Reference(s): <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Manifest](artifact/manifest.json) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/sudabg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown skill variants, JSON evolution history, benchmark results, and optional shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces evolved skill directories and may invoke OpenRouter and EvoMap workflows when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
