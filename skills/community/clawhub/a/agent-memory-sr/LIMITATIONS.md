# Limitations

## What Agent Memory Does NOT Do

**No automatic memory writing**
The init script creates the structure. Filling it in and keeping it updated is the agent's job (or yours). Agent Memory gives the agent a place to write — it doesn't write for it.

**No enforcement**
Files are plain Markdown. The agent has to actually read them. If your agent's system prompt doesn't include the load instructions, the files sit unused.

**No compaction handling**
When a session is compacted/summarized, the agent may lose context from within the session. Daily logs capture what the agent writes down — they don't automatically capture what the agent thought.

**No cross-session state synchronization**
If the same agent runs in multiple parallel sessions, memory files can get out of sync. This system is designed for single-agent-per-workspace use.

**Not a vector database**
MASTER_MAP + daily logs are flat files. No semantic search, no embedding-based retrieval. Works well for workspaces under a few hundred files; for larger codebases consider a vector index alongside this system.

**MEMORY.md size limit**
MEMORY.md should stay under ~20KB. It's loaded on startup — bloat increases context costs and slows startup. Use daily logs for raw detail; MEMORY.md for distilled essentials only.

**Templates are starting points**
The templates are generic. You will need to customize AGENTS.md and USER.md for them to be useful. An agent reading a blank USER.md learns nothing.
