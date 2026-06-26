# AgentSearch Manifesto

## Source

- Canonical URL: https://www.agentsearch.sh/manifesto
- Related URL: https://www.agentsearch.sh/

## Summary

The AgentSearch manifesto makes a sharp claim: code hallucinations are not primarily a model problem, they are a data problem. The argument is straightforward. APIs, SDKs, and docs change constantly, while model training data is always delayed. An agent can generate code that looks syntactically perfect and still fail in production because the model never saw a deprecation, rename, or breaking change that shipped after training. In that frame, the real failure is not that the model cannot reason, but that it is reasoning over stale or missing information.

From there, the manifesto proposes a filesystem-as-interface pattern for agents. Instead of inventing a custom tool layer for each documentation source, it argues that the web should become navigable in the same way a codebase is. Agents already know how to use commands like `ls`, `cd`, `cat`, `tree`, `find`, and `grep`, because Unix-style filesystem interaction is deeply represented in their training data. If documentation can be surfaced as browsable directories and files, the agent gets an interface it already understands without having to learn a new protocol at runtime.

This is also the document's critique of MCP servers and bespoke tool schemas. Those approaches can work, but they cost context window space, require documentation, and force the agent into a trial-and-error phase where it learns the shape of the interface before it can do useful work. A filesystem has a lower activation cost. The model can immediately inspect structure, search for terms, and read relevant files with primitives it already uses well.

The manifesto's broader vision is that the entire web should behave like a navigable directory tree. Doc sites, changelogs, API references, and other current information sources become places an agent can enter, inspect, and traverse as though they were local. For a knowledge base like this repo, that idea matters because it supports a future where external references are not just linked, but mirrored and made directly legible to agents through plain files.
