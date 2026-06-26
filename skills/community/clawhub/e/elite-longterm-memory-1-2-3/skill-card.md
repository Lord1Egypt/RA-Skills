## Description: <br>
Ultimate AI agent memory system for Cursor, Claude, ChatGPT & Copilot. WAL protocol + vector search + git-notes + cloud backup. Never lose context again. Vibe-coding ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsjustFred](https://clawhub.ai/user/itsjustFred) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to set up durable memory across sessions with a write-ahead session file, vector recall, Git notes, curated Markdown archives, and optional cloud-backed memory services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to keep durable local memory, which can unintentionally retain sensitive conversation or project context. <br>
Mitigation: Use it only for intended memory retention, avoid storing secrets or regulated data, and regularly review or delete SESSION-STATE.md, MEMORY.md, daily logs, vectors, and Git notes. <br>
Risk: Optional SuperMemory and Mem0 integrations may send conversation-derived data to external services. <br>
Mitigation: Enable cloud-backed integrations only after approving the provider and data handling model, and keep API keys scoped and protected. <br>
Risk: Silent persistence instructions can make it harder for users to notice what the agent saved. <br>
Mitigation: Set team policy for what may be written to memory, audit memory files periodically, and require explicit review before sharing or syncing memory stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itsjustFred/elite-longterm-memory-1-2-3) <br>
- [npm package](https://www.npmjs.com/package/elite-longterm-memory) <br>
- [GitHub repository](https://github.com/NextFrontierBuilds/elite-longterm-memory) <br>
- [Full Documentation](./SKILL.md) <br>
- [ClawdHub source listing](https://clawdhub.com/skills/elite-longterm-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory scaffolding and operational instructions; optional integrations may use OpenAI, SuperMemory, Mem0, and LanceDB.] <br>

## Skill Version(s): <br>
1.2.3 (source: SKILL.md frontmatter and package.json); ClawHub release version 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
