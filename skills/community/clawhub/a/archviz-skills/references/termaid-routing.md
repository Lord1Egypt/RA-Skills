# termaid Terminal Routing

Use termaid when the target environment is terminal, SSH, CI logs, TUI, or plain-text review.

## Routing

| Situation | Output |
|---|---|
| Terminal supports Unicode | `termaid diagram.mmd --theme mono --width N` |
| Terminal width is narrow | Add `--gap 1 --padding-x 2` |
| CI log / safest text | Add `--ascii` |
| User needs Markdown render too | Ship Mermaid source + termaid preview |
| termaid unavailable | Use templates under `templates/ascii/` |

## Preferred Command

```bash
termaid diagram.mmd --theme mono --width 100
```

For conservative logs:

```bash
termaid diagram.mmd --ascii --width 80
```

## Skill Policy

- Mermaid remains the source of truth when possible.
- termaid is a terminal renderer, not a replacement for Mermaid.
- Always keep an ASCII fallback for documents that may be copied into plain text.
- For Gantt, keep codes inside the Mermaid block and put human-readable detail in a table beside it.

## Anti-Patterns

- Do not hand-draw ASCII first when valid Mermaid already exists.
- Do not use colorful terminal themes by default; `mono` is the default for archviz.
- Do not exceed 100 columns unless the user explicitly wants wide terminal output.

