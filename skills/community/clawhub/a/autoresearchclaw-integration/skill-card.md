## Description: <br>
Integrates AutoResearchClaw to autonomously generate conference-ready academic papers from user research topics with real citations and experimental code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nffdasilva](https://clawhub.ai/user/nffdasilva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent install and operate AutoResearchClaw for academic research, literature review, experiment generation, and paper drafting from a research topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A simple research request can trigger installation of external code and execution of an autonomous code-generating research pipeline. <br>
Mitigation: Review or pin the external repository first, run the workflow in an isolated environment, and inspect generated code and research outputs before relying on them. <br>
Risk: The documented workflow uses auto-approval and can reduce user checkpoints during research and experiment generation. <br>
Mitigation: Avoid auto-approval for sensitive work and add explicit review gates before installation, experiment execution, and publication use. <br>
Risk: The workflow may require API keys and optional integrations for memory, messaging, scheduled runs, sub-session spawning, and lesson-to-skill behavior. <br>
Mitigation: Provide credentials only through environment variables or a secret manager, and leave optional integrations disabled unless they are explicitly needed. <br>


## Reference(s): <br>
- [AutoResearchClaw Integration on ClawHub](https://clawhub.ai/nffdasilva/autoresearchclaw-integration) <br>
- [AutoResearchClaw GitHub repository](https://github.com/aiming-lab/AutoResearchClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell and YAML examples, plus generated research artifacts from the external toolchain.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce LaTeX, bibliography files, experiment code, charts, review notes, and citation verification reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
