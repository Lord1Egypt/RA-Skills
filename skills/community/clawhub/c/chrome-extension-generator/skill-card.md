## Description:

Generates Chrome extension project templates, including popup, background script, content script, and options page variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and extension authors use this skill to scaffold Chrome extension projects with manifests, browser scripts, UI files, README content, and publishing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can overwrite existing files or create output outside the intended folder if given crafted input.

Mitigation: Run it only in a disposable or explicitly chosen output folder, avoid untrusted extension names or descriptions, and check for existing files before generation.

## Reference(s):

- [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)

## Skill Output:

**Output Type(s):** [code, markdown, configuration, shell commands, guidance]

**Output Format:** [Generated project files plus terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a Chrome extension directory under the selected output path.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
