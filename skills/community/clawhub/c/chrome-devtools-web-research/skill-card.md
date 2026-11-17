## Description:

Enables browser-driven web research and live site inspection through Chrome DevTools MCP over a remote-debugging Chrome session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackerchai](https://clawhub.ai/user/hackerchai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, researchers, and agent operators use this skill to inspect dynamic websites, navigate browser-visible page state, and cross-check web findings across search, social, community, and source pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for DevTools-level access to a live Chrome session, which can expose tabs, cookies, logins, and page state.

Mitigation: Use a separate temporary Chrome profile with no unrelated logged-in accounts, and close unrelated tabs before use.

Risk: The skill uses unpinned install/runtime packages, so behavior can change across installs.

Mitigation: Review and pin npm package versions where possible before deployment.

Risk: Remote debugging access can remain enabled after the task is complete.

Mitigation: Disable Chrome remote debugging when finished.

## Reference(s):

- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/hackerchai/skills/chrome-devtools-web-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and source-quality summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source-quality buckets, caveats, browser-access remediation, and concise audit notes.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
