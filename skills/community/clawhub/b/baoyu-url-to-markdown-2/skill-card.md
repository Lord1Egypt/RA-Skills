## Description:

Fetch any URL and convert it to Markdown using Chrome CDP, with rendered HTML snapshots, a Defuddle-first conversion path, a legacy fallback, optional YouTube transcript capture, wait mode for login-required pages, optional media localization, and a hosted defuddle.md fallback if local browser capture fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content operators use this skill to capture web pages as Markdown files for archiving, note-taking, content migration, or agent-readable context. It is most useful when pages need JavaScript rendering, a saved HTML snapshot, or a wait mode for user-prepared browser state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A failed local capture can send the target URL to the hosted defuddle.md fallback service.

Mitigation: Avoid private, signed, token-bearing, intranet, or authenticated URLs unless the user explicitly accepts that fallback behavior.

Risk: Media localization can make the local machine fetch arbitrary image or video URLs found in page content.

Mitigation: Keep media handling set to ask or never for untrusted pages, and review the page source before enabling automatic downloads.

Risk: Runtime dependencies are resolved through Bun or npx and the artifact does not include a lockfile.

Mitigation: Use a trusted preinstalled Bun runtime and pinned or reviewed dependencies before running the skill in a sensitive environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nengnengz/skills/baoyu-url-to-markdown-2)
- [Publisher profile](https://clawhub.ai/user/nengnengz)
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown)
- [First-time setup reference](references/config/first-time-setup.md)
- [defuddle.md fallback service](https://defuddle.md/stephango.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files with YAML front matter, sibling captured HTML snapshots when local capture succeeds, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown, HTML, image, and video files; may call a hosted fallback service when local browser capture fails.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.58.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
