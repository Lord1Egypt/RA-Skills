## Description:

Diagnose why a configured Alibaba Cloud WAF 3.0 custom protection rule is not taking effect by running read-only configuration checks, identifying the first broken link in the rule-template-object chain, and returning the relevant console fix path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External support engineers, cloud operations teams, and developers use this skill to investigate Alibaba Cloud WAF 3.0 custom rule effectiveness issues without changing customer configuration. It is intended for cases such as rules not taking effect, rules matching logs but not blocking, missed expected blocks, and CC or rate-limiting behavior that does not trigger or bans too broadly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance is broader and riskier than the stated WAF-only purpose.

Mitigation: Review setup steps before use, prefer verified or package-manager installation, avoid curl-to-bash where possible, and keep CLI plugins updated from trusted sources.

Risk: Credential or cloud access could exceed the read-only WAF investigation scope.

Mitigation: Use a least-privilege WAF read-only RAM policy, do not grant Modify/Create/Delete permissions, avoid command-line secrets, and check only credential status rather than exposing keys.

Risk: Incorrect or incomplete evidence could lead to misleading remediation advice.

Mitigation: Treat script output as evidence rather than final judgement, cite actual returned fields, mark failed or empty queries as not retrieved, and deliver any write action only as a console path for customer confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-rule-effectiveness-check)
- [Scenario Description](references/scenario-description.md)
- [Verification Method](references/verification-method.md)
- [CLI Commands and Key Fields](references/related-commands.md)
- [Read-Only RAM Policy](references/ram-policies.md)
- [Effectiveness Chain and Common Root Causes](references/effectiveness-chain-basics.md)
- [Symptom Checklists and Log Corroboration](references/symptom-checklists.md)
- [Remediation Table](references/remediation-table.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON reports from the bundled checker script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only WAF checks; reports should cite retrieved field values, note unretrieved evidence, and identify the first failing effectiveness element when available.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
