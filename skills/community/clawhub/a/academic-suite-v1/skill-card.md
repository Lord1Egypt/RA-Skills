## Description:

Complete Academic Research & Writing Suite: one-click installation for the Academic Pipeline ecosystem with literature search, research, drafting, review, integrity checking, humanization, and publication formatting dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-promax](https://clawhub.ai/user/eric-promax)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and academic writers use this meta-skill to install and start a full academic research and writing workflow. It helps coordinate literature search, deep research, paper drafting, integrity checks, peer review, revision, humanization, and final document generation through dependent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can replace multiple local OpenClaw skills through forced installation of unpinned dependencies.

Mitigation: Review each dependency separately and avoid forced installation unless replacing existing skills is intended.

Risk: The workflow includes a mandatory de-AI or humanization stage that could be misused to conceal AI assistance in academic work.

Mitigation: Use humanization only for style editing and follow institutional disclosure and academic integrity requirements.

Risk: Research topics, drafts, uploaded files, IMA paths, and API-backed searches may contain sensitive information.

Mitigation: Treat those inputs as sensitive and review dependency privacy controls before using the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eric-promax/skills/academic-suite-v1)
- [Publisher profile](https://clawhub.ai/user/eric-promax)
- [Complete usage guide](https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg)
- [GitHub repository](https://github.com/eric-promax/academic-agents.git)
- [GitHub issues](https://github.com/eric-promax/academic-agents/issues)
- [ClawHub discussions](https://clawhub.ai/eric-promax/academic-suite/discussions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and conversational guidance with inline shell commands and configuration prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide multi-stage academic workflows and final document generation through installed dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports suite version 3.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
