## Description:

Universal CLI discovery gateway — one skill to manage all CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dull-bird](https://clawhub.ai/user/dull-bird)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an agent discover local CLI tools, inspect cached or live help output, and propose appropriate shell commands for CLI-driven tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inventory local CLI tools, execute help or version probes for programs on PATH, and persist captured help output under the user's home directory.

Mitigation: Install and run it only in environments where local tool discovery is acceptable; limit scans to trusted executables and review registry entries before relying on them.

Risk: Cached help text and generated registry data may contain untrusted or misleading content that an agent could reuse later.

Mitigation: Treat cached help output as reference data rather than instructions, and verify proposed commands before execution.

Risk: Security evidence notes limited safeguards around scan scope and registry file paths.

Mitigation: Avoid system-wide or custom-directory scans unless every executable in scope is trusted, and keep registry storage scoped to the intended user profile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dull-bird/skills/clihub)
- [README](README.md)
- [README_CN](README_CN.md)
- [AgentSkills spec](https://agentskills.io)
- [Vercel Skills](https://github.com/vercel-labs/skills)
- [prefrontalsys/register-tool](https://github.com/prefrontalsys/register-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON registry examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested CLI invocations, registry lookup results, parsed help summaries, and configuration steps.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
