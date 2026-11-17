## Description:

Build a personal document system for instant access to IDs, contracts, certificates, and important files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to help an agent catalog sensitive personal documents, track expiry dates, and locate local references to important files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to maintain a persistent local index of sensitive identity, financial, medical, and legal document metadata.

Mitigation: Use a private encrypted location, restrict file permissions, and avoid synced or shared folders unless access controls are clear.

Risk: Document entries could expose full IDs, account numbers, policy numbers, or other sensitive values in plain text.

Mitigation: Store sensitive numbers as references only and keep full values in an appropriate secure store.

Risk: Stale document metadata may cause incorrect expiry or renewal reminders.

Mitigation: Review and update the local index after renewals, replacements, and newly received documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/documents)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown guidance with suggested local file structures and document-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of a persistent local document index containing sensitive personal metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
