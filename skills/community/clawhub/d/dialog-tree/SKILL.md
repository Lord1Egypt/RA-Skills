---
name: dialog-tree
description: Maintain a visual "dialog tree" — a data file plus a self-contained HTML viewer in the project repo that map the branches of a long conversation (user questions → the steps/variants of the answers) as an interactive tree with resolve/delete marks and a "built up to" marker for incremental updates. Use whenever the user asks to "create/set up a dialog tree", "update the tree", "add this to the tree", "show open branches", or mentions dialog-tree.html — and proactively offer it when a deep-dive discussion branches enough that the user risks losing track of unexplored side-threads.
---

# Dialog Tree

## Why

A "question → clarification → clarification" conversation is a depth-first search: the user dives into one branch while the unexplored sibling branches silently pile up in their head. When the tree gets deep, backtracking becomes painful. This skill offloads that bookkeeping into files: an HTML page in the project repo that shows every branch of the discussion as a tree, lets the user mark branches resolved, and delete dead ones.

The tree is built by the assistant, not by the app: the viewer only renders the data file. "Update the tree" means appending nodes to it. The tree doubles as a session conspectus — after context loss (compaction, new session) reading the data file restores the map of what was discussed, how it branched, and what is still open.

## Data / view split, file naming

Two files side by side in the project, **named after the treeId** — a generic name like `dialog-tree.html` collides as soon as one machine, one static server, or several sessions host more than one tree:

- **`<treeId>-tree.html`** — the view, a generic dependency-free renderer. Never edited per-project; upgrading the skill = replacing this file wholesale (any file name keeps working).
- **`<treeId>-tree-data.js`** — the data: `META`, `NODES`, optional `STRINGS` (UI localization). The only file the assistant edits. Loaded via a script tag, which works both over `http://localhost` and from disk (`file://` blocks `fetch` of JSON, but not script tags — that's why the data is a .js file, not .json).

The view derives the data file name from its own: `<name>.html` → `<name>-data.js`. So the two names must stay paired — when renaming, rename both, and never rename after the tree is in use without telling the user (bookmarked URLs break; localStorage marks are keyed by origin + treeId, so a file rename itself does not lose marks).

## Set up a tree in a project

1. Copy `assets/dialog-tree.html` and `assets/dialog-tree-data-template.js` (next to this SKILL.md) into the project repo as `<treeId>-tree.html` and `<treeId>-tree-data.js` (e.g. `my-api-tree.html` + `my-api-tree-data.js`). If there is no repo, ask the user where to put them.
2. In `META` (data file) set:
   - `treeId` — a unique project identifier (kebab-case, e.g. the repo name). It keys the localStorage of the user's marks: two trees sharing a treeId, opened from disk, will corrupt each other's marks.
   - `builtUpTo` — a human-readable marker of how far into the conversation the tree is built (date + a short quote of the last message that was decomposed).
3. Decompose the conversation so far into `NODES` (rules below).
4. Show the tree. JS does not execute in chat file viewers, nor in the Claude Code Browser pane for `file://` paths outside the project folder — the page looks empty there:
   - **Browser pane (preferred in Claude Code):** start a static server over the directory via `preview_start {name:"<name>"}`, open `http://localhost:<port>/<treeId>-tree.html`, and give the user that URL — the user never opens files by hand. Start the server at the beginning of every session that works with the tree. Config in `.claude/launch.json` of the working directory (create it if missing; pick the port once and never change it — the user's marks are bound to the `localhost:<port>` origin):

     ```json
     {
       "version": "0.0.1",
       "configurations": [
         { "name": "<project>-tree", "runtimeExecutable": "npx",
           "runtimeArgs": ["-y", "http-server", "<dir with the tree files>", "-p", "<port>", "-c-1"],
           "port": <port> }
       ]
     }
     ```

     Any static file server works — `npx http-server` is just a default. If Node/npx is not installed, substitute whatever the machine has (e.g. `python -m http.server <port> -d <dir>` with `"runtimeExecutable": "python"`); check availability before writing the config.
   - Otherwise the user opens `<treeId>-tree.html` from disk in a normal browser (double-click; the data file must sit next to it). Do not mix the two ways: `file://` and `localhost` have separate localStorage, marks won't sync.

## Node format

In the data file:

```js
{ id:"t2-m1", parent:"t2-mech", who:"user"|"assistant", label:"Short, ≤50 chars",
  status:"open"|"resolved", html:`<p>Details…</p><pre>code</pre>` },
```

- `who:"user"` — the user's questions/remarks (highlighted in the tree); `"assistant"` — steps, variants, parts of an answer.
- `label` — very short, what the node is about; the substance goes into `html`: a condensed digest of the answer (`<p>`, `<ul>`, `<code>`, `<pre>` with code and traces). Quality bar: the topic should be recallable from the node alone, without rereading the chat. Nodes are semantic units, not messages — one long answer may yield several nodes, several messages may collapse into one.
- `parent:null` — root level: the user's top-level questions and the main line of work.
- `status:"resolved"` — the thread was closed in chat; `"open"` — unexplored (awaiting the user's answer, an unsolved exercise, an unread topic). If the session also keeps an in-chat list/stack of open threads, keep it in sync with the open nodes — the tree is the canonical source.
- `html` is a template literal: no backticks or `${` inside; escape HTML special characters in code samples (`&lt;`, `&amp;`).

## Update the tree

On "update the tree" (or offer it yourself after a significant chunk of work):

1. Read `META.builtUpTo` in the data file — everything before that point is already decomposed.
2. Decompose the conversation after the marker into new nodes and **append** them to `NODES` (or as children of existing nodes if they continue a branch).
3. Advance `META.builtUpTo`.

Hard rules (the user's marks live in localStorage keyed by node id):
- never change or reuse ids of existing nodes — the user's resolve/delete marks would silently migrate;
- never remove nodes from `NODES` — only the user deletes, via the UI;
- editing an existing node is fine (refine label/html, flip status to resolved once the thread closes in chat) — keep its id;
- never edit the view (`<treeId>-tree.html`) — all per-project changes belong in the data file.

The user's UI marks are invisible to the assistant (localStorage never touches the files). If the user says they marked something in the UI, mirror it into the `status` field so it survives context loss and session changes.

## Verify after every edit

After editing the data file, run this smoke test — a broken template literal or a duplicate id kills the whole page silently:

```bash
node -e "
eval(require('fs').readFileSync('<treeId>-tree-data.js','utf8') + ';globalThis.__D={META,NODES}');
const {META,NODES} = globalThis.__D;
const ids = new Set(NODES.map(n=>n.id));
if (ids.size !== NODES.length) throw new Error('duplicate ids');
for (const n of NODES) if (n.parent && !ids.has(n.parent)) throw new Error('orphan '+n.id);
if (!META.treeId || !META.builtUpTo) throw new Error('META incomplete');
console.log('OK', NODES.length, 'nodes | builtUpTo:', META.builtUpTo)"
```

If Node is not installed, skip the scripted check and verify by reloading the page in the browser instead (a broken data file shows either an empty tree or the view's error banner).

If you change the view itself (skill development, not project work), verify in a real browser via the local server.

## Localization

The view ships English UI strings; to localize, define `STRINGS` in the data file (any subset of keys — see the commented block in the data template). Node content language simply follows the conversation language.
