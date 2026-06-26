## Description: <br>
Manage Edith smart glasses API keys with Unkey. Create, revoke, and list API keys via voice commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samdickson22](https://clawhub.ai/user/samdickson22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Edith smart glasses API keys backed by Unkey, including creating, listing, updating, verifying, and revoking keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent privileged control over Edith API keys. <br>
Mitigation: Install only when agent-managed Edith API keys are needed, use the least-privileged Unkey credential available, and require explicit confirmation before listing, updating, creating, or permanently deleting keys. <br>
Risk: The UNKEY_ROOT_KEY credential can grant broad key-management access if exposed. <br>
Mitigation: Store UNKEY_ROOT_KEY securely and avoid logging, displaying, or pasting it into shared outputs. <br>
Risk: Newly created API keys are returned once and should be treated as secrets. <br>
Mitigation: Show generated keys only to the intended user and avoid retaining them in logs or persistent agent memory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samdickson22/edith-api-keys) <br>
- [Unkey API](https://api.unkey.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface API key material returned by Unkey; generated keys should be handled as secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and shipables.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
