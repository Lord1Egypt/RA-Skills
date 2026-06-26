## Description: <br>
Manage document generation, storage, and tracking with automatic URL generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[171622474](https://clawhub.ai/user/171622474) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create, index, version, list, update, and archive Markdown documents with generated metadata and direct access URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documents may be reachable through the configured HTTP server. <br>
Mitigation: Use only for content intended for that server, and verify authentication, access restrictions, deletion behavior, and server ownership before storing sensitive or unreleased material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/171622474/doc-manager) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, JSON metadata, index text, and direct URL strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes document files under /home/node/clawd/docs and returns URLs using the configured HTTP base URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
