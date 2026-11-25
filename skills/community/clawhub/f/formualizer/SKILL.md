---
name: formualizer
description: Recalculate cached Excel (.xlsx) formula values, inspect cells and ranges, and trace formula precedents or dependents locally using Formualizer — zero LibreOffice, zero Python virtualenv, zero cloud upload.
---

# Formualizer Spreadsheet Recalculation & Tracing

Use Formualizer to recalculate stale Excel formula caches, verify totals, read cells/ranges, and trace formula dependency chains locally with zero cloud upload.

## Local Tooling Options

Pick whichever runtime is available in your environment:

### 1. Native CLI (`@formualizer/cli`) — fastest for large `.xlsx` files

```bash
npx -y @formualizer/cli recalc workbook.xlsx -o recalculated.xlsx
npx -y @formualizer/cli recalc workbook.xlsx --check
```

### 2. Zero-native WASM SDK (`pi-spreadsheet`) — Node 20+, Bun, or Cloudflare Workers

```bash
npm install pi-spreadsheet
```

```ts
import { recalculateXlsx, inspectWorkbook, traceWorkbook } from "pi-spreadsheet";

const receipt = await recalculateXlsx("model.xlsx", { outputPath: "model.recalc.xlsx" });
const cells = await inspectWorkbook("model.recalc.xlsx", { cells: ["Summary!G12"] });
const trace = await traceWorkbook("model.recalc.xlsx", ["Summary!G12"], { direction: "precedents", maxDepth: 2 });
```

### 3. Local stdio MCP server (`@formualizer/mcp`) — zero-install 4-verb MCP

```json
{
  "mcpServers": {
    "formualizer": {
      "command": "npx",
      "args": ["-y", "@formualizer/mcp"]
    }
  }
}
```

## Rules of Thumb

- Always recalculate after generating or modifying `.xlsx` files with Python (`openpyxl`) or Node scripts that leave formula caches empty or stale.
- Report exact formula error counts, changed cache counts, and any partial/unsupported diagnostics returned by Formualizer rather than assuming silent success.
- Keep workbook processing local; never upload private `.xlsx` files to third-party web endpoints.
