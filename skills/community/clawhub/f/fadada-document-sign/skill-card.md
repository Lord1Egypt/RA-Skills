## Description:

Fadada Document Sign helps an agent manage the Fadada FASC API 5.0 e-signature lifecycle, including contract upload, signature initiation, template lookup, task query, cancellation, and signed-contract download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fadada-esign](https://clawhub.ai/user/fadada-esign)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route contract-signing requests through Fadada, collect signer information, start or monitor e-signature tasks, cancel eligible tasks, and retrieve completed contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports production-looking Fadada credentials and a suspicious security verdict.

Mitigation: Rotate or verify that the published credentials are not real, avoid production credentials until resolved, and restrict the Fadada API app to least privilege.

Risk: Signing, upload, download, and local contract handling can expose sensitive contract links or files.

Mitigation: Treat logs, links, and downloaded contracts as sensitive; limit access, use controlled save paths, and avoid sharing generated URLs.

Risk: Production signing submission and cancellation actions can affect real contract workflows.

Mitigation: Require explicit human confirmation before creating production signing tasks, cancelling tasks, or downloading signed contracts.

## Reference(s):

- [FASC API 5.0 Reference](artifact/references/FASC_API_Reference.md)
- [Fadada API credential guide](https://dev.fadada.com/api-guide/YYNLQW2Z2W/9QMQ2MU4FGK3AOXA)
- [ClawHub skill page](https://clawhub.ai/fadada-esign/skills/fadada-document-sign)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell command examples, JSON card payloads, and file outputs for downloaded contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Fadada API operations that upload files, create or cancel signing tasks, query status, and download signed contracts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
