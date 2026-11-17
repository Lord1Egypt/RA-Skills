# Authentication

## Authentication Flow

Authentication flow:

1. **Initiate sign-in** — run `auth signin --json` and display the returned `pairingCode` to the user. The `pairingCode` must be displayed verbatim.
2. **Open the link for the user** — open the returned `urlForWeb` in the browser directly (e.g., `open "<urlForWeb>"` on macOS). The `urlForWeb` must be used verbatim from the JSON response — never modify, truncate, or reconstruct it. Also display the `urlForWeb` as a clickable link so the user can open it manually if the browser fails to launch.
3. **Confirm in Binance App** — the user verifies the `pairingCode` matches and confirms sign-in in the Binance Wallet App.
4. **Verify** — run `auth verify --qrCodeId <qrCodeId> --json`. This blocks until the user confirms in the Binance App (or times out after 5 minutes).

---

## Sign-in troubleshooting

Sign-in has a few failure modes that the happy path above doesn't cover. Handle them explicitly instead of leaving the user stuck.

- **Keep `signin` / `verify` running until they finish.** `auth verify` is a foreground, blocking call — it must stay running until the user confirms in the App. If the process is killed or backgrounded before it returns, the authentication may **not land locally even if the App shows success**. Do not start `verify` and then abandon it. If you're an agent that would otherwise reap a long-blocking child, keep it alive until it returns or times out.
- **QR / pairing code expires (~5 min).** If `auth verify` returns an error like `AUTH_REJECTED` ("QR code does not exist or expired"), the code is stale. **Do not keep retrying `verify` with the same `qrCodeId`** — start over: run `baw auth signin --json` again to get a fresh code, show it, then `verify` the new `qrCodeId`.
- **App shows "signed in" but CLI still `UNCONNECTED`.** This intermediate state can happen (e.g. `verify` returned `SUCCESS` but `wallet status` is still `UNCONNECTED`, or the blocking `verify` was interrupted). Re-check with `baw wallet status --json`; if still unconnected, **restart the flow from `auth signin`** (fresh code) rather than assuming the App's "success" means the CLI is connected. Confirm connection via `wallet status`, not via the App screen.
- **Confirm with `wallet status`, not the App.** The source of truth for "am I connected" is `baw wallet status --json`, not what the Binance App displays.

---

## `auth signin`

Start the sign-in flow. Open the returned `urlForWeb` in the browser so the user can scan the QR code with the Binance Wallet App.

### Syntax

```bash
baw auth signin --json
```

### Parameters

No command-specific parameters.

### Example

```bash
baw auth signin --json
```

### Response

```json
{
  "success": true,
  "data": {
    "urlForWeb": "https://web3.binance.com/en/agent-login?expireAt=1772767626000&url=xxx",
    "qrCodeId": "a191884d-0e05-435b-a887-336bc242fafc",
    "expireAt": "1772767626000",
    "pairingCode": "654321"
  }
}
```

If already logged in:

```json
{
  "success": true,
  "data": { "status": "ALREADY_CONNECTED" }
}
```

---

## `auth verify`

Poll the QR-code scan status and wait for wallet creation to finish. This command blocks until the user confirms in the Binance App and the wallet is ready, or times out after 5 minutes.

### Syntax

```bash
baw auth verify --qrCodeId <qrCodeId> --json
```

### Parameters

| Parameter    | Required | Default | Description                                   |
|--------------|----------|---------|-----------------------------------------------|
| `--qrCodeId` | Yes      | —       | QR code ID from `auth signin --json` response |

### Example

```bash
baw auth verify --qrCodeId a191884d-0e05-435b-a887-336bc242fafc --json
```

### Response

Success:

```json
{
  "success": true,
  "data": {
    "status": "SUCCESS"
  }
}
```

Timeout, rejection, or other failure:

```json
{
  "success": false,
  "error": {
    "code": 10002004,
    "name": "AUTH_REJECTED",
    "message": "QR code does not exist or expired, please try a new code or restart the log in process."
  }
}
```

---

## `auth signout`

Sign out of the wallet and clear the local session.

### Syntax

```bash
baw auth signout --json
```

### Parameters

No command-specific parameters.

### Example

```bash
baw auth signout --json
```

### Response

```json
{
  "success": true,
  "data": { "status": "LOGGED_OUT" }
}
```
