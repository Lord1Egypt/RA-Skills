## Description: <br>
Manage Facebook Pages via Meta Graph API by posting text, photo, or link content, listing posts, and handling comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Loui1979](https://clawhub.ai/user/Loui1979) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Facebook Page publishing and moderation workflows from an agent-assisted CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish to Facebook Pages and moderate comments using granted Page tokens. <br>
Mitigation: Review posts, target Page IDs, and moderation actions before execution, and grant only the permissions needed for the intended workflow. <br>
Risk: The bundled X/Twitter digest scripts require AUTH_TOKEN and CT0 credentials and an unmanaged bird binary. <br>
Mitigation: Do not provide AUTH_TOKEN or CT0 or run x_digest_* scripts unless that workflow is explicitly desired and the bird binary has been verified. <br>
Risk: Local tokens.json may contain Facebook Page access tokens. <br>
Mitigation: Protect the token file during use and remove it when access is no longer needed. <br>


## Reference(s): <br>
- [Graph API Reference](references/graph-api.md) <br>
- [Meta Developers Apps](https://developers.facebook.com/apps/) <br>
- [ClawHub Skill Listing](https://clawhub.ai/Loui1979/facebook-page-manager-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call Meta Graph API endpoints and may read or write local credential files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
