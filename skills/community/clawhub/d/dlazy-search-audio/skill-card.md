## Description:

Searches Pixabay Music and returns royalty-free track URLs and metadata for background music selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators can search for background music by entering 2–3 short English style keywords, then review the matching tracks' URLs and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial. Its guidance notes that the CLI authentication commands did not match the stated music-search purpose, and the package was not independently inspected.

Mitigation: Before installing or authenticating, review the pinned @dlazy/cli package and its referenced materials. Use a scoped API key and rotate or revoke it if needed.

## Reference(s):

- [dLazy CLI project page (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON search results with track URLs and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill recommends 2–3 short English style keywords; the CLI defaults to 10 results per page.]

## Skill Version(s):

1.3.42 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
