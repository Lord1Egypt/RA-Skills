## Description:

Manage arkcli profiles, their API key lists, and default resources while keeping temporary credentials and endpoints out of persistent profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using arkcli use this skill to inspect and manage persistent profiles, profile API keys, and modality defaults, with checks for profile type and identity before changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile listing and detail queries may sync remote API keys and update the local key inventory or default; profile write commands change persistent settings.

Mitigation: Before profile queries, explain the possible sync and local updates; run these management actions only for explicit profile requests, and confirm the target profile before writes. Keep credentials private.

Risk: The security scan is partial because two referenced paths were missing, so related material was not fully assessed.

Mitigation: Restore and review the missing references before relying on guidance that depends on them.

## Reference(s):

- [Profile creation guide](references/arkcli-profile-create.md)
- [Profile API key guide](references/arkcli-profile-keys.md)
- [Set a profile default resource](references/arkcli-profile-set-default.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and checks tailored to the requested profile operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
