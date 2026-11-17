## Description:

Find Mcp Directories helps agents find, rank, and shortlist directories and registries where builders can submit or list MCP servers for backlinks, referral traffic, and discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to identify MCP server directories, compare listing opportunities by authority and reach signals, and decide where to submit their server for discovery and backlinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local credential wrapper may execute commands from a workspace .env.local file before making API calls.

Mitigation: Use only in trusted workspaces, or change the authentication pattern to a harness-managed environment variable or strict non-executing dotenv parser before running authenticated calls.

Risk: Unlock calls spend ServiceGraph credits.

Mitigation: Keep unlock operations user-approved and confirm the selected apex domains and credit cost before submitting unlock requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-mcp-directories)
- [ServiceGraph API](https://api.servicegraph.co)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API endpoint examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked registry shortlists, filter suggestions, unlock guidance, and submission-priority recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
