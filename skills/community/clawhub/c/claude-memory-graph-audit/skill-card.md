## Description: <br>
Audits Claude Code session memory directories as a knowledge graph, detecting broken wikilinks, orphan pages, hub nodes, bridge candidates, and sparse clusters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to inspect local session memory Markdown as a lightweight knowledge graph and identify broken links, isolated pages, hub nodes, and bridge candidates before repairing memory content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair suggestions or link changes can alter persistent Claude memory content. <br>
Mitigation: Preview affected files and keep a backup or diff before applying repair commands or adding links. <br>
Risk: Running the audit without an explicit path targets the most recently modified Claude project memory directory. <br>
Mitigation: Pass the intended memory directory explicitly when auditing a specific project. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/heavenchenggong/claude-memory-graph-audit) <br>
- [Publisher profile](https://clawhub.ai/user/heavenchenggong) <br>
- [LLM Wiki reference](https://github.com/nashsu/llm_wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and terminal audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The audit script performs read-only checks; repair guidance may lead users to edit persistent memory Markdown after review.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
