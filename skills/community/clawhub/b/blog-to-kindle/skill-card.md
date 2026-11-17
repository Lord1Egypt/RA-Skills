## Description:

Scrape blogs and essay sites, compile them into Kindle-friendly EPUB files with AI-generated covers, and optionally send them to Kindle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainekomacx](https://clawhub.ai/user/ainekomacx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn supported blog archives or custom essay sites into Kindle-ready EPUB collections, including cover generation and delivery steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The send workflow may use an unsafe default Kindle recipient.

Mitigation: Remove hard-coded recipient defaults and require the user to confirm the Kindle email address before sending.

Risk: Mail.app automation can run unintended local actions when AppleScript arguments are not safely passed or escaped.

Mitigation: Escape or pass AppleScript values safely and review generated send commands before execution.

Risk: Fetching from untrusted custom URLs may pull unsuitable or misleading content into the EPUB.

Mitigation: Use trusted archive URLs, review fetched content before compiling, and avoid custom sources that the user has not approved.

Risk: Cover generation may involve sensitive keychain credentials and third-party API use.

Mitigation: Confirm credential handling and third-party API policy before invoking cover generation.

## Reference(s):

- [Manual Blog-to-Kindle Workflow](references/manual-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/ainekomacx/skills/blog-to-kindle)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown instructions with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce EPUB files, markdown article files, cover prompts, and Kindle delivery steps when executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
