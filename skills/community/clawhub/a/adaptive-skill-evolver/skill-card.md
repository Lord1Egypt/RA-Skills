## Description:

Skill Evolver analyzes agent execution traces to generate evidence-scored Evolution Units that update a skill's guidance over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polkalian](https://clawhub.ai/user/polkalian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review execution traces, generate evidence-scored lessons for agent skills, and manage which lessons are attached, pinned, evicted, or blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic persistence can write Evolution Units, inline SKILL.md blocks, state/config JSON, and scheduled background updates.

Mitigation: Start in manual mode and inspect generated Evolution Units before allowing SKILL.md writeback or cron-style background runs.

Risk: Trace and unit or skill text may be sent to a configured remote LLM provider.

Mitigation: Disable remote LLM unless needed, and use only trusted HTTPS LLM endpoints when remote review or generation is enabled.

Risk: Safety review weaknesses, including fail-open reviewer behavior, may allow unsafe units to pass in sensitive environments.

Mitigation: Resolve the reviewer behavior before sensitive use, and manually review and scan generated units before deployment.

Risk: Documented setup and scheduling commands reference setup/schedule files that are not present in the artifact.

Mitigation: Resolve the missing setup and schedule files before relying on automated initialization or schedule status commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/polkalian/skills/adaptive-skill-evolver)
- [Skill README](README.md)
- [Skill Definition](SKILL.md)
- [License](LICENSE)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status or configuration output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Evolution Unit Markdown files, SKILL.md inline blocks, state/config JSON, and trace/evidence history when run.]

## Skill Version(s):

2.4.13 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
