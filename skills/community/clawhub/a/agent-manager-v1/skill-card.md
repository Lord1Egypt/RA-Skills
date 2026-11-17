## Description:

Multi-Agent conversation management platform with Gemini-style UI for managing OpenClaw agents with image upload, chat history, and message isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local web, CLI, and API interface for creating, viewing, chatting with, pairing, and deleting OpenClaw agents. It is intended for managing multiple agent conversations and preserving browser-local chat history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated local APIs can run shell commands and delete files.

Mitigation: Add authentication, bind the service to 127.0.0.1, validate paths and IDs, and replace shell execution and rm -rf behavior with safer Node APIs or argument-array subprocess calls before use.

Risk: A plaintext OpenClaw token is present in the artifact evidence.

Mitigation: Remove the token from distributed files and rotate it before installing or testing the skill.

Risk: The security verdict is suspicious and recommends review before installation.

Mitigation: Use only in a tightly controlled local environment, update vulnerable dependencies, and do not expose port 3000 or run it against important OpenClaw data until issues are resolved.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/szzg007/skills/agent-manager-v1)
- [ClawHub homepage](https://clawhub.com)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [ClawHub documentation](artifact/CLAWHUB.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, JavaScript application files, JSON configuration, shell commands, API responses, and browser UI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Node.js service for OpenClaw agent management and conversation workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter, artifact _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
