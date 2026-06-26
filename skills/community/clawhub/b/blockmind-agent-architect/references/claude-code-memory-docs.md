# Claude Code Memory & CLAUDE.md

## Source

- Canonical URL: https://code.claude.com/docs/en/memory
- Related URL: https://docs.anthropic.com/en/docs/claude-code/memory

## Summary

Claude Code separates persistent guidance into two related but different systems: `CLAUDE.md` files and auto memory. The docs draw the distinction clearly. `CLAUDE.md` is authored intentionally by humans and contains instructions, conventions, project architecture, workflows, and rules the agent should follow. Auto memory is written by Claude itself as it learns patterns, commands, and debugging context while working in a given tree. That means `CLAUDE.md` is the explicit contract, while memory is the emergent operating history.

Scope matters in Claude's model. The docs describe project, user, and organization layers, which means guidance can live close to a repo, in a user's broader development environment, or at a higher organizational scope. This layered hierarchy is useful when some instructions are universally true for a team while others should apply only to one workspace. For a standalone repo like this one, the project-level `CLAUDE.md` is the key artifact because it gives Claude the local rules without depending on user-specific memory.

The documentation also calls out `.claude/rules/` for scoped rules. That is important because not all instructions should apply globally. Some constraints belong only to certain directories, file types, or workflows. Scoped rules help prevent the common problem where one large instruction file becomes too broad and starts leaking irrelevant requirements into unrelated work.

Claude loads memory at session start, which is why the docs stress keeping the startup context concise and useful. The memory documentation notes that auto memory is loaded into each session up to a threshold, while `CLAUDE.md` files are loaded in full. That creates a strong incentive to keep `CLAUDE.md` direct and well organized. The best practice is to write instructions that are durable, action-oriented, and specific enough to steer behavior, while leaving volatile or incidental details to memory and separate topic files. For this repo, Claude's model is the template for making project guidance portable, layered, and readable by both humans and agents.
