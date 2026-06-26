## Description: <br>
Query and manage personal finances via the official Actual Budget Node.js API for budget queries, transaction imports and exports, account management, categorization, rules, schedules, and bank sync for self-hosted Actual Budget instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thisisjeron](https://clawhub.ai/user/thisisjeron) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and manage a self-hosted Actual Budget instance through the official Node.js API while keeping credentials in the runtime environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change financial records when provided Actual Budget credentials. <br>
Mitigation: Store credentials outside chat and repositories, back up the budget, and require clear confirmation before imports, account changes, rules, schedules, bank sync, or api.sync(). <br>
Risk: Financial data and credentials may be exposed in agent responses or generated scripts. <br>
Mitigation: Redact passwords, sync IDs, encryption passwords, raw account data, and full transaction exports unless the user explicitly requests sensitive output. <br>


## Reference(s): <br>
- [Actual Budget ClawHub release](https://clawhub.ai/thisisjeron/actual-budget) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only analysis, proposed mutations, and credential-handling guidance for Actual Budget workflows.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
