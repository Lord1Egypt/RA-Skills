---
name: excaliclaw
version: 1.0.2
description: Create reliable Excalidraw diagrams in OpenClaw using the Excalidraw MCP, with export-safe labels, Excalifont text, and clear system-diagram structure. Use when the user asks for an Excalidraw diagram, architecture diagram, system diagram, flowchart, or hand-drawn diagram.
user-invocable: true
argument-hint: "[diagram topic]"
---

# Excaliclaw

Create diagrams with the Excalidraw MCP in a way that survives OpenClaw rendering and Excalidraw export.

## Core Rule

Use real Excalidraw elements, but do **not** rely on MCP `label` shortcuts for final diagrams.

## MCP Availability Preflight

Before creating or exporting a diagram, verify that the Excalidraw MCP tools are available in the current OpenClaw session.

Expected behavior:

1. If the Excalidraw MCP tools are available, continue with the normal diagram workflow.
2. If the tools are missing, tell the user plainly: “Excalidraw MCP is not installed or not available in this OpenClaw session.”
3. Ask whether the user wants it installed as a Streamable HTTP MCP before changing OpenClaw configuration, installing packages, or restarting/reloading services.
4. If the user agrees, use the current OpenClaw-supported MCP configuration path. Do not invent commands; check local OpenClaw docs or CLI help first if the install/config command is not already known.
5. After installation, reload/restart only what is required, then verify with a minimal hello-world Excalidraw scene before attempting the requested diagram.
6. If installation fails or the user declines, offer a fallback such as Excalidraw JSON, SVG/PNG, Mermaid, or another diagram format, and state that MCP preview/export will not be available.

Do not silently auto-install the MCP just because a diagram was requested. Installing an MCP is an environment change and needs explicit user approval unless the user already asked to set it up.

Reliable pattern:

Mandatory workflow for normal diagram requests:

1. Use `excalidraw__create_view` to render the diagram preview first as an internal quality gate. Do not skip the preview and jump straight to export unless the user explicitly asks for JSON-only or link-only output.
2. Treat the editable excalidraw.com link as the normal user-facing deliverable for Excalidraw diagram requests. Include it by default after a successful export.
3. Build the export from the same full native Excalidraw scene represented by the preview, not a simplified redraw, not a raw MCP streaming array, and not a different diagram.
4. If `create_view` returns a checkpoint id, treat it as evidence of the previewed scene. Preserve the same elements and relationships when constructing the export payload.
5. Export only a full Excalidraw scene object, never a bare element array. The exporter payload must be serialized JSON with `type: "excalidraw"`, `version`, `source`, `elements`, `appState`, and `files`.
6. Verify the exported link before replying. If the link cannot be verified as non-empty, do not deliver it as the final artifact.
7. On export failure, timeout, or blank-link verification, retry the same full scene once before simplifying. If simplification is necessary, say clearly that the exported link is a simplified fallback.
8. If a non-empty editable link still cannot be produced, do not deliver a fallback artifact. Tell the user plainly that the excalidraw.com share link failed verification, keep the inline MCP preview as diagnostic evidence only, and ask whether they want another export attempt or a different format.
9. Do not silently change tool strategy just because one export attempt failed; the known-good path is preview first, then clean full-scene export link, then verified fallback if needed.

Element construction pattern:

