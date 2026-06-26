# Handling Component Interactions

When users interact with buttons, select menus, or modals, OpenClaw delivers the interaction as a normal inbound message. No special callback system needed.

## How Interactions Arrive

OpenClaw converts Discord component interactions into readable text messages:

| Interaction | Message You Receive |
|---|---|
| Button click | `Clicked "Button Label".` |
| Select choice | `Selected value1, value2 from "Placeholder text".` |
| Select update (no values) | `Updated "Placeholder text".` |
| Modal submit | Form field values as structured text |

## Basic Handling Pattern

When a user clicks a button, you simply receive a message like:

```
Clicked "Approve".
```

Respond based on the button label:

- If the message says `Clicked "Approve"` → execute the approved action
- If the message says `Clicked "Reject"` → cancel the action
- If the message says `Selected engineer from "Choose an agent..."` → assign to engineer

No parsing of `custom_id` needed. OpenClaw handles all the plumbing.

## Select Menu Handling

For string selects:

```
Selected engineer from "Choose an agent...".
```

For multi-select:

```
Selected engineer, researcher from "Choose agents...".
```

## Updating After Interaction

After handling an interaction, update the original message to reflect the new state:

```json5
{
  action: "edit",
  channel: "discord",
  channelId: "CHANNEL_ID",
  messageId: "ORIGINAL_MSG_ID",
  components: {
    text: "✅ Approved by Linn",
    container: { accentColor: "#2ecc71" }
    // No blocks = just a text result card
  }
}
```

## Single-Use vs Reusable

**Single-use (default):** After one click, the button becomes unresponsive. Good for confirmations.

**Reusable (`reusable: true`):** Buttons stay active for multiple clicks until they expire. Good for:
- Status dashboards with ongoing actions
- Voting/polling interfaces
- Controls that should persist

```json5
{
  components: {
    reusable: true,  // ← buttons stay active
    blocks: [
      {
        type: "actions",
        buttons: [
          { label: "Refresh", style: "primary" },
          { label: "Close", style: "danger" }
        ]
      }
    ]
  }
}
```

## Async Timing

Users may click buttons minutes or hours after the message was sent. Design for this:

- Don't assume the interaction happens immediately
- Check if the context is still valid before executing
- If expired/invalid, update the message to indicate this

## Security: Restricting Access

Use `allowedUsers` on buttons to restrict who can interact:

```json5
{
  type: "actions",
  buttons: [
    {
      label: "Deploy",
      style: "success",
      allowedUsers: ["1106438955500584971"]  // Only Linn can click
    }
  ]
}
```

Unauthorized users see an ephemeral "not allowed" message. This is handled by OpenClaw automatically.

## Modal Form Handling

When a user submits a modal form, OpenClaw delivers the form data as a structured message. The field values are included in the inbound message for you to process.

```json5
// Send a message with a modal
{
  action: "send",
  channel: "discord",
  target: "channel:123",
  components: {
    text: "Need more details",
    modal: {
      title: "Task Details",
      triggerLabel: "Fill Form",
      fields: [
        { type: "text", label: "Task Name", required: true },
        { type: "select", label: "Priority", options: [
          { label: "High", value: "high" },
          { label: "Low", value: "low" }
        ]}
      ]
    }
  }
}
```

User clicks "Fill Form" → modal popup → user fills and submits → you receive form data as an inbound message.

## Pattern: Confirmation → Action → Result

The most common interactive workflow:

1. **Send** component message with action buttons
2. **Receive** click as inbound message (`Clicked "Yes".`)
3. **Execute** the requested action
4. **Edit** the original message to show the result

```json5
// Step 1: Ask
{
  action: "send",
  channel: "discord",
  target: "channel:123",
  components: {
    text: "Delete 5 old log files?",
    container: { accentColor: "#f1c40f" },
    blocks: [{
      type: "actions",
      buttons: [
        { label: "Delete", style: "danger" },
        { label: "Keep", style: "secondary" }
      ]
    }]
  }
}

// Step 2: User clicks "Delete" → receive: Clicked "Delete".

// Step 3: Execute deletion, then edit:
{
  action: "edit",
  channel: "discord",
  channelId: "CHANNEL_ID",
  messageId: "MSG_ID",
  components: {
    text: "✅ Deleted 5 log files (120MB freed)",
    container: { accentColor: "#2ecc71" }
  }
}
```
