## Description:

Automates ChatGPT Web conversations through a local browser session with persistent login state, one-shot prompts, reusable multi-turn sessions, and conversation metadata storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[placidusaxalarak](https://clawhub.ai/user/placidusaxalarak)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill when they need browser-based ChatGPT Web conversations instead of the OpenAI API, including login setup, one-shot prompts, continued conversations, reusable sessions, model selection, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reuses a logged-in ChatGPT Web session and stores browser/session artifacts locally.

Mitigation: Use a dedicated low-privilege account or isolated environment, avoid sensitive prompts, and review or clear data/ and any chatgpt-profile-* temporary directories.

Risk: Browser automation can fail when ChatGPT login, CAPTCHA, 2FA, risk review, network, proxy, or page-layout conditions change.

Mitigation: Validate authentication before use, run with a visible browser for inspection when needed, and use the troubleshooting guidance for proxy, selector, and verification failures.

Risk: First-run setup downloads dependencies and a browser into the local environment.

Mitigation: Review requirements and install only in an environment where those downloads and local runtime artifacts are acceptable.

## Reference(s):

- [CLI Reference](references/api_reference.md)
- [Troubleshooting](references/troubleshooting.md)
- [Usage Patterns](references/usage_patterns.md)
- [ChatGPT Web](https://chatgpt.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON command output from browser-driven ChatGPT Web conversations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local browser/session artifacts and optional proof screenshots under data/.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
