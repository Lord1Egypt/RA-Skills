## Description:

Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoataiza](https://clawhub.ai/user/nicoataiza)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage ClawdHub skills from an agent workflow, including search, install, update, list, authentication, and publish commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating skills through a CLI can change agent behavior through newly fetched content.

Mitigation: Review the ClawdHub CLI package, registry destination, and target skill before installing or updating.

Risk: Bulk forced updates can change all installed skills at once.

Mitigation: Use bulk forced updates only when the operator intentionally wants every installed skill changed.

Risk: Publishing a skill folder can expose unintended local files or secrets.

Mitigation: Inspect skill folders for secrets and private files before publishing.

## Reference(s):

- [ClawdHub Registry](https://clawdhub.com)
- [ClawHub Skill Page](https://clawhub.ai/nicoataiza/skills/clawdhub-bak-2026-01-28t18-01-16-10-30)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nicoataiza)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command examples and operational notes for the npm-installed clawdhub CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
