## Description:

Accidental ClawHub publish or leaked package files: scope, remove, and verify one affected version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and incident responders use this skill to contain, scope, remove, and verify a single ClawHub skill version that accidentally exposed unintended files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exact-version deletion is permanent and may remove the wrong release if the affected skill or version is misidentified.

Mitigation: Confirm the publisher identity, skill slug, affected version, latest version, and replacement status before approving deletion.

Risk: Registry exposure can be confused with Git, local cache, or conversation exposure.

Mitigation: Report registry exposure, Git exposure, local cache state, and conversation or log exposure as separate findings.

Risk: Exposed credentials, personal data, private communications, or copyrighted content may require response beyond package deletion.

Mitigation: Escalate sensitive exposed material for notification, cache purge, access review, credential rotation, or other required follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/accidental-registry-publication-response)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the exact skill slug and affected version before deletion guidance is applied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
