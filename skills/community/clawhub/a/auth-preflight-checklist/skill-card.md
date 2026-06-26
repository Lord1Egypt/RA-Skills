## Description: <br>
Preflight checklist for auth-dependent work: verify the active credential lane, runtime environment, scopes, and smallest safe live probe before writing, deploying, or debugging provider integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill before auth-dependent work to verify the active credential lane, runtime environment, access scopes, and smallest safe live probe before writes, deploys, or provider debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for workflows involving credential names, vault item references, OAuth session context, and provider metadata. <br>
Mitigation: Allow the agent to inspect only the minimum credential context needed for the task, keep probes read-only and scoped to the intended account, repo, database, app, or service, and never print secret values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/auth-preflight-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown checklist with command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable install behavior; probes should be read-only and should not print secret values.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
