## Description:

Integrates AutoResearchClaw so an agent can configure and run an autonomous research workflow that returns academic papers, citations, experiment code, and review artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nffdasilva](https://clawhub.ai/user/nffdasilva)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research-support agents use this skill to turn a research topic into an AutoResearchClaw run that can produce papers, citation files, experiment code, figures, verification reports, and peer-review notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run unpinned third-party code with approvals disabled.

Mitigation: Review before installing, run only in a sandbox or isolated workspace, pin AutoResearchClaw to a trusted commit, and avoid auto-approval for normal use.

Risk: The workflow can use network access, API credentials, scheduled jobs, messaging, browser automation, spawned sessions, memory, and skill creation integrations.

Mitigation: Limit credentials passed to the process and enable cron, memory, messaging, browser, sessions, or MetaClaw skill creation only when explicitly needed.

Risk: Autonomous research and paper generation can produce incorrect, misleading, or unsupported conclusions.

Mitigation: Review generated papers, citation files, verification reports, experiment code, and results before relying on or sharing the output.

## Reference(s):

- [AutoResearchClaw project link from artifact resources](https://github.com/aiming-lab/AutoResearchClaw)
- [AutoResearchClaw Integration ClawHub listing](https://clawhub.ai/nffdasilva/skills/autoresearchclaw-integration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and references to generated research deliverable files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to produce LaTeX, BibTeX, JSON verification reports, experiment outputs, figures, and review notes through AutoResearchClaw.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
