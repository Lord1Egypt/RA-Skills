## Description: <br>
A lightweight API mock server for prototyping and testing HTTP APIs with static or dynamic JSON responses, JSON Schema validation, generated test data, and latency simulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to stand up local mock REST endpoints for frontend-backend decoupling, automated tests, and rapid API prototyping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the mock server on a non-loopback host can expose test endpoints to other machines. <br>
Mitigation: Run with --host 127.0.0.1 unless shared network access is deliberate. <br>
Risk: Unpinned dependencies can change behavior in CI or shared-team environments. <br>
Mitigation: Install in a virtual environment and pin or lock dependencies before repeatable use. <br>
Risk: Webhook simulation is described in the release materials, but the security guidance says not to assume it exists in this version. <br>
Mitigation: Review or add webhook simulation behavior before relying on that feature. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/api-mock-server) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local server commands, mock route definitions, JSON configuration, and request validation examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
