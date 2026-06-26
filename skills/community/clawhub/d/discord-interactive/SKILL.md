---
name: discord-interactive
version: 1.1.1
description: Send Discord Components v2 interactive messages (buttons, selects, modals, rich layouts) via the message tool.
read_when:
  - You need user confirmation (Yes/No, Approve/Reject)
  - You need user selection from multiple options
  - You want to display structured information with visual distinction
  - You need to collect form data from users
  - You want to send status cards with action buttons
  - Plain text message is insufficient for the interaction
metadata:
  openclaw:
    emoji: 🔘
homepage: https://github.com/openclaw/openclaw
---

# Discord Interactive Components (Components v2)

Send rich, interactive messages in Discord using the `message` tool's `components` parameter. This replaces plain text with buttons, select menus, modals, and structured layouts.

## When to Use Components v2

**ALWAYS prefer components over plain text when:**
- You need user confirmation → buttons (Yes/No, Approve/Reject)
- You need user selection → select menus (agents, priorities, options)
- You want structured information display → text blocks + sections + separators
- You want to collect form data → modals with text inputs, selects, checkboxes
- You want visual distinction → accent-colored containers

**Use plain text when:**
- Simple conversational response, no actions needed
- Quick one-liner answer

## Quick Reference

The `components` parameter is an object with this structure:

```json5
{
  // Top-level fields
  text: "Optional top-level text (rendered as first TextDisplay)",
  reusable: true,  // Keep buttons/selects active for multiple clicks (default: single-use)
  container: {
    accentColor: "#3498db",  // Left border color (hex string or number)
    spoiler: false
  },
  // Content blocks (rendered in order inside the container)
  blocks: [
    { type: "text", text: "Markdown text block" },
    { type: "section", text: "Main text", accessory: { type: "thumbnail", url: "https://..." } },
    { type: "separator", spacing: "small", divider: true },
    { type: "actions", buttons: [{ label: "Click me", style: "success" }] },
    { type: "actions", select: { type: "string", placeholder: "Choose...", options: [...] } },
    { type: "media-gallery", items: [{ url: "https://...", description: "..." }] },
    { type: "file", file: "attachment://report.pdf" }
  ],
  // Optional modal form (auto-generates a trigger button)
  modal: {
    title: "Form Title",
    triggerLabel: "Open Form",
    fields: [{ type: "text", label: "Your name" }]
  }
}
```

## Quick Start — Confirmation

```json5
// message tool call
{
  action: "send",
  channel: "discord",
  target: "channel:CHANNEL_ID",
  components: {
    text: "**Confirm action?**",
    reusable: false,
    container: { accentColor: "#3498db" },
    blocks: [
      {
        type: "actions",
        buttons: [
          { label: "Yes", style: "success" },
          { label: "No", style: "secondary" }
        ]
      }
    ]
  }
}
```

No `custom_id` needed — OpenClaw generates unique IDs automatically. When the user clicks, you receive a message like `Clicked "Yes".`

## Key Differences from Raw Discord API

| What you might expect | What OpenClaw actually uses |
|---|---|
| `type: "container"` wrapper | `container: { accentColor: "..." }` config object |
| `type: "text_display"` | `type: "text"` in blocks |
| `type: "action_row"` with nested components | `type: "actions"` with `buttons` or `select` |
| Manual `custom_id` on buttons | Auto-generated — just set `label` and `style` |
| `accent_color: 0x3498db` | `accentColor: "#3498db"` (hex string preferred) |
| `type: "string_select"` | `select: { type: "string", ... }` inside actions block |

## Block Types Summary

| Block Type | Purpose | See |
|---|---|---|
| `text` | Markdown text | [components.md](references/components.md) |
| `section` | Text + optional thumbnail/button | [components.md](references/components.md) |
| `separator` | Divider line | [components.md](references/components.md) |
| `actions` | Buttons or select menu | [components.md](references/components.md) |
| `media-gallery` | Image gallery | [components.md](references/components.md) |
| `file` | File attachment | [components.md](references/components.md) |

## Handling Interactions

When a user clicks a button or selects an option, OpenClaw delivers it as a normal inbound message:

- Button click → `Clicked "Yes".`
- Select → `Selected option_a from "Pick an option".`

No special callback handling needed — just read the incoming message text. See [handling.md](references/handling.md) for patterns.

## Important Rules

- **No `custom_id`** — OpenClaw auto-generates unique IDs for all interactive elements
- **No `embeds`** — Components v2 and embeds cannot coexist in the same message
- **`reusable: true`** — Set this to allow buttons/selects to be clicked multiple times
- **`allowedUsers`** — Optionally restrict who can click a button (array of Discord user IDs)
- **Actions block** — Must have EITHER `buttons` OR `select`, never both
- **Max 5 buttons** per actions block, max 1 select per actions block

## Examples

See [references/examples.md](references/examples.md) for complete scenarios:
- Yes/No confirmation
- Agent/option selection
- Status card with actions
- Modal form collection
- Multi-step workflow
