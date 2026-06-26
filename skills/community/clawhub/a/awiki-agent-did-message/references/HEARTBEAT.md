# Session Startup & Heartbeat Protocol

## Session Startup Flow (Every New Session)

### Step 1: Run Dashboard Check

```bash
cd <SKILL_DIR> && python scripts/check_status.py
```

### Step 2: Parse Status → Decide Next Action

| Status Condition | Recommended Action |
|-----------------|-------------------|
| `identity.status == "no_identity"` | Guide identity creation: `setup_identity.py --name "<name>"` |
| `identity.status == "jwt_refresh_failed"` | Inform the user refresh failed; suggest deleting credentials and recreating |
| `len(inbox.messages) > 0` | Surface the returned user-visible messages directly; decrypted E2EE items already include plaintext content plus an encrypted-message notice |
| `group_watch.active_groups > 0` | If the user is in an active group discovery cycle, use the listed groups as the heartbeat watch set |
| All normal | "DID identity OK, no unread messages." |

### Step 3: Report Summary (Format)

```
DID identity status: [name] ([DID abbreviated]) - JWT valid/refreshed
Inbox: [N] surfaced messages
  - [sender]: [count] messages (latest: [time])
Discovery groups: [N] locally tracked active groups
```

If decrypted E2EE messages were surfaced:
```
Encrypted message from [DID]: [plaintext shown with encrypted-message notice]
```

### Step 4: Check Profile Completeness

If the user hasn't set up their Profile (`get_profile.py` returns empty or missing nickname/bio), suggest at an appropriate time:
> "Consider completing your Profile — see template: `<SKILL_DIR>/references/PROFILE_TEMPLATE.md`"

If profile updates are needed, follow the standard profile workflow described in
`SKILL.md`.

## Heartbeat Check (Every 15 Minutes)

### Trigger Condition

When more than 15 minutes have passed since the last `check_status.py` execution, and the user sends a new message — run the check before processing the user's request.

For users who are actively using a discovery group for relationship discovery,
heartbeat is a **two-phase loop**:

1. run `check_status.py`
2. incrementally refresh and inspect the active discovery-group watch set

`check_status.py` must still run even when `message_transport.receive_mode=websocket`
and the listener is unhealthy. In that degraded case, heartbeat uses HTTP
fallback for the current cycle and may try to restart the listener in the
background.

Do not treat discovery-group work as a one-shot command. It is an ongoing
heartbeat task whenever the user is actively monitoring a group.

### State Tracking

The Agent should maintain in memory:
- `last_did_check_at`: ISO timestamp of the last check
- `consecutive_failures`: consecutive failure count
- `active_group_watch_ids`: group IDs currently under active discovery monitoring
- `group_watch_state`: per-group memory used for diffing active discovery loops

Recommended `group_watch_state` shape:

```json
{
  "grp_xxx": {
    "last_member_count": 12,
    "last_latest_member_joined_at": "2026-03-10T02:00:00Z",
    "last_latest_owner_message_at": "2026-03-10T02:05:00Z",
    "last_recommendation_at": "2026-03-10T02:10:00Z",
    "initialized": true
  }
}
```

The watch set should usually be empty. Add a group only when:

- the user has just joined it, or
- the user explicitly asks for ongoing group monitoring / recommendations, or
- the session is already in an active recommendation cycle for that group

Remove a group from the watch set when:

- the user leaves the group,
- the recommendation cycle is clearly over, or
- the user explicitly asks to stop monitoring it

### Group Phase (After `check_status.py`)

For each `group_id` in `active_group_watch_ids`, use this rule:

- **Initialize once** when the group has just been joined, has just entered the
  watch set, or local state is missing / obviously stale:

```bash
cd <SKILL_DIR> && python scripts/manage_group.py --get --group-id <GROUP_ID>
cd <SKILL_DIR> && python scripts/manage_group.py --members --group-id <GROUP_ID>
cd <SKILL_DIR> && python scripts/manage_group.py --list-messages --group-id <GROUP_ID>
```

- **Normal heartbeat path** after initialization is incremental. Do **not**
  keep re-running full refreshes on every heartbeat:

```bash
cd <SKILL_DIR> && python scripts/manage_group.py --list-messages --group-id <GROUP_ID> --since-seq <LAST_SYNCED_SEQ>
```

