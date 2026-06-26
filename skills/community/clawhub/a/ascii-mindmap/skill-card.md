## Description: <br>
Generate and display ASCII tree diagrams from indented text outlines to visualize ideas and hierarchies in the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agent operators use this skill to turn indented outlines or bullet lists into terminal-friendly ASCII mind maps and Markdown-exportable diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local bash script that invokes python3. <br>
Mitigation: Inspect the script before deployment and run it only in an environment where local script execution is acceptable. <br>
Risk: Input outlines or stdin content may be displayed or exported directly. <br>
Mitigation: Use only outline files or piped content that are intended to be shown in terminal output or Markdown exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/ascii-mindmap) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text ASCII tree diagrams or Markdown fenced code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local bash and Python standard-library execution; output structure depends on the supplied indentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
