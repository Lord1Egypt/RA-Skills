---
name: jlceda-plugin-builder
description: >-
  AI Skill for building EasyEDA Pro extension plugins. Used when users need to create,
  modify, or debug JLCEDA/EasyEDA Pro plugins, including generating plugin code,
  querying pro-api-types API, configuring extension.json, and handling i18n localization.
  Trigger words: "EasyEDA", "嘉立创EDA", "EDA plugin", "EDA extension", "extension.json",
  "pro-api-types", "原理图", "PCB设计"
license: MIT
compatibility: Build requires Node.js 18+; runtime is EasyEDA Pro browser sandbox
metadata:
  author: JLCEDA
  version: "1.0.0"
---

# JLCEDA Plugin Builder

Build extension plugins for EasyEDA Pro. Provides a complete API query workflow, code generation standards, and debugging toolchain.

## Core Principles

1. **Never guess APIs** — Check the Skill's `index.d.ts` first; if not found = does not exist
2. **Verify class existence before use** — Search class name with `grepSearch`; no results = do not use
3. **Verify API mount path** — The class where a method is defined ≠ the property it's mounted on under `eda`
4. **Verify return type methods** — Different methods on the same class may return completely different interface types
5. **Browser APIs are forbidden in the main process** — Cannot use `localStorage`, `window`, `document`; allowed inside iframe
6. **Document type values** — SCH=1, PCB=3, FOOTPRINT=4 (PCB is not 2)

## When to Use

**Applicable:**
- Creating or modifying EasyEDA Pro extension plugins
- Querying API method signatures in `@jlceda/pro-api-types`
- Configuring `extension.json`, locales i18n files, or build processes
- Automating plugin import/debugging via `eext-dev-mcp` MCP tools

**Not applicable:**
- General TypeScript/JavaScript questions unrelated to EasyEDA Pro
- Non-EasyEDA Pro EDA tools
- Workspace has no `extension.json` and user did not request initialization

## API Query Workflow (Four Steps)

API type definition location: the `index.d.ts` file bundled with this Skill (sourced from `@jlceda/pro-api-types`). Always search in this file; do not look in `node_modules`.

### Step 1: Find the Correct Class

```bash
grepSearch "SCH_PrimitiveComponent"   # Schematic component class
grepSearch "PCB_PrimitiveVia"         # PCB via class
```

### Step 2: Verify the Class Is Mounted on the eda Object

```bash
grepSearch "sch_PrimitiveComponent:"  # Note the colon
grepSearch "dmt_SelectControl:"       # Verify mount path
```

### Step 3: Find the Method and Confirm Its Signature

```bash
grepSearch "getCurrentDocumentInfo"
```
Then use `readFile` to read the full signature and confirm parameter types and return type.

### Step 4: Verify the Return Interface Has the Required Methods

```bash
# Search the returned interface type to confirm it has the needed methods
grepSearch "ISCH_PrimitiveComponent$1"  # Interfaces with $1 suffix usually have more methods
```

**No search results = does not exist. Do not use!**

## Execution Workflow

1. **Plan** — Understand requirements, confirm target editor (home/sch/pcb) and core functionality
2. **Init** — If workspace is not initialized, run project initialization; otherwise skip
3. **Query** — Dynamically query required APIs (four-step method); every API must be verified
4. **Validate** — Verify all type signatures are complete with no guesswork; if uncertain, return to Query
5. **Confirm** — Present implementation plan to user (API list, dependencies, data flow, file changes); wait for confirmation in Supervised mode. In Autopilot mode, skip this step for straightforward changes; only pause for complex or destructive operations
6. **Execute** — Generate code; each API call corresponds to a verified signature, wrapped in `try/catch`
7. **Check** — Check runtime environment constraints; confirm no forbidden operations; if violations found, return to Execute to fix

### API Verification Checklist (Required Before Using Any API)

- [ ] `grepSearch` found the method name; confirmed return type
- [ ] `readFile` read the full signature; confirmed all parameter types and counts
- [ ] Confirmed `eda.xxx_YYY` class exists in the `class EDA` property list
- [ ] Confirmed API is mounted on the correct module
- [ ] Verified the returned interface type also has the required methods
- [ ] If using `getAllPrimitiveId`, must use a concrete type (not an abstract class)
- [ ] Document type checks use the correct `documentType` values

## Runtime Environment Constraints

| Requirement | ❌ Forbidden | ✅ Recommended |
|-------------|-------------|----------------|
| Get user input | - | `eda.sys_Dialog.showInputDialog()` |
| User selection | - | `eda.sys_Dialog.showSelectDialog()` |
| Show message | `alert()` | `eda.sys_Dialog.showInformationMessage()` |
| Confirm action | `confirm()` | `eda.sys_Dialog.showConfirmationMessage()` |
| Toast notification | DOM manipulation | `eda.sys_Message.showToastMessage()` |
| Store data | `localStorage` (main process) | `eda.sys_Storage.setExtensionUserConfig(key, value)` |
| Custom UI | Manipulate host DOM | `eda.sys_IFrame.openIFrame()` |
| Show HTML | `showInformationMessage(html)` | Must use iframe |
| Open link | `window.open()` | `eda.sys_Window.open()` |
| Browser hardware API | Use in main process | Available in iframe (`navigator.serial`, etc.) |
| IFrame data passing | `(window as any).__xxx = data` (main process and iframe window are isolated); `window.parent.eda` | ✅ Option A (recommended): Store with `eda.sys_Storage.setExtensionUserConfig(key, value)`, read in iframe with `getExtensionUserConfig(key)`; ✅ Option B: Call eda API directly from iframe (both main process and iframe can access the `eda` object; just use `eda` directly) |

## Project Initialization

When `extension.json` does not exist in the workspace:

```bash
git clone https://github.com/easyeda/pro-api-sdk.git <project-name>
cd <project-name>
npm install
npm run compile
```

## Failure Strategies

- API does not exist: Stop immediately, inform the user
- Signature uncertain: Stop generation, return to query step
- Workspace not initialized: Prompt user to initialize first
- Forbidden DOM API used: Automatically replace with `eda.sys_*` alternatives
- Menu ID conflict: Automatically add prefix to differentiate (e.g., `my-plugin-home`, `my-plugin-sch`)

## References

- Complete API module list, enum definitions → `resources/api-reference.md`
- Common pitfalls and lessons learned → `resources/experience.md`
- MCP tool documentation → "MCP Tools" section in `resources/api-reference.md`
