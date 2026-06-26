## Description: <br>
Bootstrap skill for DiagForge that helps an agent enter the repository, understand the project structure, run the canonical cold-start smoke test, and start the Visio-based drawing workflow safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qweadzchn](https://clawhub.ai/user/qweadzchn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to onboard into the DiagForge workflow, locate the source repository and entry documents, validate the Visio bridge through a smoke test, and begin producing editable Visio diagram assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to clone and operate an external DiagForge repository that is not bundled in the release. <br>
Mitigation: Review or pin the external repository before use and run the smoke test in a prepared local clone. <br>
Risk: The referenced workflow uses VISIO_BRIDGE_TOKEN and can create preview and editable output files. <br>
Mitigation: Keep VISIO_BRIDGE_TOKEN out of logs, commits, and shared transcripts, and run the workflow in an environment where generated PNG and VSDX outputs are expected. <br>


## Reference(s): <br>
- [DiagForge GitHub Repository](https://github.com/qweadzchn/DiagForge) <br>
- [ClawHub Skill Page](https://clawhub.ai/qweadzchn/diagforge-agent-visio-user) <br>
- [Publisher Profile](https://clawhub.ai/user/qweadzchn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of an external DiagForge repository and may result in preview PNG and editable VSDX files after the user runs the referenced workflow.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
