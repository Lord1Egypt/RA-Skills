# AGENTS.md — Agent Instructions for jlceda-plugin-builder

## Project Overview

JLCEDA Plugin Builder — An AI Skill for building EasyEDA Pro extension plugins. Provides API query standards, code generation templates, and a debugging toolchain.

**Language**: TypeScript (plugin code)
**Runtime**: EasyEDA Pro extension sandbox (browser environment, not Node.js)
**API Types**: `@jlceda/pro-api-types`

> For core workflow, execution steps, and runtime constraints, see `SKILL.md`.
> This file covers supplementary rules and conventions that are not in `SKILL.md`.

## Directory Structure

```
jlceda-plugin-builder/
  SKILL.md                          # Skill definition (core rules and workflow)
  AGENTS.md                         # Supplementary agent guide (this file)
  index.d.ts                        # API type definitions (from @jlceda/pro-api-types)
  resources/
    api-reference.md                # Complete API module list, enums, MCP tool docs
    experience.md                   # Common pitfalls and lessons learned
```

## API Type Source

The `index.d.ts` in this Skill directory is the authoritative API type definition file.
- Sourced from: `@jlceda/pro-api-types`
- Version: `1.0.0` (update this when re-syncing from the npm package)
- Always search in this file; do not look in `node_modules/@jlceda/pro-api-types/`

## grepSearch Standards

| Search Target | Correct | Incorrect |
|---------------|---------|-----------|
| Class/Interface name | `SCH_PrimitiveComponent` | `class SCH_PrimitiveComponent` |
| Method name | `getCurrentDocumentInfo` | `function getCurrentDocumentInfo` |
| Enum name | `EDMT_EditorDocumentType` | `enum EDMT_EditorDocumentType` |
| eda property | `dmt_SelectControl:` | `eda.dmt_SelectControl` |

## Recursive Query Triggers

When an API query result contains any of the following, you must continue querying recursively:

1. Returns `Promise<IPCB_*>` or `Promise<ISCH_*>` → Query all `getState_*` / `setState_*` methods of that interface
2. Parameter contains a complex interface → Query its property structure
3. Interface has inheritance → Query both parent and child classes
4. Return value is a union type → Query each member
5. Enum type parameter → Query all possible enum values

## Code Generation Rules

> Core rules (try/catch wrapping, browser API restrictions) are defined in `SKILL.md` Execution Workflow and Runtime Environment Constraints. The following are additional conventions:

- npm dependencies can be imported as needed; update `package.json` accordingly
- Use `console.error` (not `console.log`) in `catch` blocks for error visibility
- Prefer `async/await` over `.then()` chains for readability
- All generated code must be valid TypeScript; do not use `any` unless unavoidable

## Generated Plugin Project Structure

```
├── src/                 Main plugin code (src/index.ts is the entry point)
├── iframe/              Frontend code for custom UI panels
├── locales/             i18n files (en.json + zh-Hans.json)
├── images/              Extension preview images (logo.png + banner.png)
├── build/               Build output directory
├── extension.json       Plugin metadata and menu configuration
├── package.json         NPM configuration
└── tsconfig.json        TypeScript compilation configuration
```

## MCP Debugging Workflow (Optional)

Requires the `eext-dev-mcp` MCP service:

1. Build the plugin: `npm run build` (output in `build/dist/*.eext`)
2. Use `listDirectory` to find the absolute path of the `.eext` file
3. Use MCP tool `dev_plugin` to import
4. Use MCP tool `get_console_logs` to retrieve logs
5. Fix issues and repeat

Without MCP installed, manually upload the `.zip` file in the EDA Extension Manager.

## Do Not Modify

- `index.d.ts` — From `@jlceda/pro-api-types`; do not edit manually
- `SKILL.md` front matter — Contains Skill metadata
