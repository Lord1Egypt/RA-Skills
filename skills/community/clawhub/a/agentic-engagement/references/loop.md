# The conversation loop

Two wakes on the same chat make this a conversation instead of a send.

```
agentNativeTrigger({
  agentSlug: "email",
  config: { kinds: ["replied", "unsubscribed"] },
})

heartbeat: {
  intervalMinutes: 1440,
  maxMessages: 16,
  prompt: /* status check, not a sequence */,
}
```

`sendEmail` records which agent sent the message. When the thread's status
becomes `replied` or `unsubscribed`, the native `email` action wakes **the
same chat**. A thread that stays at `sent` never fires that trigger — the
heartbeat re-wakes the chat so the engager can call `listEmailEvents` and
decide (one follow-up, or stop).

That is the whole loop. Four ways it silently stops being a loop:

1. **A send that did not come from this agent.** A play that calls `sendEmail`
   itself starts a thread the trigger will never wake, because the trigger keys
   off chats *this* agent has emailed. First-touch belongs in a play that
   *calls the engager*, not a second send path.
2. **No heartbeat, or no `listEmailEvents`.** Silence has no event. Without a
   heartbeat the agent only wakes when they write back or opt out, so an
   unanswered first send is a dead chat. Without `listEmailEvents` a heartbeat
   infers status from chat history and may follow up on a thread that already
   replied.
3. **`kinds` that include `opened` or `interacted`.** A tracking-pixel view is
   not a reason to write. The agent wakes, spends a turn, and looks like a
   follow-up nobody asked for. `unsubscribed` is the opposite: status that
   must stop a send.
4. **A reply missing `inReplyTo` or a truncated `references` chain.** Mail
   clients split the conversation. The next wake then has no thread to
   continue, and the lead sees two emails instead of one.

Status is the mailbox event on the thread (`sent`, `replied`, `unsubscribed`,
and later `opened` / `clicked` / `bounced`). The engager reads it from
`listEmailEvents` — or from the trigger payload on a reply/unsubscribe wake —
not by calling `mailboxManagement`. Opens and clicks are not in trigger
`kinds`, so they never look like a reason to write.

Threading rules live in `infra/agents/engager.prompt.ts` and are the contract
the evaluator scores. `mailboxUuid` is locked on the `sendEmail` use in
`infra/agents/engager.ts`, so the agent cannot pick a different inbox.

Warm-up is not in the project spec. After the mailbox is `active`:

```sh
cargo-ai mailboxManagement mailbox start-warmup <uuid>
cargo-ai mailboxManagement mailbox get-send-allowance <uuid>
```

A mailbox that never starts warm-up stays at five real sends a day. The ramp
is a ceiling, not a target.
