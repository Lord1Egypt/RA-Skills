## Description:

Helps agents create Remotion-based video advertisements in 15-, 30-, or 60-second formats with scene-based storytelling and render or preview commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to produce structured Remotion video ad compositions for digital advertising. It helps plan ad duration, scene timing, React components, composition registration, and render or preview commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx commands can resolve a different Remotion package version at runtime.

Mitigation: Use a project package.json and lockfile, run npm ci, and invoke a pinned local Remotion binary.

## Reference(s):

- [Ad Format Specifications](references/formats.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TSX code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Remotion composition guidance for 15s, 30s, and 60s landscape ads at 60fps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
