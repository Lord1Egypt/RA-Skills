## Description:

Conduct comprehensive AI-powered research with citations via the Tavily CLI and return structured reports grounded in web sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to run Tavily CLI research tasks for comparisons, market scans, literature reviews, and multi-source topic investigations that require cited synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to pipe a downloaded installer script into bash when the Tavily CLI is missing.

Mitigation: Review the installer separately and preinstall the Tavily CLI through a trusted, versioned process before enabling routine research use.

Risk: The skill can start CLI authentication during a normal research request.

Mitigation: Authenticate the Tavily CLI through an approved setup flow before use and avoid interactive login during agent-run research tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-tavily-research)
- [Tavily CLI install script](https://cli.tavily.com/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, or JSON reports with citations, depending on Tavily CLI options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research tasks can stream progress, run asynchronously with request polling, save reports to files, or return structured JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
