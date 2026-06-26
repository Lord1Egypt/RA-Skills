## Description: <br>
Codon organizes agent memory as a navigable, zero-dependency filesystem where each item gets a human-readable numbered address such as 10.03-client-name.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pauldub](https://clawhub.ai/user/pauldub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Codon to organize persistent workspace memory as local Markdown files with numbered addresses, indexes, and a fixed taxonomy for people, projects, resources, and work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory files may contain secrets or sensitive personal or business data. <br>
Mitigation: Review the MEMORY directory periodically and avoid storing secrets or sensitive data unless local Markdown storage is acceptable. <br>
Risk: The initializer writes a MEMORY directory and index files into the workspace. <br>
Mitigation: Run initialization only in the intended workspace and inspect the created files after setup. <br>


## Reference(s): <br>
- [Codon homepage](https://github.com/pauldub/codon) <br>
- [ClawHub skill page](https://clawhub.ai/pauldub/codon) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and local Markdown file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains a workspace MEMORY directory with category folders and index Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
