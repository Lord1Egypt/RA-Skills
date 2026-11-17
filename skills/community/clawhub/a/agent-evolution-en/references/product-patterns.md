# Product Patterns and Integration

These products illustrate memory mechanisms. Check files, interfaces, load timing, and permissions in the user's actual host. Prefer existing memory and verify retrieval in a later session when cross-session use matters.

| Product and mechanism | Design in this Skill |
| --- | --- |
| **Hermes Agent** supports post-turn self-improvement review and improvement during use. It distinguishes compact persistent memory from procedural skills loaded on demand. [Persistent Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) · [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | Capture outcomes as they emerge and support a closing review. Keep frequently used facts and cues short. Retrieve complex practices as needed. |
| **Claude Code** Auto Memory reads and writes project memory during work. `MEMORY.md` indexes topic files. [How Claude remembers your project](https://code.claude.com/docs/en/memory) | Use a compact entry point for locating topic records and artifacts. Retrieve examples, raw records, and evidence as needed. |
| **OpenClaw** separates daily notes and long-term memory, supports saving important context before compaction, and consolidates candidates. [Memory overview](https://docs.openclaw.ai/concepts/memory) | Save important milestones before changing tasks. Preserve the status of early observations and untested ideas. Consolidate when supporting evidence becomes available. |
| **GitHub Copilot Memory** keeps source locations for repository facts, rechecks citations before use, and can reinforce or retire older memories. [About GitHub Copilot Memory](https://docs.github.com/en/copilot/concepts/prompting-and-context/copilot-memory) | Include sources, project scope, and a recheck trigger. Revalidate consequential sources before reuse and replace outdated entries. |
| **Letta** uses Git-backed MemFS for inspectable, editable memory. [Memory & dreaming](https://docs.letta.com/configuration/memory) | Version durable changes that affect future behavior and retain a way to roll them back. Capture ordinary artifacts with a lighter operation. |

## Enable the Skill in a project

- **On demand.** Invoke the Skill to capture results during work or request a closing review.
- **Ongoing use.** Add a short instruction to a project entry point chosen by the user. Specify where the agent can read and write and how often it should review. For example, in the `AGENTS.md` the host loads or an equivalent file, write: “Retrieve relevant project memories when needed. Capture reusable outcomes during work. Briefly review each task at the end and save useful additions.” Preserve the host's instruction precedence.
- **Lifecycle events.** An authorized host integration can run the same review at task completion. Without such an integration, run the review in the current session before delivering. Ongoing operation depends on how the project enables the installed Skill.
- **Verify integration.** Use a second session to run a relevant task. Check that the agent reads and uses a specific record. Try an unrelated task to check that it leaves project-specific rules outside their scope.
