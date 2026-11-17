## Description:

Quark Scan image and document processing skill that helps agents use `yescan` for OCR, image translation and enhancement, conversion to Word/Excel/PDF, and ID photo generation from user-provided images or URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yescan-ai](https://clawhub.ai/user/yescan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process user-selected image or document inputs through Quark Scan for OCR extraction, image cleanup, document conversion, and generated ID photos. It is intended for cases where the user has explicitly provided a local image path or HTTP(S) URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or documents are sent to Quark Scan for processing and may contain sensitive or personal information.

Mitigation: Use the skill only when the user explicitly provides the image path or URL and accepts that the content will be processed by Quark Scan.

Risk: The skill requires a `SCAN_WEBSERVICE_KEY` credential for Quark Scan API access.

Mitigation: Store the key only in a trusted account or environment, avoid exposing configuration files in screenshots or logs, and rotate the key if compromise is suspected.

Risk: The workflow can install or upgrade the `yescan` CLI without a pinned package version.

Mitigation: Prefer an isolated virtual environment and pin or review the `yescan` version before use in sensitive environments.

Risk: Generated image and document files may remain in temp directories after processing.

Mitigation: Clean local temp output directories such as `/tmp/imgs/` and `/tmp/documents/` after handling sensitive content.

## Reference(s):

- [Quark Scan Open Platform](https://scan.quark.cn/business)
- [ClawHub Skill Page](https://clawhub.ai/yescan-ai/skills/alibaba-quark-scanking-all)
- [Security Policy](artifact/SECURITY.md)
- [Privacy, Data Flow, and Key Security](artifact/references/privacy.md)
- [Implementation Details](artifact/references/implementation.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON CLI responses, OCR text, and local output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `yescan` CLI, a configured `SCAN_WEBSERVICE_KEY`, runtime scene discovery, and user-provided image path or URL input; generated image and document outputs may be written to local temp directories or a caller-specified output directory.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
