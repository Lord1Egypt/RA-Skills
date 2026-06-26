# Examples

## Example 1: Merge two app identities into one subject

Input records:

```json
{
  "source_agent": "main-agent",
  "app_context": "main-agent",
  "open_id": "ou_app_a",
  "user_id": "g123",
  "union_id": "on_abc",
  "name": "Alice",
  "phone": "+8613000000000",
  "captured_at": "2026-03-30T10:00:00+08:00"
}
```

```json
{
  "source_agent": "research-agent",
  "app_context": "research-agent",
  "open_id": "ou_app_b",
  "user_id": "g123",
  "union_id": "on_abc",
  "name": "Alice",
  "phone": "+8613000000000",
  "captured_at": "2026-03-30T10:05:00+08:00"
}
```

Expected result:
- one subject
- two app identities
- merge key = `union_id`

## Example 2: Route outbound DM from a specific account

Goal:
- send from `research-agent` account to the same human

Process:
1. resolve subject by `union_id`/`user_id`
2. pick `app_context=research-agent`
3. read `open_id=ou_app_b`
4. send with:

```text
accountId=research-agent
target=user:ou_app_b
```

## Example 3: Ambiguous merge goes to pending review

If a new record has:
- no reliable `union_id`
- a `user_id` that matches more than one subject

Do not merge automatically.
Send it to `pending_reviews`.
