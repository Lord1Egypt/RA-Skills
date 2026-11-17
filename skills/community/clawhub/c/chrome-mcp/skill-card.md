## Description:

Controls a locally running, logged-in Chrome browser session through Chrome DevTools MCP for browsing, page inspection, JavaScript execution, screenshots, and website interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumint](https://clawhub.ai/user/lumint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent control a real local Chrome session for authenticated browsing, page inspection, DOM interaction, screenshots, and site-specific actions such as X posts, reposts, likes, and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Chrome session and may access private accounts, messages, financial sites, or workplace sites.

Mitigation: Use a separate limited-privilege browser profile and avoid granting access to sensitive accounts or sites.

Risk: The skill includes state-changing browser actions such as posting, reposting, liking, and deleting content.

Mitigation: Require explicit confirmation of the account, target, and action before allowing posts, deletions, or similar changes.

Risk: The fallback CDP script is external to the provided artifact and lacks integrity evidence in this bundle.

Mitigation: Avoid the fallback unless the script has been independently reviewed and verified.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/lumint/skills/chrome-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with tool-call recipes, command-style steps, selectors, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Chrome session with remote debugging enabled and Chrome DevTools MCP tools; the external CDP fallback should be independently verified before use.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
