# Component Examples

Complete, ready-to-use examples for common scenarios. All examples use the `message` tool.

## 1. Simple Yes/No Confirmation

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    text: "🧹 **Cleanup Request**\n\nDelete 5 temporary files (120MB)?",
    container: { accentColor: "#3498db" },
    blocks: [
      {
        type: "actions",
        buttons: [
          { label: "Yes, clean up", style: "success" },
          { label: "No, keep them", style: "secondary" }
        ]
      }
    ]
  }
}
```

When user clicks → you receive: `Clicked "Yes, clean up".` or `Clicked "No, keep them".`

## 2. Agent Selection (Select Menu)

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    text: "🎯 **Assign Task**\n\nSelect the best agent for this task:",
    container: { accentColor: "#667eea" },
    blocks: [
      {
        type: "actions",
        select: {
          type: "string",
          placeholder: "Choose an agent...",
          options: [
            {
              label: "Engineer",
              value: "engineer",
              description: "Python, algorithms, code review",
              emoji: { name: "🛠️" }
            },
            {
              label: "Researcher",
              value: "researcher",
              description: "Literature, theory, analysis",
              emoji: { name: "🔬" }
            },
            {
              label: "Writer",
              value: "writer",
              description: "Documentation, LaTeX, reports",
              emoji: { name: "📝" }
            }
          ]
        }
      }
    ]
  }
}
```

When user selects → you receive: `Selected engineer from "Choose an agent...".`

## 3. Task Status Card

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:THREAD_ID",
  components: {
    reusable: true,
    container: { accentColor: "#f1c40f" },
    blocks: [
      {
        type: "section",
        texts: [
          "🎯 **TASK_001: Implement Filter**",
          "Status: 🔵 In Progress\nAssigned: Engineer\nETA: 2 hours"
        ],
        accessory: { type: "thumbnail", url: "https://cdn.example.com/task-icon.png" }
      },
      { type: "separator" },
      {
        type: "actions",
        buttons: [
          { label: "Complete", style: "success" },
          { label: "Blocked", style: "danger" },
          { label: "Update", style: "primary" }
        ]
      }
    ]
  }
}
```

## 4. Priority Selection (Button Grid)

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    text: "⚡ **Set Priority**\n\nHow urgent is this task?",
    container: { accentColor: "#e74c3c" },
    blocks: [
      {
        type: "actions",
        buttons: [
          { label: "🔴 High", style: "danger" },
          { label: "🟡 Medium", style: "primary" },
          { label: "🟢 Low", style: "secondary" }
        ]
      }
    ]
  }
}
```

## 5. Modal Form Collection

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    text: "📋 **Submit a Bug Report**",
    container: { accentColor: "#e74c3c" },
    blocks: [
      { type: "text", text: "Click the button below to fill out the bug report form." }
    ],
    modal: {
      title: "Bug Report",
      triggerLabel: "Report Bug",
      triggerStyle: "danger",
      fields: [
        {
          type: "text",
          label: "Bug Title",
          placeholder: "Brief description...",
          required: true,
          style: "short"
        },
        {
          type: "text",
          label: "Steps to Reproduce",
          placeholder: "1. Go to...\n2. Click...\n3. See error",
          required: true,
          style: "paragraph"
        },
        {
          type: "select",
          label: "Severity",
          options: [
            { label: "Critical", value: "critical" },
            { label: "Major", value: "major" },
            { label: "Minor", value: "minor" }
          ]
        }
      ]
    }
  }
}
```

## 6. Multi-Step Workflow

```json5
// Step 1: Request confirmation
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    text: "📋 **New Request**\n\nRun full system analysis?",
    container: { accentColor: "#667eea" },
    blocks: [
      {
        type: "actions",
        buttons: [
          { label: "▶️ Start Analysis", style: "success" },
          { label: "Cancel", style: "secondary" }
        ]
      }
    ]
  }
}

// Step 2: User clicks "Start Analysis" → you receive: Clicked "▶️ Start Analysis".
// Update message to show progress:
{
  action: "edit",
  channel: "discord",
  channelId: "CHANNEL_ID",
  messageId: "ORIGINAL_MSG_ID",
  components: {
    text: "🔄 **Analysis Running...**\n\nThis may take a few minutes.",
    container: { accentColor: "#f1c40f" }
  }
}

// Step 3: After completion, update with results:
{
  action: "edit",
  channel: "discord",
  channelId: "CHANNEL_ID",
  messageId: "ORIGINAL_MSG_ID",
  components: {
    text: "✅ **Analysis Complete**\n\nFound 3 issues, 12 warnings.",
    reusable: true,
    container: { accentColor: "#2ecc71" },
    blocks: [
      { type: "separator" },
      {
        type: "actions",
        buttons: [
          { label: "View Report", style: "primary" },
          { label: "Download CSV", style: "secondary" }
        ]
      }
    ]
  }
}
```

## 7. Information Card (No Buttons)

Components don't have to be interactive. Use them for rich formatting:

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    container: { accentColor: "#2ecc71" },
    blocks: [
      { type: "text", text: "## 📊 Daily Summary" },
      { type: "separator", spacing: "small" },
      {
        type: "section",
        texts: [
          "**Tasks Completed:** 12",
          "**In Progress:** 3\n**Blocked:** 1"
        ]
      },
      { type: "separator", spacing: "small" },
      { type: "text", text: "_Updated at 2026-03-09 18:00 CST_" }
    ]
  }
}
```

## 8. Restricted Button Access

Only specific users can click:

```json5
{
  action: "send",
  channel: "discord",
  target: "channel:1477679555148779662",
  components: {
    text: "🔒 **Admin Action Required**",
    container: { accentColor: "#e74c3c" },
    blocks: [
      {
        type: "actions",
        buttons: [
          {
            label: "Approve Deploy",
            style: "success",
            allowedUsers: ["1106438955500584971"]
          },
          {
            label: "Reject",
            style: "danger",
            allowedUsers: ["1106438955500584971"]
          }
        ]
      }
    ]
  }
}
```

Users not in `allowedUsers` will see an ephemeral denial message.
