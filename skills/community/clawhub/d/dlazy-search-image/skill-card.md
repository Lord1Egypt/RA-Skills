## Description:

Image search tool: queries Pixabay image API by keywords and returns image URLs and metadata for references, backgrounds, and design assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search Pixabay by keyword to find image URLs and metadata for reference images, backgrounds, and design assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan did not inspect the external dLazy CLI or establish that its commands perform the stated Pixabay search; the documented workflow also requires dLazy authentication.

Mitigation: Before use, decide whether you trust dLazy, review the CLI behavior, configure authentication, and confirm that returned results suit the intended search.

## Reference(s):

- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [JSON, Image URLs, Image metadata]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results contain image URLs and metadata; the skill also documents optional saving of a result asset to a local path.]

## Skill Version(s):

1.3.42 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
