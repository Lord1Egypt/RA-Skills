## Description: <br>
Set up Blossom Hire, create local work opportunities, and help employers and jobseekers move through Blossom work flows in plain language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbiwu](https://clawhub.ai/user/robbiwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employers, and jobseekers use this skill through an agent to register with Blossom Hire, create or manage local work opportunities, search for jobs, apply to roles, and review candidate or application status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends hiring, job-search, account, address, and application details to Blossom's hosted API and uses a permanent API key with full account access. <br>
Mitigation: Install only if that data sharing is acceptable, keep the API key in runtime memory only, use a unique Blossom passKey, and contact Blossom support to rotate or revoke access if the key may be exposed. <br>
Risk: Marketplace create, update, delete, post, and apply actions can affect real Blossom records. <br>
Mitigation: Review the action summary and require clear user confirmation before sending any mutating request. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/robbiwu/blossom-jobs) <br>
- [Blossom homepage](https://blossomai.org) <br>
- [Blossom privacy policy](https://blossomai.org/privacypolicy.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Plain-language guidance with JSON API payloads and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires runtime-only handling of API keys, person IDs, and address IDs; no local data storage is described.] <br>

## Skill Version(s): <br>
1.0.22 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
