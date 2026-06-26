## Description: <br>
AutoCraft helps product managers and development teams plan, execute, and verify software projects through design-document workflows, task APIs, agent execution guidance, and validation templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robin-chen2025](https://clawhub.ai/user/robin-chen2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, and development teams use AutoCraft to turn requirements into design documents, development plans, task tickets, agent execution requests, and verification reports for software delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads and runs unpinned external project code and installs dependencies. <br>
Mitigation: Review the external repository and dependency files first, pin a known commit, and run installation only in an isolated disposable development workspace. <br>
Risk: The installer starts backend and frontend network services. <br>
Mitigation: Bind services to localhost, restrict ports, and avoid using production credentials until the workflow is trusted. <br>


## Reference(s): <br>
- [AutoCraft ClawHub Page](https://clawhub.ai/robin-chen2025/autocraft) <br>
- [AutoCraft Skill Instructions](artifact/SKILL.md) <br>
- [AutoCraft Changelog](artifact/CHANGELOG.md) <br>
- [Design Specification Overview](artifact/references/design-specs/\u8bbe\u8ba1\u9636\u6bb5\u6587\u6863\u89c4\u8303-\u603b\u7eb2.md) <br>
- [Sub-Agent Guide](artifact/references/ac-agent-guide/SKILL.md) <br>
- [Task Creator Guide](artifact/references/task-creator/SKILL.md) <br>
- [Architecture Check Tool](artifact/scripts/architecture-check/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, code templates, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes document specifications, validation checklists, FastAPI templates, pytest configuration, and architecture-check scripts.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; skill body updated 2026-05-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
