## Description:

Find beach and island resorts, including oceanfront rooms, private beaches, tropical stays, direct beach access, and water activities, using Fliggy-powered live travel search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find beach, oceanfront, and island resort options with current booking links. It is intended for resort discovery and comparison workflows that require live travel-search output rather than static travel knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned third-party flyai CLI globally.

Mitigation: Use a pinned and reviewed CLI version in a sandbox, and require approval before installing or executing it.

Risk: Travel input can be used to build shell commands for live searches.

Mitigation: Validate and quote user-provided parameters before command execution, and restrict commands to documented flyai parameters.

Risk: The runbook describes persisting raw user queries in a local execution log.

Mitigation: Disable local logging or redact personal travel details before retaining execution logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/beachfront-resort-finder)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to include live booking links from flyai CLI output and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
