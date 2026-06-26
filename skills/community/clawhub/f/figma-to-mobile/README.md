# figma-to-mobile

Convert Figma designs to production-ready mobile UI code using AI.

Supports: **Jetpack Compose** · **Android XML** · **SwiftUI** · **UIKit**

## Demo

Here's a side-by-side comparison using a [Material Design 3 Messaging App](https://www.figma.com/community/file/1169726503071187057/) from Figma Community:

![Figma to Compose comparison](assets/demo-comparison.png)

**Left:** Figma design · **Right:** Generated Jetpack Compose code running in Android Studio

The tool reads the Figma design tree (auto-layout, style refs, variants) and generates idiomatic code — not pixel-positioned boxes.

## How It Works

1. **Fetch** — Python script calls Figma API to extract the node tree
2. **Interpret** — AI analyzes layout semantics: "6 similar rows → `LazyColumn`", "horizontal stack → `Row`"
3. **Generate** — Outputs platform-idiomatic code with proper theming (Material3, SF Symbols, etc.)
4. **Iterate** — Refine through natural language: "make the header sticky", "switch to dark theme"

## Install

### OpenClaw

```bash
clawhub install figma-to-mobile
```

### Claude Code

Copy the `figma-to-mobile` folder into your project:
```
your-project/.claude/skills/figma-to-mobile/
```

### GitHub Copilot

Copy the `figma-to-mobile` folder into your project:
```
your-project/.agents/skills/figma-to-mobile/
```

## Setup

1. Get a Figma Personal Access Token:
   - Figma → Avatar → Settings → Security → Personal Access Tokens
   - Generate a new token (starts with `figd_`)

2. Set the environment variable:
   ```bash
   # macOS/Linux
   export FIGMA_TOKEN="figd_your_token_here"

   # Windows PowerShell
   $env:FIGMA_TOKEN = "figd_your_token_here"
   ```
   Never paste tokens into chat logs. If you insist on using a `.env` file, edit it locally and ensure it is ignored by git.

## Usage

Paste a Figma design link in your AI assistant's chat:

> Convert this to Jetpack Compose: https://www.figma.com/design/xxx/Project?node-id=100-200

The agent will:
1. Fetch the design data from Figma API
2. Ask clarifying questions (platform, list vs static, etc.)
3. Generate production-ready code files
4. Iterate based on your feedback — only patches the changed lines, never regenerates the full file unless you ask

## What Makes It Different

| Feature | Screenshot-based tools | figma-to-mobile |
|---------|----------------------|-----------------|
| Input | Screenshot/image | Figma API (design tree) |
| Layout understanding | Pixel positions | Auto-layout semantics |
| Output quality | Absolute positioning | Idiomatic code (LazyColumn, VStack, etc.) |
| Iteration | Re-screenshot | Natural language refinement |
| Cost | Paid subscription | Free & open source |

## What's in the Box

```
figma-to-mobile/
├── SKILL.md              # Agent instructions (the brain)
├── scripts/
│   └── figma_fetch.py    # Figma API data fetcher
├── references/
│   ├── compose-patterns.md   # Jetpack Compose mapping rules
│   ├── xml-patterns.md       # Android XML mapping rules
│   ├── swiftui-patterns.md   # SwiftUI mapping rules
│   └── uikit-patterns.md     # UIKit mapping rules
└── assets/
    └── demo-comparison.png   # Demo comparison image
```

## Requirements

- Python 3.10+ with `requests` package
- Figma Personal Access Token (free)

## License

MIT
