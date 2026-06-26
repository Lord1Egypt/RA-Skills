## Description: <br>
Automates research by conducting literature searches, running experiments, and generating LaTeX papers from detailed research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donwrightdesigns](https://clawhub.ai/user/donwrightdesigns) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research teams use this skill to turn a detailed research topic into a structured autonomous run that searches literature, designs and executes experiments, and prepares paper artifacts. It is best suited for users who can review generated code, citations, and research outputs before relying on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate and execute code during autonomous research runs. <br>
Mitigation: Run it in Docker mode when feasible, set network_policy to none for untrusted topics, and review generated code and commands before execution. <br>
Risk: The skill may call external LLM and search services and use credentials from environment variables. <br>
Mitigation: Use a disposable workspace with minimal secrets, provide only the credentials needed for a run, and disable OpenCode, ACP, or agentic modes unless they are required. <br>
Risk: Auto-approval can bypass human gates for topics or experiments that need review. <br>
Mitigation: Avoid --auto-approve for untrusted, sensitive, or high-impact research topics and inspect citations, experiment results, and paper claims before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/donwrightdesigns/auto-research-claw) <br>
- [README](README.md) <br>
- [Integration Guide](docs/integration-guide.md) <br>
- [Tester Guide](docs/TESTER_GUIDE.md) <br>
- [Example Configuration](config.researchclaw.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, LaTeX, BibTeX, JSON reports, generated experiment code, shell commands, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces research artifacts that require human review, especially generated code, experiment results, citations, and claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
