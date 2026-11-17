## Description:

AI UGC video production from the terminal using the `agent-media` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevo-david](https://clawhub.ai/user/nevo-david)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to guide agents through generating short UGC and SaaS review videos with the `agent-media` CLI, including script preparation, actor selection, B-roll screenshots, subtitles, and job management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI authenticates with an external service and may upload user-provided screenshots, face photos, voice samples, and video files.

Mitigation: Use a contained environment for installation and execution, and get explicit user permission before sending private or third-party media to the service.

Risk: The skill depends on an npm-distributed CLI package.

Mitigation: Verify the npm package before installation and review the package source or publisher details when supply-chain assurance is required.

Risk: Browsing product URLs or using third-party images can introduce privacy, copyright, or permission issues.

Mitigation: Ask the user before browsing product URLs or reusing third-party images, and prefer user-provided or clearly authorized assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nevo-david/skills/agent-media)
- [agent-media CLI npm package](https://www.npmjs.com/package/agent-media-cli)
- [agent-media GitHub repository](https://github.com/gitroomhq/agent-media)
- [agent-media official website](https://agent-media.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can reference external media URLs, local media paths, actor or persona choices, script duration limits, and generated job URLs from the CLI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
