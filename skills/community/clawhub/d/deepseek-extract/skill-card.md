## Description:

Extract full conversation content from DeepSeek shared chat links and export the conversation as Markdown or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zz0116](https://clawhub.ai/user/zz0116)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to extract conversations from DeepSeek share URLs they are authorized to access and save the results locally for review or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DeepSeek shared conversations may contain sensitive or private content saved to local files.

Mitigation: Use only share links the user is allowed to access, choose the output path deliberately, and delete or protect exported transcript files after use.

Risk: Browser automation and Playwright dependencies expand the local execution environment.

Mitigation: Install Playwright and Chromium in an isolated virtual environment or container and pin reviewed dependency versions in stricter environments.

Risk: Automated extraction can fail or return incomplete content when a page is slow, lazy-loaded, or protected by anti-bot controls.

Mitigation: Verify the exported file before relying on it, retry with a longer timeout or headed mode when needed, and fall back to manual copying if automated access is blocked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zz0116/skills/deepseek-extract)
- [Project homepage](https://github.com/zz0116/deepseek-extract)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON files with command-line status messages and agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output path is ./deepseek_conversation.md; JSON output is available with the --format json option.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
