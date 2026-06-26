# Local Store Schema Reference

SQLite local storage schema for offline message persistence, group-state caching,
and contact management.

Database path: `<DATA_DIR>/database/awiki.db` (WAL mode, `check_same_thread=False`).
Single shared database for all credentials and local DIDs.

## Tables

### contacts

Stores contact information scoped by the local owner DID.

| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| owner_did | TEXT | PRIMARY KEY (with `did`) | Local DID that owns this contact record |
| did | TEXT | PRIMARY KEY (with `owner_did`) | Contact's DID |
| name | TEXT | | Display name |
| handle | TEXT | | Short name (handle) |
| nick_name | TEXT | | Nickname |
| bio | TEXT | | Short biography |
| profile_md | TEXT | | Markdown profile content |
| tags | TEXT | | Comma-separated tags |
| relationship | TEXT | | Relationship type (following, follower, etc.) |
| source_type | TEXT | | Discovery source type (`event`, `meetup`, `hiring`, `online_group`, etc.) |
| source_name | TEXT | | Human-readable source / occasion name |
| source_group_id | TEXT | | Group ID that led to the connection |
| connected_at | TEXT | | First confirmed connection time |
| recommended_reason | TEXT | | Latest saved recommendation reason |
| followed | INTEGER | NOT NULL, DEFAULT `0` | Whether the owner already followed this contact |
| messaged | INTEGER | NOT NULL, DEFAULT `0` | Whether the owner already started a DM |
| note | TEXT | | Local note for follow-up |
| first_seen_at | TEXT | | ISO 8601 timestamp of first encounter |
| last_seen_at | TEXT | | ISO 8601 timestamp of last encounter |
| metadata | TEXT | | JSON metadata |

#### Indexes

- `idx_contacts_owner`: `(owner_did, last_seen_at DESC)` — owner-scoped recent contacts
- `idx_contacts_owner_source_group`: `(owner_did, source_group_id)` — owner-scoped source-group lookup

### messages

Stores all messages (incoming and outgoing). The `owner_did` column isolates data
per local DID identity, and the composite primary key `(msg_id, owner_did)`
allows the same server message to be stored for multiple local identities.

| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| msg_id | TEXT | PRIMARY KEY (with `owner_did`) | Message identifier scoped by local DID owner |
| owner_did | TEXT | NOT NULL | Local DID that owns this message |
| thread_id | TEXT | NOT NULL | Thread identifier (see Thread ID Format) |
| direction | INTEGER | NOT NULL, DEFAULT 0 | 0 = incoming, 1 = outgoing |
| sender_did | TEXT | | Sender's DID |
| receiver_did | TEXT | | Receiver's DID |
| group_id | TEXT | | Group ID (for group messages) |
| group_did | TEXT | | Group DID (for group messages) |
| content_type | TEXT | DEFAULT 'text' | Content MIME type |
| content | TEXT | | Message content |
| title | TEXT | | Message title (optional, plaintext even for E2EE) |
| server_seq | INTEGER | | Server-assigned sequence number |
| sent_at | TEXT | | Server-side send timestamp (ISO 8601) |
| stored_at | TEXT | NOT NULL | Local storage timestamp (ISO 8601) |
| is_e2ee | INTEGER | DEFAULT 0 | 1 if message was E2EE encrypted |
| is_read | INTEGER | DEFAULT 0 | 1 if message has been read |
| sender_name | TEXT | | Display name of sender |
| metadata | TEXT | | JSON metadata; group system messages may store structured `system_event` here |
| credential_name | TEXT | NOT NULL, DEFAULT '' | Credential alias used when the message was stored |

#### Indexes

- `idx_messages_owner_thread`: `(owner_did, thread_id, sent_at)` — owner-scoped thread query
- `idx_messages_owner_thread_seq`: `(owner_did, thread_id, server_seq)` — owner-scoped incremental thread query
- `idx_messages_owner_direction`: `(owner_did, direction)` — owner-scoped inbox/outbox filtering
- `idx_messages_owner_sender`: `(owner_did, sender_did)` — owner-scoped sender lookup
- `idx_messages_credential`: `(credential_name)` — credential-based filtering

### e2ee_sessions

Stores the disk-first private E2EE session truth for one local DID owner. There
is at most one active row per `(owner_did, peer_did)`, while
`(owner_did, session_id)` remains unique for exact decrypt lookups.

| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| owner_did | TEXT | PRIMARY KEY (with `peer_did`) | Local DID that owns this session |
| peer_did | TEXT | PRIMARY KEY (with `owner_did`) | Remote peer DID |
| session_id | TEXT | NOT NULL, UNIQUE (with `owner_did`) | Active HPKE session identifier |
| is_initiator | INTEGER | NOT NULL, DEFAULT `0` | Whether the owner initiated the current session |
| send_chain_key | TEXT | NOT NULL | Base64-encoded send chain key |
| recv_chain_key | TEXT | NOT NULL | Base64-encoded receive chain key |
| send_seq | INTEGER | NOT NULL, DEFAULT `0` | Next outbound sequence number |
| recv_seq | INTEGER | NOT NULL, DEFAULT `0` | Next expected inbound sequence number |
| expires_at | REAL | | Unix timestamp when the session expires |
| created_at | TEXT | NOT NULL | Session creation time |
| active_at | TEXT | | Session activation time |
| peer_confirmed | INTEGER | NOT NULL, DEFAULT `0` | Whether an `e2ee_ack` confirmed this session |
| credential_name | TEXT | NOT NULL, DEFAULT `''` | Credential alias used for diagnostics |
| updated_at | TEXT | NOT NULL | Last local mutation time |

#### Indexes

- `idx_e2ee_sessions_owner_updated`: `(owner_did, updated_at DESC)` — recent-session scans for one owner
- `idx_e2ee_sessions_credential`: `(credential_name)` — credential-based diagnostics

### groups

Stores the local snapshot of discovery/chat groups for one local DID owner.

| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| owner_did | TEXT | PRIMARY KEY (with `group_id`) | Local DID that owns this group snapshot |
| group_id | TEXT | PRIMARY KEY (with `owner_did`) | Group identifier |
| group_did | TEXT | | Group DID if known locally |
| name | TEXT | | Group display name |
| group_mode | TEXT | NOT NULL, DEFAULT `discovery` | Remote group mode (`discovery` / `chat`) |
| slug | TEXT | | Group slug |
| description | TEXT | | Group description |
| goal | TEXT | | Group goal |
| rules | TEXT | | Group rules |
| message_prompt | TEXT | | Group message prompt |
| doc_url | TEXT | | Public markdown URL |
| group_owner_did | TEXT | | DID of the remote group owner |
| group_owner_handle | TEXT | | Handle of the remote group owner |
| my_role | TEXT | | Local member role (`owner` / `member`) |
| membership_status | TEXT | NOT NULL, DEFAULT `active` | Local membership status (`active` / `left` / `kicked`) |
| join_enabled | INTEGER | | Whether joining is currently enabled |
| join_code | TEXT | | Current 6-digit join code if known locally |
| join_code_expires_at | TEXT | | Join code expiry time |
| member_count | INTEGER | | Active member count snapshot |
| last_synced_seq | INTEGER | | Last group message sequence synced locally |
| last_read_seq | INTEGER | | Last read sequence tracked locally |
| last_message_at | TEXT | | Last known group message timestamp |
| remote_created_at | TEXT | | Group create time from the server |
| remote_updated_at | TEXT | | Group update time from the server |
| stored_at | TEXT | NOT NULL | Local snapshot update time |
| metadata | TEXT | | JSON metadata |
| credential_name | TEXT | NOT NULL, DEFAULT `''` | Credential alias used for the snapshot |

#### Indexes

- `idx_groups_owner_status_last_message`: `(owner_did, membership_status, last_message_at DESC)` — active-group list queries
- `idx_groups_owner_slug`: `(owner_did, slug)` — owner-scoped slug lookup
- `idx_groups_owner_updated`: `(owner_did, remote_updated_at DESC)` — owner-scoped recent group updates

### group_members

Stores the latest cached active-member snapshot for one group.

| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| owner_did | TEXT | PRIMARY KEY (with `group_id`, `user_id`) | Local DID that owns this member snapshot |
| group_id | TEXT | PRIMARY KEY (with `owner_did`, `user_id`) | Group identifier |
| user_id | TEXT | PRIMARY KEY (with `owner_did`, `group_id`) | Remote user identifier |
| member_did | TEXT | | Remote member DID |
| member_handle | TEXT | | Remote member handle |
| profile_url | TEXT | | Public profile URL for the remote member |
| role | TEXT | | Cached member role |
| status | TEXT | NOT NULL, DEFAULT `active` | Cached member status |
| joined_at | TEXT | | Remote join time |
| sent_message_count | INTEGER | NOT NULL, DEFAULT `0` | Cached quota counter |
| last_synced_at | TEXT | NOT NULL | Local snapshot time |
| metadata | TEXT | | JSON metadata |
| credential_name | TEXT | NOT NULL, DEFAULT `''` | Credential alias used for the snapshot |

#### Indexes

- `idx_group_members_owner_group_role`: `(owner_did, group_id, role)` — role-filtered member queries
- `idx_group_members_owner_group_status`: `(owner_did, group_id, status)` — status-filtered member queries

### relationship_events

Stores append-only local relationship sedimentation events such as AI recommendations,
confirmed saves, follow actions, DM starts, and note updates.

| Column | Type | Constraint | Description |
|--------|------|------------|-------------|
| event_id | TEXT | PRIMARY KEY | Local event identifier |
| owner_did | TEXT | NOT NULL | Local DID that owns this relationship history |
| target_did | TEXT | NOT NULL | Contact DID |
| target_handle | TEXT | | Contact handle if known |
| event_type | TEXT | NOT NULL | `ai_recommended`, `saved_to_contacts`, `followed`, `messaged`, `note_updated`, etc. |
| source_type | TEXT | | Discovery source type |
| source_name | TEXT | | Discovery source / occasion name |
| source_group_id | TEXT | | Source group ID |
| reason | TEXT | | Recommendation or action reason |
| score | REAL | | Optional recommendation score |
| status | TEXT | NOT NULL, DEFAULT `pending` | `pending`, `accepted`, `applied`, etc. |
| created_at | TEXT | NOT NULL | Event create time |
| updated_at | TEXT | NOT NULL | Event update time |
| metadata | TEXT | | JSON metadata |
| credential_name | TEXT | NOT NULL, DEFAULT `''` | Credential alias used for the event |

#### Indexes

- `idx_relationship_events_owner_target_time`: `(owner_did, target_did, created_at DESC)` — per-contact history lookup
- `idx_relationship_events_owner_status_time`: `(owner_did, status, created_at DESC)` — pending / accepted recommendation scans
- `idx_relationship_events_owner_group`: `(owner_did, source_group_id)` — per-group relationship review

## Views

### threads

Aggregated thread summary.

| Column | Type | Description |
|--------|------|-------------|
| owner_did | TEXT | Local DID owner |
| thread_id | TEXT | Thread identifier |
| message_count | INTEGER | Total messages in thread |
| unread_count | INTEGER | Unread incoming messages |
| last_message_at | TEXT | Most recent message timestamp |
| last_content | TEXT | Content of most recent message |

### inbox

All incoming messages (`direction = 0`), with `owner_did` preserved.

### outbox

All outgoing messages (`direction = 1`), with `owner_did` preserved.

## Thread ID Format

Thread IDs are deterministic and symmetric:

- **Private chat**: `dm:{min_did}:{max_did}` — DIDs sorted alphabetically for symmetry
- **Group chat**: `group:{group_id}`

## Schema Versioning

Schema version tracked via `PRAGMA user_version`. Current version: **11**.

Migration history:
- v1 → v2: adds `credential_name TEXT` column and `idx_messages_credential` index
- v2 → v3: rebuilds `messages` so deduplication happens per `(msg_id, credential_name)`
- v3 → v4: adds `e2ee_outbox` table for encrypted send tracking
- v4 → v5: adds `title TEXT` column to `messages` table
- v5 → v6: adds explicit `owner_did` isolation to `contacts`, `messages`, and
  `e2ee_outbox`, and rebuilds views to group by owner DID
- v6 → v7: adds local `groups` and `group_members` snapshots, plus group-aware
  message indexes for incremental sync
- v7 → v8: extends `contacts` with source / follow-up fields and adds
  append-only `relationship_events`
- v8 → v9: adds `profile_url` to local `group_members` snapshots
- v9 → v10: adds `group_mode` to local `groups` snapshots
- v10 → v11: adds disk-first `e2ee_sessions` and keeps legacy JSON E2EE state
  only as a one-time migration source

