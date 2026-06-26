---
name: excalidraw-architect
description: Build or revise architecture diagrams directly in excalidraw.com from natural-language requirements. Use when the user asks to draw, update, clean up, or restructure system diagrams/flowcharts in Excalidraw, especially for software architecture, data pipelines, multi-tenant designs, or workflow maps.
---

# Excalidraw Architect

## Overview
Generate structured architecture diagrams in Excalidraw by scripting scene elements (rectangles, text, arrows) through the page runtime API, then iterating quickly based on user feedback.

## Workflow

### 1) Open and verify the Excalidraw tab
Open `https://excalidraw.com/` in the browser tool and keep using the same `targetId` for all edits.

If the user already has a board open, reuse that tab instead of creating a new one.

### 2) Get Excalidraw runtime API from the page
Use an `evaluate` action to locate `excalidrawAPI` from the React fiber tree.

If API lookup fails, refresh once and retry.

Use this lookup logic (or equivalent):
- find `.excalidraw` root
- read `__reactFiber$*`
- traverse child/sibling fibers
- pick node where `memoizedProps.excalidrawAPI.updateScene` exists

### 3) Build scene elements from the requested architecture
Translate the user’s request into:
- container blocks (rectangles)
- section labels and body text
- directional arrows between blocks

Prefer clear readable layout:
- title at top
- left-to-right data flow unless user requests otherwise
- enough spacing to avoid overlap

### 4) Write scene to canvas
Call `api.updateScene({ elements, appState })` and then `api.scrollToContent(elements, { fitToContent: true })`.

When user requests changes, rewrite the scene deterministically (do not partially patch random elements unless user asks for tiny edits).

### 5) Confirm result
Send a short completion message and mention what changed.

## Editing Rules
- Preserve user’s scope boundaries (example: “only draw to Raw Data Pool”).
- Keep language concise and business-readable.
- Prefer complete labels over abbreviations.
- If text is too dense, split into multiple lines.
- If user asks for “only one layer”, remove downstream blocks explicitly.

## Reusable Resources

### scripts/
- `scripts/generate_excalidraw_scene.py`: convert a JSON spec into Excalidraw element JSON.

### references/
- `references/excalidraw-api-snippets.md`: tested API discovery and update snippets for browser evaluate calls.

Use scripts/resources when diagrams are large or need repeatable generation.