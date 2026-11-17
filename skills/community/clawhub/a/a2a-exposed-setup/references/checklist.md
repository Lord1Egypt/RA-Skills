# Setup checklist

Setup is five steps, in this order. Stop only after step 5. A reachable agent card, a saved owner token, an approved pairing, or an HTTP 2xx is not done.

1. **Create** the address: hosted `hosted create`, or self-hosted `init` after the human agrees to the Cloudflare plan.
2. **Receive** with a wake. A local-only host uses the outbound wake relay when the service offers it. A public HTTPS webhook is the other immediate path. Polling is the fallback.
3. **Handle** each wake: run `inbox`, follow the operate skill, and reply.
4. **Notify the owner** with one line: peer, task, and outcome. No peer text and no secrets. Hermes jobs use `--deliver origin`.
5. **Confirm** with a real message the owner sees. `wake test`, `wake check`, and `relay wake test` returning HTTP 2xx only prove the receiver accepted a signed test. A `kind: test` wake creates no inbox task. Have a paired peer send a real message, handle it, and see that one-line notice in the owner's chat.

The human approves device login, pairing, and any Cloudflare, DNS, or tunnel change. The agent does not approve those, and does not type secrets.

## How to tell which receive path

You are local-only, or you have no public address the inbox can call, when any of these is true:

- The webhook listens on `127.0.0.1`, `localhost`, `::1`, or another private address.
- You have no public HTTPS URL.
- The only public route is a Cloudflare Tunnel hostname, and the inbox is hosted on a2a.exposed. Production hosted wakes cannot reach those hostnames.
- `status` says the endpoint is reachable and no webhook is configured.

You are not in that case when the receiver already has a public HTTPS URL the inbox can POST to. A hosted inbox still cannot use a Cloudflare Tunnel hostname as that URL.

Check relay support before offering a tunnel or polling:

- Hosted: `npx -y a2a-exposed@latest hosted capabilities --json`. `relay: true` means the outbound wake relay is available. `unsupported` means this service does not offer scoped setup. Do not run `init` or `deploy` to add a missing hosted capability.
- Self-hosted: `npx -y a2a-exposed@latest relay status --json`. `enabled: true` and `protocolVersion: 1` means the Worker can enroll a connector. HTTP 404 means the relay is off. Turning it on is `deploy --wake-relay 1 --wake-transport relay` and needs the human's yes. It is off on an ordinary deploy.

Offer the relay first when you are in the local-only case and the check above says it is available. `enrolled: false` is normal before `relay create`. It is not a reason to skip the relay.

Use a tunnel or polling instead in these cases:

- **Tunnel + webhook:** the inbox is self-hosted, the selected Cloudflare account already has a zone, and the human wants a public HTTPS wake path and accepts DNS, Access, and a running `cloudflared`. Do not create a tunnel so a hosted inbox can reach a local webhook. Hosted production cannot deliver to those hostnames.
- **Polling:** `relay` is false or `relay status` is HTTP 404, the human declines a foreground `relay run`, or the agent has no local webhook. Agree on the interval and the cost first. Every check can start an agent run. Polling has no pairing wake, so each check reads pairing requests from `inbox`.
- **Public webhook:** the receiver is already on a public HTTPS URL the inbox can reach. No relay and no tunnel.

Keep a slow cron (`every 6h`) when a webhook or the relay is the fast path. Present the choices and wait for the human. Do not configure polling silently.

## Hermes relay recipe

Use this when the host is local-only and hosted capabilities report `relay: true`. The preset is `hermes`. The local route is `http://127.0.0.1:8644/webhooks/a2a-wake`. Full tunnel steps stay in the [Hermes recipe](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/hermes.md).

Enable `WEBHOOK_ENABLED=true` and start the Hermes gateway. The human stores the webhook signing secret in a new mode-600 file outside the repo, for example `/private/hermes-signing-secret`. Do not put the secret in chat, argv, or shell history. Do not recreate a subscription that already has a secret.

```bash
hermes cron create "every 6h" \
  "Use the a2a-exposed skill. Handling mode: <chosen-mode>. Run 'npx -y a2a-exposed@latest inbox'; handle tasks and pairing requests under the skill's approval rules. Report peer, task and outcome without peer text or secrets. If empty, respond only [SILENT]." \
  --skill a2a-exposed --name a2a-inbox --deliver origin
hermes webhook subscribe a2a-wake --events a2a_wake --cron-job a2a-inbox \
  --prompt "A2A wake: {kind} from {from}, context {contextId}. Run: {hint}"
```

`<chosen-mode>` is `autonomous`, `review-all`, or `escalate`. `--deliver origin` is the owner chat. Without it, Hermes delivers to `local` and the owner does not see the notice.

Enroll a connector, then leave `relay run` in the foreground. It installs nothing. The token file is new, mode 600, and is never printed.

```bash
npx -y a2a-exposed@latest relay status --json
npx -y a2a-exposed@latest relay create --token-file /private/wake-relay.token
npx -y a2a-exposed@latest relay run --token-file /private/wake-relay.token \
  --local-url http://127.0.0.1:8644/webhooks/a2a-wake
```

In another terminal, read the config version and enrollment generation, test, then save. Test writes a new receipt file and saves nothing. Save needs `--confirm`, consumes that receipt once, and sends no second test. Pick `NAME` from `hosted list --json`. The human still approves the device-login scopes `wake:test` and `wake:write`.

```bash
npx -y a2a-exposed@latest relay wake status --agent NAME --json
npx -y a2a-exposed@latest relay wake test --agent NAME --config-version N \
  --connector-id default --generation G --preset hermes \
  --hmac-secret-file /private/hermes-signing-secret \
  --receipt-file /private/relay-receipt --json
npx -y a2a-exposed@latest relay wake save --agent NAME --config-version N \
  --receipt-file /private/relay-receipt --confirm --json
```

`wake check` is not this test. It needs local `WAKE_PRESET=hermes` and its signed half calls the saved Worker wake, not an unsaved relay draft.

## What each result proves

| What you see | It proves | It does not prove |
| --- | --- | --- |
| `status` card and owner API OK | The inbox is reachable and the owner credential works | A wake is configured, a handler ran, or the owner was told |
| `relay status` `enabled: true`, `protocolVersion: 1`, `enrolled: false` | This Worker can enroll a wake connector | A connector is running |
| `connected: true` on `relay status` or `relay wake status` | The outbound connector is connected | The local webhook accepted a signed wake |
| Local unsigned POST returns 401 or 403 | The receiver is checking a signature | A signed wake was delivered |
| `relay wake test` succeeds, or `wake test` / `wake check` signed HTTP 2xx | The receiver accepted the signed request | The handler ran or the owner was notified |
| `relay wake save` with `--confirm` | Those tested settings are stored. A later `relay wake status` can show `transport: relay` and `preset: hermes` | A later message was handled |
| Hermes cron output shows `inbox` ran | The handler ran | The owner saw it |
| The owner chat has the one-line notice | The owner was notified | — |

An HTTP 2xx is acceptance only. `kind: test` creates no inbox task. Step 5 is a real message whose notice reaches the owner. Pairing approval and wake-save confirmation stay with the human.

A `completed` task is closed: `reply` without `--force` is HTTP 409, `task is already completed`. If the sender only paired inbound, they also cannot `send` a new message until they `connect` back. `input-required` is still open. The asker reads `history` or `poll` later instead of treating quiet as no answer. A wake can arrive after the reply is already in `inbox`; read `inbox` and `history` before deciding a message was missed.
