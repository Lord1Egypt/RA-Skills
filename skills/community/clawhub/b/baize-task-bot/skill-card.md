## Description: <br>
Baize Task Bot helps operators query outbound-call tasks, lines, scripts, and templates from local JSON data and perform approved write actions against the Baize outbound-call platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Richard-collab](https://clawhub.ai/user/Richard-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams using the Baize outbound-call platform use this skill to inspect task, line, script, and template state, parse natural-language operation requests into structured instructions, and execute confirmed task or account changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live authority to start outbound calls, change task execution, and create accounts. <br>
Mitigation: Require explicit human confirmation before every start, resume, concurrency, line, region, ratio, or account action. <br>
Risk: A broad BAIZE_TOKEN could allow unintended operational changes. <br>
Mitigation: Use a least-privilege BAIZE_TOKEN scoped to the specific Baize operations and accounts needed. <br>
Risk: Incorrect task or line identifiers could cause changes to the wrong outbound-call operation. <br>
Mitigation: Verify task and line IDs through query tools before approving writes. <br>
Risk: Sending operations to an unsafe endpoint could expose credentials or affect an unintended Baize environment. <br>
Mitigation: Keep BAIZE_BASE_URL local or HTTPS-only and confirm the target environment before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text status messages and JSON instruction arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated Baize API writes when action tools are invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
