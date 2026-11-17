## Description:

Automates local browser-use CLI and Python workflows for opening pages, interacting with pages, taking screenshots, extracting HTML and links, debugging sessions, and capturing login QR codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjiajie](https://clawhub.ai/user/fengjiajie)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run local browser automation in OpenClaw containers or hosts, including screenshot and HTML inspection, persistent browser sessions, and optional browser-agent runs with an OpenAI-compatible LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser page content, screenshots, prompts, URLs, and session-derived context may be processed by the configured external LLM provider.

Mitigation: Use only approved providers and avoid internal, authenticated, regulated, or credential-heavy pages unless that data sharing is approved.

Risk: Persistent browser sessions can retain authenticated or sensitive browsing state.

Mitigation: Clear persistent browser sessions when they are no longer needed and avoid reusing sessions across unrelated tasks.

Risk: Browser automation can click, type, and extract content from live pages.

Mitigation: Review target URLs, tasks, screenshots, and HTML outputs before running actions that could affect accounts, data, or external systems.

Risk: QR-code and data-image extraction can capture login material from screenshots or page HTML.

Mitigation: Treat generated screenshots, crops, and extracted images as sensitive files and store or delete them according to the workspace data policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengjiajie/skills/browser-use-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, cropped image files, extracted image files, and browser-agent final-result text when the described commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
