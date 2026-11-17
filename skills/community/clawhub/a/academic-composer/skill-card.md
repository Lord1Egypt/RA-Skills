## Description:

Assists with academic research and writing by collecting sources, building evidence-mapped outlines, drafting cited essays, and optionally improving style with local analysis.

This skill is for research and development only.

## Publisher:

[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and educators use this skill to find academic source metadata, create source-mapped outlines, format citations, and prepare research drafts or study aids. It is not intended for submitting AI-generated work as original academic assessment content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command templates may include user-controlled topics or DOI strings.

Mitigation: Review before installation, use an isolated environment, and pass user input through stdin or safely constructed argument arrays instead of shell interpolation.

Risk: Essay content may be transmitted to a remote LLM provider depending on the host agent configuration.

Mitigation: Avoid pasting sensitive or private essay text unless the agent's LLM data flow is understood; use a local model when content must remain on-device.

Risk: A predictable temporary essay path such as /tmp/essay.txt can expose or overwrite draft content on shared systems.

Mitigation: Prefer stdin or a unique, access-controlled temporary file for local style analysis.

Risk: The skill can be misused to submit AI-generated work as original academic work.

Mitigation: Keep the academic integrity disclaimer visible and limit use to research drafts, study aids, source organization, and citation learning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin0818-lxd/skills/academic-composer)
- [Publisher profile](https://clawhub.ai/user/kevin0818-lxd)
- [Project homepage](https://github.com/kevin0818-lxd/academic-composer)
- [Security and intended use](SECURITY.md)
- [Essay templates](skill/references/essay_templates.md)
- [Citation formatting rules](skill/references/citation_formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown with cited essay drafts, source lists, outlines, citation sections, and optional style-analysis tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local Python scripts for Semantic Scholar metadata search and local style analysis; essay generation and rewriting depend on the host agent's LLM configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
