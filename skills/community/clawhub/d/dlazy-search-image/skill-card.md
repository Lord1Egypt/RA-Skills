## Description:

The release describes this skill as querying the Pixabay image API by keyword and returning image URLs and metadata for references, backgrounds, and design assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and developers can use the release's image-search function to look for candidate image URLs and metadata by keyword for visual references, backgrounds, and design assets. Scanner evidence reports a mismatch between this stated purpose and the documented dLazy CLI authentication and invocation, so the advertised behavior remains unconfirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner evidence reports a mismatch between the stated Pixabay image-search purpose and the documented dLazy CLI authentication and invocation; the CLI package and some referenced files were not inspected.

Mitigation: Review the published CLI package and referenced files, and confirm the advertised search behavior before installing or relying on results.

Risk: The skill documentation says search prompts and parameters are sent to dLazy's hosted API.

Mitigation: Avoid sending confidential or sensitive query content unless the service's data handling terms are suitable for that content.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-search-image)
- [dLazy CLI repository listed in skill metadata](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [JSON, Image URLs, Image metadata]

**Output Format:** [JSON response containing image search results and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documented options include query, image type, orientation, page, results per page, and language; results can optionally be saved to a local path.]

## Skill Version(s):

1.3.45 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
