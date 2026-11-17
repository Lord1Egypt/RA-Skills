# Session, Accounts, and Scope

Everything else in this skill depends on one object. The session response is the only authority on where to send calls, which accounts the token can see, what each account supports, and how big a request may be.

**Before discovering anything**, read `## Account Map`, `## Mailbox Map` and `## Identities` in `~/Clawic/data/fastmail-api/memory.md` — or the files `## Boxes` points to. Discover only what is missing or contradicted. **After any discovery**, write the account rows, the observed limits, and every mailbox and identity id you resolved back in the same turn (`memory-template.md`). Re-resolving ids every session is the single largest waste in JMAP work, and the second-largest source of writes to the wrong account.

**Contents:** [The Session Call](#the-session-call) · [Reading the Accounts Map](#reading-the-accounts-map) · [Capabilities Are Per Account](#capabilities-are-per-account) · [Tokens and Scopes](#tokens-and-scopes) · [Mailbox Roles](#mailbox-roles) · [When to Rediscover](#when-to-rediscover)

## The Session Call

```bash
curl -sS "${FASTMAIL_API_BASE:-https://api.fastmail.com/jmap/session}" \
  -H "Authorization: Bearer $FASTMAIL_API_TOKEN" | jq
```

What comes back, and what each field is for:

| Field | Use |
|---|---|
| `apiUrl` | Every method call POSTs here. Take it from the response; a hardcoded value survives right up until it does not |
| `downloadUrl` | URI template with `{accountId}`, `{blobId}`, `{type}`, `{name}` — attachment and raw-message export (`migration.md`) |
| `uploadUrl` | URI template with `{accountId}` — blob upload before attaching (`sending.md`) |
| `eventSourceUrl` | URI template with `{types}`, `{closeafter}`, `{ping}` — change notifications (`sync.md`) |
| `accounts` | Map of accountId → `{name, isPersonal, isReadOnly, accountCapabilities}` |
| `primaryAccounts` | Map of capability URN → the accountId to use by default for that capability |
| `capabilities` | What the *token* can do, with the core limits attached |
| `state` | Opaque string that changes when the session itself changes; a cheap way to know a rediscovery is due |
| `username` | The account the token belongs to — useful in a summary, never a substitute for `accountId` |

Precedence for which account a call scopes to: `default_account_id` from `config.yaml` → the `primaryAccounts` entry for that capability → nothing, which means ask. When more than one account exists and no preference is set, name the one you chose out loud before acting.

## Reading the Accounts Map

The map contains every account the token can reach, which on a Fastmail account with sharing or delegation is more than one. Three fields decide behaviour:

- **`isPersonal: false`** — a shared or delegated account. Writes here are visible to other people immediately; there is no draft state that hides them.
- **`isReadOnly: true`** — every write returns `accountReadOnly`. This is not a token problem and no retry fixes it; the grant itself is read-only. Check it *before* building the payload, and record it in `## Account Map`.
- **`accountCapabilities`** — the per-account capability objects, with the mail limits inside. An account can be missing a capability the token has.

Typical failure this prevents: the token's `primaryAccounts` for mail is the personal account, the user says "archive the support queue", and the support queue is a second, shared account. Nothing errors. The archive happens in the wrong mailbox.

## Capabilities Are Per Account

Two independent lists, and confusing them produces the most-misdiagnosed error in JMAP:

| List | Answers | Failure when wrong |
|---|---|---|
| `capabilities` (top level) | What this **token** was granted | Naming a missing URN in `using` → request-level `unknownCapability` |
| `accounts[id].accountCapabilities` | What this **account** supports | Calling a method for a capability the account lacks → `accountNotSupportedByMethod` |

Standard URNs in play: `urn:ietf:params:jmap:core` (always), `urn:ietf:params:jmap:mail`, `urn:ietf:params:jmap:submission` (sending), plus contacts and calendars capabilities whose exact URN depends on which revision the server implements — read them from the session rather than typing them from memory (`contacts.md`, `calendar.md`). Fastmail's masked email lives under a vendor URN, `https://www.fastmail.com/dev/maskedemail` (`masked-email.md`).

Rule: **`using` contains exactly the capabilities the request needs, and every one of them appears in `capabilities`.** Including a URN you do not use costs nothing but noise; including one you were not granted fails the entire envelope, including the calls that would have worked.

## Tokens and Scopes

- The JMAP API expects a **bearer API token**, created in Fastmail's settings with per-capability scopes. App passwords are a different credential aimed at IMAP, SMTP and CalDAV clients — reaching for one when a JMAP call fails is a detour, not a fix.
- **Scope is chosen at creation and cannot be widened later** by changing the request. A token issued read-only for mail will fail every `/set` with a permissions error no matter how the payload is shaped; the answer is a new token, and the old one should then be revoked rather than left alive.
- Grant the narrowest scope the work needs. A triage automation does not need calendars; a calendar sync does not need submission. The blast radius of a leaked token is exactly its scope.
- The token value never appears in a file, a log line, a summary, or an echoed header. In anything written down it becomes `env:FASTMAIL_API_TOKEN` (`memory-template.md`).
- If the token is suspected exposed — pasted into a chat, committed, printed in output — say so in one line and treat revocation as the first step, before any further calls.

## Mailbox Roles

Roles are how a mailbox is identified across accounts, languages, and renames. `Mailbox/get` returns `role` alongside `name`, `parentId`, `sortOrder`, `totalEmails`, `unreadEmails`, `myRights`.

| Role | What it is | Note |
|---|---|---|
| `inbox` | Delivery target | The only role guaranteed to exist |
| `archive` | Long-term keep | Absent on accounts that never enabled it — check before assuming a destination |
| `drafts` | Where `$draft` messages live | `sending.md` removes membership here on successful send |
| `sent` | Where sent copies land | Added by `onSuccessUpdateEmail`, not automatically |
| `junk` | Spam | The move is what the server acts on; the `$junk` keyword alone is metadata |
| `trash` | Soft delete | Server retention is finite — "recoverable" has an expiry date |

`myRights` on each mailbox (`mayAddItems`, `mayRemoveItems`, `maySetSeen`, `mayDelete`, `mayCreateChild`…) is per-mailbox permission inside a shared account. A batch that passes the account-level check can still fail per mailbox; read `myRights` on the destination before a bulk move into a shared account.

Store every resolved id with the role you resolved it by (`## Mailbox Map`). A stored id whose row has no role can only be re-verified by name, which is the fragile path Rule 2 exists to avoid.

## When to Rediscover

| Trigger | What to redo |
|---|---|
| No `## Account Map` in memory, or it lacks the capability in question | Full session call, write everything back |
| `accountNotFound`, `unknownCapability`, or `accountNotSupportedByMethod` | Full session call — the stored picture is stale or the token changed |
| A mailbox id returns `notFound` in a `/set` | `Mailbox/get` for that account; a deleted-and-recreated mailbox has a new id under the same name |
| The user mentions a new alias, domain, or shared account | Identities and accounts only |
| Session `state` differs from the one you stored | Full session call |
| Everything resolves and nothing errored | Nothing — a session call per operation is waste, and it is not a health check |
