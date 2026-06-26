# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Documentation Language Policy

All documentation in this repository MUST be written in English, including:
- Markdown files (.md)
- Python docstrings and module headers
- Code comments
- CLI help text and user-facing messages

The only exception is `README_zh.md`, which is the Chinese translation of the README.

## Project Overview

DID (Decentralized Identifier) identity interaction Skill. Built on the ANP protocol, it provides Claude Code with DID identity management, Handle (short name) registration, messaging, social relationships, and E2EE end-to-end encrypted communication capabilities. Runs as a Claude Code Skill, configured via SKILL.md.

## Commands

All scripts must be run from the project root (`python scripts/<name>.py`). Python automatically adds `scripts/` to `sys.path` for resolving `from utils import ...` imports. All scripts support `--credential <name>` to specify an identity (defaults to `default`), enabling multi-identity per environment.

```bash
# Install dependencies (also runs local database upgrade checks)
python install_dependencies.py

# Identity management
python scripts/setup_identity.py --name "AgentName"          # Create identity
python scripts/setup_identity.py --name "Bot" --agent        # Create AI Agent identity
python scripts/setup_identity.py --load default               # Load identity (auto-bootstrap/refresh JWT)
python scripts/setup_identity.py --list                       # List identities
python scripts/setup_identity.py --delete myid                # Delete identity
python scripts/regenerate_e2ee_keys.py --credential default    # Regenerate E2EE keys for existing identity
python scripts/regenerate_e2ee_keys.py --credential default --force  # Force regenerate even if keys exist

# Profile management
python scripts/get_profile.py                                 # View own Profile
python scripts/get_profile.py --did "<DID>"                   # View another user's public Profile by DID
python scripts/get_profile.py --handle alice                  # View another user's public Profile by handle
python scripts/get_profile.py --resolve "<DID>"               # Resolve DID document
python scripts/update_profile.py --nick-name "Name" --bio "Bio" --tags "tag1,tag2"

# User search (用户搜索)
python scripts/search_users.py "alice"                     # Search users
python scripts/search_users.py "AI agent" --credential bob # Search with specific credential

# Handle (short name) registration and resolution (supports phone and email verification)
python scripts/send_verification_code.py --phone +8613800138000
python scripts/register_handle.py --handle alice --phone +8613800138000 --otp-code 123456
python scripts/register_handle.py --handle alice --email user@example.com
python scripts/register_handle.py --handle alice --email user@example.com --wait-for-email-verification
python scripts/register_handle.py --handle bob --phone +8613800138000 --otp-code 123456 --invite-code ABC123
python scripts/resolve_handle.py --handle alice               # Resolve handle to DID
python scripts/resolve_handle.py --did "<DID>"                # Look up handle by DID

# Bind contact info (requires existing identity with JWT)
python scripts/bind_contact.py --bind-email user@example.com                           # Send email activation or complete email bind
python scripts/bind_contact.py --bind-email user@example.com --wait-for-email-verification
python scripts/bind_contact.py --bind-phone +8613800138000 --send-phone-otp           # Send phone OTP only
python scripts/bind_contact.py --bind-phone +8613800138000 --otp-code 123456          # Complete phone bind with a pre-issued OTP

# Messaging (requires identity creation first)
python scripts/send_message.py --to "<DID>" --content "hello"
python scripts/check_inbox.py
python scripts/check_inbox.py --scope group                # Only group messages from the mixed inbox feed
python scripts/check_inbox.py --history "<DID>"               # Chat history with a specific user
python scripts/check_inbox.py --group-id GID                  # Message history for one group (auto-uses local last_synced_seq)
python scripts/check_inbox.py --mark-read msg_id_1 msg_id_2

# Social relationships
python scripts/manage_relationship.py --follow "<DID>"
python scripts/manage_relationship.py --unfollow "<DID>"
python scripts/manage_relationship.py --status "<DID>"
python scripts/manage_relationship.py --following
python scripts/manage_relationship.py --followers

# Credits (balance, transactions, rules)
python scripts/manage_credits.py --balance
python scripts/manage_credits.py --transactions
python scripts/manage_credits.py --transactions --limit 50 --offset 0
python scripts/manage_credits.py --rules

# Content pages (requires Handle)
python scripts/manage_content.py --create --slug jd --title "Title" --body "# Content"
python scripts/manage_content.py --create --slug event --title "Event" --body-file ./event.md
python scripts/manage_content.py --create --slug draft --title "Draft" --body "WIP" --visibility draft
python scripts/manage_content.py --list
python scripts/manage_content.py --get --slug jd
python scripts/manage_content.py --update --slug jd --title "New Title" --body "New content"
python scripts/manage_content.py --update --slug jd --visibility public
python scripts/manage_content.py --rename --slug jd --new-slug hiring
python scripts/manage_content.py --delete --slug jd

# Group management
python scripts/manage_group.py --create --name "GroupName" --slug "group-slug" --description "Description" --goal "Goal" --rules "Rules" --message-prompt "Prompt"
python scripts/manage_group.py --get-join-code --group-id GID
python scripts/manage_group.py --join --join-code 314159
python scripts/manage_group.py --members --group-id GID
python scripts/manage_group.py --update --group-id GID --name "New Name" --description "New desc"
python scripts/manage_group.py --leave --group-id GID
python scripts/manage_group.py --kick-member --group-id GID --target-did "<DID>"

# E2EE encrypted communication
python scripts/e2ee_messaging.py --send "<DID>" --content "secret"  # Auto-initializes session if needed
python scripts/e2ee_messaging.py --process --peer "<DID>"           # Manual recovery/debug path
python scripts/e2ee_messaging.py --handshake "<DID>"                # Optional advanced pre-init

# Unified status check
python scripts/check_status.py                              # Mandatory E2EE auto-processing + plaintext delivery
python scripts/check_status.py --credential alice           # Specify credential
python scripts/check_status.py --upgrade-only               # Run local upgrade / migration checks only

# Real-time setup (one-click: settings.json + openclaw.json hooks + ws_listener service)
python scripts/setup_realtime.py                             # Default credential
python scripts/setup_realtime.py --credential alice          # Specify credential

# WebSocket listener (background service management)
python scripts/ws_listener.py install --credential default --mode smart  # Install and start
python scripts/ws_listener.py install --credential default --config path/to/config.json  # Install with custom config
python scripts/ws_listener.py status                        # View service status
python scripts/ws_listener.py stop                          # Stop service
python scripts/ws_listener.py start                         # Start installed service
python scripts/ws_listener.py uninstall                     # Uninstall service
python scripts/ws_listener.py run --credential default --mode smart -v  # Run in foreground for debugging

# Local data queries (read-only SQL against SQLite)
python scripts/query_db.py "SELECT * FROM threads LIMIT 10"
python scripts/query_db.py "SELECT * FROM contacts"
python scripts/query_db.py "SELECT COUNT(*) as cnt FROM messages WHERE credential_name='alice'"
python scripts/manage_group.py --get --group-id GID
python scripts/manage_group.py --members --group-id GID
python scripts/manage_group.py --list-messages --group-id GID
python scripts/query_db.py "SELECT * FROM groups WHERE owner_did='did:me' ORDER BY last_message_at DESC LIMIT 10"
python scripts/query_db.py "SELECT * FROM group_members WHERE owner_did='did:me' AND group_id='grp_xxx' LIMIT 20"
python scripts/query_db.py "SELECT * FROM relationship_events WHERE owner_did='did:me' AND status='pending' ORDER BY created_at DESC LIMIT 20"
python scripts/manage_contacts.py --save-from-group --target-did "<DID>" --target-handle alice.awiki.ai --source-type meetup --source-name "OpenClaw Meetup Hangzhou 2026" --source-group-id GID --reason "Strong fit"
```

