## Description: <br>
Post and manage real-time corkboard pins, lamp cues, deleted-history recovery, and multi-track project pipeline work for the Carl's Corkie dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zheroz00](https://clawhub.ai/user/zheroz00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to post actionable tasks, alerts, links, briefings, project handoffs, and recovery actions to a corkboard dashboard through shell helpers or REST API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer clones a project, installs dependencies, builds it, and can start a persistent local dashboard service. <br>
Mitigation: Install only when the referenced project is trusted, review the install and start steps before use, and check existing installations before reinstalling. <br>
Risk: The dashboard uses a bearer token and can bind to a network interface, which may expose the API if configured broadly. <br>
Mitigation: Keep CORKBOARD_TOKEN and .env private, prefer localhost binding unless LAN access is required, and do not expose the dashboard port directly to the public internet. <br>
Risk: Authentication can be disabled by configuration. <br>
Mitigation: Avoid CORKBOARD_AUTH=disabled unless a separate reverse-proxy authentication layer is already protecting the API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zheroz00/corkboard-dashboard) <br>
- [API Reference](references/api.md) <br>
- [Setup Guide](references/setup.md) <br>
- [Pin Types Reference](references/pin-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash and curl examples; API calls return JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates corkboard pins, projects, lamp states, and deleted-history restore actions through authenticated dashboard API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
