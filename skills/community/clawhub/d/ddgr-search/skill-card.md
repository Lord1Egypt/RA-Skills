## Description:

Performs command-line web searches with ddgr and a configurable result count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javedniazi](https://clawhub.ai/user/javedniazi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run lightweight web searches from the command line when they need a small number of search results during a workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the search service used by ddgr.

Mitigation: Avoid submitting confidential, regulated, or sensitive query text unless that service is approved for the workflow.

Risk: The skill depends on the locally installed ddgr command.

Mitigation: Install ddgr from a trusted source and keep the local package updated before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javedniazi/skills/ddgr-search)
- [Publisher profile](https://clawhub.ai/user/javedniazi)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Command-line text returned by ddgr, with agent-facing guidance where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ddgr command-line tool to be installed and available on PATH.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
