## Description:

Autonomous freelance job monitoring agent for finding and ranking AI and automation freelance leads, with the included script currently focused on Hacker News Who is Hiring results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanxevo3](https://clawhub.ai/user/lanxevo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and freelancers use this skill to generate a prioritized Markdown digest of potential AI and automation freelance leads. It is useful for lead triage, keyword filtering, and experimenting with a lightweight command-line job scanner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release description claims broader job-board coverage than the included script demonstrates, so results may be incomplete or empty.

Mitigation: Treat the scanner as a rough HN-focused prototype and verify important leads against their original sources before acting.

Risk: The script invokes the authenticated gh CLI and depends on local command availability and credentials.

Mitigation: Review the script before running it in an authenticated environment and run it with credentials limited to the intended read-only discovery workflow.

Risk: The output option writes to a user-supplied path, which could overwrite an existing local file.

Mitigation: Use a dedicated report path and avoid sensitive or important files when passing --output.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, files, guidance]

**Output Format:** [Markdown digest printed to stdout, with optional Markdown file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports keyword, minimum-pay, and output-file command-line options.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
