## Description: <br>
Generate cryptographically secure random passwords with customizable character sets, controllable length, optional character exclusions, and no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate strong random passwords, API keys, or tokens with configurable length, count, and character sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan summary flags this release as suspicious because review tooling may run with broad local authority. <br>
Mitigation: Review before installing, prefer no-yolo review settings unless elevated authority is intentional, and run in a workspace without unrelated secrets. <br>
Risk: Disabling every character class can produce empty password values. <br>
Mitigation: Keep at least one character class enabled and check generated output before using it as a secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-password-generator-v2) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON object with generated passwords and length metadata; Markdown may include command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Password length, count, and included character classes are configurable.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
