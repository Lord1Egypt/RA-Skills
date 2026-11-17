## Description:

Searches, compares, and shortlists Microsoft Dynamics 365 implementation partners by product, industry, and region using the Top Dynamics Partners MCP-backed directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colingreig](https://clawhub.ai/user/colingreig)

### License/Terms of Use:

MIT-0

## Use Case:

External users, consultants, project managers, and Dynamics buyers use this skill to find, compare, and shortlist Microsoft Dynamics 365 ERP and CRM implementation partners, including Business Central and Finance & Operations specialists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can run an unpinned npm package locally through npx.

Mitigation: Use a pinned or locked installation of the MCP SSE bridge before deployment.

Risk: Partner search and shortlist prompts may send project details to topdynamicspartners.com.

Mitigation: Avoid confidential budget, timeline, or implementation details unless sharing them with that third-party service is approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/colingreig/skills/dynamics-partner-advisor)
- [Top Dynamics Partners](https://topdynamicspartners.com)
- [MCP Server Documentation](https://topdynamicspartners.com/resources/mcp-server)
- [GitHub Repository](https://github.com/ignitemarketing/dynamics-partner-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include partner search results, detailed partner profiles, ranked shortlists, match reasoning, and MCP setup configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
