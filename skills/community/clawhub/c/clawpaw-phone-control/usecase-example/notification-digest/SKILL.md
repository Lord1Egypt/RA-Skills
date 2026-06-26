---
name: notification-digest
description: Get a summary of recent phone notifications grouped by app. Use when user says "check my notifications", "what did I miss", "any alerts", etc.
disable-model-invocation: true
---

# Notification Digest

Collect and summarize recent phone notifications. Uses the ClawPaw `notifications` tool directly — no UI navigation needed for reading. UI control is only needed if the user wants to open an app to act on a notification.

## Step 1 — Fetch notifications

Call `notifications` tool (no parameters needed). It returns all notifications collected since ClawPaw started.

If the result is empty (`data: []`), tell the user: "No notifications collected yet. Notifications are captured from the moment ClawPaw starts — if the app was just launched, new notifications will appear over time."

## Step 2 — Organize and summarize

Group notifications by app (package name / app label). For each group:
- App name
- Number of notifications
- Each notification: title, text, timestamp

**Example output:**

```
Phone Notifications — 5 total across 3 apps:

**WhatsApp** (2)
- my Bro: "你换模型了吗" — 18:58
- Group "Work": "Meeting at 3pm" — 17:30

**Gmail** (2)
- "Your order has shipped" from Amazon — 16:00
- "Weekly digest" from GitHub — 15:30

**Calendar** (1)
- "Team standup in 15 minutes" — 14:45
```

Prioritize by recency (newest first within each group).

## Step 3 — Act on notifications (if requested)

If the user wants to act on a specific notification (e.g., "open that WhatsApp message", "reply to the email"):

1. Identify the app package name from the notification
2. `shell` → `monkey -p <package> -c android.intent.category.LAUNCHER 1`
3. `snapshot` — navigate to the relevant screen
4. Perform the requested action (read, reply, dismiss, etc.)

For common apps, use the dedicated skill if available:
- WhatsApp messages → use `whatsapp-messages` skill
- Instagram → use `instagram-post` skill

## Important Notes

1. **Notification access permission** must be granted to ClawPaw in the device settings (Settings → Notification access → ClawPaw → ON). Without this, the `notifications` tool returns empty.
2. Notifications are collected **from the moment ClawPaw starts** — it does not have historical data from before the app launched.
3. Some notifications may contain sensitive information (banking, 2FA codes). Present them to the user but never log or store them.
4. The `sms` tool can also read SMS messages directly, including auto-extracting verification codes — use it if the user asks specifically about text messages or OTP codes.
