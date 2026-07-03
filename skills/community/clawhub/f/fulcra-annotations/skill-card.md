## Description: <br>
Fulcra Annotations lets an agent create, list, update, delete, record, and verify Fulcra annotation definitions and events through the Fulcra Life API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use this skill when a user wants an agent to set up reusable Fulcra annotation definitions, log approved moment, boolean, numeric, or scale annotation records, inspect annotation identifiers, or build a workflow that writes and verifies Fulcra annotations. <br>

### Deployment Geography for Use: <br>
Global, subject to Fulcra account availability, network access to https://api.fulcradynamics.com, and the user's local privacy and compliance requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Annotation values and notes may become persistent personal data in the user's Fulcra account. <br>
Mitigation: Install only for user-directed Fulcra annotation work, review write prompts before approval, and avoid real private data in public demos. <br>
Risk: Deletion or changes to existing annotation definitions could alter a user's tracking setup. <br>
Mitigation: Ask for explicit user approval before update or delete operations and use dry-run mode before risky writes. <br>
Risk: Fulcra credentials or private records could be exposed through chat or logs if handled carelessly. <br>
Mitigation: Do not print tokens, credential files, direct capability URLs, or raw private records; use the trusted CLI or secret-manager token flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arc-claw-bot/skills/fulcra-annotations) <br>
- [Fulcra API OpenAPI document](https://api.fulcradynamics.com/openapi.json) <br>
- [Publisher profile](https://clawhub.ai/user/arc-claw-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Agent guidance plus JSON-producing command-line helper operations for Fulcra annotation definitions and records.] <br>
**Output Parameters:** [Annotation type, name or ID, value when required, note, tags, timestamps, source metadata, dry-run mode, and Fulcra authentication environment settings.] <br>
**Other Properties Related to Output:** [The bundled helper uses Python and uv, pins authenticated API calls to the Fulcra API host, supports dry-run writes, and treats a write as confirmed only after readback verification.] <br>

## Skill Version(s): <br>
1.0.13 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
