## Description: <br>
Helps an agent reflect on its work, capture corrections and command failures, and organize persistent learning records for future sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill with OpenClaw-compatible agents to capture user corrections, command failures, outdated knowledge, and reusable workflow improvements across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad always-on hooks can persistently influence agent behavior and learning capture. <br>
Mitigation: Prefer project-scoped hooks with restrictive matchers, and avoid global hooks unless the repository and scripts are trusted. <br>
Risk: Learning files or memory updates can accidentally capture secrets, credentials, personal data, raw transcripts, or unredacted command output. <br>
Mitigation: Require explicit review before writing to memory or agent instruction files, and store only short redacted summaries. <br>
Risk: Persistent self-improvement records can introduce incorrect or misleading guidance into later sessions. <br>
Mitigation: Review proposed learning entries before promotion to AGENTS.md, SOUL.md, TOOLS.md, MEMORY.md, or reusable skills. <br>


## Reference(s): <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or remind the agent to create or update learning files and agent instruction files; review changes before persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
