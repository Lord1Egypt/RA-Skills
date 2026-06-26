## Description: <br>
Ultimate AI agent memory system that combines bulletproof WAL protocol, vector search, git-based knowledge graphs, cloud backup, and maintenance hygiene for Clawdbot, Moltbot, Claude, GPT agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjscjj](https://clawhub.ai/user/mjscjj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to set up durable working memory, semantic recall, Git-based decision records, curated memory files, and optional cloud memory for Clawdbot, Moltbot, Claude, GPT, and similar agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory may retain sensitive conversation details longer than intended. <br>
Mitigation: Avoid secrets, customer data, regulated data, and sensitive business context unless explicit retention rules, redaction, review, and deletion controls are in place. <br>
Risk: Optional Mem0, SuperMemory, or other cloud memory features may transmit conversation content to third-party services. <br>
Mitigation: Do not enable cloud memory features until the transmitted data, provider storage behavior, and deletion controls are understood and approved. <br>
Risk: Silent memory capture can store preferences, decisions, or facts without enough consent or sensitivity filtering. <br>
Mitigation: Require explicit consent or policy approval for auto-capture and review stored memories periodically for sensitivity and relevance. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mjscjj/elite-longterm-memory-lobster) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>
- [npm package](https://www.npmjs.com/package/elite-longterm-memory) <br>
- [bulletproof-memory](https://clawdhub.com/skills/bulletproof-memory) <br>
- [lancedb-memory](https://clawdhub.com/skills/lancedb-memory) <br>
- [git-notes-memory](https://clawdhub.com/skills/git-notes-memory) <br>
- [memory-hygiene](https://clawdhub.com/skills/memory-hygiene) <br>
- [supermemory](https://clawdhub.com/skills/supermemory) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create SESSION-STATE.md, MEMORY.md, and memory/ daily log files when the included CLI is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
