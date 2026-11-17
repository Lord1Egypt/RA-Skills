## Description:

Turns a written civil-affairs materials list into 8 to 20 labeled voice clips, one per cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Civil-affairs office staff and their agents use this skill to turn an existing materials checklist into short, labeled instruction clips for marriage, birth, household, appointment, and related service cues. It supports a free slot plan before any paid voice cloning or speech generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a shared Beatra device authorization with broad account powers, including paid account actions.

Mitigation: Install only when that account-level access is acceptable, keep the device token private, and use the documented revoke or reauthorization flow when access should change.

Risk: Automatic updates are enabled by default and can replace package-owned code before ordinary commands.

Mitigation: Review the package before use and disable silent update checks with `python3 scripts/mcp_client.py update --auto off` when fixed local code is required.

Risk: Voice cloning can misuse a staff likeness if a sample is available but not authorized.

Mitigation: Proceed with cloning only after explicit likeness and voice rights are confirmed, and inspect the authorized sample before upload.

Risk: Paid clone or speech generation can be duplicated during retries or transport uncertainty.

Mitigation: Use one opaque `client_request_id` per paid request, poll existing tasks, and retry only byte-identical arguments with the same request identity.

Risk: Civil-affairs instruction clips could be mistaken for eligibility, approval, grant, or document decisions.

Mitigation: Read only the supplied materials list and explicitly avoid adding approvals, eligibility results, grants, or document claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/beatra-ai/skills/civil-affairs-voice)
- [Beatra Skill Homepage](https://beatra.ai/skills/civil-affairs-voice)
- [Civil affairs voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; generated Beatra tasks can return MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans a labeled slot list before paid work, then can guide one speech generation request per slot and optional voice cloning with task polling and billing reporting.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
