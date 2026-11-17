## Description:

Feynman Lobster reads a user's project code and notes, then teaches relevant concepts and asks Feynman-style questions when the project context calls for it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lysandre001](https://clawhub.ai/user/lysandre001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this OpenClaw skill to create project-based learning contracts, connect local code or notes as context, and receive contextual explanations, progress checks, and Feynman-style questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local web panel can expose stored project and profile data through an unauthenticated local API.

Mitigation: Use the panel only in trusted local environments and require a per-launch token before using it with sensitive projects.

Risk: Dashboard rendering may display stored data unsafely.

Mitigation: Escape stored dashboard data before enabling the panel for sensitive work.

Risk: The skill can summarize selected local code and notes into persistent local contract, profile, and memory files.

Mitigation: Only provide paths you are comfortable having read and summarized, use an isolated workspace for sensitive projects, and confirm how to delete generated state files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lysandre001/skills/feynman-lobster)
- [PyTorch documentation](https://docs.pytorch.org/docs/stable/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with occasional JSON snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local contract, profile, and project-memory files in the user's OpenClaw workspace while treating referenced project resources as read-only context.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
