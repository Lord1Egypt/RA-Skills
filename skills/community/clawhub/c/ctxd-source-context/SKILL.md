---
name: ctxd-source-context
description: Use ctxd to inspect tracked source paths and read current context for an agent task. Apply when a user wants answers grounded in changing project sources, needs to refresh indexed context, or wants to verify an edit or removal through ctxd.
license: MIT-0
metadata:
  author: Team CTXD
  homepage: https://ctxd.dev
---

# Read current source context with ctxd

ctxd synchronizes source content into ctxfs. Use its path and read tools to inspect the source before answering. The agent still chooses relevant material and explains what the evidence supports.

## Connect to the existing source

Use the existing ctxd MCP connection when available. Begin with `tree` using an empty prefix, a small depth and a bounded limit. Choose the root relevant to the user's task, then inspect that root with `ls`, `tree` or `glob`.

Pass paths returned by these tools to `stat`, `read` or `read_lines`. MCP paths look like `local-files/<folder-id>/relative/path`; a friendly CLI folder name is not the MCP path. Respect byte, line and result limits. Narrow a query when its result is incomplete.

Read enough of the source to answer the question, then identify the source path and relevant lines in the answer. A successful synchronization is not evidence that an answer is correct; the returned source content is the evidence.

## Refresh changing context

When the task depends on a recent change, synchronize the configured sources before reading. Run on the machine hosting ctxd, as the operating-system user who configured its store:

```bash
python -m ctxd.tracker_service sync-once
```

Read the same returned source path again after synchronization. If a source was removed, check the parent tree and confirm the old path is unavailable. Do not continue using cached content as current evidence.

Editing or deleting a source is separate from reading it. Change source files only when the user's task calls for that change. For a demonstration, use a disposable fixture rather than a real project file.

## Set up ctxd when needed

For an existing installation, inspect `ctxd backend status` and `ctxd folders list` before changing configuration. Reuse a healthy store. When the task calls for a new local setup, run on the user's Linux workstation as their normal user, with Python 3.11 or 3.12 and the system `ps` command available:

```bash
pip install ctxd
ctxd --version
ctxd backend set ctxfs
ctxd backend status
```

The local setup needs no hosted account or API key. The commands above match the published 0.1.16 package. If the installed CLI differs, inspect its help before changing configuration.

Register only the source folder the user selected. Replace the example path and alias with that folder:

```bash
ctxd folders add /path/to/source --name Source
python -m ctxd.tracker_service sync-once
ctxd tracker start
```

Start the MCP client as the same operating-system user. Point it at the `ctxd-mcp` executable from the environment where ctxd is installed:

```json
{
  "mcpServers": {
    "ctxd": {
      "command": "ctxd-mcp"
    }
  }
}
```

The connection uses local standard input/output. A client running elsewhere does not gain access to this machine's store from this configuration. Read content is available to the client and its configured model provider.

## Choose working operations

Use MCP `ls`, `tree`, `glob`, `stat`, `read` and `read_lines` for source inspection. The 0.1.16 MCP `grep` wrapper fails; use Python or the CLI for exact text search. On the same workstation and as the configured user, a CLI search against the registered alias is:

```bash
ctxd files grep "search text" --prefix Source --limit 20
```

Use the MCP tree to obtain a canonical path before a subsequent MCP read. Do not substitute semantic-search claims for exact matching, and do not infer untracked sources or cloud connectors from a repository link.

[Get started with ctxd](https://ctxd.dev) · [Source and installation](https://github.com/ctxddev/ctxd-agent-plugin) · [Star ctxd](https://github.com/ctxd-dev/ctxd)
