## Description: <br>
Creates AI-friendly project structures using progressive disclosure indexing, including AGENTS.md, module INDEX.md files, llms.txt, and file intent headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[in12hacker](https://clawhub.ai/user/in12hacker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assisted engineering teams use this skill to create or maintain repository navigation files, module indexes, intent headers, and related documentation so agents can find code and assess modification impact efficiently. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated navigation files and intent headers can steer future agent behavior and may become misleading if stale or too broad. <br>
Mitigation: Review generated guidance before committing it, scope it to the repository, and keep Tier A indexes updated atomically with related code changes. <br>
Risk: Repository guidance files can accidentally disclose sensitive project details if created from private context without review. <br>
Mitigation: Check generated AGENTS.md, INDEX.md, llms.txt, and file headers for secrets or inappropriate internal details before publication. <br>


## Reference(s): <br>
- [Index Templates](references/index-templates.md) <br>
- [Index Maintenance](references/index-maintenance.md) <br>
- [Documentation Standards](references/doc-standards.md) <br>
- [Language Adaptation](references/language-adaptation.md) <br>
- [Naming & API Conventions](references/naming-api-conventions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance, repository documentation files, and code comments or headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update AGENTS.md, module INDEX.md files, llms.txt, documentation indexes, and file intent headers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
