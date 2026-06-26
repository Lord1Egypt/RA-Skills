## Description: <br>
Manage Bring! shopping lists by helping users set up credentials, select a default list, and add, view, check off, uncheck, or remove grocery-list items through Bring!'s API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maikimolto](https://clawhub.ai/user/maikimolto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Bring! accounts use this skill through an agent to configure local credentials and manage shopping-list items, including shared lists and a default list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Bring! credentials and cached tokens that grant ongoing account access from the local machine. <br>
Mitigation: Prefer terminal-based credential entry, keep the local credentials and token files owner-only, and treat both files as secrets. <br>
Risk: Remove operations permanently delete list items and changes sync immediately to shared Bring! lists. <br>
Mitigation: Confirm destructive actions with the user, especially on shared lists or batch removals. <br>
Risk: Server security evidence marks the release suspicious and advises trusted-context installation. <br>
Mitigation: Install only in a trusted staff or developer context and follow the server-provided security guidance before approving privileged workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maikimolto/bring-list) <br>
- [Bring! website](https://getbring.com) <br>
- [Bring! API endpoint used by the skill](https://api.getbring.com/rest) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; writes local credential and token files when configured.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
