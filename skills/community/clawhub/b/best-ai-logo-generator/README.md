# AI Logo Generator — Claude Code Skill

Generate professional AI logos directly from your terminal using [ailogogenerator.online](https://ailogogenerator.online). Describe your brand, pick a vibe, and get a production-ready logo file in seconds — no design skills required.

---

## Install

```bash
npx skills add qq919006380/ai-logo-generator
```

That's it. Claude Code picks up skills from `~/.claude/skills/` automatically.

---

## Usage

Open Claude Code and describe what you need:

```
> /ai-logo-generator

You: Make a logo for my startup "Luminary" — clean, modern, light purple and white

Claude: Generating your logo for Luminary...
        Generating... (3s elapsed)
        Generating... (6s elapsed)
        Done! Saved to ./logo-luminary.png
```

You can also trigger it conversationally without the slash command:

```
You: I need a dark techy logo for my CLI tool called "Stackr", icon only, no text

Claude: [loads ai-logo-generator skill automatically and generates]
```

---

## Authentication

The first time you run the skill, it opens your browser to log in or register at ailogogenerator.online. After you authenticate, the token is stored at:

```
~/.config/ailogogenerator.online/auth.json
```

Subsequent runs use the cached token — no browser needed. To log out or switch accounts, delete that file and run the skill again.

---

## How it works

```
You describe the logo
        |
        v
Claude checks ~/.config/ailogogenerator.online/auth.json
        |
   token found?
   /          \
  Yes           No
  |              |
  |         login.mjs opens browser
  |         captures ?token= from callback
  |         saves to auth.json
  |              |
  +------+-------+
         |
         v
  POST /api/ai/logo/generate
  (subject, vibe, colors, text, shape...)
         |
         v
  Poll /api/ai/logo/query every 3s
         |
    status: completed
         |
         v
  Download imageUrl -> ./logo-*.png
         |
         v
  Show saved path to user
```

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `subject` | string | What the logo represents (required) |
| `vibe` | string | Style — modern, minimalist, bold, playful, elegant, vintage, techy |
| `colors` | string[] | Hex colors e.g. `["#1a1a2e","#e94560"]`. Empty = AI picks |
| `text` | string or null | Text to render. `null` = icon-only |
| `withBackground` | boolean | Include a background (default: false = transparent) |
| `shape` | string | square, circle, hexagon, free |
| `detail` | string | Free-text detail — "use a coffee cup silhouette" |

---

## Credits

Each logo generation costs 4 credits. New accounts receive bonus credits on registration. Top up at [ailogogenerator.online](https://ailogogenerator.online).

---

## Requirements

- [Claude Code CLI](https://claude.ai/code)
- Node.js >= 18
- Internet connection

---

## License

[MIT-0 (MIT No Attribution)](./LICENSE)
