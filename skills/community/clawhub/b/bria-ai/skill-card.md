## Description:

Bria.ai image API skill that guides agents to authenticate, generate images from prompts, edit images with natural language, remove backgrounds, and create product lifestyle shots through Bria endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and marketing teams use this skill through an agent to generate, edit, upscale, restore, and remove backgrounds from images with Bria.ai for product, campaign, and design workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials are cached in ~/.bria/credentials and may be exposed on shared or sensitive machines.

Mitigation: Use the skill on user-controlled machines, lock down ~/.bria and ~/.bria/credentials to the current user, and rotate Bria credentials if they may have been stored with permissive permissions.

Risk: Local or remote images can be sent to Bria API endpoints during generation and editing workflows.

Mitigation: Use only non-confidential images unless the user's Bria terms and data-handling requirements permit uploading that content.

Risk: Environment overrides such as BRIA_AUTH_BASE or BRIA_API_BASE can redirect authentication or API calls unexpectedly.

Mitigation: Verify endpoint-related environment variables before use and avoid running the skill in untrusted shell environments.

## Reference(s):

- [Bria.ai Homepage](https://bria.ai)
- [Full API docs for agents](https://docs.bria.ai/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/galbria/skills/bria-ai)
- [Capabilities & Prompt Recipes](references/capabilities.md)
- [API Endpoints Reference](references/api-endpoints.md)
- [Shell Client](references/code-examples/bria_client.sh)
- [Auth Helper](references/code-examples/bria_auth.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and API result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bria authentication and may cache credentials in ~/.bria/credentials.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
