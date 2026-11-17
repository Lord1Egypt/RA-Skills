## Description:

Use Google Gemini as a subscription-backed sub-agent for text analysis, long-context processing, summarization, Q&A, and medium-complexity coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedo0626](https://clawhub.ai/user/tedo0626)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to route text, summarization, long-context, and moderate coding work to Gemini through a local CLI workflow. It is not intended for OpenClaw-native tool use, real-time data access, or tasks that require OpenClaw session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs global command-line tools and writes a global ask-gemini wrapper.

Mitigation: Review the install script before running it, prefer user-local pinned installs where possible, and use a disposable or tightly scoped workspace.

Risk: The documented Gemini agentic coding flow can auto-approve file writes and shell commands.

Mitigation: Avoid unattended approval flags unless that behavior is explicitly desired, and review Gemini's proposed file and shell changes before applying them.

Risk: Prompts and piped files may be sent to Gemini through Google authentication.

Mitigation: Do not send secrets, credentials, proprietary code, or private documents unless that data flow has been approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tedo0626/skills/gemini-sub-agent)
- [Google Cloud CLI apt key](https://packages.cloud.google.com/apt/doc/apt-key.gpg)
- [Google Cloud CLI apt repository](https://packages.cloud.google.com/apt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown and shell command examples, with CLI-generated text or code responses during use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Gemini CLI with subscription-backed Google authentication and may run agentic coding flows that read and write local files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
