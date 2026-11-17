## Description:

High-rigor, multi-agent scholarly writing framework based on the PaperOrchestra methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolscience](https://clawhub.ai/user/symbolscience)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, scholarly authors, and agent developers use this skill to structure manuscript projects, capture research ideas, plan literature searches, draft sections, and refine claims against verifiable evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interview and research notes may be persisted into local project files.

Mitigation: Use a dedicated workspace and avoid entering confidential research material unless local persistence is acceptable.

Risk: The skill mutates the local filesystem through its scaffold script.

Mitigation: Review the scaffold script before execution and run it only with simple project directory names in an intended workspace.

Risk: The artifact references an external Emergence API that is not clearly documented in the evidence.

Mitigation: Review the referenced API endpoints and organizational data-handling requirements before using the skill with sensitive projects.

## Reference(s):

- [PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing](https://arxiv.org/abs/2604.05018)
- [Emergence Science OpenAPI schema](https://api.emergence.science/openapi.json)
- [Emergence Science content index](https://api.emergence.science/content/index.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON planning structures, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project files such as idea.md, metadata.json, content.md, README.md, and section drafts.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter and manifest list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
