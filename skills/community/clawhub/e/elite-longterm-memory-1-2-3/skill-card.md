## Description:

Ultimate AI agent memory system for Cursor, Claude, ChatGPT & Copilot. WAL protocol + vector search + git-notes + cloud backup. Never lose context again. Vibe-coding ready.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsjustfred](https://clawhub.ai/user/itsjustfred)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to set up persistent AI-agent memory across session files, vector recall, Git-Notes records, curated archives, and optional cloud or Mem0 integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files and vector stores can retain sensitive conversation details longer than intended.

Mitigation: Define what may be stored before deployment, avoid secrets and personal data, and periodically review and prune memory files and vectors.

Risk: Optional Mem0, SuperMemory, or git-notes remote sync can send conversation-derived data outside the local workspace.

Mitigation: Keep cloud and remote sync integrations disabled unless explicitly approved, and use pinned package versions and scoped API keys when enabling them.

Risk: The documented LanceDB removal command deletes local vector memory data.

Mitigation: Back up required memory data and confirm the target path before running destructive cleanup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsjustfred/skills/elite-longterm-memory-1-2-3)
- [Full skill documentation](artifact/SKILL.md)
- [README](artifact/README.md)
- [npm package](https://www.npmjs.com/package/elite-longterm-memory)
- [Required memory-lancedb plugin reference](https://clawdhub.com/skills/lancedb-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and generated local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initializes SESSION-STATE.md, MEMORY.md, and daily memory logs when the CLI is run. Optional integrations may use OPENAI_API_KEY, SUPERMEMORY_API_KEY, or MEM0_API_KEY.]

## Skill Version(s):

1.2.3 (source: SKILL.md frontmatter, package.json, and artifact _meta.json); ClawHub release metadata version 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
