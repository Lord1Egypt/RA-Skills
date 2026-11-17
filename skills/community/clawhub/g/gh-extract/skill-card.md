## Description:

Extract content from a GitHub url.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch content from public GitHub repository, tree, or blob URLs, printing text to stdout or saving a fetched file when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill can fetch and save content from arbitrary URLs, which is broader than users would expect for a GitHub extraction tool.

Mitigation: Review before installing, use only trusted public GitHub URLs, and avoid arbitrary URLs or --save until the skill enforces a GitHub-only allowlist, validates redirects, adds timeouts and size limits, and removes the original-URL fallback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guoqiao/skills/gh-extract)
- [ClawHub Homepage](https://clawhub.ai/guoqiao/gh-extract)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Plain text content, temporary file paths, and Markdown usage guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and wget; supports public GitHub repository, tree, and blob URLs.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
