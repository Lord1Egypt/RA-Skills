## Description:

Runs a guided Cargo quickstart that searches for company lookalikes, people by persona, or fast-growing companies, presents the results, and offers to save the search as a recurring play.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users who are new to Cargo can preview a starter company or people search, review the returned rows and credit cost, and choose whether to save the search as a recurring play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency uses an unpinned latest release and may change in a future update.

Mitigation: Use a reviewed, pinned CLI release and review changes before updating it.

Risk: Search inputs may be sent to AI Ark without a privacy disclosure.

Mitigation: Explain that search inputs go to AI Ark and get the user's approval before sending sensitive information.

Risk: The security scan was partial because two local references could not be resolved.

Mitigation: Review the unresolved references before relying on the scan assessment.

## Reference(s):

- [Cargo Quickstart on ClawHub](https://clawhub.ai/cargo-ai/skills/cargo-quickstart)
- [Cargo skills repository](https://github.com/getcargohq/cargo-skills)
- [Cargo publisher profile](https://clawhub.ai/user/cargo-ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Guided conversation with Cargo CLI commands and a Markdown results table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents up to 25 search results with a credit receipt and offers a recurring play.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
