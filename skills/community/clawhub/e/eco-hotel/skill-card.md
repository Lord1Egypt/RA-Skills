## Description:

Eco Hotel helps agents search flights for eco-hotel and sustainable travel destinations using FlyAI/Fliggy CLI results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and travel-support agents use this skill to collect route details, run FlyAI/Fliggy flight searches, and format bookable eco-hotel or sustainable travel options. It is intended for real-time travel search workflows where results must come from CLI output rather than model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to install a global FlyAI CLI package before serving travel requests.

Mitigation: Review the package source and installation policy before deployment; prefer pinned or verified CLI versions where possible.

Risk: The skill routes broad travel searches through one provider and requires provider booking links.

Mitigation: Disclose the provider dependency to users and validate that returned booking links are appropriate before presenting results.

Risk: User-supplied route and date values are passed into shell commands.

Mitigation: Validate and quote command arguments before execution, and ask for missing origin, destination, or date details instead of guessing.

## Reference(s):

- [eco-hotel ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/eco-hotel)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with CLI command examples, comparison tables, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to come from FlyAI CLI output and include a Book link for each result.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
