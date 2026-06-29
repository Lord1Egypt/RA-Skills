## Dark Mode Token System

### Light Mode (default)

| Token | Value | Role |
|---|---|---|
| surface | #f5f0eb | Background |
| surface-alt | #e8e4e0 | Elevated surface |
| text-primary | #1B365D | Main text |
| text-secondary | #44403c | Secondary text |
| border | #a8a29e | Borders |
| accent | #002FA7 | Signature accent |

### Dark Mode

| Token | Value | Role |
|---|---|---|
| surface | #1a1814 | Background |
| surface-alt | #2a2520 | Elevated surface |
| text-primary | #e8e4e0 | Main text |
| text-secondary | #a8a29e | Secondary text |
| border | #44403c | Borders |
| accent | #58a6ff | Accent (lighter for dark bg) |

### Mermaid Init (dark mode)
```
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#2a2520', 'primaryTextColor': '#e8e4e0', 'primaryBorderColor': '#44403c', 'lineColor': '#a8a29e', 'tertiaryColor': '#1a1814', 'fontSize': '13px'}}}%%
```

### CSS Custom Properties
```css
:root {
  --surface: #f5f0eb;
  --surface-alt: #e8e4e0;
  --text-primary: #1B365D;
  --text-secondary: #44403c;
  --border: #a8a29e;
  --accent: #002FA7;
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface: #1a1814;
    --surface-alt: #2a2520;
    --text-primary: #e8e4e0;
    --text-secondary: #a8a29e;
    --border: #44403c;
    --accent: #58a6ff;
  }
}
```
