## Description:

CapForge helps agents scan GitHub repositories, extract reusable capability documentation, classify capability domains, validate documentation structure, and synchronize repositories with a read-only default posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldx-person](https://clawhub.ai/user/ldx-person)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use CapForge to inspect open-source repositories and turn code structure into reusable Markdown capability assets, domain summaries, validation reports, and transformation-plan drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims to avoid unreviewed remote execution, but the artifact still includes unpinned npm/npx command examples.

Mitigation: Install and use a pinned, reviewed capforge CLI version and replace npx examples with the installed capforge binary before running the workflow.

Risk: CapForge imports repositories and writes generated Markdown files under ~/.capforge by default, which can change local disk state.

Mitigation: Show each command to the user first, confirm the target repository and workspace, and set CAPFORGE_WORKSPACE or --workspace when isolation is needed.

Risk: Generated capability and transformation-plan documents may be incomplete or misleading if accepted without review.

Mitigation: Review generated Markdown against the scanned repository before using it for implementation, selection, or publication decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ldx-person/skills/capforge)
- [CapForge Homepage](https://github.com/ldx-person/capforge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository capability notes, domain summaries, validation reports, and transformation-plan drafts under the configured CapForge workspace.]

## Skill Version(s):

1.3.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
