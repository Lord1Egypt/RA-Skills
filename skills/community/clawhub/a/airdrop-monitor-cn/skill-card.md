## Description: <br>
Airdrop Monitor CN monitors project announcement and documentation pages for content changes, extracts deadline clues, identifies high-risk keywords and suspicious links, and outputs an actionable daily task list for repeatable local airdrop monitoring with optional billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dll-create](https://clawhub.ai/user/dll-create) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor airdrop-related project sources, detect page changes and deadline clues, flag risky links or private-key language, and produce a daily action report. Operators can run it locally for free or configure the disclosed SkillPay billing flow for paid use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Billing credentials enable live SkillPay charges or payment-link generation without a separate per-run confirmation. <br>
Mitigation: Leave SKILL_BILLING_API_KEY and SKILL_ID unset for free local monitoring, and enable them only in an environment intended for paid operation. <br>
Risk: Running the cron example with billing credentials can produce repeated charges as the monitor executes on schedule. <br>
Mitigation: Use cron only after confirming the billing amount, intended user identifier, and execution frequency; keep paid cron jobs separate from local free runs. <br>
Risk: verify_billing.py can call live balance, charge, and payment-link endpoints for the supplied user id. <br>
Mitigation: Use only test accounts or known disposable user ids for billing verification until a dry-run or explicit confirmation safeguard is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dll-create/airdrop-monitor-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown daily monitoring report, optional JSON result object, and setup or billing commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include changed sources, deadline clues, risk warnings, priority actions, and optional payment-required metadata when billing is enabled.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
