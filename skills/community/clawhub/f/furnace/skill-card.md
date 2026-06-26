## Description: <br>
Furnace temperature and control manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a small local command-line record and configuration utility for entries stored under ~/.furnace. It should not be treated as a real furnace monitor, furnace controller, or safety-critical industrial workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill name and description suggest furnace temperature or control functionality, while the evidence shows a generic local record and configuration utility. <br>
Mitigation: Use it only for local note-style records and configuration values; do not rely on it for furnace monitoring, furnace control, industrial operations, or safety-critical decisions. <br>
Risk: Records and configuration are stored locally under ~/.furnace by default and can be removed or exported by the script. <br>
Mitigation: Avoid storing secrets or important operational data unless the local data directory, deletion behavior, and export files are acceptable for your environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/furnace) <br>
- [Publisher homepage](https://bytesagain.com) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output and JSONL/CSV file exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local records under ~/.furnace by default; FURNACE_DIR can override the data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
