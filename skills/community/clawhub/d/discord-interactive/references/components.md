# Components v2 Reference

Complete reference for all block types and properties in OpenClaw's `components` parameter.

## Top-Level Structure

The `components` object you pass to the `message` tool:

```json5
{
  text: "Top-level text (optional)",
  reusable: true,       // Allow multiple interactions (default: single-use)
  container: {
    accentColor: "#5865F2",  // Hex color string or number
    spoiler: false
  },
  blocks: [ /* block objects */ ],
  modal: { /* modal spec */ }
}
```

| Property | Type | Required | Description |
|---|---|---|---|
| `text` | string | No | Top-level text, rendered as the first TextDisplay in the container |
| `reusable` | boolean | No | `true` = buttons/selects stay active after first click |
| `container` | object | No | Container styling config |
| `container.accentColor` | string/number | No | Left border color. Hex string `"#3498db"` or number |
| `container.spoiler` | boolean | No | Hide container behind spoiler |
| `blocks` | array | No | Ordered list of content blocks |
| `modal` | object | No | Modal form definition (auto-generates trigger button) |

## Block Type: `text`

Markdown text block.

```json5
{
  type: "text",
  text: "**Bold** and _italic_ text with `code`"
}
```

| Property | Type | Required | Description |
|---|---|---|---|
| `text` | string | Yes | Markdown content |

Supports Discord markdown: `**bold**`, `_italic_`, `` `code` ``, etc.

## Block Type: `section`

Text content with optional thumbnail or button accessory.

```json5
// With single text
{
  type: "section",
  text: "Main description text",
  accessory: {
    type: "thumbnail",
    url: "https://example.com/image.png"
  }
}

// With multiple texts
{
  type: "section",
  texts: ["**Title**", "Description line 1", "Description line 2"],
  accessory: {
    type: "thumbnail",
    url: "https://example.com/image.png"
  }
}

// With button accessory
{
  type: "section",
  text: "Click the button →",
  accessory: {
    type: "button",
    button: { label: "Open", style: "primary" }
  }
}
```

| Property | Type | Required | Description |
|---|---|---|---|
| `text` | string | One of text/texts required | Single text content |
| `texts` | string[] | One of text/texts required | Multiple text entries (max 3) |
| `accessory` | object | No | Side element: `thumbnail` or `button` |
| `accessory.type` | `"thumbnail"` \| `"button"` | Yes (if accessory) | Accessory type |
| `accessory.url` | string | For thumbnail | Image URL |
| `accessory.button` | ButtonSpec | For button | Button specification |

## Block Type: `separator`

Horizontal divider line.

```json5
{ type: "separator" }

// With options
{ type: "separator", spacing: "small", divider: true }
```

| Property | Type | Required | Description |
|---|---|---|---|
| `spacing` | `"small"` \| `"large"` | No | Spacing around separator |
| `divider` | boolean | No | Show visible line |

## Block Type: `actions`

Interactive elements — buttons OR a select menu (not both).

### With Buttons

```json5
{
  type: "actions",
  buttons: [
    { label: "Approve", style: "success" },
    { label: "Reject", style: "danger" },
    { label: "Later", style: "secondary" }
  ]
}
```

### With Select Menu

```json5
{
  type: "actions",
  select: {
    type: "string",
    placeholder: "Choose an option...",
    options: [
      { label: "Option A", value: "a", description: "First option" },
      { label: "Option B", value: "b", description: "Second option" }
    ]
  }
}
```

**Rules:**
- Max 5 buttons per actions block
- Max 1 select per actions block
- Cannot have BOTH buttons and select in the same actions block

### Button Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `label` | string | Yes | Button text (max 80 chars) |
| `style` | string | No | `"primary"` (blue), `"secondary"` (gray), `"success"` (green), `"danger"` (red), `"link"` (blue, opens URL) |
| `url` | string | For link buttons | URL to open (required when style is `"link"`) |
| `emoji` | object | No | `{ name: "✅" }` or `{ name: "custom", id: "123", animated: false }` |
| `disabled` | boolean | No | Gray out the button |
| `allowedUsers` | string[] | No | Discord user IDs allowed to click (others get denied) |

**Button Styles:**

| Style | Color | Use For |
|---|---|---|
| `primary` | Blue | Main action (default) |
| `secondary` | Gray | Alternative/cancel |
| `success` | Green | Confirm/approve |
| `danger` | Red | Delete/reject |
| `link` | Blue | Opens URL (no interaction callback) |

**Link Button Example:**
```json5
{ label: "Open Docs", style: "link", url: "https://docs.openclaw.ai" }
```

