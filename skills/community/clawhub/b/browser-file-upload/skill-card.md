## Description:

Automates uploading files to web pages via agent-browser CLI, with support for file input selectors and flexible local path formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixizi](https://clawhub.ai/user/weixizi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to upload local files into browser-based forms, either through direct agent-browser commands or the bundled helper script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to a website selected by the user or agent.

Mitigation: Confirm the destination domain is trusted and verify the selected file does not contain secrets, credentials, private workspace data, or other sensitive content before upload.

Risk: Automatic file-input discovery may select the wrong element on complex pages.

Mitigation: Prefer explicit CSS selectors such as input[type=file] or a known file input id when available.

Risk: The bundled Python helper may be unreliable because release security guidance notes a syntax issue from unescaped Windows paths in its docstring.

Mitigation: Use direct agent-browser commands until the helper script is fixed or validated in the target runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixizi/skills/browser-file-upload)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Guidance]

**Output Format:** [Markdown with bash command examples and Python helper script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser upload commands and path-resolution guidance; upload behavior depends on the target page and agent-browser availability.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
