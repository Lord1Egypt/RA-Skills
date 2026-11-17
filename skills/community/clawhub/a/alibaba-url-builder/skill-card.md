## Description:

Builds Alibaba.com URLs for agent navigation across product searches, product detail pages, supplier profiles, RFQ pages, and special sections, with traffic_type=ags_llm tracking on each URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeyu426](https://clawhub.ai/user/zeyu426)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, procurement teams, and sourcing agents use this skill to construct Alibaba.com navigation URLs for product discovery, supplier research, RFQ access, and market exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier subdomain inputs can produce non-Alibaba or malformed navigation targets.

Mitigation: Validate supplier subdomains as single DNS labels before navigation and reject schemes, slashes, dots, and other host-control characters.

Risk: Every generated URL includes traffic_type=ags_llm, which identifies agent-origin traffic.

Mitigation: Use the generated URLs only where this tracking parameter is acceptable for the workflow and audience.

Risk: Install and release guidance includes mutable npm/npx commands, and release.sh can publish the skill and push repository contents.

Mitigation: Pin CLI package versions where possible and inspect release.sh carefully before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeyu426/skills/alibaba-url-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with URL strings, Python helper code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated URLs include the traffic_type=ags_llm tracking parameter.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
