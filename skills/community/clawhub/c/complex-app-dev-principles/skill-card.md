## Description: <br>
Guides developers through modular complex-app development using staged design, independent modules, confirmation-based locking, sequential testing, and final verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smxtx](https://clawhub.ai/user/smxtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan, scaffold, test, lock, and review modules for complex app builds or refactors. It is especially oriented toward modular APP workflows that require clear interfaces, staged confirmation, and final delivery checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local helper scripts can create module folders, README files, lock records, and symlinks in the working project. <br>
Mitigation: Run scripts only from the intended project directory and review generated changes in version control before accepting them. <br>
Risk: The workflow may influence cleanup or refactoring decisions during modular development. <br>
Mitigation: Review proposed cleanup, locking, and refactoring changes against project requirements before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smxtx/complex-app-dev-principles) <br>
- [Module Design Template](references/module_design_template.md) <br>
- [API Specification](references/api_specification.md) <br>
- [Test Case Template](references/test_case_template.md) <br>
- [Delivery Checklist](references/delivery_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with optional generated project files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create module folders, README files, lock records, and symlinks when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
