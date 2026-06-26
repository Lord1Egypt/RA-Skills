# Fumadocs

## Source

- Canonical URL: https://fumadocs.dev
- Related URL: https://fumadocs.dev/docs/getting-started

## Summary

Fumadocs is a React.js documentation framework designed to make docs sites feel like composable application infrastructure rather than a fixed theme. The homepage presents it as a framework that works with "any React.js framework, CMS — anything," and the supported starter flow explicitly includes Next.js, Waku, TanStack Start, and React Router. That flexibility matters for this repository because it means the knowledge base can stay markdown-first today without locking itself out of a future site implementation choice.

MDX support is a major reason Fumadocs is relevant. The framework supports plain Markdown for simple pages and richer MDX for developers who need JSX, custom components, includes, code tabs, callouts, and typed code examples. This is a strong fit for a knowledge wiki because some pages should remain lightweight summaries while others may eventually need interactive examples, embedded diagrams, or generated API views.

The architecture is explicitly composable. Fumadocs is separated into content, core, and UI layers. `fumadocs-mdx` handles content authoring, `fumadocs-core` provides the headless source and docs logic, and `fumadocs-ui` provides presentation components. That separation is important because it means the content model does not have to be tightly bound to one visual shell. A repo can keep markdown as the source of truth while choosing how much framework and how much custom UI to adopt.

The Obsidian angle makes it especially relevant here. The `fumadocs-obsidian` extension is built to handle Obsidian-style markdown, which aligns directly with the Karpathy-style wiki workflow this repo is implementing. In other words, Fumadocs can act as the browser layer for notes and wiki pages that were authored in an Obsidian-friendly filesystem. The result is a promising path from plain markdown knowledge assets to a polished docs site without giving up portability or agent-readable files.
