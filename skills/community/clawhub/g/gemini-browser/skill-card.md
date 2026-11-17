## Description:

Query Google Gemini via browser automation using OpenClaw's Browser Relay when an agent needs to ask Gemini questions and retrieve responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eccstartup](https://clawhub.ai/user/eccstartup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate authenticated Gemini interactions through a manually attached Chrome tab, submit prompts, wait for completion, and extract Gemini responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a manually attached Gemini tab in a real Chrome session, so the agent may access visible account context in that tab.

Mitigation: Use a dedicated Chrome profile and non-primary Google account, and attach only the Gemini tab intended for automation.

Risk: The documented input path uses raw JavaScript evaluation and can mishandle untrusted prompt text if inserted directly into the snippet.

Mitigation: Safely encode prompt text as data before injection and review JavaScript snippets before execution.

Risk: Clipboard-based extraction may expose or overwrite global clipboard contents.

Mitigation: Prefer DOM or text extraction when possible, and review clipboard contents before using them elsewhere.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eccstartup/skills/gemini-browser)
- [Publisher profile](https://clawhub.ai/user/eccstartup)
- [Google Gemini](https://gemini.google.com)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with browser command examples and extracted Gemini response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw Browser Relay, a manually attached Gemini tab, and an authenticated Chrome session.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