1. Draw the shape first.
2. Draw a separate explicit `text` element for the label.
3. Bind box labels to their shapes using Excalidraw container text fields (`containerId` on the text + matching `{ "type": "text", "id": ... }` in the shape's `boundElements`). This is mandatory for editable box labels unless preview/export proves it broken.
4. Bind arrows based on meaning, not just appearance: if the arrow means “this step talks to that specific step/box,” bind it with `startBinding` and `endBinding`; route around labels if needed. Do **not** bind arrows that merely point into a lane, group, or general area without targeting a specific box.
5. For every bound arrow, include reciprocal `{ "type": "arrow", "id": ... }` entries in both connected shapes' `boundElements`.
6. Do not downgrade semantic box-to-box arrows to loose visual arrows for speed, token pressure, or because MCP `read_me` examples use simpler arrows. If an arrow would be expected to follow a box when moved, it must be bound in both preview and export.
7. Set `fontFamily: 1` on every text element to use Excalidraw's hand-drawn Excalifont.
7. Include `width` and `height` on every text element.
8. Put text elements after their shapes in draw order.
9. Label major boxes and important arrows unless the user explicitly wants an unlabeled or abstract diagram.
10. Export/share only after checking that labels rendered correctly in the MCP preview.
11. Before exporting, verify that the export JSON still contains `containerId`, shape `boundElements`, and arrow `startBinding`/`endBinding`. Do not flatten bound labels or connected arrows into loose visual text/lines during export.
12. If the delivered diagram is intended to be editable, perform an explicit arrow-editability audit: every semantic box-to-box connector must have `startBinding`, `endBinding`, and matching reciprocal arrow entries in both endpoint shapes' `boundElements`.

## Recommended Element Recipe

### Labeled box

Best default for editable diagrams: bind the text to the rectangle so Excalidraw treats it as the box label when the user drags or edits the box.

```json
[
  {
    "type": "rectangle",
    "id": "box-api",
    "x": 100,
    "y": 100,
    "width": 180,
    "height": 70,
    "backgroundColor": "#d0bfff",
    "fillStyle": "solid",
    "roundness": { "type": 3 },
    "strokeColor": "#8b5cf6",
    "boundElements": [{ "type": "text", "id": "txt-api" }]
  },
  {
    "type": "text",
    "id": "txt-api",
    "x": 130,
    "y": 123,
    "width": 120,
    "height": 24,
    "text": "API Server",
    "fontSize": 16,
    "fontFamily": 1,
    "strokeColor": "#1e1e1e",
    "containerId": "box-api",
    "textAlign": "center",
    "verticalAlign": "middle"
  }
]
```

If bound container text fails in MCP preview or export, fall back to the same explicit text element without `containerId`/`boundElements`. Keep the label visually centered, but tell the user it may not move with the box. Do not silently fall back.

Avoid this shortcut for final deliverables:

```json
{
  "type": "rectangle",
  "id": "api",
  "label": { "text": "API Server" }
}
```

The `label` shortcut may look convenient, but it has proven flaky in OpenClaw/Excalidraw MCP export paths. Do not use shortcut labels in either preview or export payloads for final deliverables; otherwise exported diagrams can appear correct while losing editability.

### Connected arrow

Bind based on meaning, not just appearance. When an arrow means “this step talks to that specific step/box,” bind the endpoints to the source and target boxes. This lets Excalidraw keep the arrow attached when the user moves either box.

For arrow binding to survive editing/export, include both sides of the relationship:

- The arrow has `startBinding` and `endBinding` with the connected shape IDs.
- Each connected shape has a matching `boundElements` entry for the arrow.
- The arrow endpoint coordinates should land on or very near the connected shapes' edges. Do not rely on bindings alone while leaving arrow geometry floating in whitespace.

Prefer simple straight bound arrows first. Avoid multi-segment/elbow bound arrows unless you verify they render and remain editable correctly; they can look warped or appear unbound in Excalidraw exports. If labels or spacing make the connection awkward, fix the layout by moving boxes/labels before adding complex arrow routing.

Do **not** bind arrows that only point into a lane, group, note area, or nearby whitespace. For example, in swim lane diagrams, an arrow may leave one box and point generally into another lane before the next step appears; that should remain a visually positioned arrow, not a box-bound connector.

```json
[
  {
    "type": "rectangle",
    "id": "box-client",
    "x": 100,
    "y": 100,
    "width": 140,
    "height": 70,
    "backgroundColor": "#a5d8ff",
    "fillStyle": "solid",
    "roundness": { "type": 3 },
    "boundElements": [{ "type": "arrow", "id": "arr-client-api" }]
  },
  {
    "type": "rectangle",
    "id": "box-api",
    "x": 380,
    "y": 100,
    "width": 140,
    "height": 70,
    "backgroundColor": "#d0bfff",
    "fillStyle": "solid",
    "roundness": { "type": 3 },
    "boundElements": [{ "type": "arrow", "id": "arr-client-api" }]
  },
  {
    "type": "arrow",
    "id": "arr-client-api",
    "x": 240,
    "y": 135,
    "width": 140,
    "height": 0,
    "points": [[0, 0], [140, 0]],
    "endArrowhead": "arrow",
    "strokeColor": "#1e1e1e",
    "startBinding": { "elementId": "box-client", "fixedPoint": [1, 0.5] },
    "endBinding": { "elementId": "box-api", "fixedPoint": [0, 0.5] }
  }
]
```

Use common `fixedPoint` values:

- Right edge: `[1, 0.5]`
- Left edge: `[0, 0.5]`
- Top edge: `[0.5, 0]`
- Bottom edge: `[0.5, 1]`

### Labeled arrow

Prefer a bound arrow plus a separate text element near the arrow:

```json
[
  {
    "type": "arrow",
    "id": "arr-client-api",
    "x": 260,
    "y": 130,
    "width": 120,
    "height": 0,
    "points": [[0, 0], [120, 0]],
    "endArrowhead": "arrow",
    "strokeColor": "#1e1e1e",
    "startBinding": { "elementId": "box-client", "fixedPoint": [1, 0.5] },
    "endBinding": { "elementId": "box-api", "fixedPoint": [0, 0.5] }
  },
  {
    "type": "text",
    "id": "txt-client-api",
    "x": 290,
    "y": 100,
    "width": 70,
    "height": 20,
    "text": "HTTPS",
    "fontSize": 14,
    "fontFamily": 1,
    "strokeColor": "#757575"
  }
]
```

If arrow binding fails in MCP preview or export, fall back to visually positioned arrows and tell the user they may need to reconnect arrows manually. This is an explicit fallback, not a silent simplification.

Regression guard: after a diagram looks visually correct, still inspect the generated/export JSON for every semantic connector. A beautiful render is not enough; if moving either connected box would leave the arrow behind, the diagram failed the editability requirement.

Use visually positioned arrows, not bindings, when:

- the arrow points to a lane or region rather than a specific box
- the arrow lands near text, a label, or empty space inside another lane
- the arrow represents continuation, return direction, or emphasis rather than a strict object-to-object connection
- binding would make later manual editing more surprising than helpful
- a multi-point/elbow bound arrow renders awkwardly or appears detached after export

## Font Guidance

Default to:

```json
"fontFamily": 1
```

This maps to Excalidraw's hand-drawn Excalifont in normal Excalidraw scenes.

If the user asks for font options, verify the current Excalidraw element model before giving exact numeric values. Common Excalidraw families are hand-drawn/Excalifont, normal/sans, code/monospace, and comic-style, but do not promise exact IDs without checking.

## Diagram Quality Checklist

Before exporting/delivering:

- Title is visible.
- Every major element has visible text.
- Important connections have visible labels.
- Text uses `fontFamily: 1`.
- Text has `width` and `height`.
- Box labels use `containerId` + matching shape `boundElements`; if not, the final answer explicitly says labels are visually placed only.
- Arrows that semantically connect two specific boxes use `startBinding` and `endBinding` with the correct shape IDs; if not, the final answer explicitly says arrows are visually placed only.
- Connected boxes include reciprocal `boundElements` entries for their connected arrows.
- Export payload preserves those same `containerId`, `boundElements`, `startBinding`, and `endBinding` fields; do not convert editable relationships into loose shapes during export.
- Prefer straight bound arrows; only use elbow/multi-point bound arrows after preview/export verification.
- Arrows that only point into lanes, groups, labels, whitespace, or general regions remain visually positioned and unbound.
- Text appears after its shape in element order.
- No text overlaps other text, arrows, or important shapes.
- Arrows avoid crossing through text, labels, or important content wherever possible.
- The MCP preview shows labels before exporting.
- The export payload contains no `cameraUpdate`, `delete`, `restoreCheckpoint`, or other MCP-only pseudo-elements.
- The export payload preserves native editability metadata: box-label `containerId`/`boundElements` and arrow `startBinding`/`endBinding` where present in the preview.
- The exported Excalidraw link has been verified as non-empty before being delivered.
- If the exported link cannot be verified, the reply does not present it as the final artifact and does not include a fallback artifact unless the user explicitly asks for one.
- The exported Excalidraw link is included if requested or expected.

## Preview vs Export Rule

Preview and export are different artifacts:

- Preview payloads may use `cameraUpdate` to guide the OpenClaw live canvas and verify readability.
- Export payloads must be clean native Excalidraw scenes intended for excalidraw.com.
- Clean export means removing MCP-only pseudo-elements, not flattening or stripping Excalidraw editability metadata.
- Preserve valid native Excalidraw metadata in exports: container text (`containerId` + matching shape `boundElements`) and bound arrows (`startBinding`/`endBinding` + reciprocal shape `boundElements`).
- The preview is mostly an internal quality gate; the editable Excalidraw link is the normal deliverable.

## Final Export Payload Rule

**Critical export criterion:** never include `cameraUpdate` or any other MCP-only pseudo-element in an excalidraw.com export payload.

`cameraUpdate` is only stage direction for the OpenClaw live preview. It is not a real Excalidraw scene element.

When exporting to excalidraw.com:

0. Start from the already-previewed diagram whenever possible. The expected sequence is `create_view` -> inspect/preserve the preview scene -> `export_to_excalidraw` with a full native scene object.
1. Strip all `cameraUpdate`, `delete`, `restoreCheckpoint`, and other MCP-only pseudo-elements.
2. Do **not** strip native Excalidraw editability fields such as `containerId`, shape `boundElements`, arrow `startBinding`, arrow `endBinding`, `groupIds`, or arrow labels.
3. **Do not pass the raw element array to `export_to_excalidraw`.** `create_view` takes an array, but the exporter needs a serialized full scene object.
4. Export a real Excalidraw scene payload with `type`, `version`, `source`, `elements`, `appState`, and `files`.
4. Ensure `elements` is non-empty and contains actual shapes/arrows/text, not only preview/camera metadata.
5. After export, verify the share link before replying. Use the browser when available, or another concrete inspection path that proves the link contains non-empty scene data. Do not rely on the exporter returning a URL as proof.
6. If the first share link opens empty or export times out, regenerate the export from the same full scene object before replying.
7. Do not deliver an empty, camera-only, raw-array, or unrelated simplified export link.
8. If you must simplify to recover from repeated export failures, disclose that the link is a simplified fallback and keep the inline preview as the source of truth.
9. If verification still fails, do not provide any fallback artifact by default. Say the export failed verification and ask whether the user wants another attempt or a different requested format. No fallback is better than surprising the user with an artifact they did not ask for.

Minimal export shape:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "openclaw",
  "elements": [
    { "type": "rectangle", "id": "example", "x": 0, "y": 0, "width": 160, "height": 80 }
  ],
  "appState": { "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

## Memory & User Preference Guidance

If a user states a durable Excalidraw preference, such as always wanting editable links with diagram replies, update the appropriate OpenClaw memory using the workspace memory policy. Keep it concise and preference-focused; do not store one-off diagram details or broken-export noise.

## Artifact Progression Guidance

For blog posts, tutorials, case studies, or debugging write-ups, keep useful intermediate Excalidraw links instead of replacing them all.

Good progression artifacts include:

- First hello-world or minimal proof-of-life scene.
- Broken/empty export that motivated a fix.
- Early rough diagram before layout or label improvements.
- Final polished diagram.

Use these links as iteration evidence when they help tell the story. Do not clutter normal user deliverables with every intermediate link unless the user is writing about the process.

## Fallbacks

If labels or fonts fail again:

1. Regenerate with fewer, larger boxes and explicit text.
2. Avoid all `label` shortcut fields.
3. If bound container text fails, remove `containerId`/`boundElements` and use visually positioned standalone text.
4. If arrow binding fails, first check that connected shapes include matching arrow `boundElements`; if it still fails, remove `startBinding`/`endBinding` and use visually positioned arrows.
5. If still broken, use another export path such as SVG/PNG or a different diagram tool.
6. Tell the user plainly that the MCP/export path is dropping metadata.

## Style Defaults

- Use Excalidraw's built-in pastel palette where possible.
- Keep diagrams readable at Discord/web preview sizes.
- Prefer fewer large elements over many tiny elements.
- Use camera updates for complex diagrams, but keep the final overview clear.
- For system diagrams, show boundaries such as cluster, control plane, worker nodes, services, storage, and external clients.
- Do not add a legend by default. Add one only if the user asks, or if the diagram uses 3+ arrow styles/colors whose meanings are not obvious. Prefer direct labels near arrows when that is enough.

## Readability Budget

Default to a readable overview unless the user explicitly asks for a dense/deep technical diagram.

- Aim for roughly 8-12 major boxes or groups in the main view.
- Use `fontSize: 16` as the minimum for normal labels and body text.
- Use `fontSize: 20+` for titles, section headers, and key concepts.
- Prefer overview + callout boxes over cramming every detail into one canvas.
- If the topic needs more detail, create a secondary zoom/callout area or suggest a follow-up diagram.
- The user can override this when they want a denser architecture map, but readability wins by default.

## Arrow Routing

Treat arrow routing as a first-class readability concern.

Best effort rules:

- Avoid drawing arrows through text, labels, or the center of important boxes.
- Prefer orthogonal paths with bends around content when a straight arrow would cross labels.
- Put arrow labels beside the line, not directly under another arrow.
- Leave whitespace corridors between groups for traffic arrows.
- If multiple arrows must cross the same area, route one above and one below rather than stacking them.
- Use dashed arrows only for secondary/control/config flows, but still keep them away from text.
- If a perfect route is too hard in generated coordinates, make a cleaner first draft and tell the user it may need minor manual nudging in Excalidraw.

### Arrow Routing Recipes

Use these common patterns before inventing custom paths:

#### Left-to-right pipeline

- Arrange stages horizontally with consistent spacing.
- Route primary data flow as solid arrows from right edge to left edge.
- Put arrow labels above the line, centered in the whitespace between boxes.
- If a side input exists, place it above or below the relevant stage and route a short orthogonal arrow into that stage.

#### Hub-and-spoke

- Put the shared service, broker, bus, or control component in the center.
- Place clients around the perimeter in clusters.
- Route arrows radially, but bend them around central labels.
- Use color or labels to distinguish inbound vs outbound flows.

#### Top-down control plane

- Put users/API/automation at the top, control plane in the middle, workers/data plane at the bottom.
- Use vertical solid arrows for primary commands or traffic.
- Use dashed arrows for reconciliation, discovery, metadata, health checks, and configuration.
- Keep the control-plane box wide enough that arrows can land on edges instead of crossing its title.

#### Dashed metadata/control flows

- Use dashed arrows only for secondary relationships: metadata, config, coordination, replication hints, offset commits, health checks.
- Keep dashed arrows thinner or visually lighter than primary data-path arrows.
- Label dashed flows explicitly so they are not confused with user/data traffic.
- Route dashed flows around the outside edge of major groups when possible.
