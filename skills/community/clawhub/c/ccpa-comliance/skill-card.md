## Description: <br>
A local CCPA/CPRA compliance helper for checking California consumer privacy obligations, consumer rights workflows, opt-out mechanisms, service-provider requirements, and compliance documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill as a local checklist and report generator for preliminary CCPA/CPRA self-assessment, consumer rights review, opt-out mechanism review, and compliance documentation support. It is not a substitute for professional legal advice. <br>

### Deployment Geography for Use: <br>
United States (California) <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents checklist and pass/fail-style outputs that may be mistaken for legal compliance verification. <br>
Mitigation: Treat outputs as preliminary guidance only and require independent legal review before making CCPA/CPRA compliance decisions. <br>
Risk: Local reports or configuration inputs may contain sensitive personal or business details. <br>
Mitigation: Run the skill locally, restrict access to generated files, and avoid entering sensitive details unless local storage is appropriately protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwumit/ccpa-comliance) <br>
- [CCPA law reference](references/ccpa-law.md) <br>
- [Security check guide](SECURITY_CHECK_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local script outputs in JSON or text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python standard library scripts; generated reports may be written to local files when output paths are provided.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence, CHANGELOG, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
