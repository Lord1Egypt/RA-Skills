## Description: <br>
3-brain filesystem + memory reference utility for LYGO-based agents. Use to design, organize, and maintain a durable file/folder memory system (indexes, reference .txt links, logging, retrieval) without overwriting existing data. Works best on fresh OpenClaw/Clawhub Havens with the full LYGO Champion stack, but is compatible with any agent that can read/write files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepSeekOracle](https://clawhub.ai/user/DeepSeekOracle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to design and maintain durable workspace memory systems with folders, indexes, reference stubs, and structured logs. It is most useful when setting up a fresh agent workspace or improving retrieval in an existing file-based memory layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files may accidentally capture secrets or unnecessary personal data. <br>
Mitigation: Review proposed memory, reference, index, and log content before writing it, and keep secrets or unnecessary personal data out of persistent files. <br>
Risk: Filesystem organization changes can confuse retrieval if they overwrite or replace existing structure. <br>
Mitigation: Use the skill additively: create missing folders or new dated files, append to existing indexes and logs, and ask for human approval before reorganizing existing content. <br>


## Reference(s): <br>
- [BOOK BRAIN Examples & Patterns](references/book-brain-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/DeepSeekOracle/book-brain) <br>
- [LYGO Champion Hub](https://deepseekoracle.github.io/Excavationpro/LYGO-Network/champions.html#champions) <br>
- [Eternal Haven portal](https://EternalHaven.ca) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with suggested file paths, folder layouts, index stubs, logs, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces additive, human-reviewed filesystem organization guidance and should not silently delete or overwrite existing files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
