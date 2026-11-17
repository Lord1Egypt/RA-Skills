## Description:

Call Cutout.Pro visual processing APIs to perform background removal, face cutout, and photo enhancement with either file upload or image URL input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutout-pro](https://clawhub.ai/user/cutout-pro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-processing agents use this skill to remove image backgrounds, cut out face or hair regions, enhance low-quality photos, and return processed images or Base64 result data through the Cutout.Pro API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, image URLs, portraits, identity documents, regulated data, private signed URLs, or internal-only assets may be sent to Cutout.Pro for processing.

Mitigation: Use only images and URLs the user is authorized to send to Cutout.Pro, and avoid sensitive or regulated inputs unless organizational approval covers that processing.

Risk: API key setup guidance may lead users to place CUTOUT_API_KEY in a local .env file without confirming repository ignore rules.

Mitigation: Prefer environment-variable or secrets-manager storage, keep CUTOUT_API_KEY out of source control, and add or verify a real .gitignore before creating a .env file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cutout-pro/skills/cutout-visual-api)
- [Cutout.Pro website](https://www.cutout.pro)
- [Cutout.Pro API key page](https://www.cutout.pro/user/secret-key)
- [Cutout.Pro error codes](https://www.cutout.pro/apidoc/error-code)
- [API Reference](references/api-reference.md)
- [Setup Guide](references/setup-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python CLI usage, JSON status output, binary image files, Base64 image data, and metadata JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processed image files are saved under data/outputs by default; URL mode and Base64 mode return JSON-compatible image data, and face cutout can include facial landmark data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
