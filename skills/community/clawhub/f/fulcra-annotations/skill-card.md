## Description: <br>
Create, list, update, and record Fulcra annotations through the Fulcra Life API for agent workflows that write user-approved annotation events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create Fulcra annotation definitions, record moment, boolean, numeric, and scale annotation events, and verify writes through readback. It is intended for workflows that need authenticated, user-approved writes to a Fulcra account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has an under-disclosed endpoint override that could redirect Fulcra access tokens and annotation data. <br>
Mitigation: Install only in trusted runtimes, avoid setting FULCRA_API_BASE unless intentionally targeting a controlled server, and keep FULCRA_CLI_COMMAND restricted to the real Fulcra CLI. <br>
Risk: The skill can create, update, delete, and record data in a Fulcra account. <br>
Mitigation: Review each create, update, delete, or record action before it writes account data; use dry-run for risky writes and require readback verification before treating records as confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arc-claw-bot/fulcra-annotations) <br>
- [README.md](artifact/README.md) <br>
- [Fulcra Annotation API Notes](artifact/references/api-notes.md) <br>
- [Fulcra OpenAPI document](https://api.fulcradynamics.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes require Fulcra authentication; record commands should be treated as confirmed only after readback reports verified_matches >= 1.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
