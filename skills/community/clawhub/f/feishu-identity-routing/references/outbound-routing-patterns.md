# Outbound Routing Patterns

This skill separates outbound routing into three layers:

1. **Global subject resolution**
   - identify the same human by `union_id` first, then `user_id`
2. **App-context identity selection**
   - choose the correct app-local `open_id` for the target account/app
3. **Provider target construction**
   - build the actual delivery target expected by the provider/tool

## Why this matters

In Feishu, the same human can have different `open_id` values across different apps.
So this is wrong:

- resolve a person once
- reuse one `open_id` everywhere

This is correct:

- resolve the person globally
- resolve the target app/account
- choose that app's `open_id`
- construct the provider target from that `open_id`

## Feishu direct message pattern

```text
subject -> target app/account -> app-local open_id -> user:<open_id>
```

Required pairing:

- `accountId=<matching Feishu account>`
- `target=user:<open_id for that same app/account>`

## Generalizable design

Although this skill is Feishu-focused, the same pattern works more broadly:

- stable global identity key
- local account/app identity key
- provider-specific target format

That makes the workflow reusable for:

- multi-agent messaging
- account-scoped notifications
- permissions or document workflows
- future channels with app-local user identifiers
