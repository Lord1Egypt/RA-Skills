## Description:

Guides an agent to help a user make coiled pine needle baskets by identifying suitable needles, planning harvest and conditioning schedules, calculating coil dimensions, tracking progress, and producing templates for logs, tests, inventory, and barter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External craft users use this skill to plan and track coiled pine needle basket making while they perform the physical harvesting, sorting, coiling, wrapping, finishing, and testing themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned installer command can expose users to supply-chain risk if the CLI or package source is not trusted.

Mitigation: Use a pinned and trusted ClawHub CLI version, or install and test the skill in a low-privilege environment before regular use.

Risk: The workflow may use location data, photos, and local progress logs for pine identification and basket tracking.

Mitigation: Share only the minimum location and photo detail needed, avoid sensitive background content in images, and store generated logs in an appropriate local workspace.

Risk: Basket making involves physical hazards such as sharp tools, skin irritation, repetitive strain, unsuitable plant material, and local harvesting restrictions.

Mitigation: Follow the skill's glove, tool-handling, patch-test, ergonomic break, and local regulation checks; stop the workflow when rash, strain, or uncertain plant identification occurs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/coiled-pine-needle-basket-making-basics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline templates and shell install command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local progress logs, harvest reports, inventory records, and barter text when the agent has filesystem access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