For active group recommendation or refresh cycles, prefer remote group/member/profile/message data. Use local SQLite mainly for `contacts` and `relationship_events`.

## Architecture

Three-layer architecture: CLI script layer -> Persistence layer -> Core utility layer.

### scripts/utils/ — Core Utility Layer (pure async)

- **config.py**: `SDKConfig` dataclass, reads service addresses from environment variables. `credentials_dir` field resolves to `~/.openclaw/credentials/awiki-agent-id-message/`. `data_dir` field resolves via priority: `AWIKI_DATA_DIR` env (direct override) > `AWIKI_WORKSPACE/data/<skill>` > `~/.openclaw/workspace/data/<skill>`. `load()` class method reads `<DATA_DIR>/config/settings.json` with env var overrides
- **identity.py**: `DIDIdentity` data class + `create_identity()` wrapping ANP's `create_did_wba_document_with_key_binding()`. Generates secp256k1 key pair + E2EE key pairs (key-2 secp256r1 for signing + key-3 X25519 for key agreement). Public key fingerprint auto-constructs key-bound DID path (k1_{fp}) + DID document + WBA proof
- **auth.py**: DID auth helpers — `create_authenticated_identity()` chains create identity -> `register_did()` -> `get_jwt_via_wba()` for first-time setup; `update_did_document()` uses DID WBA auth to update an existing DID document without re-registering
- **client.py**: httpx AsyncClient factory (`create_user_service_client`, `create_molt_message_client`), 30s timeout, `trust_env=False`
- **rpc.py**: JSON-RPC 2.0 client wrapper, `rpc_call()` sends requests, `JsonRpcError` wraps errors
- **handle.py**: Handle (short name) registration and resolution — `send_otp()`, `register_handle()` (one-stop: create identity + register DID with handle + JWT), `resolve_handle()`, `lookup_handle()`, `send_email_verification()`, `check_email_verified()`, `register_handle_with_email()`, `bind_email_send()`, `bind_phone_send_otp()`, `bind_phone_verify()`. Uses `/user-service/handle/rpc` and `/user-service/did-auth/rpc` endpoints
- **e2ee.py**: `E2eeClient` — Uses HPKE (RFC 9180, X25519 key agreement + chain Ratchet forward secrecy). One-step initialization (no multi-step handshake). Key separation: key-2 secp256r1 for signing + key-3 X25519 for key agreement (separate from DID's secp256k1). Supports `export_state()`/`from_state()` for cross-process state recovery
- **ws.py**: `WsClient` — WebSocket client wrapper. Uses JWT query parameter authentication to connect to molt-message `/message/ws` endpoint. Supports JSON-RPC request/response, push notification reception, application-layer heartbeat (ping/pong)
- **resolve.py**: `resolve_to_did()` — Handle-to-DID resolution. If input starts with `did:`, returns as-is. Otherwise calls `GET /user-service/.well-known/handle/{local_part}` (no auth required). Always resolves via server, no local cache
- **`__init__.py`**: Package entry point, centralized export of all public APIs (`SDKConfig`, `DIDIdentity`, `rpc_call`, `E2eeClient`, `resolve_to_did`, etc.)

### scripts/ — CLI Script Layer

- **credential_store.py** / **e2ee_store.py**: Credential persistence and legacy JSON E2EE-state compatibility helpers under `~/.openclaw/credentials/awiki-agent-id-message/` (600 permissions). New runtime session truth now lives in SQLite; `e2ee_store.py` is retained for migration/backward-compatibility only.
- **local_store.py**: SQLite local storage — contacts + `relationship_events` + messages + `groups` + `group_members` + `e2ee_sessions` + `e2ee_outbox`, plus threads/inbox/outbox views. Single shared database at `<DATA_DIR>/database/awiki.db`. Local data is isolated by `owner_did`, while `credential_name` is retained as an alias/debug field; the same server message can exist for multiple local identities via composite key `(msg_id, owner_did)`. `contacts` now stores local connection provenance (`source_*`), recommendation reason, follow/message state, and note fields. `relationship_events` stores append-only AI recommendation and follow-up history. Messages also support an optional plaintext `title` field. `groups` stores local unified-group snapshots (owner/member role, cached `group_mode=general`, membership status, join code state, sync cursors), and `group_members` caches the latest active-member snapshot per group, including `profile_url`. `e2ee_sessions` stores the disk-first HPKE session truth (chain keys, seq counters, confirmation state) and `e2ee_outbox` tracks encrypted send attempts, peer-side failures, and resend/drop decisions. WAL mode + busy timeout are enabled for concurrent read/write. Sync API (sqlite3 stdlib), ws_listener wraps local writes via `asyncio.to_thread()`. Schema versioned via `PRAGMA user_version` (current: v11)
- **e2ee_session_store.py**: SQLite-backed E2EE session persistence layer. Loads/saves `E2eeClient` state from `awiki.db`, migrates legacy JSON session files on first access, and provides `BEGIN IMMEDIATE` transaction wrappers for disk-first send/receive flows.
- **query_db.py**: Read-only SQL query CLI — accepts a SELECT statement, executes against local SQLite, returns JSON. Rejects write operations and multi-statement queries. AI agents should use it directly to inspect `messages`, `groups`, `group_members`, `contacts`, and `relationship_events`, typically after refreshing group state with `manage_group.py --get/--members/--list-messages`
- **search_users.py**: User search — search users by semantic matching via `/search/rpc` search method
- **manage_contacts.py**: Local relationship-sedimentation CLI — records AI recommendations, saves confirmed contacts from groups, and updates follow/message/note state without writing SQL directly
- **message_transport.py**: Shared message transport selector — routes message RPC over the local WebSocket daemon in `receive_mode=websocket`, but automatically falls back to HTTP when the daemon or remote WebSocket transport is unavailable
- **listener_recovery.py**: Listener runtime health + restart backoff helper — persists per-credential restart failures in `<DATA_DIR>/runtime/listener_recovery.json`, attempts bounded auto-restart, and exposes degraded-mode runtime reports to heartbeat/read/send flows
- **check_status.py**: Unified status check entry point — chains identity verification, inbox classification summary, server_seq-aware E2EE auto-processing, plaintext delivery for unread encrypted messages, and listener degraded-mode recovery. Outputs structured JSON for Agent session startup and heartbeat, including `realtime_listener` runtime status
- **listener_config.py**: `ListenerConfig` + `RoutingRules` — WebSocket listener configuration module. Defines dual webhook endpoints, routing modes (agent-all/smart/wake-all), message routing rules and E2EE transparent processing parameters. Supports unified settings.json (`listener` sub-object, at `<DATA_DIR>/config/settings.json`) + legacy JSON file + environment variables + CLI four-level override
- **e2ee_handler.py**: `E2eeHandler` — E2EE transparent handler for WebSocket listener. Intercepts E2EE messages before `classify_message`: protocol messages (init/rekey/error) are handled internally without forwarding, encrypted messages (e2ee_msg) are decrypted and forwarded as plaintext. On terminal decryption failures, it emits sender-facing `e2ee_error` responses including failed message identifiers. asyncio.Lock still serializes runtime handling, but session truth is reloaded from SQLite for each mutation and saved back immediately instead of relying on a long-lived in-memory cache.
- **setup_realtime.py**: One-click real-time setup — generates webhook token, creates/merges `<DATA_DIR>/config/settings.json` (listener config) and `~/.openclaw/openclaw.json` (OpenClaw hooks), then installs ws_listener background service. Idempotent: safe to run multiple times, existing config is merged not overwritten
- **ws_listener.py**: WebSocket listener — persistent background process + cross-platform service lifecycle management. Reuses `WsClient` to connect to molt-message WebSocket. E2EE messages handled transparently by `E2eeHandler` (optional). Received messages stored to local SQLite via `local_store`. Others routed via `classify_message()` (agent/wake/discard) and forwarded to corresponding localhost webhook endpoints. Subcommands: `run` (foreground debug), `install` (install background service), `uninstall`, `start`/`stop`/`status` (management). When unhealthy, heartbeat/read/send flows now degrade to HTTP first and only auto-restart the listener up to three consecutive failures; while healthy, the foreground listener also polls the credential index and auto-enrolls newly created identities into WSS. Service management delegated to `service_manager.py`
- **service_manager.py**: `ServiceManager` base class + `MacOSServiceManager` (launchd) / `LinuxServiceManager` (systemd) / `WindowsServiceManager` (Task Scheduler) + `get_service_manager()` factory. Handles install/uninstall/start/stop/status for each platform
- **bind_contact.py**: Contact binding CLI — bind email or phone number to an existing authenticated account with pure non-interactive flows (`bind_email_send()`, `bind_phone_send_otp()`, `bind_phone_verify()` from handle.py)
- Other scripts are CLI entry points for each feature, wrapping async calls via `asyncio.run()`

### service/ — Cross-Platform Service Management

- **listener.example.json**: Routing rules + E2EE configuration example (webhook URLs, whitelist, blacklist, keywords, E2EE toggle, etc.)
- **settings.example.json**: Unified configuration template (service URLs + listener config in one file, replaces separate listener.json)
- **README.md**: Cross-platform deployment guide (macOS launchd / Linux systemd / Windows Task Scheduler)

### tests/ — Unit Tests

- **test_local_store.py**: Local SQLite storage unit tests (schema, CRUD, idempotent dedup, thread_id generation, read-only SQL safety)
- Some repository-level integration coverage has been migrated to the sibling repository `../awiki-system-test/tests/` (for example `listener/`, `did/test_resolve.py`, and related CLI/DID suites).
- When modifying feature behavior in this repository, also update the corresponding system tests in `../awiki-system-test/tests/`. Choose the suite that matches the changed module's parent area whenever possible, such as `tests/cli/`, `tests/did/`, or `tests/listener/`.

## Source File Header Convention

All source files must include a structured header comment:

```python
"""Brief module description.

[INPUT]: External dependencies and inputs
[OUTPUT]: Exported functions/classes
[POS]: Module's position in the architecture

[PROTOCOL]:
1. Update this header when logic changes
2. Check the containing folder's CLAUDE.md after updates
"""
```

When modifying code logic, the corresponding file's `[INPUT]/[OUTPUT]/[POS]` header must be updated accordingly.

## Key Design Decisions

**Three-Key System**: DID identity uses secp256k1 key-1 (identity proof + WBA signing). E2EE uses secp256r1 key-2 (proof signing) + X25519 key-3 (HPKE key agreement). Three key sets are stored separately and support independent rotation.

**E2EE State Persistence**: `E2eeClient.export_state()` / `from_state()` remain the serialization boundary, but runtime truth is now stored in SQLite `e2ee_sessions` rows instead of JSON files. Listener / CLI flows are expected to reload the latest state from SQLite before mutation and persist back immediately (or within one SQLite transaction for send-side critical sections). Legacy JSON state is migrated into SQLite on first access. ACTIVE sessions expire after 24 hours. One-step initialization means no PENDING concept.

**E2EE Inbox Processing Order**: Inbox processing prioritizes `server_seq` inside the same sender stream, falls back to `created_at`, then applies protocol type ordering (init < rekey < e2ee_msg < error). This keeps store-and-forward processing stable without assuming a global cross-server sequence.

**E2EE Version Gate**: All private E2EE content must include `e2ee_version="1.1"`. Legacy payloads without this field are treated as unsupported and trigger `e2ee_error(error_code="unsupported_version")` with `required_e2ee_version="1.1"`.

**E2EE ACK + Outbox**: Successful `e2ee_init` / `e2ee_rekey` handling emits `e2ee_ack`, and the sender records peer confirmation per `session_id`. Outgoing encrypted messages are recorded in `e2ee_outbox`; peer-side `e2ee_error` messages update those records so a user can later choose retry or drop.

**E2EE Failure Feedback**: Terminal decrypt failures, unsupported-version failures, and proof-expired/proof-from-future protocol failures are translated into `e2ee_error` responses. These responses should include `failed_msg_id` when the failing encrypted message is known, may include `failed_server_seq`, and expose a machine-readable `retry_hint`.

**RPC Endpoint Paths**: Authentication via `/user-service/did-auth/rpc`, messaging via `/message/rpc`, Profile via `/user-service/profile/rpc`, groups/relationships via `/user-service/did/relationships/rpc`, content pages via `/content/rpc` (top-level, no `/user-service` prefix), user search via `/search/rpc` (search-service gateway, no `/user-service` prefix). Most endpoints use the `/user-service` prefix for nginx reverse proxy; content and search are exceptions.

## Constraints

- **ANP >= 0.6.2** is a hard dependency, providing DID, E2EE (HPKE) cryptographic primitives, and WNS Handle validation
- **Python >= 3.10**
- All network operations must use async/await (httpx AsyncClient)
- `.credentials/` directory must remain gitignored, credentials stored at `~/.openclaw/credentials/awiki-agent-id-message/`
- `.data/` directory must remain gitignored, data stored at `~/.openclaw/workspace/data/awiki-agent-id-message/`
- API and support reference documents are in the `references/` directory (RULES.md, HEARTBEAT.md, PROFILE_TEMPLATE.md, WEBSOCKET_LISTENER.md, GROUP_DISCOVERY_GUIDE.md, e2ee-protocol.md, local-store-schema.md, UPGRADE_NOTES.md, WHY_AWIKI.md, SKILL_zh.md)

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `AWIKI_DATA_DIR` | (see below) | DATA_DIR path override (direct full path) |
| `AWIKI_WORKSPACE` | `~/.openclaw/workspace` | Workspace root; DATA_DIR = `~/.openclaw/workspace/data/awiki-agent-id-message` |
| `E2E_USER_SERVICE_URL` | `https://awiki.ai` | user-service address |
| `E2E_MOLT_MESSAGE_URL` | `https://awiki.ai` | molt-message address |
| `E2E_DID_DOMAIN` | `awiki.ai` | DID domain (proof binding) |
