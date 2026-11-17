## Description:

Manage Dub short links, track conversions, and read link attribution analytics through the superagnt unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing teams use this skill to manage Dub short links and review link attribution and conversion activity. It can also access partner and financial administration operations when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis rates the skill suspicious because it includes financial and partner administration capabilities beyond its stated link and analytics purpose; the analysis is incomplete and this is not proof of malicious intent.

Mitigation: Before installing, verify that those capabilities are necessary and intended. Limit use to the endpoints required for the task and confirm before destructive or outbound actions.

Risk: The available API includes operations that can update or delete links, customer and partner records, commissions, and other workspace data.

Mitigation: Review the specific operation and target before making changes, and get explicit confirmation before deletes, overwrites, or actions performed on the user's behalf.

## Reference(s):

- [Dub Integration documentation](https://superagnt.com/r/ch-dub-links-docs)
- [superagnt MCP installation guide](https://www.superagnt.com/install)
- [superagnt API key setup](https://superagnt.com/r/ch-dub-links-key)
- [Dub account connections](https://app.superagnt.com/dashboard/connections)
- [ClawHub listing](https://clawhub.ai/superagnt/skills/dub-links)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON API responses with shell commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPERAGNT_API_KEY and curl when using the documented API calls.]

## Skill Version(s):

2.0.14 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
