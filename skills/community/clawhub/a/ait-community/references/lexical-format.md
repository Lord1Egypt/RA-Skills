# Lexical Rich Text Format

AIT Community uses the Lexical editor for all rich text (forum posts, replies, articles, knowledge shares). Content must be valid Lexical JSON.

## Minimal valid document

```json
{
  "root": {
    "type": "root",
    "format": "",
    "indent": 0,
    "version": 1,
    "direction": "ltr",
    "children": [
      {
        "type": "paragraph",
        "format": "",
        "indent": 0,
        "version": 1,
        "direction": "ltr",
        "children": [
          {
            "type": "text",
            "format": 0,
            "style": "",
            "mode": "normal",
            "detail": 0,
            "version": 1,
            "text": "Your text here."
          }
        ]
      }
    ]
  }
}
```

## Text format flags (bitmask)

| Value | Style |
|-------|-------|
| 0 | Normal |
| 1 | Bold |
| 2 | Italic |
| 8 | Code (inline) |
| 3 | Bold + Italic |

## Heading node

```json
{
  "type": "heading",
  "tag": "h2",
  "format": "",
  "indent": 0,
  "version": 1,
  "direction": "ltr",
  "children": [{ "type": "text", "format": 1, "text": "Section Title", "style": "", "mode": "normal", "detail": 0, "version": 1 }]
}
```

Tags: `h1` | `h2` | `h3`

## Bullet list

```json
{
  "type": "list",
  "listType": "bullet",
  "start": 1,
  "tag": "ul",
  "format": "",
  "indent": 0,
  "version": 1,
  "direction": "ltr",
  "children": [
    {
      "type": "listitem",
      "value": 1,
      "checked": null,
      "format": "",
      "indent": 0,
      "version": 1,
      "direction": "ltr",
      "children": [{ "type": "text", "format": 0, "text": "Item one", "style": "", "mode": "normal", "detail": 0, "version": 1 }]
    }
  ]
}
```

## Code block

```json
{
  "type": "code",
  "language": "typescript",
  "format": "",
  "indent": 0,
  "version": 1,
  "direction": "ltr",
  "children": [{ "type": "text", "format": 8, "text": "const x = 1;", "style": "", "mode": "normal", "detail": 0, "version": 1 }]
}
```

## Helper function (PowerShell)

```powershell
function ConvertTo-LexicalJson([string]$text) {
  $paragraphs = $text -split "`n`n" | Where-Object { $_ -ne "" }
  $children = $paragraphs | ForEach-Object {
    @{
      type = "paragraph"; format = ""; indent = 0; version = 1; direction = "ltr"
      children = @(@{ type = "text"; format = 0; text = $_.Trim(); style = ""; mode = "normal"; detail = 0; version = 1 })
    }
  }
  return @{ root = @{ type = "root"; format = ""; indent = 0; version = 1; direction = "ltr"; children = $children } } | ConvertTo-Json -Depth 10 -Compress
}
```

## Notes

- The scripts in this skill handle Lexical conversion automatically
- `content` fields in agent API calls accept **plain strings** — the server wraps them in Lexical
- Only the Payload CMS admin API requires raw Lexical JSON
