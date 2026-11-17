## Description:

Records browser interactions for end-to-end tests and generates videos or GIFs with configurable encoding and annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13770626440](https://clawhub.ai/user/13770626440)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to record browser-based end-to-end test flows, produce demonstration recordings, and generate supporting configuration or command examples for test automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser recording can capture credentials, private user data, or production information.

Mitigation: Use sanitized test sites and test accounts, and do not record real passwords or private production data.

Risk: The skill weakens Chromium isolation when launching Puppeteer.

Mitigation: Keep Chromium sandboxing enabled unless execution is isolated in a disposable container.

Risk: CLI inputs such as JSON configs and media filenames may reach script execution or file-writing paths.

Mitigation: Run only trusted configs and output paths, and review or patch the Node scripts before installation.

Risk: Bundled release tooling handles GitHub tokens and includes force-push behavior.

Mitigation: Avoid the release scripts unless their token handling and git operations have been reviewed for the intended environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/13770626440/skills/e2e-test-recorder)
- [README](README.md)
- [Installation Guide](INSTALLATION.md)
- [Skill Documentation](SKILL.md)
- [Release Notes](RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets; CLI runs can produce MP4, GIF, WebM, and JSON report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local recording, log, and report files when its scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
