## Description:

Behavioral guidelines to reduce common LLM coding mistakes when writing, reviewing, or refactoring code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to keep code changes simple, scoped, explicit about assumptions, and tied to verifiable success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation suggests unpinned npx and global npm installer commands, while the executable installer script is not present in the reviewed artifact.

Mitigation: Review the files being installed, pin and verify the npm package version, and inspect the installer script before running it in sensitive environments.

Risk: The guidance intentionally biases agents toward caution, which can slow trivial coding tasks or add unnecessary clarification steps.

Mitigation: Apply the skill with judgment for small, low-risk edits and keep success criteria proportional to the task.

## Reference(s):

- [Andrej Karpathy observation on LLM coding pitfalls](https://x.com/karpathy/status/2015883857489522876)
- [ClawHub skill listing](https://clawhub.ai/sg345662365-oss/skills/andrej-karpathy-skills)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, code, shell commands]

**Output Format:** [Markdown guidance with optional code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent behavior guidance only; no API calls, credentials, or MCP tools are required by the skill instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
