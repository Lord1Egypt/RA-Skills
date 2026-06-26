# Common Development Recipes

Step-by-step procedures for common Fable development tasks. Each recipe is a checklist — follow every step.

## Adding a New IPC Channel (Frontend -> Backend)

1. **Handler**: Add method in the appropriate handler class (`src/backend/handlers/`)
2. **Register**: Add `ipcMain.handle("channel:name", handler)` in `src/backend/main.ts`
3. **Preload**: Expose via `contextBridge` in `electron/preload.ts`
4. **Types**: Add to `Window.api` interface in `src/global.d.ts`
5. **Call**: Use `window.api.newMethod()` in frontend code

For **push events** (backend -> frontend):
1. Add method to `ITransport` interface (`src/backend/transport/baseTransport.ts`)
2. Implement in `IpcTransport` (`src/backend/transport/ipcTransport.ts`)
3. Add listener in `electron/preload.ts` with `ipcRenderer.on(channel, handler)`
4. Expose as `window.api.onEventName(callback)` returning cleanup function
5. Add to `Window.api` in `src/global.d.ts`

## Adding a New Command

1. **Define**: Create in `src/frontend/services/commandInfra/commands/definitions/` (in `fileCommands.ts`, `viewCommands.ts`, or new category)
2. **Export**: Add to `definitions/index.ts` barrel export
3. **Register**: Add to `CommandInfraProvider.tsx` registration block
4. **Keybinding** (optional): Add in `keybindings/defaults.ts`
5. **Context keys** (optional): Add constants in `context/keys.ts`

Command execution modes:
- **No args** (keyboard): evaluates `when` clause, reads `contextService`
- **With args** (programmatic): skips `when` clause, uses provided arguments

## Adding a New File SubType

1. **Schema**: Create `src/shared/{subType}.ts` with `createDefault*File()` and `parse*File()` functions
2. **Creation**: Add case in `fileCommands.ts` `file.create` — set subType in metadata + default content
3. **Handler component**: Create in `src/frontend/components/fileViewer/handlers/`
4. **Routing**: Add case in `ContentViewer.tsx` routing (dispatches `subType` before `category`)
5. **Stats portal** (optional): Add in `fileViewer/handlers/statusBarStats/`
6. **i18n**: Add keys to BOTH `en` and `zh-CN` locale files
7. **Context menu**: Add creation entry in `FileExplorer.tsx`
8. **Agent tools** (optional): Add descriptors in `src/shared/toolDescriptors.ts` + executors in `toolFactory.ts`

## Adding a New Agent Tool

1. **Descriptor**: Add `ToolDescriptor` in `src/shared/toolDescriptors.ts`
2. **Executor**: Add function in `toolFactory.ts` `buildExecutors()`
3. **Read-only?**: If yes, add tool ID to `READ_ONLY_TOOL_IDS` set
4. **Confirmation?**: If destructive, set `requiresConfirmation: true`
5. **i18n**: Add tool name keys in `chat.json` (both locales — active/done variants)
6. **Agent allowlists**: Update relevant agent `allowedTools` arrays if needed

## Adding i18n Strings

1. Determine the correct namespace from the 8 available: `common`, `fileExplorer`, `chat`, `project`, `editor`, `agentBuilder`, `graph`, `agentDefinition`
2. Add key to `src/locales/en/{namespace}.json`
3. Add same key to `src/locales/zh-CN/{namespace}.json` (translate or leave English placeholder)
4. In React: `const { t } = useTranslation("{namespace}")` then `{t("keyName")}`
5. Outside React: `i18n.t("{namespace}:keyName")`
6. For rich text with interpolation: use `<Trans>` component

## Adding a Sidebar Panel Tab

1. Add tab ID to `SidebarTab` type in `Sidebar.tsx`
2. Create panel component in `src/frontend/components/{panelName}/`
3. Add tab button and conditional rendering in `Sidebar.tsx`
4. Add i18n keys for tab label and panel content

