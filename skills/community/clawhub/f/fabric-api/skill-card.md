## Description: <br>
Create, search, and manage Fabric resources via the Fabric HTTP API (notepads/notes, folders, bookmarks, files, tags). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to read, create, search, upload, delete, and recover content in a Fabric workspace through the Fabric HTTP API. It is useful when an agent needs Fabric-aware request guidance, API payload examples, or cross-platform helper commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change content in a user's Fabric workspace when given a Fabric API key. <br>
Mitigation: Use a scoped or revocable Fabric API key where available, keep the key out of prompts and logs, and install only for agents that should manage Fabric workspace content. <br>
Risk: Delete, recover, bulk-write, and file-upload operations can modify workspace state. <br>
Mitigation: Review these operations and their payloads before execution, and avoid blind retries on create or write operations that could duplicate content. <br>
Risk: Changing FABRIC_BASE or using --with-key on arbitrary absolute URLs could send credentials to an unintended endpoint. <br>
Mitigation: Keep FABRIC_BASE pointed at the real Fabric API unless intentionally using another trusted endpoint, and avoid --with-key for untrusted absolute URLs. <br>


## Reference(s): <br>
- [Fabric homepage](https://fabric.so) <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/fabric-api) <br>
- [OpenAPI spec](artifact/fabric-api.yaml) <br>
- [Fabric API skill reference](artifact/references/REFERENCE.md) <br>
- [Troubleshooting Fabric API requests](artifact/references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Fabric HTTP API through Node or Python helper scripts and print JSON or text response bodies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
