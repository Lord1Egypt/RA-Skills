## Description: <br>
Checks OpenClaw and ClawHub skills against Agora Sentinel trust data for malware, prompt injection, data theft, dangerous permissions, and related security risks before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Folvindine](https://clawhub.ai/user/Folvindine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check ClawHub skill trust scores before installing new skills and to audit installed OpenClaw skills for security concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled checker scripts may execute local commands if a malicious or compromised API response is interpolated into Python source. <br>
Mitigation: Review or patch the JSON parsing so API responses are passed as data, not executable Python source, before relying on the scripts. <br>
Risk: Skill checks disclose queried skill slugs to checksafe.dev. <br>
Mitigation: Use the skill only when sharing checked skill names with that service is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Folvindine/agora-sentinel) <br>
- [Agora Sentinel homepage](https://checksafe.dev) <br>
- [Agora Sentinel dashboard](https://checksafe.dev/dashboard/) <br>
- [Badge API endpoint](https://checksafe.dev/api/v1/skills/{slug}/badge.json) <br>
- [Full report API endpoint](https://checksafe.dev/api/v1/skills/{slug}/report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal-style security reports; direct API calls return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries public checksafe.dev endpoints by skill slug; no API key or account is required.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
