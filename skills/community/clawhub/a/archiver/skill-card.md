## Description: <br>
Use the Archiver library for streaming archive packaging in Node.js, including ZIP/TAR archives, streams, strings, buffers, file paths, directories, glob patterns, and custom formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to write Node.js archive-packaging code and guidance for ZIP/TAR creation, streaming downloads, directory packaging, file filtering, event handling, and custom archive formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archive packaging can unintentionally include sensitive or bulky paths when broad directory inputs are used. <br>
Mitigation: Review selected files and prefer glob ignore patterns for paths such as .git, node_modules, secrets, and build outputs before creating archives. <br>


## Reference(s): <br>
- [Archiver API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/archiver) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
