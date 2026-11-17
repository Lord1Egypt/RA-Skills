## Description:

Codebase intelligence that generates structured navigation maps with file:line references so agents can avoid repeatedly scanning the same files during code exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keshav55](https://clawhub.ai/user/keshav55)

### License/Terms of Use:


## Use Case:

Developers and coding agents use Atris to build and maintain an `atris/MAP.md` navigation index for a repository, then consult that map before searching code. The skill is used for codebase exploration, locating symbols and entry points, and onboarding to unfamiliar projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated `atris/MAP.md` may include secrets, private paths, or sensitive architecture details if committed or shared without review.

Mitigation: Review `atris/MAP.md` before committing or sharing it, and remove secrets, credentials, private paths, and sensitive architecture notes.

Risk: Navigation guidance can become stale after code moves, deletions, or major refactors.

Mitigation: Update map entries surgically when files change, and regenerate affected sections when references are clearly stale.

## Reference(s):

- [Atris ClawHub skill page](https://clawhub.ai/keshav55/skills/atris)
- [Publisher profile](https://clawhub.ai/user/keshav55)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown navigation map with file:line references and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates `atris/MAP.md` in the target repository; requires ripgrep (`rg`) for scanning.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
