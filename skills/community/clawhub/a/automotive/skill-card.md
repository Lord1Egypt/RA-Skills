## Description:

Automotive helps agents create and edit vehicle images with Bria.ai endpoints for scene generation, reflections, tire refinement, segmentation, atmospheric effects, and lighting harmonization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and creative teams use this skill to produce automotive marketing, dealership, configurator, catalog, and social media imagery from vehicle photos or image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Bria account credentials and can cache API tokens in ~/.bria/credentials.

Mitigation: Install only for trusted users, restrict ~/.bria permissions, and review token storage before using the skill in shared environments.

Risk: Vehicle images or image URLs are uploaded to Bria API endpoints during normal workflows.

Mitigation: Avoid sensitive, confidential, or internal vehicle images unless the intended Bria account and data handling terms are acceptable.

Risk: The helper performs HTTPS API calls using the configured Bria base URL and API token.

Mitigation: Keep the default trusted Bria HTTPS endpoint or review any BRIA_API_BASE override before execution.

## Reference(s):

- [API Endpoints Reference](references/api-endpoints.md)
- [Shell Client](references/code-examples/bria_client.sh)
- [Bria automotive docs](https://docs.bria.ai/product-shot-editing/automotive-endpoints)
- [ClawHub skill page](https://clawhub.ai/galbria/skills/automotive)
- [Publisher profile](https://clawhub.ai/user/galbria)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, and API response URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or download edited vehicle image files when the agent runs the documented API workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
