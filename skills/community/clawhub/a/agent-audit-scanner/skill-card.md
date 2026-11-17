## Description:

Agent Audit Scanner scans OpenClaw skills for prompt injection, credential leaks, unsafe code execution, MCP misconfiguration, privilege escalation, obfuscated commands, and social-engineering patterns across OWASP Agentic AI threat categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[headyzhang](https://clawhub.ai/user/headyzhang)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to audit OpenClaw skills and local OpenClaw/MCP configuration before enabling or deploying skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can attempt to install the external agent-audit package without a pinned version.

Mitigation: Install agent-audit manually from a trusted and pinned source in an isolated environment before running the bundled wrappers.

Risk: A clean result may be misleading if the underlying scanner errors or produces no output.

Mitigation: Treat scanner errors, empty output, or missing scanner dependencies as manual-review conditions rather than as proof that a skill is safe.

Risk: Audits read local OpenClaw skill directories and OpenClaw/MCP configuration files.

Mitigation: Run the audit with least-privilege access in an isolated environment and review which local paths are being scanned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/headyzhang/skills/agent-audit-scanner)
- [Project homepage and source](https://github.com/HeadyZhang/agent-audit)
- [Common Threats in OpenClaw Skills](references/common-threats.md)
- [OWASP Agentic AI Top 10 Agent Audit Rules](references/owasp-asi-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal reports, with JSON scanner output available from the underlying scanner command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings with BLOCK, WARN, INFO, and CLEAN severity tiers.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
