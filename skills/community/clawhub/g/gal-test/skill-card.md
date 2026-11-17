## Description:

AI image generation, editing, background removal, upscaling, restyling, and product visual workflows through Bria.ai APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levdavid1](https://clawhub.ai/user/levdavid1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to produce image assets, transparent cutouts, image edits, product photos, and batch visual workflows through Bria.ai endpoints. It is intended for external visual content creation tasks where prompts and selected images can be sent to Bria.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected images and prompts to Bria.ai.

Mitigation: Avoid sensitive images and prompts unless Bria.ai data handling is acceptable for the intended use.

Risk: The skill handles reusable Bria credentials and may cache them under ~/.bria/credentials.

Mitigation: Store credentials only on private machines and prefer a secure secret store or tightly permissioned credential file.

Risk: The security review warns against environments where BRIA_API_BASE or response URLs could be influenced by untrusted code.

Mitigation: Run the skill only in trusted environments and review endpoint configuration before making API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/levdavid1/skills/gal-test)
- [Publisher profile](https://clawhub.ai/user/levdavid1)
- [Bria.ai homepage](https://bria.ai)
- [Bria agent API documentation](https://docs.bria.ai/llms.txt)
- [API Endpoints Reference](references/api-endpoints.md)
- [Shell Client](references/code-examples/bria_client.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Bria.ai result URLs and local credential setup instructions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
