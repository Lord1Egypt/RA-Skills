## Description:

Search the web using Google Gemini via OpenClaw-controlled Chrome with remote debugging enabled and an approved user profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream007007s](https://clawhub.ai/user/dream007007s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send web-search requests to Google Gemini through an existing Chrome session controlled by OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can access the user's existing Chrome session and open tabs.

Mitigation: Close sensitive tabs before use and approve the browser connection only for the intended task.

Risk: Using Chrome remote debugging can expose browser control beyond the immediate search workflow.

Mitigation: Use a dedicated Chrome profile when possible and disable the remote debugging port after the task is complete.

## Reference(s):

- [Google Gemini](https://gemini.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with browser automation guidance and inline shell commands when Chrome setup is required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an approved user Chrome profile and remote debugging access when attaching to an existing session.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
