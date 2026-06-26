# PDF Generator Schema Reference

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Document title (heading1) |
| `subtitle` | string | Subtitle below title (heading3) |
| `author` | string | Author name |
| `date` | string | Date string |
| `accent_color` | string | Accent color hex (default: #e94560) |
| `header_color` | string | Table header color (default: #1a1a2e) |
| `styles` | object | Custom style overrides |
| `sections` | array | Content sections |
| `output` | string | Output PDF path (alternative to CLI --output) |

## Section Types

### text
```json
{"type": "text", "text": "Body paragraph text."}
```

### heading
```json
{"type": "heading", "text": "Section heading"}
```

### subheading
```json
{"type": "subheading", "text": "Subheading text"}
```

### highlight
```json
{"type": "highlight", "text": "Important callout in accent color."}
```

### list
```json
{"type": "list", "items": ["First item", "Second item", "Third item"]}
```

### table
```json
{
  "type": "table",
  "data": [
    ["Column 1", "Column 2", "Column 3"],
    ["Value 1", "Value 2", "Value 3"],
    ["Value 4", "Value 5", "Value 6"]
  ]
}
```
- First row is treated as header (bold, white text on header_color background)
- Rows alternate white/#f5f5f5

### image
```json
{
  "type": "image",
  "path": "/absolute/path/to/image.png",
  "width": 120,
  "height": 80
}
```
- width/height in mm (default: 150x80)
- Path must be absolute or relative to script execution

### pagebreak
```json
{"type": "pagebreak"}
```

## Example: Mautic Campaign Report

```json
{
  "title": "Mautic Kampagnenbericht",
  "subtitle": "Q1 2026",
  "author": "PragDev-Mautic",
  "date": "2026-04-27",
  "accent_color": "#e94560",
  "sections": [
    {"type": "heading", "text": "Kampagnenbersicht"},
    {"type": "table", "data": [
      ["Kampagne", "Gesendet", "Offen", "Klicks"],
      ["Newsletter April", "1,234", "456", "89"],
      ["Product Launch", "2,500", "890", "234"]
    ]},
    {"type": "pagebreak"},
    {"type": "heading", "text": "Top Kontakte"},
    {"type": "list", "items": ["Kontakt A", "Kontakt B", "Kontakt C"]}
  ]
}
```