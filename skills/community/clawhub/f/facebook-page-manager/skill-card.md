## Description: <br>
Manage Facebook Pages via Meta Graph API: create text, photo, and link posts; list page posts; and list, reply to, hide, or delete comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longmaba](https://clawhub.ai/user/longmaba) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to operate Facebook Pages from an agent-assisted workflow, including publishing page content and moderating comments through Meta Graph API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes X/Twitter-to-Facebook digest scripts that are not part of the stated Facebook Page management workflow and require sensitive X AUTH_TOKEN and CT0 cookies. <br>
Mitigation: Review the artifact before installation, do not provide X cookies unless the digest workflow is intentional, and remove the x_digest scripts when they are not needed. <br>
Risk: Facebook Page tokens can authorize publishing and comment moderation actions. <br>
Mitigation: Use only Page tokens whose posting and moderation permissions are acceptable for the target Page, track where tokens.json is stored, and revoke or delete tokens when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longmaba/facebook-page-manager) <br>
- [Graph API Reference](artifact/references/graph-api.md) <br>
- [Meta App Dashboard](https://developers.facebook.com/apps/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API-backed posting and moderation actions that require Meta Page tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
