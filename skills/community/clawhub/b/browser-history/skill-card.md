## Description:

Searches a Chrome browsing-history SQLite database for URLs, titles, visit counts, recent visits, and YouTube results using shell commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therohitdas](https://clawhub.ai/user/therohitdas)

### License/Terms of Use:


## Use Case:

Developers or agent users can use this skill to locate entries in a permitted Chrome profile's local browser history and return matching URLs, titles, visit counts, or recency-ordered results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private browsing-history data from a named Chrome profile without built-in consent checks.

Mitigation: Use only with explicit permission from the Chrome profile owner and limit results to the minimum needed.

Risk: The artifact includes browser-hiding behavior that can reduce user visibility into actions taken by an agent.

Mitigation: Avoid the hide or minimize command and keep browser activity visible to the profile owner.

Risk: Copying the Chrome history database to a temporary path can leave sensitive local data behind.

Mitigation: Use secure temporary files, delete copies after use, and prefer a revised workflow with cleanup and URL redaction.

Risk: Opening retrieved URLs can navigate to sensitive or unintended pages.

Mitigation: Require user confirmation before opening any browser-history result.

## Reference(s):

- [Browser History skill page](https://clawhub.ai/therohitdas/skills/browser-history)
- [Publisher profile](https://clawhub.ai/user/therohitdas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash and SQLite command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output local browsing-history data such as URLs, page titles, visit counts, and recent-visit ordering.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
