## Description: <br>
Clovercli helps agents guide CloverCLI usage for Clover POS inventory, orders, payments, customers, employees, discounts, reports, and related merchant data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to install and run CloverCLI commands for Clover POS account management, reporting, exports, and merchant data inspection or updates. <br>

### Deployment Geography for Use: <br>
US, Europe, Latin America, and sandbox environments, based on the documented Clover region options. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Clover POS credentials and merchant account access. <br>
Mitigation: Use the least-privileged token available, avoid storing long-lived credentials in shell startup files, and install only after trusting the external CloverCLI package. <br>
Risk: Create, delete, raw API, and export commands can affect POS data or expose business records. <br>
Mitigation: Confirm high-impact actions before execution, protect exported reports, and review raw API requests before running them. <br>
Risk: The artifact includes an embedded known-client merchant ID. <br>
Mitigation: Ignore or remove the known-client merchant ID before operational use. <br>


## Reference(s): <br>
- [ClawHub Clovercli listing](https://clawhub.ai/G9Pedro/clovercli) <br>
- [npm package: @versatly/clovercli](https://www.npmjs.com/package/@versatly/clovercli) <br>
- [GitHub repository: Versatly/clovercli](https://github.com/Versatly/clovercli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CloverCLI command examples, environment variable setup, export options, and safety reminders for credentialed POS operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact describes CloverCLI package version 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
