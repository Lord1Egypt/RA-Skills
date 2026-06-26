## Description: <br>
DeepVista Card helps agents manage DeepVista knowledge cards, including creating, searching, reading, organizing, editing, pinning, archiving, and deleting context cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to operate DeepVista Vistabase knowledge cards through the DeepVista CLI. It supports read workflows such as list, get, hybrid search, semantic similarity, and regex grep, plus user-confirmed write workflows for create, update, edit, delete, pin, and archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive commands can change or delete DeepVista knowledge-base records. <br>
Mitigation: Confirm with the user before running create, update, edit, delete, pin, or archive commands, and show the resulting card URL after create or update when available. <br>
Risk: The skill depends on the DeepVista CLI package and the deepvista-shared authentication/profile skill. <br>
Mitigation: Install the DeepVista CLI only from trusted sources and complete the shared authentication/profile setup before using card commands. <br>


## Reference(s): <br>
- [DeepVista CLI](https://cli.deepvista.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/jingconan/deepvista-vistabase-card) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline DeepVista CLI commands and DeepVista card URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations should be confirmed with the user before execution; create and update workflows should show the resulting card URL when available.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
