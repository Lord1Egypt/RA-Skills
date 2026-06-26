## Description: <br>
Bambuddy provides an agent-facing REST API reference for managing a self-hosted Bambuddy instance for Bambu Lab 3D printers, including printer status, print archives, queues, filament, camera snapshots, smart plugs, settings, system info, and related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdstudios](https://clawhub.ai/user/zdstudios) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and control a self-hosted Bambuddy server from an agent, including printer monitoring, archive and queue management, settings, and administrative workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A powerful Bambuddy API key can control printers, manage Bambuddy data, change settings, and administer API keys. <br>
Mitigation: Use a dedicated least-privilege API key, prefer read-only permissions for monitoring, and require explicit confirmation before destructive or printer-control actions. <br>
Risk: Camera snapshots, support bundles, discovery, and smart plug actions can expose operational data or affect local devices. <br>
Mitigation: Run the skill only against a trusted Bambuddy server and confirm before saving snapshots, downloading support bundles, using discovery, or toggling smart plugs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zdstudios/bambuddy) <br>
- [Publisher profile](https://clawhub.ai/user/zdstudios) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAMBUDDY_URL, BAMBUDDY_API_KEY, curl, and jq; binary endpoints may produce downloaded files such as camera snapshots or support bundles.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
