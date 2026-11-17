---
name: manage-inbox
description: Read, triage and answer BulkPublish Inbox conversations (DMs, reviews, comment threads) and comments on published posts. Use when the user asks about messages, DMs, reviews, comments, replies, or wants to clear, assign or moderate their inbox.
---

# BulkPublish — Inbox and Comments

The Inbox gathers direct messages, reviews and comment threads from the user's
connected accounts. Comment tools work on the comments under a published post.

## The rule that matters most

**Every reply, message and deletion goes to a real person, immediately, and
cannot be unsent.** Before calling `reply_to_conversation`, `reply_to_comment`
or `moderate_comment` with `action: "delete"`:

1. Show the user the **exact text** you will send (or the comment you will delete).
2. Name the **recipient**: the platform, the user's account it goes out from,
   and the person it is addressed to.
3. Wait for an explicit yes for **that** message. Approval of one reply is not
   approval of the next.

Never send in bulk. If the user asks you to "answer all of these", draft every
reply, show them one by one (or as a numbered list the user approves item by
item), and send only the ones they confirmed. Drafting is always safe; sending
is not.

Liking, hiding and unhiding a comment are reversible, but still say what you are
about to do before doing it.

## Tools

```
list_conversations     list conversations
get_conversation       messages in one conversation
reply_to_conversation  send a DM or review reply now (cannot be unsent)
update_conversation    mark read, archive / reopen, snooze, assign
list_post_comments     comments on a published post
reply_to_comment       public reply under a comment (cannot be unsent)
moderate_comment       like, unlike, hide, unhide or delete a comment
```

### list_conversations

Filters, all optional: `status` (`open`, `archived`, `snoozed`), `kind`
(`dm`, `review`, `comment`), `platforms`, `channelId`, `assigned` (`me`,
`unassigned`, or a teammate's user id), `q` (text search), `limit`, and
`cursor` from the previous page.

### get_conversation

Returns the newest 500 messages, oldest first. Reading a conversation does
**not** mark it read; use `update_conversation` for that, and only when the user
wants it.

### reply_to_conversation

`text` up to 4,000 characters, `mediaIds` up to 4 (ids from `upload_media`).

### update_conversation

Mark read or unread, archive or reopen, snooze until a time (at most 90 days
ahead), assign to a teammate or unassign.

### moderate_comment

`action` is `like`, `unlike`, `hide`, `unhide` or `delete`. Deleting needs an
owner, admin or approver role on the workspace.

## When something is refused

Explain it in plain words and say what the user can do. Do not repeat error
codes or technical wording back to them.

- **Plan.** The Inbox is part of the Pro and Business plans; replying to or
  moderating comments on a post is on every plan except Free. When a call is
  refused for the plan, say so and suggest upgrading. Reading a post's
  comments works on every plan.
- **Reconnect needed** (`RECONNECT_REQUIRED`). The account was connected before
  message or comment access was granted. Ask the user to reconnect that channel
  from the Channels page, then try again.
- **Not available on that network.** Some platforms do not allow sending DMs or
  replying through BulkPublish yet. Tell the user to answer on the platform
  itself.
- **Role.** Deleting a comment needs an owner, admin or approver; suggest asking
  one of them.
- **Too fast.** Sending is limited to 30 messages and 10 comment replies a
  minute. Wait a minute and continue; do not retry in a tight loop.
- **X messages** count against the plan's X allowance. Mention this before a
  long run of X replies.

## Recipes

**Triage the inbox**
1. `list_conversations` with `status: "open"` (add `assigned: "me"` if asked)
2. `get_conversation` on the ones that look urgent
3. Summarise: who wrote, on which account, what they want
4. Offer next steps (reply, assign, snooze, archive) and act only on what the
   user picks

**Answer a DM or review**
1. `get_conversation` to read the thread
2. Draft a reply and show it with platform, account and recipient
3. On a clear yes, `reply_to_conversation`
4. Ask whether to archive or mark it read

**Work through comments on a post**
1. `list_posts` with `status: "published"`, then `list_post_comments`
2. Group the comments (questions, praise, complaints, spam)
3. Draft replies; confirm each one before `reply_to_comment`
4. Propose hiding spam; delete only when the user explicitly asks
