## Description: <br>
Knot Agent Editor helps authorized users inspect, regenerate, modify, and publish Knot platform agent draft configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or administrators with Knot agent management access use this skill to inspect agent drafts, list manageable agents and models, regenerate drafts, edit draft metadata, system prompts, and default models, and publish approved changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles JWT and API credentials while normal HTTPS certificate checks are disabled. <br>
Mitigation: Install only if the publisher is trusted, run it only in authorized environments, and prefer a version that enables TLS certificate validation or uses a trusted CA bundle before using real credentials. <br>
Risk: Regenerate, modify, and publish commands can make real remote changes to Knot agent drafts or production agent behavior. <br>
Mitigation: Confirm the target agent, review draft staleness and permissions, and require explicit user approval before running commands that overwrite drafts or publish changes. <br>


## Reference(s): <br>
- [Knot Agent Editor API Reference](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/editor1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live API calls require KNOT_JWT_TOKEN and KNOT_USERNAME.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
