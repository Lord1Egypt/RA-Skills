## Description: <br>
Use Chanjing customised person APIs to create, inspect, list, poll, and delete custom digital humans from uploaded source videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upload local source videos to Chanjing, create custom digital humans, inspect or list created persons, poll creation status, and delete resources that are no longer needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates local Chanjing credentials, including access tokens persisted in credentials.json. <br>
Mitigation: Keep ~/.chanjing/credentials.json private with restrictive permissions and do not commit it to version control. <br>
Risk: The skill uploads user-selected videos and can send callback results to a user-provided endpoint. <br>
Mitigation: Upload only videos intended for Chanjing and use --callback only with endpoints you control and trust. <br>
Risk: Delete commands can remove Chanjing customised person resources. <br>
Mitigation: Double-check person IDs before running delete_person.py or equivalent delete workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binkes/chanjing-customised-person) <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [Chanjing Open API login](https://www.chanjing.cc/openapi/login) <br>
- [Reference](reference.md) <br>
- [Examples](examples.md) <br>
- [Machine-readable manifest](manifest.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script outputs such as IDs, URLs, tab-separated summaries, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts use Python standard library only, read local Chanjing credentials, upload user-selected videos, and may persist refreshed access tokens to credentials.json.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
