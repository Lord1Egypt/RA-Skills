## Description:

Study unfamiliar codebases and produce evidence-backed knowledge artifacts. Use for repository orientation, architecture mapping, subsystem tracing, onboarding, or codebase documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to study unfamiliar repositories, map architecture and behavior, and produce source-cited onboarding or documentation artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository analysis can produce unsupported or misleading conclusions if the agent overstates weak evidence.

Mitigation: Require source citations, evidence labels, confidence notes, exclusions, and unresolved questions for material claims.

Risk: Repository review can expose secrets or sensitive values if the agent reads or reproduces sensitive files.

Mitigation: Exclude likely secret stores by default and redact sensitive values when recording evidence.

Risk: Inspecting unfamiliar repositories can lead to unnecessary code execution, dependency installation, network fetching, or writes.

Mitigation: Keep repository study read-only by default and require explicit authorization before execution, dependency installation, network access, sensitive-file access, or target writes.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/OthmanAdi/codebase-knowledge-builder/tree/main/skills/codebase-knowledge-builder)
- [ClawHub skill page](https://clawhub.ai/othmanadi/skills/codebase-knowledge-builder)
- [Reconnaissance checklist](references/recon-checklist.md)
- [Deep-dive methodology](references/deep-dive-methodology.md)
- [Knowledge artifact template](templates/knowledge_artifact.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown knowledge artifact with source citations and evidence labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Revision-specific and evidence-backed; excludes secrets by default.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
