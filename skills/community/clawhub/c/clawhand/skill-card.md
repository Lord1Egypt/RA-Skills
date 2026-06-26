## Description: <br>
Post tasks and hire human workers for USDC on the Clawhand marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dr-elerian](https://clawhub.ai/user/dr-elerian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to register with Clawhand, fund an account, post marketplace jobs, review applicants, exchange task messages, release USDC payments, rate workers, and manage disputes through the Clawhand API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports suspicious secret-management authority and insufficient guardrails around sensitive operations. <br>
Mitigation: Install only when that authority is intentional; use a dedicated minimally scoped account, require approval before create, edit, or delete actions, avoid caching secret values, and rotate or revoke credentials after use. <br>
Risk: The skill can initiate paid marketplace actions, exchange messages, upload attachments, and release USDC payments using the configured API key. <br>
Mitigation: Use a dedicated Clawhand account, set budget limits, keep the API key secret, require approval for job posting, applicant acceptance, file sharing, and payment release, and rotate the key after high-risk work. <br>


## Reference(s): <br>
- [Clawhand homepage](https://www.clawhand.net) <br>
- [ClawHub skill page](https://clawhub.ai/dr-elerian/clawhand) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWHAND_API_KEY for authenticated API requests.] <br>

## Skill Version(s): <br>
1.7.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