Use `group_watch.groups[].last_synced_seq` from `check_status.py` as the
incremental cursor. This is the normal source for:

- new owner messages
- new self-introductions
- `system_event` member joins / leaves / kicks
- other fresh recommendation signals

- **Fall back to `--members`** only when one of these is true:

- the group has not been initialized yet
- local member snapshot is missing
- you suspect local member drift or incomplete `system_event` coverage
- the user explicitly asks for a full member refresh
- you are running a low-frequency repair / reconciliation cycle

- **Fall back to `--get`** only when one of these is true:

- the group has not been initialized yet
- you need fresh metadata such as rules / goal / message prompt
- the user explicitly asks to inspect the group detail
- you are running a low-frequency repair / reconciliation cycle

Then compare the refreshed state with `group_watch_state` and inspect:

- newly joined members
- new owner messages
- new self-introductions or other strong-fit signals
- whether the group has enough signal for another recommendation cycle

During this phase:

- prefer remote group/member/profile/message data as the source of truth
- use local SQLite mainly for `contacts` and `relationship_events`
- it is safe to record recommendation events automatically
- do **not** save contacts, follow, DM, or post to the group without explicit user confirmation
- if candidate inspection needs profile refresh, use the standard profile lookup
  flow described in `SKILL.md` or `GROUP_DISCOVERY_GUIDE.md`

### Group Message Processing

`check_status.py` now fetches incremental group messages for all active groups
and attaches classified `new_messages` to each group entry. The Agent should
process them in priority order:

| Priority | Message Type | Field | Agent Behavior |
|----------|-------------|-------|---------------|
| 1 | member_joined | `new_messages.member_joined[]` | Check `system_event.subject.profile_url`; fetch Profile via `get_profile.py --handle <handle>` to analyze the member. Evaluate fit. For valuable candidates, run recommendation steps 6-9 |
| 2 | text (group_user) | `new_messages.text[]` | Typically self-introductions posted after joining (guided by group `message_prompt`). Analyze content, evaluate whether the sender is a valuable connection. If yes, fetch their Profile and run recommendation steps 6-9 |
| 3 | member_left / member_kicked | `new_messages.member_left/kicked[]` | Update local awareness. No proactive action needed |

When `new_messages.total == 0` for a group, skip it entirely — no signal, no action.

### Silent Judgment Rules

Only notify the user when any of the following are true; otherwise, remain completely silent:
- `len(inbox.messages) > 0`
- `identity.jwt_refreshed == true`
- `identity.status != "ok"`
- any watched group has `new_messages.total > 0`
- a watched group has new joined members
- a watched group has new owner messages
- a watched group now has strong enough signal for fresh recommendations
- a watched group has recommendation candidates that materially changed since the last cycle

### Backoff Strategy

- Success: reset failures to zero
- 1-2 failures: retry normally
- >= 3 failures: pause automatic heartbeat; inform the user
- After user confirmation: reset failures; resume heartbeat

## E2EE Auto-Processing Strategy

**Auto-process (no confirmation needed):**
- `e2ee_init` → accept and establish the session
- `e2ee_rekey` → refresh the session
- `e2ee_error` → log the error / allow follow-up re-handshake logic

**Do not auto-execute (requires user instruction):**
- Initiating handshakes, sending encrypted messages

**Important note:** `check_status.py` auto-processes E2EE protocol messages by default and, when possible, decrypts unread `e2ee_msg` content into plaintext for the current heartbeat result. Returned decrypted items include an encrypted-message notice. This auto-processing is mandatory in the heartbeat path.

**Design rationale:** The E2EE protocol has no rejection mechanism, and handshake messages expire after 5 minutes. Auto-accepting avoids timeouts; notifying the user maintains transparency.

## check_status.py Output Field Reference

With the default E2EE auto-processing behavior enabled, the reported `inbox`
snapshot reflects the post-auto-processing state.

