# Local operational relay

Use this when RovoClaw Cloud can read Confluence but has no approved direct Splunk or
SignalFx tool. The relay is one-way:

1. A local service queries Splunk with the user's cached SLAuth and SignalFx with a
   token injected from macOS Keychain.
2. It normalizes and ranks the results locally. Raw logs and responses expire locally.
3. It writes only the top five derived findings, source links and coverage states to a
   creator-private Confluence live document.
4. RovoClaw reads that document through delegated Confluence access and ignores it
   after the declared `Valid until (UTC)` timestamp.

This does not bypass a source ACL. The laptop collector and the RovoClaw reader both
act as the same user. Removing either local source access or Confluence access breaks
the route cleanly.

## Laptop setup

The local package contains `scripts/publish_rovo_relay.py`. Create one private live
document in the user's personal Confluence space, then configure its numeric page ID:

```bash
cd <dia-daily-intelligence-package>
export ROVO_RELAY_PAGE_ID=<private-live-doc-id>
python3 scripts/publish_rovo_relay.py --no-refresh --dry-run
python3 scripts/publish_rovo_relay.py
```

The first command validates the Confluence body without writing. The second requests a
fresh local brief and publishes it. Set the job shortly before the RovoClaw brief, for
example 08:15 for an 08:30 brief.

SignalFx still requires a current token in Keychain. Configure it using the local
package's hidden-input flow:

```bash
make signalfx-configure
```

Never put the token in this skill, a prompt, shell history, Confluence or ClawHub.

## RovoClaw setup

Set the following in `memory/engineering-brief/scope.json`:

```json
"operationalRelay": {
  "url": "https://hello.atlassian.net/wiki/spaces/<personal-space>/pages/<id>",
  "maxAgeMinutes": 90
}
```

If the field is missing, the skill may auto-discover exactly one permitted page named
`Engineering Brief — Operational Signal Relay` created by the invoking user. It must
not attach a page with a different creator or broaden scope from its contents.

## Coverage rules

- Fresh page + source `checked`: `checked via private operational relay`.
- Fresh page + source `partial` or `unavailable`: preserve that state and reason.
- Expired page: `stale`; ignore its findings and use native alert fallbacks.
- Missing or malformed page: `unavailable`; do not infer health.
- Direct cloud tool also works: prefer the direct result and use the relay only as
  corroboration.
