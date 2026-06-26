# Fable Architecture Reference

## Layer Stack

```
Frontend (React renderer process)
    | window.api (contextBridge)
Preload (electron/preload.ts)
    | ipcRenderer.invoke / ipcRenderer.on
IPC Main (src/backend/main.ts -- ipcMain.handle registrations)
    |
Handler classes (fileHandlers, projectHandlers, agentHandlers, agentFlowHandlers)
    |
ProjectManager (singleton -- project CRUD, mounting, event routing)
    |
IndexedFsService extends EventEmitter implements FsService
    |
fs-extra (filesystem reads/writes)
    |
UserDataService (better-sqlite3 -- global project registry)
```

## Backend

### Entry flow

1. `electron/main.js` imports `registerIpcHandlers` from `src/backend/main.ts`
2. `registerIpcHandlers(mainWindow)` creates a `ProjectManager` singleton, an `IpcTransport`, and four handler classes
3. All `ipcMain.handle(...)` registrations live in `main.ts`

### IndexedFsService

The primary filesystem implementation. Manages:
- `currentProject: IndexedProjectMeta` -- full project JSON in memory
- `currentIdToNode: Map<string, IndexedFileNode>` -- O(1) id-to-node lookup
- `currentMetadataCache: Map<string, FileMetadata>` -- loaded metadata per file

Tree mutation pattern (all operations):
1. Mutate the in-memory `IndexedFileNode` tree directly
2. Update the `idToNode` map to stay in sync
3. Write the entire `IndexedProjectMeta` to `.fablex.json` via `fs.writeJson`
4. Emit a `fileChanged` event with type (create/delete/move/rename/update/metadata-update)

