# Karpathy LLM Wiki

## Source

- Canonical URL: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Summary

Karpathy's "LLM wiki" pattern is the clearest statement of why a maintained wiki should exist as its own layer rather than being treated as a side effect of prompting. The core model has three layers. First come the raw sources: papers, docs, transcripts, notes, logs, or any other primary material you do not want to lose or reinterpret prematurely. Second comes the wiki: a curated, continually improved markdown layer where the knowledge from those sources is normalized into pages that are easier to navigate, link, and maintain. Third comes conversation: the chat interaction where an LLM helps answer questions, draft plans, or explore ideas using the wiki as the already-compiled knowledge base.

The key insight is that knowledge work should be compiled once and then maintained, not re-derived from scratch every time someone asks a question. If the model has to reread the same raw inputs on every prompt, you are paying the same comprehension cost repeatedly, inviting inconsistency, and making the result dependent on prompt wording. A wiki flips that model. Important facts and relationships are distilled once into durable pages, and future chats can spend their attention budget on the new question instead of on reconstructing the whole background context.

Karpathy also frames Obsidian as a kind of IDE for knowledge. That metaphor is important because it treats markdown files, links, folders, and search as the developer environment for thinking. In this model, pages are not static documentation produced at the end of work. They are the live working surface where ideas are refined, connected, and kept current over time.

The pattern scales across multiple use cases. For personal knowledge management, it gives one person a durable memory substrate that survives across projects and sessions. For research, it helps consolidate papers, experiments, and notes into reusable synthesis. For businesses and teams, it creates a human-browsable and agent-usable knowledge layer that can absorb raw operating material and turn it into continuously improved institutional understanding.
