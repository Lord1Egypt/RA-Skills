## Description:

CNKI is a unified entry point for searching China National Knowledge Infrastructure, retrieving paper details, downloading PDF or CAJ files, exporting citations, and browsing journal information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to run CNKI literature workflows from an agent: keyword and advanced search, article metadata lookup, downloads, citation export, and journal table-of-contents queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a logged-in Chrome profile for CNKI operations.

Mitigation: Use a dedicated browser profile for CNKI and avoid profiles containing unrelated logged-in accounts.

Risk: User-supplied URLs can direct browser automation beyond the intended CNKI page scope.

Mitigation: Limit supplied URLs to official CNKI pages and manually review navigation before sensitive actions.

Risk: Downloads and Zotero or RIS exports can create files or modify local citation workflows.

Mitigation: Manually confirm downloads and exports, and review generated files or Zotero entries before relying on them.

Risk: CAPTCHA, login state, and access permissions can block or alter expected behavior.

Mitigation: Complete CNKI verification manually and confirm account download permissions before requesting download or export actions.

## Reference(s):

- [ClawHub skill page for cnki](https://clawhub.ai/jirboy/skills/cnki)
- [ClawHub publisher profile for jirboy](https://clawhub.ai/user/jirboy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with structured literature metadata, citation/export instructions, and inline commands or browser automation snippets when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate browser-driven CNKI downloads or Zotero/RIS exports when the user has access and confirms required steps.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
