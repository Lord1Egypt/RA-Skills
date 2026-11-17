## Description:

Automatically switches Git branches and runs an app packaging script with branch, platform, build type, version, upload, API key, and release note options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heigher](https://clawhub.ai/user/heigher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to package Android and iOS apps from a local repository, optionally switching branches, selecting build variants, and uploading build artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pgyer API keys may be exposed in chat or result messages.

Mitigation: Use a secure secret source where possible, avoid pasting API keys into chat, and mask keys in any progress or result output.

Risk: The skill can mutate the local Git repository by fetching, checking out branches, and pulling changes before packaging.

Mitigation: Run only in the intended repository, require a clean working tree, and ask for explicit confirmation before branch switching, fetching, pulling, building, or uploading.

Risk: Upload-enabled builds may publish artifacts to Pgyer.

Mitigation: Confirm the upload choice, destination, version, release notes, and credentials before starting the packaging workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Markdown status and result messages with inline shell commands and generated artifact paths or links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report generated APK or IPA files and Pgyer download links when upload is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
