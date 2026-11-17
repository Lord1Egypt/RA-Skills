## Description:

Keep project documentation in sync with code changes by identifying affected docs, drafting targeted updates, and maintaining doc site structure for mkdocs, docusaurus, and vitepress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chriscox](https://clawhub.ai/user/chriscox)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to identify documentation affected by code changes, draft focused updates, maintain documentation site navigation, and audit stale docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct-apply mode can modify documentation files, update doc-site navigation, and create local branch commits.

Mitigation: Use review-first mode for sensitive repositories and inspect proposed diffs before applying or committing changes.

Risk: Issue mode can create a GitHub issue through the authenticated gh session.

Mitigation: Confirm the target repository and review the issue title and body before asking the skill to create an issue.

Risk: Generated documentation updates can be incomplete or misleading if the underlying code changes are misunderstood.

Mitigation: Review generated changes against the relevant diffs and keep edits focused on the documented behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with proposed file edits, shell commands, and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or directly apply documentation edits, update doc-site navigation, create branch commits, or create GitHub issues depending on user preference.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
