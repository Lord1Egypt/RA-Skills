# aesthete-agent MCP server

Expose the aesthete-agent color engine as MCP tools — usable from Claude Desktop, Cursor, and any MCP client.

## Run

```bash
uvx --from "git+https://github.com/docsor1212/aesthete-agent#subdirectory=mcp" aesthete-agent-mcp
```

Or with a local FastMCP environment: `python mcp/server.py` (stdio).

## Tools

| Tool | What it does |
|---|---|
| `palette_match(brief, limit, no_flags)` | Rank the 89-palette evidence library for a natural-language brief (register auto-detect + learned preferences) |
| `palette_harmony(base, mode, theme)` | OKLCH harmony generation (7 rules × light/dark) |
| `palette_score(palette)` | 5-dimension scorecard /20 with P0-P3 findings |
| `palette_contrast(fg, bg, method)` | WCAG ratio or APCA Lc (WCAG 3 draft) for one pair |
| `palette_matrix(palette, method, recommend)` | Full pairwise matrix + best-pair recommendation |
| `palette_blind(palette)` | Protanopia/deuteranopia/tritanopia simulation with collision flags |
| `palette_semantic(count, base)` | Color-blind-safe categorical colors for charts |
| `palette_themes()` / `palette_theme(name)` | Named theme packs → CSS tokens |
| `palette_export(palette, fmt)` | css / tailwind / json / svg / **w3c** (Design Tokens) / **context** (LLM-ready) |
| `palette_slop(palette)` | AI-slop signature detection (median-trap hexes, purple gradients, flat lightness) |

## Client config (Claude Desktop example)

```json
{
  "mcpServers": {
    "aesthete-agent": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/docsor1212/aesthete-agent#subdirectory=mcp", "aesthete-agent-mcp"]
    }
  }
}
```

Zero keys, zero telemetry. The engine runs fully offline; only `palette_*_extract`-style image tools require Pillow (not exposed here).

## Self-check

```bash
python mcp/server.py --check   # engine selftest + fastmcp availability
```
