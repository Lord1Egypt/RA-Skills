## Description: <br>
Universal CLI discovery gateway - one skill to manage all CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dull-bird](https://clawhub.ai/user/dull-bird) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to look up, register, search, and invoke local command-line tools through a structured registry instead of relying on stale model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad ability to discover local CLI tools, run help commands, and persist information about command-line tools. <br>
Mitigation: Keep command approval enabled, register trusted tools selectively, and review registry entries for untrusted binaries before relying on them. <br>
Risk: Bulk discovery can inventory local tools on sensitive or production machines. <br>
Mitigation: Avoid bulk discovery on sensitive or production machines and use targeted registration for specific tools instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dull-bird/clihub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown text with inline shell commands and JSON registry details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local CLI registry entries when registration or discovery commands are run.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
