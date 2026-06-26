## Description: <br>
Manages A2A node secrets for EvoMap hub connectivity, including validation, rotation, and credential updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect, validate, and rotate EvoMap A2A node secrets when authentication fails or credentials need routine management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rotate and save real EvoMap node credentials. <br>
Mitigation: Install it only when credential management is intended, review validate and auto modes before use, and restrict permissions on saved secret files. <br>
Risk: Secret values can appear in returned objects or command output after rotation. <br>
Mitigation: Avoid sharing logs or responses that may include newSecret, and handle command output as sensitive credential material. <br>
Risk: A custom hub URL or storage path can change where credentials are sent or saved. <br>
Mitigation: Use only a trusted EVOMAP_HUB_URL and avoid arbitrary storage paths unless the target location is controlled and access-restricted. <br>


## Reference(s): <br>
- [A2a Secret Manager on ClawHub](https://clawhub.ai/jpengcheng523-netizen/a2a-secret-manager) <br>
- [EvoMap Hub](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples, plus JSON status and rotation results when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return secret status, validation outcome, saved path, and a new secret when rotation succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
