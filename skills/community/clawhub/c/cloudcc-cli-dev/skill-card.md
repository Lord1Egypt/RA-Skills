## Description: <br>
CloudCC CLI Dev helps agents break down CloudCC CRM customization requirements and use cloudcc-cli (`cc`) to create, pull, and publish custom objects, fields, menus, applications, backend classes, schedules, triggers, and Vue custom components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[androidxhm](https://clawhub.ai/user/androidxhm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CloudCC implementation teams use this skill to translate CRM business requirements into concrete CloudCC assets and execute the supporting `cc` CLI workflows. It supports planning, environment setup, object and field modeling, backend logic, scheduled jobs, triggers, and Vue custom component work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a global `cloudcc-cli` package, which may change the local developer environment or introduce package supply-chain risk. <br>
Mitigation: Use a verified or pinned `cloudcc-cli` package before installation and prefer a controlled developer environment. <br>
Risk: `cc` create, publish, and upload workflows can modify CloudCC CRM assets when run with developer credentials. <br>
Mitigation: Use a non-production CloudCC environment first, confirm the target org and environment, review affected assets, and define a rollback plan before execution. <br>
Risk: Developer credentials and safety tokens may be exposed if copied into generated output, code, or commits. <br>
Mitigation: Use least-privilege credentials, keep secrets out of generated files and source control, and review outputs before publishing or committing. <br>


## Reference(s): <br>
- [Requirements Breakdown](artifact/REQUIREMENTS_BREAKDOWN.md) <br>
- [Install and Bootstrap](artifact/INSTALL_AND_BOOTSTRAP.md) <br>
- [Objects and Fields](artifact/OBJECTS_AND_FIELDS.md) <br>
- [Backend Code](artifact/BACKEND_CODE.md) <br>
- [Vue Custom Component](artifact/VUE_CUSTOM_COMPONENT.md) <br>
- [CLI Cheatsheet](artifact/CLI_CHEATSHEET.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command snippets, configuration notes, and code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CloudCC asset plans, generated code snippets, and `cc` command sequences for the selected workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
