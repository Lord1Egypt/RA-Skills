## Description: <br>
Academic Suite v1 is a meta-skill for installing and coordinating an academic research and writing pipeline with literature search, research, drafting, integrity checking, peer review, de-AI rewriting, and final formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric-promax](https://clawhub.ai/user/eric-promax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and run a multi-skill academic writing workflow for papers, theses, literature reviews, review and revision, integrity verification, and publication formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The suite updates multiple unpinned agent-skill dependencies during installation, which can change behavior across releases. <br>
Mitigation: Review the dependency list before installation, install only from a trusted publisher, and avoid forced replacement unless intentionally overwriting existing skills. <br>
Risk: The workflow may use sensitive API credentials or knowledge-base paths for literature and knowledge-base access. <br>
Mitigation: Provide only narrowly scoped credentials and paths needed for the current research task. <br>
Risk: Generated academic content can contain incorrect citations, facts, or undeclared AI assistance. <br>
Mitigation: Independently verify citations, data, and facts, and follow institutional or publisher AI-disclosure rules before using outputs. <br>
Risk: The mandatory de-AI rewriting stage may affect academic transparency or alter wording after review. <br>
Mitigation: Use rewriting for style only after integrity review, preserve citations and data, and keep a process record for disclosure and review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eric-promax/academic-suite-v1) <br>
- [Full usage guide](https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration prompts, and generated academic workflow artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request research configuration, knowledge-base paths, API credentials, and user confirmation at gated workflow stages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 3.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
