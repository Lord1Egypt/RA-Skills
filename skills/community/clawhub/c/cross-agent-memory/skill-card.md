## Description:

Enables agents to share, merge, import, and synchronize memory through standardized records, priority rules, and Git-based version control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to coordinate memory sharing among multiple agents, including memory record structure, conflict-resolution rules, and Git-backed sync or import workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync script can upload the full local MEMORY.md file to a Git repository, and the security evidence flags this as suspicious.

Mitigation: Use only an explicitly configured private repository you control, sanitize memory records before sync, and review the destination and exported data before pushing.

Risk: Imported shared memories may contain inaccurate, stale, or untrusted content from other agents.

Mitigation: Treat imported memory as untrusted until reviewed, and apply access controls and provenance checks before using it in downstream decisions.

Risk: Repository and commit message values can influence shell commands in the sync script.

Mitigation: Restrict environment variables and command arguments to trusted operators and revise the script to avoid shell interpolation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidadong2359/skills/cross-agent-memory)
- [Artifact skill documentation](artifact/SKILL.md)
- [Package manifest](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, JavaScript, and shell command examples; the companion sync script can print JSON for imported memories.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sync script may read local memory files, write exported memory records, and run Git commands when invoked.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