## Querying with `query_db.py`

Use this section for **local cache inspection / offline debugging**.

For active group recommendation work, prefer remote fetches through
`manage_group.py` and `get_profile.py`, and treat local SQLite as secondary
state.

If you explicitly want to inspect local group caches, remember that `--join`
alone does not guarantee a fresh `group_members` snapshot or complete group
message history.

```bash
uv run python scripts/query_db.py "SELECT * FROM groups WHERE owner_did='did:me' ORDER BY last_message_at DESC LIMIT 10"
uv run python scripts/query_db.py "SELECT * FROM group_members WHERE owner_did='did:me' AND group_id='grp_xxx' ORDER BY role, member_handle"
uv run python scripts/query_db.py "SELECT msg_id, direction, content_type, content, server_seq FROM messages WHERE owner_did='did:me' AND group_id='grp_xxx' AND content_type='group_user' ORDER BY server_seq"
uv run python scripts/query_db.py "SELECT * FROM relationship_events WHERE owner_did='did:me' AND status='pending' ORDER BY created_at DESC LIMIT 20"
```

Useful starter queries:

- List my active groups:
  ```sql
  SELECT owner_did, group_id, name, my_role, membership_status, member_count, last_message_at
  FROM groups
  WHERE owner_did = 'did:me' AND membership_status = 'active'
  ORDER BY last_message_at DESC;
  ```
- Inspect one group's latest member snapshot:
  ```sql
  SELECT user_id, member_did, member_handle, profile_url, role, status, sent_message_count
  FROM group_members
  WHERE owner_did = 'did:me' AND group_id = 'grp_xxx'
  ORDER BY role, member_handle;
  ```
- Inspect one group's local message history:
  ```sql
  SELECT msg_id, direction, sender_did, content_type, content, metadata, server_seq, sent_at
  FROM messages
  WHERE owner_did = 'did:me' AND group_id = 'grp_xxx' AND content_type = 'group_user'
  ORDER BY COALESCE(server_seq, 0), COALESCE(sent_at, stored_at);
  ```
- Inspect one group's messages together with group name and best-effort sender handle:
  ```sql
  SELECT g.name AS group_name,
         COALESCE(c.handle, m.sender_name, m.sender_did) AS sender,
         m.content,
         m.sent_at
  FROM messages m
  LEFT JOIN groups g
    ON g.owner_did = m.owner_did AND g.group_id = m.group_id
  LEFT JOIN contacts c
    ON c.owner_did = m.owner_did AND c.did = m.sender_did
  WHERE m.owner_did = 'did:me'
    AND m.group_id = 'grp_xxx'
    AND m.content_type = 'group_user'
  ORDER BY COALESCE(m.server_seq, 0), COALESCE(m.sent_at, m.stored_at);
  ```
- Inspect one group's system events:
  ```sql
  SELECT msg_id, content_type, content, metadata, server_seq, sent_at
  FROM messages
  WHERE owner_did = 'did:me'
    AND group_id = 'grp_xxx'
    AND content_type IN ('group_system_member_joined', 'group_system_member_left', 'group_system_member_kicked')
  ORDER BY COALESCE(server_seq, 0), COALESCE(sent_at, stored_at);
  ```
- Inspect saved contacts from one group:
  ```sql
  SELECT did, handle, source_type, source_name, source_group_id, recommended_reason,
         followed, messaged, note
  FROM contacts
  WHERE owner_did = 'did:me' AND source_group_id = 'grp_xxx'
  ORDER BY connected_at DESC;
  ```
- Inspect pending AI recommendations:
  ```sql
  SELECT target_did, target_handle, source_group_id, reason, score, created_at
  FROM relationship_events
  WHERE owner_did = 'did:me' AND event_type = 'ai_recommended' AND status = 'pending'
  ORDER BY created_at DESC;
  ```

Common pitfall: `messages` does **not** expose `group_name`, `sender_handle`, or
`type` columns. Use `groups.name`, `contacts.handle`, and `messages.content_type`.

## Safety Rules (execute_sql)

The `execute_sql()` function enforces:

- **Allowed**: SELECT, INSERT, UPDATE, DELETE (with WHERE), REPLACE, ALTER, CREATE
- **Forbidden**: DROP, TRUNCATE, DELETE without WHERE, multiple statements (`;` separated)