### Select Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | string | No | `"string"` (default), `"user"`, `"role"`, `"mentionable"`, `"channel"` |
| `placeholder` | string | No | Hint text when nothing selected |
| `options` | array | For string type | Selection choices (max 25) |
| `minValues` | number | No | Minimum selections |
| `maxValues` | number | No | Maximum selections |

**Select Option Properties:**

| Property | Type | Required | Description |
|---|---|---|---|
| `label` | string | Yes | Display text (max 100 chars) |
| `value` | string | Yes | Value returned on selection (max 100 chars) |
| `description` | string | No | Secondary text (max 100 chars) |
| `emoji` | object | No | `{ name: "🛠️" }` |
| `default` | boolean | No | Pre-selected |

## Block Type: `media-gallery`

Image gallery.

```json5
{
  type: "media-gallery",
  items: [
    { url: "https://example.com/image1.png", description: "First image" },
    { url: "https://example.com/image2.png", description: "Second image", spoiler: true }
  ]
}
```

| Property | Type | Required | Description |
|---|---|---|---|
| `items` | array | Yes | Non-empty array of media items |
| `items[].url` | string | Yes | Image URL |
| `items[].description` | string | No | Alt text |
| `items[].spoiler` | boolean | No | Hide behind spoiler |

## Block Type: `file`

File attachment reference.

```json5
{
  type: "file",
  file: "attachment://report.pdf",
  spoiler: false
}
```

| Property | Type | Required | Description |
|---|---|---|---|
| `file` | string | Yes | Must start with `attachment://` followed by filename |
| `spoiler` | boolean | No | Hide behind spoiler |

**Note:** Provide the actual file via the message tool's `media`/`path`/`filePath` parameter. The `file` block references it by name.

## Modal

Modal popup form. OpenClaw auto-generates a trigger button.

```json5
{
  modal: {
    title: "Submit Details",
    triggerLabel: "Fill Form",      // Button text (default: "Open form")
    triggerStyle: "primary",        // Button style
    fields: [
      {
        type: "text",
        label: "Your Name",
        placeholder: "Enter name...",
        required: true,
        style: "short"              // "short" (default) or "paragraph"
      },
      {
        type: "select",
        label: "Priority",
        options: [
          { label: "Low", value: "low" },
          { label: "High", value: "high" }
        ]
      },
      {
        type: "checkbox",
        label: "Features",
        options: [
          { label: "Dark mode", value: "dark" },
          { label: "Notifications", value: "notif" }
        ]
      }
    ]
  }
}
```

**Modal Field Types:**

| Type | Description | Requires `options`? |
|---|---|---|
| `text` | Text input (short or paragraph) | No |
| `select` | Dropdown select | Yes |
| `checkbox` | Multiple choice checkboxes | Yes |
| `radio` | Single choice radio buttons | Yes |
| `role-select` | Discord role picker | No |
| `user-select` | Discord user picker | No |

**Modal Field Properties:**

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Field type (see above) |
| `label` | string | Yes | Field label |
| `name` | string | No | Field name for results (auto-generated if omitted) |
| `description` | string | No | Helper text |
| `placeholder` | string | No | Placeholder text |
| `required` | boolean | No | Whether field is required |
| `options` | array | For select/checkbox/radio | Same format as select options |
| `style` | `"short"` \| `"paragraph"` | No | For text fields only |
| `minLength`/`maxLength` | number | No | For text fields |
| `minValues`/`maxValues` | number | No | For select/checkbox fields |

**Limits:** Max 5 fields per modal.

## Complete Example

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:123456789012345678",
  components: {
    reusable: true,
    container: { accentColor: "#667eea" },
    blocks: [
      {
        type: "section",
        texts: ["**Task Review**", "Please review and approve the proposed changes"],
        accessory: { type: "thumbnail", url: "https://cdn.example.com/task.png" }
      },
      { type: "separator" },
      {
        type: "actions",
        buttons: [
          { label: "Approve", style: "success", allowedUsers: ["123456789012345678"] },
          { label: "Reject", style: "danger" },
          { label: "Snooze", style: "secondary" }
        ]
      }
    ],
    modal: {
      title: "Rejection Reason",
      triggerLabel: "Add Details",
      triggerStyle: "secondary",
      fields: [
        { type: "text", label: "Reason", style: "paragraph", required: true }
      ]
    }
  }
}
```

## Accent Color Examples

| Color | Hex | Use |
|---|---|---|
| Blue (info) | `"#3498db"` | General information |
| Green (success) | `"#2ecc71"` | Success/completion |
| Red (danger) | `"#e74c3c"` | Error/warning |
| Yellow (warning) | `"#f1c40f"` | In progress/caution |
| Purple | `"#9b59b6"` | Special/featured |
| Discord Blurple | `"#5865F2"` | Default/neutral |
