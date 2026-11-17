## Description:

WIME Creator helps agents call WIME OpenAPI workflows to remove image backgrounds and generate AI product photos from local image files or public image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxiaolong98](https://clawhub.ai/user/liuxiaolong98)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and ecommerce content teams use this skill to prepare product images, remove backgrounds, and generate AI product photography through WIME's API. The skill is intended for workflows where users provide local image files or public image URLs and receive generated image result URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided image files, image URLs, and prompts to WIME services.

Mitigation: Confirm the user trusts the publisher and WIME with the images and prompts before processing sensitive, private, unreleased, or regulated content.

Risk: Credential handling is loose enough that running the authentication helper directly can expose a real WIME access token.

Mitigation: Avoid invoking scripts/wime_auth.py with a real token until token redaction is fixed; keep WIME_ACCESS_TOKEN in environment or secret storage and do not print authentication structures.

Risk: Remote URL handling and image downloads can create security exposure if non-public or redirected targets are allowed.

Mitigation: Use only public http/https image URLs, reject localhost and private network targets, validate redirects, and prefer versions that limit downloads and use safe temporary files.

Risk: The security verdict is suspicious, with guidance to review before installation.

Mitigation: Review the publisher, endpoint configuration, remote URL behavior, and temporary file handling before deploying the skill in a production agent environment.

## Reference(s):

- [WIME OpenAPI Site](https://wime-ai.com/)
- [Image Upload API](references/upload-image.md)
- [Background Removal API](references/cutout.md)
- [Product Photo Generation API](references/photo-shoot.md)
- [Task Query API](references/asset-query.md)
- [Global Error Codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets, plus generated image result URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WIME_ACCESS_TOKEN; WIME_BASE_URL is optional and defaults to the production WIME endpoint.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
