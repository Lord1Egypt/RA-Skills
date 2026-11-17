## Description:

Set up brave_shim as a free local proxy that routes OpenClaw Brave web_search requests to DuckDuckGo without a Brave API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weare20202020](https://clawhub.ai/user/weare20202020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and run a local Brave-compatible search shim, patch OpenClaw's Brave provider endpoint, and configure web search without a Brave API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites OpenClaw's installed Brave provider code.

Mitigation: Use it only in a disposable or tightly controlled OpenClaw environment and back up OpenClaw files before patching.

Risk: The setup flow clones and runs unpinned third-party code and Python dependencies.

Mitigation: Inspect and pin the brave_shim repository and dependencies before installation.

Risk: Search queries or LLM context may pass through the local shim and its dependencies.

Mitigation: Avoid sending sensitive searches or LLM context through the shim unless the local service and dependencies are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weare20202020/skills/brave-shim)
- [brave_shim repository](https://github.com/asoraruf/brave_shim)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Python and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local setup, OpenClaw configuration, provider patching, service startup, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