The internal `IndexedFileNode` has `parent: string` (parent's id, `""` for root). The tree is a nested JSON structure. A `Map<id, IndexedFileNode>` is built on load for O(1) lookups.

### ReferenceIndexService

Maintains a reverse-index of graph node references across project files:
- **Forward index**: `sourceFileId -> Set<targetFileId>`
- **Reverse index**: `targetFileId -> FileReferenceEntry[]`
- Rebuilt on `mountProject()` by scanning all graph files
- Updated incrementally on graph content changes via `reindexFile()`
- Pushed to frontend via `transport.sendReferenceIndexUpdate()`

### Event flow (backend to frontend)

`IndexedFsService` emits `"fileChanged"` events. `ProjectManager.mountProject()` listens and routes:
- Structural changes -> `transport.sendFileTreeUpdate(tree)` -> full tree push
- User-created files -> `transport.sendFileCreated(id)` -> triggers rename mode
- Content updates -> `transport.sendFileContentUpdate(id, null)` -> cache invalidation
- Graph file changes -> `referenceIndexService.reindexFile()` -> `transport.sendReferenceIndexUpdate()`

`STRUCTURAL_FILE_CHANGES` = `["create", "delete", "move", "rename", "reorder", "metadata-update"]`. Content `"update"` does NOT trigger tree rebroadcast.

### UserDataService

Global SQLite DB (`userdata.db`) in `app.getPath("userData")/Fable/`. Only stores the project registry (id, root, name, word count, status). Separate from per-project data.

### FileWatcherManager

Uses Chokidar for OS-level file watching:
- Single active watcher per project
- Config: `ignoreInitial: true`, ignores hidden files
- Events: `add`, `change`, `unlink`
- Started on `mountProject()`, stopped on unmount

### IPC channels (file operations)

| Channel | Handler | Notes |
|---|---|---|
| `file:read` | `readFile` | Returns UTF-8 or base64 string |
| `file:write` | `writeFile` | Accepts UTF-8 or base64 |
| `file:create` | `createFile` | `index=-1` appends at end |
| `file:move` | `moveFile` | Same-parent reorder and cross-parent move |
| `file:rename` | `renameFile` | Max length 255 chars |
| `file:delete` | `deleteFile` | `descendantsOnly=true` empties a folder |
| `file:duplicate` | `duplicateFile` | Deep-copies subtree with new ULIDs |
| `file:updateMetadata` | `updateFileMetadata` | Shallow merge with existing |
| `file:selectImport` | (dialog) | File dialog for OS import |
| `file:readFromOS` | (direct) | Read arbitrary OS file to base64 |

### IPC channels (project operations)

| Channel | Handler | Notes |
|---|---|---|
| `project:create` | `createProject` | Init project + persist |
| `project:list` | `listProjects` | All registered projects |
| `project:get` | `getProject` | Single project metadata |
| `project:remove` | `removeProject` | Remove metadata only |
| `project:mount` | `mountProject` | Start watching + broadcast tree |
| `project:validatePath` | `validateProjectPath` | Check folder/index exist |
| `project:showInFolder` | (shell) | Open in OS file explorer |
| `project:getStatuses` | `getProjectStatuses` | Custom status definitions |
| `project:updateStatuses` | `updateProjectStatuses` | Persist custom statuses |
| `project:select` | (dialog) | File dialog for project selection |

### IPC channels (agent/chat)

| Channel | Handler | Notes |
|---|---|---|
| `agent:listModels` | `listModels` | Available LLM models |
| `agent:listAgents` | `listAgents` | Built-in + project agents |
| `agent:createSession` | `createSession` | New chat session |
| `agent:listSessions` | `listSessions` | All sessions |
| `agent:getSession` | `getSession` | Session details |
| `agent:deleteSession` | `deleteSession` | Delete session |
| `agent:sendMessage` | `sendMessage` | Blocking message |
| `agent:sendMessageStreaming` | `sendMessageStreaming` | Async streaming |
| `agent:getMessages` | `getMessages` | Session message history |
| `agent:forkSession` | `forkSession` | Clone up to message |
| `agent:updateSessionTitle` | `updateSessionTitle` | Rename session |
| `agent:abort` | `abortGeneration` | Cancel generation |
| `agent:resolveToolConfirmation` | `resolveToolConfirmation` | Approve/deny tool |

### IPC channels (agentflow/workflow)

| Channel | Handler | Notes |
|---|---|---|
| `agentFlow:run` | `run` | Start workflow execution |
| `agentFlow:abort` | `abort` | Cancel running workflow |
| `agentFlow:resolveApproval` | `resolveApproval` | Approve/deny action |

### Transport channels (push events)

| Channel | Purpose |
|---|---|
| `transport:file_tree_update` | Full tree on structural changes |
| `transport:file_created` | User-initiated creates (triggers rename mode) |
| `transport:file_content_update` | External content changes |
| `transport:fs_event` | Raw filesystem watcher events |
| `transport:reference_index_update` | Graph reference index update |
| `transport:stream_chunk` | Streaming LLM response chunks |
| `agent:streamEvent` | Agent tool call / intermediate events |
| `agentFlow:streamEvent` | Agent workflow events |

## Frontend

### Provider tree (App.tsx)

```tsx
<QueryProvider>             // TanStack QueryClient init + queryService.initialize()
  <CommandInfraProvider>    // Registers commands, keybindings; activates global hotkeys
    <TooltipProvider>       // Radix UI tooltips
      <ProjectList | ProjectWorkspace>
    </TooltipProvider>
  </CommandInfraProvider>
</QueryProvider>
```

### Component organization

- `ProjectWorkspace.tsx` -- 3-panel layout (file explorer | editor | sidebar) using `react-resizable-panels`. Owns file selection/activation, save logic, collection view state.
- `FileExplorer.tsx` -- `react-arborist` virtualized tree. DnD, context menus, inline rename.
- `ContentViewer` -- dispatches by `metadata.subType` then `metadata.category`: `RichTextHandler` | `ImageHandler` | `AgentFlowHandler` | `AgentDefinitionHandler` | `GraphHandler` | `FallbackHandler`.
- `CollectionViewer` -- when active file has children, shows alternate views: `scroll` (stacked editors), `corkboard` (visual board). Registered via `CollectionViewRegistry` singleton.
- `Sidebar.tsx` -- Right panel with "companion" (chat) and "references" tabs.
- `StatusBar.tsx` -- Bottom bar with file status dropdown, tags, dynamic stats portal.
- `TitleBar.tsx` -- Top bar with logo, back button, project name, Omnibar trigger.
- `TopBar.tsx` -- File toolbar portal, collection view buttons, comments toggle.
- `Omnibar.tsx` -- Fuzzy file search (Ctrl+P) with recent selections.

### Data flow: complete mutation cycle

Example: DnD move in FileExplorer

```
1. react-arborist onMove({ dragIds, parentId, index })
2. commandService.execute("file.move", fileId, parentId, index)
3. queryService.mutations.moveFile(params)     [createTreeMutation factory]
4. [OPTIMISTIC] moveInTree(tree, ...) -> queryClient.setQueryData -> UI updates instantly
5. [ASYNC] window.api.moveFile(...) -> IPC -> FileHandlers -> IndexedFsService
6. IndexedFsService mutates in-memory tree, writes .fablex.json, emits "fileChanged"
7. ProjectManager routes event -> transport.sendFileTreeUpdate(tree)
8. IPC push -> window.api.onFileTreeUpdate -> queryClient.setQueryData (authoritative)
9. React re-renders with final server state
```

On error at step 5, the createTreeMutation factory restores the snapshot from step 3.

### File selection model

- `selectedFileId` (context key): highlighted in explorer, changes on arrow keys AND click
- `activeFileId` (context key): file shown in editor, only changes on Enter/click
- `selectionContext` bundle: atomically updates SELECTED_FILE_ID, SELECTED_FILE_NAME, SELECTED_IS_FOLDER, etc. in one `setMultiple` call

### FileExplorer DnD details

- `react-arborist` Tree component with `dndRootElement` set to the container div
- `childrenAccessor`: `(d) => d.children ?? []` -- always returns array, any file is a valid drop target
- Auto-expand on 600ms hover during drag (`DRAG_OVER_EXPAND_DELAY_MS`)
- Custom `FileExplorerCursor` renders a `DropIndicator` line at drop position
- Parent expansion on selection: `useLayoutEffect` calls `treeRef.current.openParents(selectedId)`

### React contexts

- `FocusedEditorContext` -- Tracks which editor has focus in multi-file (collection) views; manages find/replace state
- `SelectionContext` -- Stores user-selected text as `SelectionItem[]` for chat mentions
- `GraphEditingContext` -- Graph editor state (node/edge selection, editing mode)
- `ProjectStatusContext` -- Shared status definitions for the project

## Shared Code (src/shared/)

Code in `src/shared/` is imported by BOTH frontend and backend. It must not use:
- Browser APIs (window, document, DOM)
- Node.js APIs (fs, path, process)
- React or any frontend framework

Currently contains:
- `graph.ts` -- GraphFile schema, parsing, defaults
- `graphUtils.ts` -- Pure graph query/mutation functions, Graphology bridge, formatting for LLM
- `agentFlow.ts` -- AgentFlowFile schema, parsing, defaults
- `agentDefinition.ts` -- Agent definition schema, XML serialization for LLM context
- `toolDescriptors.ts` -- 43 shared tool definitions used by both UI commands and LLM agent tools
- `formatFileForAgent.ts` -- Format file content for LLM context (Plate->Markdown, metadata->XML)
- `parseJson.ts` -- Safe JSON parsing with LLM output extraction
- `services/searchService.ts` -- Fuzzy search (fuzzysort) with query parsing

## Build System

### Dev mode
`npm run dev:electron` runs concurrently:
1. Vite dev server at localhost:3000 (renderer)
2. `wait-on http://localhost:3000 && electron electron/main.js`

In dev, `electron/main.js` dynamically imports `src/backend/main.ts` (TypeScript directly).

### Production build
`npm run build`:
1. `vite build` -- bundles renderer into `dist/`
2. `node scripts/build-backend.mjs` -- esbuild compiles backend to `dist/backend/`

In production, `electron/main.js` imports from `dist/backend/main.js`.

### Packaging
`electron-forge` with `@electron-forge/maker-squirrel` (Windows), `maker-zip`, `maker-deb`, `maker-rpm`.

### Key build config
- `vite.config.ts`: `base: "./"` for correct relative paths in packaged app
- `optimizeDeps.exclude` for native modules (`better-sqlite3`, `@grpc/grpc-js`, `@google/adk`, `adk-llm-bridge`)
- Path alias `"@/*": ["./*"]` maps to repo root
- `postinstall` runs `electron-rebuild -f -w better-sqlite3`
