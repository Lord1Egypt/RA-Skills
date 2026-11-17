---
name: coret-mindmap
description: Create, inspect, update, illustrate, export, and share live mind maps in coret.id through its MCP tools. Use when a user asks to turn notes, meetings, research, plans, or outlines into a Coret mind map, or to work with an existing Coret map, node, Spidol drawing, sketch, image, export, or share link.
---

# Coret Mind Map

Use the Coret MCP tools as the execution surface. Do not reimplement the REST API.

## Before You Start

1. Confirm the Coret MCP server is connected and has a `CORET_API_KEY`.
2. Prefer a `crt_test_` key while testing a new workflow. Use `crt_live_` only when the user intends to change production workspace data.
3. Before a live write, confirm the connected workspace is the intended target when the workspace is not already clear from context.
4. Use `get_skill_doc` when you need request schemas, limits, image metadata, sharing rules, or response examples. Do not guess undocumented fields.
5. Never print, store, commit, or place the API key in a URL, prompt, map, log, or share link.

## Workflow

### Read or Inspect

- Use `list_maps` to find the target instead of guessing an ID.
- Use `get_map` or `list_nodes` before changing an existing map.
- Preserve node IDs, notes, ordering, styles, and unrelated branches unless the user asks to change them.

### Create

1. Turn the source into a short hierarchy: one clear root, distinct branches, concise node text, and notes only where detail helps.
2. If the user's structure is ambiguous or the write is large, show the proposed hierarchy before writing.
3. Call `create_map`, read the created map to obtain its root node, then add nodes. Prefer `batch_nodes` for a coherent multi-node write; keep each batch at or below the documented limit.
4. Read the final map and report its title, ID, and a compact summary of what changed.

### Update

1. Read the current map and identify the smallest set of nodes that must change.
2. Use `update_map`, `add_node`, `update_node`, or `batch_nodes` without rebuilding unaffected branches.
3. Read the changed map again and verify the requested state.

### Images, Drawings, Sketches, Exports, and Sharing

- For map images, call `upload_image`, then use the returned URL in the node image metadata described by `get_skill_doc`.
- Use `get_drawings` and `put_drawings` for freehand Spidol marks directly over the mind-map canvas, such as circling or underlining existing ideas. Read first and preserve unrelated strokes; an empty array clears every stroke.
- Use `put_sketch` only for a separate free-form whiteboard with boxes, sticky notes, text, arrows, or strokes. Do not use sketch when the user asks to mark the mind map itself.
- Use `export_map` for JSON, Markdown, or text output.
- Create a public share link only when the user asks to share or needs a browser link. State the permission and expiry.

## Safety

- Get explicit confirmation immediately before `delete_map` or `delete_node`, unless the user already explicitly requested that exact deletion. Explain that deleting a node also deletes its descendants.
- Treat `batch_nodes` as destructive when it contains update or delete operations; summarize the affected branches before calling it.
- Do not broaden scopes, switch from test to live, or create a public share link silently.
- If a tool returns an auth, scope, validation, rate-limit, or quota error, report it plainly and stop retrying unchanged input.
- If a multi-step write fails partway, read the current map before retrying so completed operations are not duplicated.

## Completion

Finish with the observable result: map title and ID, changes made, verification performed, and share URL only when one was requested or created.
