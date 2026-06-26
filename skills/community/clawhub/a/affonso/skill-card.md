## Description: <br>
Manage affiliate marketing programs via the Affonso CLI: create affiliates, track referrals, handle commissions, process payouts, and configure program settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zilvestro](https://clawhub.ai/user/zilvestro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External affiliate program operators and developers use this skill to administer Affonso programs from an agent workflow, including affiliate onboarding, referral tracking, commission review, payout processing, coupon management, and program configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live authority over payouts, commissions, program settings, credentials, and tracking data. <br>
Mitigation: Use a least-privilege API key where available, store it in environment variables or a secret manager, and confirm every payout, approval, deletion, commission, and settings change before execution. <br>
Risk: Affiliate and referral workflows may involve email, IP, user-agent, and referral tracking data. <br>
Mitigation: Operate the skill only under applicable privacy notices, consent requirements, and internal data-handling policies. <br>
Risk: Headless environments cannot complete browser-based authentication. <br>
Mitigation: Authenticate with AFFONSO_API_KEY and verify access with affonso whoami --json; do not use affonso login. <br>


## Reference(s): <br>
- [Affonso Homepage](https://affonso.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/zilvestro/affonso) <br>
- [Command Reference](references/COMMAND_REFERENCE.md) <br>
- [Program Settings Guide](references/PROGRAM_SETTINGS_GUIDE.md) <br>
- [Workflow Recipes](references/WORKFLOWS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json, avoid browser login, and request confirmation before destructive or payout-related actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
