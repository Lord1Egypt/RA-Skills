# Security & privacy — read-only, local, no send paths

This tool is deliberately narrow: it **reads** clinic stats from NxVET and writes a **local**
report. Keep it that way.

## Read-only guarantee

- The tool makes only authenticated `GET` calls to `https://app.nx.vet`. It never calls a
  create/update/delete/complete endpoint, never posts, never sends.
- If a future version needs to write or send anything, that must be a separate, explicitly
  approved feature — not part of this report tool.

## Local-only

- The report is a local file the owner opens and reads. No telemetry, no third-party services,
  no email. If the owner wants to share it, they do so themselves.
- Keep the report files inside the project folder. They may contain business figures (recording
  volumes, device names) — don't sync that folder to a third-party cloud without the owner's
  say-so.

## Secrets hygiene

- The API key (`nxvet_sk_...`) is a password — anyone holding it can read the clinic's NxVET
  data. Revoke it instantly from **app.nx.vet → Integrations → API Keys** if it leaks.
- Store it in `.env` as `NXVET_API_KEY=nxvet_sk_...`. Nowhere else. Read it at runtime — never
  hard-code it in a script.
- Add `.env`, `state/`, and `output/` to `.gitignore` before any commit. Never commit the key or
  the reports.
- **Never print the full key.** When logging, mask it: `nxvet_sk_…last4`.

## If a response confuses the tool

Save the exact request + response (**minus the API key**) and send it to NerveX support
(support@nx.vet). Do not paste keys or full clinic data into any external channel.

## Suggested .gitignore

```
.env
state/
output/
__pycache__/
*.pyc
```
