## Description: <br>
Aria2 Downloader helps an agent add and manage aria2 download tasks for magnet links, torrent files, and HTTP file URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahiven](https://clawhub.ai/user/ahiven) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to control a local aria2 RPC service from an agent, including adding downloads, checking task status, pausing, resuming, and removing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill examples include a concrete aria2 RPC token. <br>
Mitigation: Replace the token before use and prefer an environment variable or protected local configuration for the RPC secret. <br>
Risk: The skill relies on an aria2 RPC service that can control downloads. <br>
Mitigation: Keep the RPC service bound to localhost or otherwise protected, and avoid exposing it to untrusted networks. <br>
Risk: The advertised completion workflow can transfer files to 115 cloud storage and delete local files through a separate host hook. <br>
Mitigation: Inspect the hook script before enabling it, restrict it to a dedicated download directory, and confirm that local deletion is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahiven/aria2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided download URLs, torrent files, or magnet links against a host aria2 RPC service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
