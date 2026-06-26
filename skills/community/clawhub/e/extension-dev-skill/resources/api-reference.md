# EasyEDA Pro API Complete Reference

## Table of Contents

1. [API Type Definition Location](#api-type-definition-location)
2. [Global Object eda Property List](#global-object-eda-property-list)
3. [Primitive Type System](#primitive-type-system)
4. [Common Enums](#common-enums)
5. [MCP Tool Documentation](#mcp-tool-documentation)

---

## API Type Definition Location

**Complete API definitions**: the `index.d.ts` file bundled with this Skill (sourced from `@jlceda/pro-api-types`).

> Before using any API, you must dynamically query and confirm the latest signature via `grepSearch` + `readFile` in the Skill's `index.d.ts`. Do not look in `node_modules`. Never guess from memory.

### index.d.ts File Structure

The entire file is wrapped in a `declare global { }` block; all enums, interfaces, and classes are globally declared. The `eda` object is declared at the end of the file:

```typescript
declare global {
    // Enums, class definitions...
    class EDA {
        sch_Document: SCH_Document;
        // ...
    }
    const eda: EDA;
}
```

⚠️ Important: The file contains four types of declarations with different meanings:

| Declaration | Prefix Example | Meaning |
|-------------|---------------|---------|
| `class` | `DMT_*`, `SCH_*`, `PCB_*`, `SYS_*` | Callable classes, mounted on the `eda` object |
| `interface` | `IDMT_*`, `ISCH_*`, `IPCB_*`, `ISYS_*` | Data structures, used as method parameters or return types |
| `enum` | `EDMT_*`, `ESCH_*`, `EPCB_*`, `ESYS_*` | Enum constants, global scope, not mounted on `eda` |
| `type` | `TPCB_*`, `TSYS_*` | Type aliases, used for parameter or return type constraints |

When searching, use only the name itself without any keyword prefix; let the search results tell you which declaration type it actually is.

Search tips:
- Search for classes/interfaces: Use the name directly, e.g., `IPCB_PrimitiveComponent`, `IDMT_EditorDocumentItem` (without `class`/`interface`)
- Search for methods: Use the method name directly, e.g., `getState_PinName`
- Search for `eda` property list: Search for `class EDA`
- If no results: Check spelling, or search only the core term (e.g., `PrimitiveComponent` instead of `IPCB_PrimitiveComponent`)

---

## Global Object eda Property List

> The following list comes from the property definitions of `class EDA` in `index.d.ts`. To confirm the latest list, search for `class EDA`.

### Document Tree Management (dmt_*)

| Property | Class |
|----------|-------|
| `eda.dmt_Board` | DMT_Board |
| `eda.dmt_EditorControl` | DMT_EditorControl |
| `eda.dmt_Folder` | DMT_Folder |
| `eda.dmt_Panel` | DMT_Panel |
| `eda.dmt_Pcb` | DMT_Pcb |
| `eda.dmt_Project` | DMT_Project |
| `eda.dmt_Schematic` | DMT_Schematic |
| `eda.dmt_SelectControl` | DMT_SelectControl |
| `eda.dmt_Team` | DMT_Team |
| `eda.dmt_Workspace` | DMT_Workspace |

### Component Library Management (lib_*)

| Property | Class |
|----------|-------|
| `eda.lib_3DModel` | LIB_3DModel |
| `eda.lib_Cbb` | LIB_Cbb |
| `eda.lib_Classification` | LIB_Classification |
| `eda.lib_Device` | LIB_Device |
| `eda.lib_Footprint` | LIB_Footprint |
| `eda.lib_LibrariesList` | LIB_LibrariesList |
| `eda.lib_PanelLibrary` | LIB_PanelLibrary |
| `eda.lib_SelectControl` | LIB_SelectControl |
| `eda.lib_Symbol` | LIB_Symbol |

### PCB Editing (pcb_*)

| Property | Class |
|----------|-------|
| `eda.pcb_Document` | PCB_Document |
| `eda.pcb_Drc` | PCB_Drc |
| `eda.pcb_Event` | PCB_Event |
| `eda.pcb_Layer` | PCB_Layer |
| `eda.pcb_ManufactureData` | PCB_ManufactureData |
| `eda.pcb_MathPolygon` | PCB_MathPolygon |
| `eda.pcb_Net` | PCB_Net |
| `eda.pcb_Primitive` | PCB_Primitive |
| `eda.pcb_PrimitiveArc` | PCB_PrimitiveArc |
| `eda.pcb_PrimitiveAttribute` | PCB_PrimitiveAttribute |
| `eda.pcb_PrimitiveComponent` | PCB_PrimitiveComponent |
| `eda.pcb_PrimitiveDimension` | PCB_PrimitiveDimension |
| `eda.pcb_PrimitiveFill` | PCB_PrimitiveFill |
| `eda.pcb_PrimitiveImage` | PCB_PrimitiveImage |
| `eda.pcb_PrimitiveLine` | PCB_PrimitiveLine |
| `eda.pcb_PrimitiveObject` | PCB_PrimitiveObject |
| `eda.pcb_PrimitivePad` | PCB_PrimitivePad |
| `eda.pcb_PrimitivePolyline` | PCB_PrimitivePolyline |
| `eda.pcb_PrimitivePour` | PCB_PrimitivePour |
| `eda.pcb_PrimitivePoured` | PCB_PrimitivePoured |
| `eda.pcb_PrimitiveRegion` | PCB_PrimitiveRegion |
| `eda.pcb_PrimitiveString` | PCB_PrimitiveString |
| `eda.pcb_PrimitiveVia` | PCB_PrimitiveVia |
| `eda.pcb_SelectControl` | PCB_SelectControl |

### Panel Editing (pnl_*)

| Property | Class |
|----------|-------|
| `eda.pnl_Document` | PNL_Document |

### Schematic Editing (sch_*)

| Property | Class |
|----------|-------|
| `eda.sch_Document` | SCH_Document |
| `eda.sch_Drc` | SCH_Drc |
| `eda.sch_Event` | SCH_Event |
| `eda.sch_ManufactureData` | SCH_ManufactureData |
| `eda.sch_Netlist` | SCH_Netlist |
| `eda.sch_Primitive` | SCH_Primitive |
| `eda.sch_PrimitiveArc` | SCH_PrimitiveArc |
| `eda.sch_PrimitiveAttribute` | SCH_PrimitiveAttribute |
| `eda.sch_PrimitiveBus` | SCH_PrimitiveBus |
| `eda.sch_PrimitiveCircle` | SCH_PrimitiveCircle |
| `eda.sch_PrimitiveComponent` | SCH_PrimitiveComponent \| SCH_PrimitiveComponent3 |
| `eda.sch_PrimitivePin` | SCH_PrimitivePin |
| `eda.sch_PrimitivePolygon` | SCH_PrimitivePolygon |
| `eda.sch_PrimitiveRectangle` | SCH_PrimitiveRectangle |
| `eda.sch_PrimitiveText` | SCH_PrimitiveText |
| `eda.sch_PrimitiveWire` | SCH_PrimitiveWire |
| `eda.sch_SelectControl` | SCH_SelectControl |
| `eda.sch_SimulationEngine` | SCH_SimulationEngine |
| `eda.sch_Utils` | SCH_Utils |

### System Functions (sys_*)

| Property | Class |
|----------|-------|
| `eda.sys_ClientUrl` | SYS_ClientUrl |
| `eda.sys_Dialog` | SYS_Dialog |
| `eda.sys_Environment` | SYS_Environment |
| `eda.sys_FileManager` | SYS_FileManager |
| `eda.sys_FileSystem` | SYS_FileSystem |
| `eda.sys_FontManager` | SYS_FontManager |
| `eda.sys_FormatConversion` | SYS_FormatConversion |
| `eda.sys_HeaderMenu` | SYS_HeaderMenu |
| `eda.sys_I18n` | SYS_I18n |
| `eda.sys_IFrame` | SYS_IFrame |
| `eda.sys_LoadingAndProgressBar` | SYS_LoadingAndProgressBar |
| `eda.sys_Log` | SYS_Log |
| `eda.sys_Message` | SYS_Message |
| `eda.sys_MessageBox` | SYS_MessageBox |
| `eda.sys_MessageBus` | SYS_MessageBus |
| `eda.sys_PanelControl` | SYS_PanelControl |
| `eda.sys_RightClickMenu` | SYS_RightClickMenu |
| `eda.sys_Setting` | SYS_Setting |
| `eda.sys_ShortcutKey` | SYS_ShortcutKey |
| `eda.sys_Storage` | SYS_Storage |
| `eda.sys_Timer` | SYS_Timer |
| `eda.sys_ToastMessage` | SYS_ToastMessage |
| `eda.sys_Tool` | SYS_Tool |
| `eda.sys_Unit` | SYS_Unit |
| `eda.sys_WebSocket` | SYS_WebSocket |
| `eda.sys_Window` | SYS_Window |

---

## Primitive Type System

### Base Interfaces

- `IPCB_PrimitiveAPI` — Unified interface for primitive management classes (`create` / `delete` / `modify` / `get` / `getAll`)
- `IPCB_Primitive` — Primitive instance base interface (`getState_PrimitiveType` / `toAsync` / `toSync` / `done`)

### setState_* Behavior Differs Between PCB and SCH

- **PCB primitives**: `setState_*` methods return `this`, supporting method chaining. Call `.done()` to commit: `line.setState_StartX(100).setState_StartY(200).done()`
- **SCH primitives**: `setState_*` does NOT commit changes. You must use the class-level `modify()` method instead. See `resources/experience.md` #8 for details.

### Inheritance Example

- `IPCB_PrimitiveComponentPad extends IPCB_PrimitivePad` — Component pad inherits from pad
- `ISCH_Primitive` — Schematic primitive base interface, uses `getState_*` for reading but requires `modify()` for writing

### Important: Always Query Before Use

Do not rely on memorized method names. Every `getState_*` / `setState_*` method and every class method must be verified via `grepSearch` + `readFile` in `index.d.ts` before use. The type definitions are the single source of truth.

### API Stability Markers

| Marker | Meaning |
|--------|---------|
| `@beta` | Interface may change in future versions |
| `@alpha` | Early stage; interface may change significantly |
| `@internal` | Should not be used in extensions |

---

## Common Enums

> Enum value types vary — some are numbers, some are strings. You must query `index.d.ts` to confirm before use; do not assume the type.

### EDMT_EditorDocumentType — Editor Document Type (Numeric Enum)

```typescript
enum EDMT_EditorDocumentType {
    HOME = -1,                  // Home page
    BLANK = 0,                  // Blank page
    SCHEMATIC_PAGE = 1,         // Schematic page
    SYMBOL_COMPONENT = 2,       // Component symbol
    PCB = 3,                    // PCB
    FOOTPRINT = 4,              // Footprint
    PCB_2D_PREVIEW = 12,        // PCB 2D preview
    SYMBOL_CBB = 17,            // Reusable block symbol
    SYMBOL_NET_FLAG = 18,       // Net flag symbol
    SYMBOL_NET_PORT = 19,       // Net port symbol
    SYMBOL_DRAWING = 20,        // Drawing symbol
    SYMBOL_NON_ELECTRICAL = 21, // Non-electrical symbol
    SYMBOL_SHORT_CIRCUIT_FLAG = 22, // Short circuit flag symbol
    PANEL = 26,                 // Panel
    PANEL_3D_PREVIEW = 27,      // Panel 3D preview
    PANEL_LIBRARY = 29,         // Panel library
    PCB_3D_PREVIEW = 15,        // PCB 3D preview
}
```

### EDMT_ItemType — Project Tree Node Type (String Enum)

```typescript
enum EDMT_ItemType {
    WORKSPACE = "Workspace",
    TEAM = "Team",
    FOLDER = "Folder",
    PROJECT = "Project",
    CBB_PROJECT = "CBB Project",
    BOARD = "Board",
    SCHEMATIC = "Schematic",
    CBB_SCHEMATIC = "CBB Schematic",
    SCHEMATIC_PAGE = "Schematic Page",
    PCB = "PCB",
    CBB_PCB = "CBB PCB",
    PANEL = "Panel",
}
```

---

## MCP Tool Documentation

MCP service name: `eext-dev-mcp`
Dependency: Chrome Remote Debugging Protocol (port 9222), auto-launches Chrome
Chrome path: `C:\Program Files\Google\Chrome\Application\chrome.exe`
Login cache: `mcp-eext-dev\.browser-data` (login state persisted; no repeated QR code scanning needed)
Log cache limit: 500 entries

### import_plugin

Import a local plugin file into EasyEDA Pro.

```
Parameters:
  pluginPath: string   # Absolute path to the plugin .zip file

Behavior:
  Auto-opens browser → If not logged in, shows QR code page → After login:
  Advanced → Extension Manager → Upload plugin file → Import
```

### dev_plugin

Import a plugin and enable console monitoring (for development debugging).

```
Parameters:
  pluginPath: string   # Absolute path to the plugin .zip file

Behavior:
  Same import flow as import_plugin
  Additionally enables browser console monitoring, auto-capturing console.log/warn/error/info and page errors
  After import, use get_console_logs to continuously retrieve logs
```

### get_console_logs

Retrieve EasyEDA browser console logs (requires prior `dev_plugin` call to enable monitoring).

```
Parameters:
  filter?: string    # Filter keyword, matches log type or content (e.g., "error", "warn")
  count?: number     # Return the most recent N log entries; defaults to all
  clear?: boolean    # Whether to clear the log cache after retrieval; defaults to false
```

---
