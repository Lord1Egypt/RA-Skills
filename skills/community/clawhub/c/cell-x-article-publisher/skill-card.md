## Description:

Publishes existing Markdown articles to X Articles drafts by preparing rich text, media placement, clipboard content, and reusable Playwright login state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they already have a finished Markdown long-form article and need an agent to prepare and save it as an X Articles draft. It helps parse article structure, handle images and dividers, prepare rich-text clipboard content, and reuse local login state when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local X/Twitter browser cookies and create a reusable Playwright login-state file.

Mitigation: Use it only on trusted machines and treat ~/.cache/x-article-publisher/x-storage-state.json like a password; do not share, commit, sync, or log it, and delete it after use.

Risk: Markdown image handling can download remote HTTPS images and may match missing filenames from common personal folders.

Mitigation: Review Markdown from untrusted sources before parsing, prefer known local image paths, and inspect generated asset paths before browser automation.

Risk: Fresh dependency installation can pull current package versions at runtime.

Mitigation: Pin and review dependencies before use in controlled or production environments.

Risk: Automating a logged-in X/Twitter browser session can affect the user's account if the workflow is expanded beyond draft saving.

Mitigation: Keep the default draft-only boundary, avoid automatic final publishing, and use a dedicated browser profile or manual login when appropriate.

## Reference(s):

- [OpenClaw homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/x-article-publisher)
- [Workflow](artifact/references/workflow.md)
- [Cookie Sync](artifact/references/cookie-sync.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON parse output, HTML clipboard content, generated image files, and Playwright storage-state configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce temporary local image assets, copied clipboard content, and a local Playwright storage-state JSON file for X/Twitter authentication reuse.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
