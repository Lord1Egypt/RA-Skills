## Description:

Uses analogies to explain complex medical concepts in accessible terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to generate accessible educational explanations and analogies for supported medical concepts for child, patient, or student audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --output path can overwrite arbitrary writable files available to the local Python process.

Mitigation: Run the skill in a sandbox or workspace-only environment and avoid absolute paths or parent-directory paths for --output.

Risk: Medical explanations may be mistaken for clinical advice because the medical-use limits are under-disclosed.

Mitigation: Treat outputs as educational summaries and require qualified clinical review before using them for healthcare decisions.

## Reference(s):

- [Concept Explainer ClawHub listing](https://clawhub.ai/aipoch-ai/skills/concept-explainer)
- [Concept Explainer - References](references/guidelines.md)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [JSON printed to stdout or written to a user-provided output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes concept, explanation, analogy, and audience fields; listing mode prints available concepts.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact/SKILL.md frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
