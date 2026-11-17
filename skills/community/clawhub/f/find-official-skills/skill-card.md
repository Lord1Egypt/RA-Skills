## Description:

Find official, trusted, vendor-owned AI agent skills from Skillscout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ulyanas](https://clawhub.ai/user/ulyanas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to find official or trusted vendor-owned skills for a company, product, domain, or task and get concise install guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Displayed install commands could be copied into a shell without review.

Mitigation: Before running a command, confirm that it has the expected simple form `npx skills add owner/repo@skill-name` and does not contain extra shell syntax, unexpected repositories, or unrelated commands.

Risk: Skill recommendations depend on Skillscout as the source of truth for official skill listings.

Mitigation: Install the skill only when Skillscout is an acceptable source for the user's official-skill lookup workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ulyanas/skills/find-official-skills)
- [Server-resolved GitHub provenance](https://github.com/ulyanas/skillscout-skills/tree/main/skills/find-official-skills)
- [Skillscout official skills directory](https://skillscout.sh/data/official-skills-universal.json)
- [Skillscout official skills search](https://skillscout.sh/official/?q=grafana)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with install commands and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include grouped results, total match counts, source links, and a search link depending on the user's request.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
