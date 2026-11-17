## Description:

Converts single images or folders of local JPG, PNG, and WEBP product photos into e-commerce descriptions with Grok Vision AI using XAI_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and developers use this skill to generate product listing copy from local product photos, either one image at a time or in batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen local files are sent to xAI for processing, and the security evidence notes that any readable local file path may be uploaded if selected.

Mitigation: Run the skill only against intended product image files, avoid untrusted paths or broad folders, and keep it away from directories that may contain credentials, documents, or source code secrets.

Risk: The security evidence notes missing extension validation, symlink rejection, image-content checks, and size limits.

Mitigation: Review selected files before execution and use bounded product-image folders until stricter validation and file-size controls are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loutai0307-prog/skills/ai-product-description-from-image)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text product descriptions printed to stdout, with shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-image and folder batch workflows with style and language options.]

## Skill Version(s):

2.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
