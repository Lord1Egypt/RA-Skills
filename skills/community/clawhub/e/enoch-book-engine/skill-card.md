## Description:

Create or edit books with the Enoch Book Engine, including strict B5 pages, inline SVG diagrams, and mandatory screenshot-based visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwithenoch](https://clawhub.ai/user/aiwithenoch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authors use this skill to create or edit fixed-layout B5 books in an Enoch Book Engine repository while preserving source-file boundaries and visual QA gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to edit book source files and run local npm verification in the target repository.

Mitigation: Review the target repository's scripts before execution when the project is not already trusted.

Risk: Book edits can introduce incorrect facts, misleading prose, clipped diagrams, or poorly contained logos.

Mitigation: Keep source material grounded, run the required verification command, inspect listed screenshots, and only acknowledge visual QA after manual review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiwithenoch/skills/enoch-book-engine)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline file paths and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs local book source edits and requires npm-based verification with screenshot review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
