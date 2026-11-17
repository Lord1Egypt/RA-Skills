## Description:

Use this skill when the user wants to check what data their shared agent can access, inspect what's being shared, review privacy, or see what guests will see.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to audit shared agent links, review what data and capabilities are exposed, and recommend narrowing or revoking access when sensitive content may be visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use PULSE_API_KEY access to inspect private notes and sharing information.

Mitigation: Use read-only or least-privilege credentials where possible and avoid running searches outside the intended audit scope.

Risk: The skill includes actions that can modify or revoke share links.

Mitigation: Require explicit confirmation of the target link, scope, and intended change before any PATCH or DELETE request.

Risk: A wrong link or scope selection could expose or alter sharing settings unintentionally.

Mitigation: Manually verify the exact link identifier and current permissions before applying recommended access changes.

## Reference(s):

- [Examine Sandbox API Reference](reference/API.md)
- [Audit a Share Link Before Sending](examples/audit-link.md)
- [ClawHub skill page](https://clawhub.ai/xisen-w/skills/examine-sandbox)
- [Publisher profile](https://clawhub.ai/user/xisen-w)
- [Aicoo API base URL](https://www.aicoo.io/api/v1)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize active share links, visitor activity, sensitive-content search results, and recommended access changes.]

## Skill Version(s):

2.0.0 (source: skill metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
