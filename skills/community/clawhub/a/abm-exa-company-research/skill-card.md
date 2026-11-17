## Description:

Researches a company using Exa web search to produce an overview of its products, funding, team, recent news, and competitive position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to gather company intelligence for competitive research, partnership evaluation, prospect qualification, and related business analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command examples can execute unintended commands if crafted company names, domains, or result IDs are substituted literally.

Mitigation: Call the Exa CLI with shell-free argument arrays or otherwise validate and quote inputs before execution.

Risk: The skill may read local product-marketing context files when they exist.

Mitigation: Use the skill only in workspaces where those context files are approved for agent access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-exa-company-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown company research report with bullet lists, dated news items, and a leadership table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source caveats and notes when findings appear outdated or unverified.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
