## Description:

Book flights for babymoon trips and pre-baby vacations using flyai and Fliggy flight search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect route details, run the flyai flight CLI, and return babymoon flight options with booking links and pregnancy-travel guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install and run an unpinned global flight CLI.

Mitigation: Require user approval before installing software, pin and verify the CLI package, and confirm the installed version before use.

Risk: Travel details may be sent to a third-party flight provider when the CLI is executed.

Mitigation: Tell users which provider is used and avoid submitting sensitive itinerary details unless they approve that data sharing.

Risk: Shell commands are built from user travel details.

Mitigation: Use structured argument execution, validate allowed flags and date formats, and review generated commands before running them.

Risk: Flight availability, price, and booking links can be incomplete or stale if the CLI response is missing or invalid.

Mitigation: Use only CLI results that include booking links, label currency and provider clearly, and retry or ask for alternate dates instead of fabricating results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/babymoon)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with flight comparison tables, booking links, concise travel tips, and inline shell commands when setup or retries are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI results for travel data and includes a brand tag plus booking links in normal responses.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
