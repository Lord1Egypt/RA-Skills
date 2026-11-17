## Description:

Firecrawl Interact helps agents control a live browser session for scraped pages, including clicking, form filling, navigation, authenticated sessions, and data extraction using prompts or code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill when ordinary scraping is not enough and a page requires clicks, form entry, pagination, login, infinite scroll, or a multi-step flow before information can be extracted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows an agent to control a live browser session, including interactions that may submit data or change account state.

Mitigation: Require explicit user confirmation before credentials, submissions, purchases, or account changes.

Risk: Authenticated browser profiles can persist cookies and local storage across sessions.

Mitigation: Use separate least-privilege browser profiles, avoid saving sessions for sensitive accounts, and prefer read-only reconnects when state should not be updated.

Risk: The release evidence flags an unpinned npx runtime dependency.

Mitigation: Prefer a pinned or preinstalled Firecrawl CLI before enabling the skill in higher-trust environments.

## Reference(s):

- [Firecrawl Interact ClawHub release](https://clawhub.ai/eohmig/skills/firecrawl-interact)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline CLI commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May target a prior scrape ID, use browser profiles, set execution timeouts, and write command output to a file path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
