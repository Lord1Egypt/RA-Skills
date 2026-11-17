## Description:

Turns a written elder-checkup schedule into 8 to 20 labeled voice clips, one spoken notice per schedule cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External community-office staff and their agents use this skill to convert an already-written elder-checkup schedule into labeled spoken notice clips while avoiding medical advice or invented details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests broad shared Beatra device authorization.

Mitigation: Install only on an approved Beatra account, review account permissions and billing controls before use, and disconnect through the bundled uninstall flow when access is no longer needed.

Risk: Silent package updates are enabled by default.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` or run a manual update check before use.

Risk: Paid speech generation or voice cloning can spend Beatra credits, and unsafe retries can duplicate work.

Mitigation: Confirm live pricing before paid calls, use one opaque `client_request_id` per request, and retry only byte-identical arguments with the same request identity.

Risk: Voice cloning can involve a person's likeness.

Mitigation: Clone only with explicit voice rights, inspect the authorized sample first, and upload local samples only through the bundled client.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/elder-checkup-voice)
- [Elder checkup voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with labeled lists, JSON payload examples, shell commands, and returned audio file artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans are free until the user approves paid clone or speech generation; final charges come from returned Beatra task billing fields.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