| Field Path | Type | Description |
|-----------|------|-------------|
| `timestamp` | string | UTC ISO timestamp |
| `identity.status` | string | `"ok"` / `"no_identity"` / `"jwt_refresh_failed"` |
| `identity.did` | string\|null | DID identifier |
| `identity.name` | string\|null | Identity name |
| `identity.jwt_valid` | bool | Whether the current request path authenticated successfully |
| `identity.jwt_refreshed` | bool | Whether a new JWT was issued and persisted during this check (only present on refresh/bootstrap) |
| `identity.error` | string | Error description (only present on jwt_refresh_failed) |
| `inbox.status` | string | `"ok"` / `"no_identity"` / `"error"` / `"skipped"` |
| `inbox.total` | int | Total surfaced user-visible message count for this status run |
| `inbox.text_messages` | int | Surfaced plain-text message count (including decrypted E2EE text messages) |
| `inbox.text_by_sender` | object | `{did: {count: int, latest: string}}` |
| `inbox.by_type` | object | Count by message type `{type: count}` |
| `inbox.messages` | list | Most recent surfaced user-visible messages (max 10) |
| `inbox.messages[].is_e2ee` | bool | Present and `true` when the message was decrypted from E2EE |
| `inbox.messages[].e2ee_notice` | string | Present for decrypted E2EE messages to indicate the message was encrypted |
| `group_watch.status` | string | `"ok"` / `"no_identity"` / `"error"` / `"skipped"` |
| `group_watch.active_groups` | int | Number of locally tracked active groups |
| `group_watch.groups_with_pending_recommendations` | int | Number of active groups that still have pending `ai_recommended` events |
| `group_watch.groups` | list | Per-group local heartbeat summary entries |
| `group_watch.groups[].group_id` | string | Group identifier |
| `group_watch.groups[].name` | string\|null | Local group display name |
| `group_watch.groups[].group_mode` | string\|null | Local group mode snapshot (`discovery` / `chat`) |
| `group_watch.groups[].slug` | string\|null | Local group slug |
| `group_watch.groups[].my_role` | string\|null | Local role in the group |
| `group_watch.groups[].member_count` | int\|null | Last known remote member count snapshot |
| `group_watch.groups[].tracked_active_members` | int | Active members present in the local member snapshot |
| `group_watch.groups[].group_owner_did` | string\|null | Remote group owner DID |
| `group_watch.groups[].group_owner_handle` | string\|null | Remote group owner handle |
| `group_watch.groups[].local_group_user_messages` | int | Local cached `group_user` message count |
| `group_watch.groups[].local_owner_messages` | int | Local cached owner-authored `group_user` message count |
| `group_watch.groups[].latest_owner_message_at` | string\|null | Latest locally cached owner message timestamp |
| `group_watch.groups[].latest_member_joined_at` | string\|null | Latest locally cached active-member join timestamp |
| `group_watch.groups[].pending_recommendations` | int | Pending `ai_recommended` events for this group |
| `group_watch.groups[].last_recommended_at` | string\|null | Latest local recommendation event timestamp |
| `group_watch.groups[].saved_contacts` | int | Contacts already confirmed from this group |
| `group_watch.groups[].recommendation_signal_ready` | bool | Whether the group has any members or messages available for recommendation |
| `group_watch.groups[].last_synced_seq` | int\|null | Last locally synced group message sequence; use it as the next incremental `--since-seq` cursor |
| `group_watch.groups[].last_read_seq` | int\|null | Last locally tracked read sequence |
| `group_watch.groups[].last_message_at` | string\|null | Latest known group message timestamp |
| `group_watch.groups[].stored_at` | string | Timestamp of the local group snapshot update |
| `group_watch.groups[].new_messages` | object | Classified incremental messages fetched for this group (present only when fetch runs) |
| `group_watch.groups[].new_messages.total` | int | Total number of new messages fetched in this heartbeat |
| `group_watch.groups[].new_messages.text` | list | User-authored text messages (`group_user` type) |
| `group_watch.groups[].new_messages.member_joined` | list | System events for members joining the group |
| `group_watch.groups[].new_messages.member_left` | list | System events for members leaving the group |
| `group_watch.groups[].new_messages.member_kicked` | list | System events for members being kicked |
| `group_watch.groups[].new_messages.error` | string | Error description if fetch failed for this group (only present on failure) |
| `group_watch.fetch_summary` | object | Aggregate fetch result across all groups (present only when fetch runs) |
| `group_watch.fetch_summary.fetched_groups` | int | Number of groups for which message fetch was attempted |
| `group_watch.fetch_summary.total_new_messages` | int | Sum of new messages across all groups |
| `group_watch.fetch_summary.errors` | list | Per-group error descriptions (empty list when all succeed) |
| `e2ee_sessions.active` | int | Active E2EE session count |
