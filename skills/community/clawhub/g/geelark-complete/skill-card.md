## Description: <br>
All-in-one Skill fuer GeeLark: Setup, lokale API, nativer Sync-Transport, UI/RPA-Fallback, Posting-Flow, Verifikation und Troubleshooting in einem durchgaengigen Runbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pagebabe](https://clawhub.ai/user/Pagebabe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run GeeLark setup, local API checks, native sync workflows, UI/RPA fallback steps, posting preparation, verification, and troubleshooting from one operational runbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad local GeeLark automation using credentials and helper scripts. <br>
Mitigation: Install only in a trusted local GeeLark environment, inspect the helper scripts before use, and use a least-privilege GeeLark token. <br>
Risk: Credential, session, phone_id, proxy, or private profile data could be exposed through logs, command history, or persistent memory. <br>
Mitigation: Keep GEELARK_API_KEY out of logs and command history, and do not let the agent save sensitive operational data to memory unless explicitly intended. <br>
Risk: Write actions or UI automation may affect the wrong workspace, profile, or browser state. <br>
Mitigation: Confirm the exact workspace and profile before write or UI actions, and require the skill's documented verification checks after each step. <br>


## Reference(s): <br>
- [GeeLark Complete on ClawHub](https://clawhub.ai/Pagebabe/geelark-complete) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational verification and troubleshooting guidance; users must review local helper scripts and credentials handling before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
