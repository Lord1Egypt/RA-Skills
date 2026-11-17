## Description:

AI Orchestrator provides DeepSeek AI access through Puppeteer browser automation with a CDP interceptor, persistent daemon mode, health checks, graceful shutdown, PM2 management, and `.deepseek.json` configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external users use this skill to ask DeepSeek for code analysis, review, generation, text analysis, summarization, and translation through a local CLI and browser automation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and piped files are sent to DeepSeek through browser automation.

Mitigation: Use only with content approved for DeepSeek, and avoid sending sensitive or regulated files unless that use is explicitly allowed.

Risk: The skill uses a persistent authenticated Chromium daemon with local profile, session, endpoint, log, and diagnostic state.

Mitigation: Run it under an isolated OS user or container, restrict permissions on `.profile`, `.sessions`, and `.daemon-ws-endpoint`, and avoid boot persistence unless it is required.

Risk: Unsafe local file and browser-control practices need review before use on shared or sensitive machines.

Mitigation: Review the release before installation, update the dependency tree, validate session names before use, and run health checks in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ciklopentan/skills/ai-orchestrator)
- [AI Orchestrator reference manual](artifact/REFERENCE.md)
- [Network-first pipeline manual](artifact/PHASE1-MANUAL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown on stdout, often with code blocks; optional diagnostics may be written as JSON or JSONL files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DeepSeek free-tier responses can be truncated; long work should be split across sessions.]

## Skill Version(s):

2.0.11 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
