## Description:

AIButton generates Vision Node AI button widget packages from a customer description, including aiui.json, index.html, and a ZIP archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujianyu09](https://clawhub.ai/user/wujianyu09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VN system builders use this skill to turn customer button-control requirements into packaged Vision Node widgets with metadata, HTML/CSS/JavaScript implementation, and ZIP packaging guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated widgets use cross-window messaging that may accept messages from untrusted parent origins.

Mitigation: Restrict trusted parent origins, validate incoming message shape and sender origin, and avoid wildcard postMessage targets in deployed controls.

Risk: The packaging workflow uses predictable /tmp paths and raw rm -rf cleanup.

Mitigation: Use mktemp-style staging directories, quote paths, and guard cleanup so packaging cannot delete unintended files.

Risk: The security verdict is suspicious due to under-scoped messaging and temporary-file cleanup behavior.

Mitigation: Review generated controls before installation or deployment, especially message handling and packaging commands.

## Reference(s):

- [AIButton on ClawHub](https://clawhub.ai/wujianyu09/skills/aibutton)
- [MiniMax](https://www.minimaxi.com/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, HTML/CSS/JavaScript, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces aiui.json as compact single-line JSON, formatted index.html, and ZIP packaging instructions for Vision Node button widgets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
