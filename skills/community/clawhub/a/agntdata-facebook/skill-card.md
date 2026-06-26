## Description: <br>
Use one API key to pull Facebook page, group, marketplace, video, post, comment, and ad data as structured JSON for agents, automations, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and data teams use this skill to configure and call agntdata Facebook endpoints for social listening, creator intelligence, marketplace research, ads discovery, alerts, dashboards, and analytics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AGNTDATA_API_KEY and sends submitted Facebook links, queries, IDs, use-case descriptions, and media URLs to a third-party API provider. <br>
Mitigation: Keep AGNTDATA_API_KEY in a secret environment variable and avoid confidential or private data unless the provider and use case are approved. <br>
Risk: Calls to the third-party API may consume credits or create billing exposure. <br>
Mitigation: Monitor agntdata credit and billing limits, and test with narrow queries before broad automation. <br>
Risk: The artifact recommends a related plugin for native tooling, but that plugin is separate from this skill release. <br>
Mitigation: Review the recommended plugin independently before installing or using it. <br>


## Reference(s): <br>
- [agntdata Facebook API Reference](https://agnt.mintlify.app/apis/social/facebook) <br>
- [agntdata Documentation](https://agnt.mintlify.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaencarrodine/agntdata-facebook) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with curl examples and JSON tool schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY; API responses are structured JSON from a credit-based third-party Facebook data API.] <br>

## Skill Version(s): <br>
1.0.15 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
