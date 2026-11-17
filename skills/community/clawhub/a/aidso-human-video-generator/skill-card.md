## Description:

Extract text from reference videos or generate and track digital-human videos from user-provided copy through AIDSO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangyuanmile-coder](https://clawhub.ai/user/tangyuanmile-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users can bind their AIDSO account, extract a reference video's spoken copy, and generate a digital-human video from text they provide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe authorization-file handling could let another local user redirect account access or overwrite files.

Mitigation: Prefer a version that validates authorization-file ownership and save destinations. If proceeding, set AIDSO_CREDENTIALS_FILE inside an existing private, user-owned directory.

Risk: Content submitted for text extraction or video generation is shared with AIDSO.

Mitigation: Submit only content you intend to share with AIDSO.

Risk: Preview charges may differ from expectations.

Mitigation: Verify preview charges independently before use.

## Reference(s):

- [AIDSO API specification](artifact/references/api-spec.md)
- [ClawHub skill page](https://clawhub.ai/tangyuanmile-coder/skills/aidso-human-video-generator)
- [Publisher profile](https://clawhub.ai/user/tangyuanmile-coder)

## Skill Output:

**Output Type(s):** [Text, URLs, Task IDs, Guidance]

**Output Format:** [Text and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted video copy, generation task identifiers, and video or preview links.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
