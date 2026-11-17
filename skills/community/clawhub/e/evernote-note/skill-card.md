## Description:

Evernote Note helps agents search, browse, read, create, append to, and web-clip notes in Evernote/Yinxiang accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage personal Evernote/Yinxiang notes from an agent, including search, reading, note creation, appending content, and clipping web pages after configuring their own account tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and modify a user's note account through powerful Evernote/Yinxiang tokens.

Mitigation: Install only when that level of account access is acceptable, keep tokens in environment variables, and rotate or revoke them if exposure is suspected.

Risk: Create, append, and web-clip workflows can write to the wrong note or notebook if the agent acts on an ambiguous request.

Mitigation: Before write or clipping actions, require the agent to restate the target note, notebook, and URL and ask for confirmation.

Risk: Private note contents or sensitive URLs could be exposed in shared conversations or terminal logs.

Mitigation: Show only titles and summaries in group contexts, avoid clipping sensitive or internal URLs, and avoid running test scripts where terminal output is logged.

Risk: Unpinned Python dependencies and local test scripts can create reproducibility and operational risk.

Mitigation: Pin dependencies in a dedicated environment before deployment and run tests only in a controlled local shell.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heavenchenggong/skills/evernote-note)
- [Evernote Note release notes](artifact/PUBLISH.md)
- [EDAM API reference](artifact/references/api.md)
- [RESTful clipping API reference](artifact/references/api-restful.md)
- [Yinxiang developer documentation](https://dev.yinxiang.com/doc/)
- [ENML specification](https://dev.yinxiang.com/doc/articles/enml.php)
- [Evernote SDK for Python](https://github.com/yinxiang-dev/evernote-sdk-python)
- [evernote2 library](https://github.com/JackonYang/evernote2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash snippets plus API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided EVERNOTE_TOKEN for core note workflows and YX_AUTH_TOKEN for web clipping.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact metadata, published 2026-06-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
