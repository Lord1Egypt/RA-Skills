## Description: <br>
Company Api helps teams using a Tuoluojiang back-office platform query and manage company data such as daily reports, projects, finances, customers, contracts, and products through shell-based API commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-j-j](https://clawhub.ai/user/mr-j-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and operations teams use this skill to configure authenticated access to a Tuoluojiang company platform and run commands for querying or updating operational records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores internal platform API keys, a login password, and token material locally. <br>
Mitigation: Use a least-privilege or test account, verify the configured base URL, and keep generated configuration and token files out of shared, synced, or versioned folders. <br>
Risk: Some commands can create or modify company records. <br>
Mitigation: Review arguments and target environment before running production-changing commands such as project-add, task-add, and product-add. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mr-j-j/company-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, API calls] <br>
**Output Format:** [Shell command output and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local configuration and token cache files during setup; some commands can create or modify company records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