## Adding a New Editor Toolbar Button

1. Plate toolbar is portaled to `#file-toolbar-portal` in `TopBar.tsx`
2. Add button to the appropriate toolbar kit in `src/frontend/styles/plate/`
3. For custom functionality, create a Plate plugin or use an existing one
4. Register in the editor's plugin configuration

## Adding a Collection View Mode

1. Create view component implementing `CollectionViewProps`
2. Register via `CollectionViewRegistry.register()` in `src/frontend/components/collectionViewer/registry.ts`
3. Call registration in `registerAllViews()`
4. Add i18n keys for view name/description in `fileExplorer.json`
5. View button auto-appears in `TopBar.tsx` when file has children

## Adding a Context Menu Item (File Explorer)

1. Add menu item in `FileExplorer.tsx` context menu section
2. Wire to a command: `commandService.execute("command.id", node.id, ...args)`
3. Add i18n key for the label
4. If new command needed, follow "Adding a New Command" recipe above

## Modifying the File Tree (Mutations)

**Always use the optimistic update pattern:**

1. Add pure transformation function in `src/frontend/services/query/treeTransformations.ts`
   - Must return new array/object, never mutate in place
   - Recalculate `siblingIndex` on affected children
2. Add mutation in `queryService.mutations` using `createTreeMutation` factory
3. Add IPC call in the mutation's async handler
4. Backend: implement in `IndexedFsService` (mutate in-memory tree -> write `.fablex.json` -> emit event)

## Adding File Metadata Fields

1. Add optional field to `FileMetadata` interface in `src/types.ts`
2. **Must be optional** — existing files won't have it, code must handle `undefined`
3. Update `updateFileMetadata` handler if needed (it does shallow merge)
4. If displayed in UI, add to relevant component + i18n
5. If searchable, update `SearchService` in `src/shared/services/searchService.ts`

## Working with the Agent/Chat System

Key hooks and services:
- `useChat(projectId)` — full chat lifecycle (sessions, messages, streaming)
- `AgentService` — backend orchestrator
- `ToolFactory` — builds agent tools from shared descriptors
- `ProviderRegistry` — resolves model IDs to LLM adapters

See `references/agent-system.md` for full architecture.

## Verification Checklist

Before considering any change complete:

- [ ] `npm run check` passes (lint + format + TypeScript)
- [ ] i18n keys added to BOTH locales
- [ ] `src/global.d.ts` updated if IPC channels changed
- [ ] New user-facing elements have tooltips
- [ ] Tree mutations are pure (no in-place mutation)
- [ ] Shared code (`src/shared/`) has no browser/Node imports
- [ ] E2E tests written for new features run and pass (`npm run test:e2e`)

## Where to Look First (by Task Type)

| Task | Start here |
|---|---|
| UI bug | Component in `src/frontend/components/`, inspect with React DevTools |
| File operation bug | `src/backend/services/indexedFsService.ts` + `treeTransformations.ts` |
| Editor bug | `src/frontend/styles/plate/` (plugins) + `fileViewer/handlers/` |
| Command not working | `commandInfra/commands/definitions/` + `context/keys.ts` |
| IPC error | `electron/preload.ts` + `src/backend/main.ts` + `src/backend/handlers/` |
| AI/chat issue | `src/backend/services/agent/` + `src/frontend/hooks/useChat.ts` |
| Graph issue | `src/shared/graph.ts` + `src/frontend/components/graph/` |
| i18n missing | `src/locales/{en,zh-CN}/{namespace}.json` |
| DnD/tree issue | `FileExplorer.tsx` + `treeTransformations.ts` + `queryService.mutations` |
| State/cache issue | `src/frontend/services/query/queryService.ts` + hooks in `hooks/queries/` |
| Styling issue | `src/frontend/styles/` + `tailwind.config.js` |
