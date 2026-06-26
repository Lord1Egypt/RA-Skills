## Description: <br>
Check domain availability via Vercel and buy/manage domains via Vercel CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check Vercel domain availability, review pricing, and prepare Vercel CLI commands for domain management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct token-backed domain purchase commands can spend money without a clear confirmation gate. <br>
Mitigation: Require explicit approval for the exact domain and cost before purchase commands run, and prefer the interactive Vercel CLI purchase flow. <br>
Risk: The skill relies on the user's authenticated Vercel CLI session for live domain operations. <br>
Mitigation: Use an account or team context with appropriate permissions and review proposed domain-management commands before execution. <br>


## Reference(s): <br>
- [Domain Check on ClawHub](https://clawhub.ai/BrennerSpear/domain-check) <br>
- [Vercel Registrar price endpoint](https://api.vercel.com/v1/registrar/domains/example.com/price) <br>
- [Vercel Registrar domains endpoint](https://api.vercel.com/v1/registrar/domains) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Vercel CLI authentication for live domain operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
