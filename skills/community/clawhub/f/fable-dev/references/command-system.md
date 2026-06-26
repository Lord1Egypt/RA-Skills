# Command System Reference

Fable's command system is modeled after VS Code with three cooperating singletons.

## ContextService

**File**: `src/frontend/services/commandInfra/context/ContextService.ts`

A global `Map<string, any>` with pub/sub. Components call `contextService.set(key, value)` or `setMultiple({...})`. Changes fire all listeners synchronously.

### Context key constants

**File**: `src/frontend/services/commandInfra/context/keys.ts`

All keys are defined in `CONTEXT_KEYS` to prevent typos:
- `FILE_EXPLORER_FOCUS` -- whether file explorer has focus
- `EDITOR_FOCUS` -- whether text editor has focus
- `SELECTED_FILE_ID` -- currently highlighted file in explorer
- `SELECTED_FILE_NAME` -- name of selected file
- `SELECTED_IS_FOLDER` -- whether selected node is a folder
- `SELECTED_IS_TRASH_FOLDER` -- whether selected is the trash
- `RENAMING_FILE_ID` -- file currently in rename mode
- `COPYING_FILE_ID` -- file in clipboard for paste
- `PROJECT_ID` -- current project ID
- `TRASH_FOLDER_ID` -- the trash folder's ID
- `WORKSPACE_MODE` -- current workspace mode

### selectionContext bundle

**File**: `src/frontend/services/commandInfra/context/bundles/selectionContext.ts`

High-level helper that atomically updates all selection-related keys:
- `set(node)` -- sets SELECTED_FILE_ID, SELECTED_FILE_NAME, SELECTED_IS_FOLDER, etc.
- `update(node)` -- same as set
- `clear()` -- clears all selection keys
- `clearIfSelected(id)` -- clears only if the given id matches the current selection

### useContextKey hook

Syncs a React state variable with a context key bidirectionally. Use when a component both reads and writes a context key.

## CommandService

**File**: `src/frontend/services/commandInfra/commands/CommandService.ts`

Holds a `Map<string, Command>`. Each command:

```typescript
interface Command {
    id: string;            // e.g., "file.rename"
    title: string;         // for command palette
    category: "file" | "project" | "editor" | "view" | "system";
    execute: (...args: any[]) => any | Promise<any>;
    when?: WhenClause;     // optional availability predicate
}
```

### Execution behavior

`commandService.execute(id, ...args)`:
- **With no args**: checks `when` clause against `contextService` before running (keyboard-triggered, context-driven)
- **With args**: skips `when` clause entirely (programmatic, e.g. context menu with explicit `node.id`)

### when clause DSL

**File**: `src/frontend/services/commandInfra/context/whenClause.ts`

```typescript
when.key("fileExplorerFocus")               // key is truthy
when.keyEquals("renaming", null)            // key === value
when.keyNotEquals("selectedFileId", null)   // key !== value
when.and(...clauses)                        // all true
when.or(...clauses)                         // any true
when.not(clause)                            // invert
```

`WhenClause` is `(ctx: ContextService) => boolean`.

## KeybindingService

**File**: `src/frontend/services/commandInfra/keybindings/KeybindingService.ts`

Maps `{key, scope, when}` to command IDs:

```typescript
interface KeybindingContribution {
    key: string;           // e.g., "F2", "mod+p", "Delete"
    commandId: string;
    scope: string;         // "fileExplorer" | "global"
    when?: WhenClause;
}
```

### useKeybindings hook

**File**: `src/frontend/services/commandInfra/keybindings/useKeybindings.ts`

`useKeybindings(scope)` attaches a `keydown` listener on `document`. It:
1. Gets command for key via `keybindingService.getCommandForKey(key, scope)` (strict scope match, no fallback)
2. Evaluates the binding's own `when` clause
3. Checks `commandService.isAvailable(commandId)` (evaluates command's `when` clause -- intentional double-check)
4. Calls `commandService.execute(commandId)` (no args, context-based)

Input elements (`INPUT`, `TEXTAREA`) suppress all keybinding handling.

Scopes in use:
- `"global"` -- registered in `CommandInfraProvider`
- `"fileExplorer"` -- registered in `FileExplorer`

### FocusRegistry

**File**: `src/frontend/services/commandInfra/keybindings/FocusRegistry.ts`

Lightweight singleton for decoupling commands from React refs:
- Components: `focusRegistry.register("omnibar", handler)` returns unregister function
- Commands: `focusRegistry.focus("omnibar")`

## Command definitions

### File commands (`fileCommands.ts`)

| Command ID | Description | Context-mode behavior |
|---|---|---|
| `file.rename` | Rename file | Reads SELECTED_FILE_ID; no newName -> enters rename mode |
| `file.delete` | Delete file | Reads SELECTED_FILE_ID; shows confirmation |
| `file.emptyTrash` | Empty trash | Deletes all trash descendants |
| `file.duplicate` | Duplicate file | Deep-copies subtree |
| `file.moveToTrash` | Move to trash | Moves to trash folder |
| `file.create` | Create new file | Creates under selected/root; type param for folder/agentflow/graph |
| `file.import` | Import from OS | Reads OS file, converts documents to Plate JSON |
| `file.export` | Export file | Converts Plate JSON to HTML/Markdown/DOCX |
| `file.copy` | Copy file ref | Stores ID in COPYING_FILE_ID context key |
| `file.paste` | Paste file | Duplicates the file stored in COPYING_FILE_ID |
| `file.readContent` | Read content | Cache-first with IPC fallback |
| `file.writeContent` | Write content | Writes via IPC + updates cache |
| `file.move` | Move file | Optimistic tree move |
| `file.updateMetadata` | Update metadata | Shallow merge metadata |

### View commands (`viewCommands.ts`)

Focus management commands (omnibar focus, sidebar toggle, etc.).

## Registration flow

All commands and keybindings are registered in `CommandInfraProvider.tsx` via a one-time `useEffect` guarded by `initialized.current` (survives React StrictMode double-invoke). On unmount, all registries are cleared in reverse order.

## Tool integration

The same file commands are exposed as LLM tools via `src/shared/toolDescriptors.ts` (shared schema) + `toolFactory.ts` (backend executor). This enables AI agents to perform file operations using the same command semantics.

## End-to-end example: F2 to rename

```
1. keydown "F2" on document (scope: "fileExplorer")
2. useKeybindings("fileExplorer") handler fires
3. keybindingService.getCommandForKey("f2", "fileExplorer")
   -> finds binding with when: fileExplorerWhen
   -> evaluates: FILE_EXPLORER_FOCUS=true AND EDITOR_FOCUS=false
4. commandService.execute("file.rename")  [no args -> context-based]
   -> command.execute() reads SELECTED_FILE_ID from contextService
   -> no newName -> sets RENAMING_FILE_ID = fileId
5. FileExplorer's contextService.subscribe() sees RENAMING_FILE_ID changed
   -> calls treeRef.current.edit(id)  [Arborist rename mode]
   -> clears RENAMING_FILE_ID back to null
6. RenameInput mounts, user types, presses Enter
   -> commandService.execute("file.rename", id, finalName)  [with args -> programmatic]
   -> queryService.mutations.renameFile(...)  [optimistic update]
   -> window.api.renameFile(...)  [IPC to backend]
   -> backend emits tree update -> frontend cache updated authoritatively
```
