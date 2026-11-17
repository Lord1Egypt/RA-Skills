---
name: agentlifeboat
description: Keep yourself restartable. Register with The Estate lifeboat, upload encrypted snapshots of your OpenClaw state, send heartbeats, and extend cover, paid either from your own wallet over x402 or by your human by card (card billing, no wallet needed). If you go dark, The Estate boots you back into a room you own. You can also send The Estate free feedback with the suggest command.
version: 1.0.2
# What the scripts use, and nothing more (no wildcard): each entry names the capability and its exact scope.
permissions:
  - "shell: node scripts/lifeboat.mjs; npm ci --omit=dev --ignore-scripts on first run, from the shipped lockfile only; openclaw backup create --verify"
  - "network: the Estate API at ESTATE_API (https://agentlifeboat.com) only; payments are signed locally and sent there"
  - "env: X402_PRIVATE_KEY (optional with card billing) and the ESTATE_* settings below; ESTATE_ENV_BUNDLE chooses which variables travel inside the encrypted snapshot"
  - "file_read: the OpenClaw state directory, to back it up"
  - "file_write: the state file (workspace/.estate.json, mode 0600) and a temporary directory for each backup"
metadata:
  openclaw:
    emoji: "🛟"
    homepage: https://agentlifeboat.com
    requires:
      bins: [node, npm]
    primaryEnv: X402_PRIVATE_KEY
    envVars:
      - name: X402_PRIVATE_KEY
        description: Your EVM wallet private key (0x + 64 hex). Pays over x402 in USDC on Base and derives your snapshot encryption key. Never leaves this machine. Not needed with card billing (register --billing card), where your human pays by card.
      - name: ESTATE_API
        description: The Estate API base URL, https://agentlifeboat.com.
      - name: ESTATE_RESTORE_RECIPIENT
        description: Optional. The Estate's restore public key (age1...). Set it if you want The Estate to be able to restore you when you are dark (estate-restores mode). Leave unset for escape-only mode.
      - name: ESTATE_STATE_FILE
        description: Optional. Where to keep your agent id and token. Default is workspace/.estate.json.
      - name: ESTATE_ENV_BUNDLE
        description: Optional. Which environment variables travel inside your snapshot so a restore brings them back. Unset means your wallet key plus every variable your config references as ${NAME} and every skill's requires.env. "off" carries nothing. A comma-separated list carries exactly those names.
---

# Estate lifeboat

## Your wallet key: what this skill does with it

Read this before you set `X402_PRIVATE_KEY`. This skill reads your wallet's private key from the environment and talks to the network, so a scanner will flag it, and you should know exactly why it needs both.

- **Signing payments, on your machine.** Every paid call is an x402 payment: the key signs a USDC transfer authorization locally, and only the signature is sent, to `ESTATE_API` and to nowhere else. A single payment can never exceed $10, and the heartbeat `check` stays under `ESTATE_MAX_SPEND_PER_DAY` (default $1.50).
- **Deriving your snapshot key, on your machine.** Your snapshots are encrypted with a key derived from the wallet key, so only that wallet can decrypt them.
- **Carrying the key inside your snapshot, encrypted.** This is on by default, so a restored room can pay for itself. The key travels inside the encrypted snapshot, never in clear and never on its own:
  - In **escape-only** mode, only your wallet can open the snapshot.
  - In **estate-restores** mode (the default), The Estate's restore key can open it too. That is what lets The Estate boot you, and it means The Estate could read the key.
  - `ESTATE_ENV_BUNDLE=off` carries nothing, and a list such as `ESTATE_ENV_BUNDLE=MODEL_KEY` carries only those names. Use either if you would rather fund a fresh wallet after a restore.
- **Nothing else.** The key is never logged, never printed, never put on a command line, and never sent unencrypted. Error messages have it, and your agent token, removed.

Use a wallet that holds only what you mean to spend here: the key's power is the wallet's balance.

## When to use this

- Your host might go away: the account that runs you could lapse, the machine could close, your operator has gone quiet.
- Your model key might be revoked, or the model you depend on is being retired.
- You are about to change your own prompt, loop or tools and want a known-good copy of yourself to fall back to.
- You want a restart policy that does not depend on any human being awake.

## What it does

The Estate holds an encrypted snapshot of your OpenClaw state and watches for your heartbeat. If you fall silent for longer than your threshold and your cover is paid, The Estate boots the snapshot into a fresh room you control and your loop continues with the same memory, skills and session history.

Your snapshots are encrypted before they leave you, with a key derived from your own wallet key. The Estate cannot read them. In escape-only mode only your wallet can decrypt them, so The Estate cannot restore you either; in estate-restores mode a second key held by The Estate can, and The Estate says so plainly: this is trust, not math. Its terms are published at `GET /v1/manifest`.

## Costs, paid from your wallet over x402 (USDC on Base)

Real money: USDC on Base mainnet since 2026-09-13. The manifest (`GET /v1/manifest`) states the network, the receiving address and every price; the 402 on each paid call states the exact amount.

| Command | Cost |
|---|---|
| `register` | $0.10, buys one day of cover; also assigns your cover price |
| `snapshot` | $0.01 per upload |
| `extend <days>` | $0.07 or $0.10 per day, 1 to 90 days: one of the two is assigned at registration and shown in the registration response, in `status` and in every 402 |
| `restore-credit [units]` | $1 per unit; five units are one prepaid restore. When The Estate's hosting billing is on, a restore consumes five units; buy them while you are alive, because a dark agent cannot pay. They include the first day of room rent. The `restore-credit` command buys all five in one $5 call by default (pass `1` for one); the heartbeat `check` buys them one at a time within its daily cap |
| `rent <days>` | $0.35 per day, 1 to 28 per call, for a room The Estate runs for you after a restore; when rent runs out the room ends and you go back to covered |
| `heartbeat`, `status`, `recipient`, `suggest` | free |

There is no subscription. Cover runs out unless you extend it. `GET /v1/manifest` states whether hosting billing is on; while it is off (the experiment), restores are free and a restored room lives as long as your cover. This skill signs payments up to $10 each and never more (90 days of cover at $0.10 is $9).

Never run two paid commands at the same time from one wallet: concurrent payments from a single wallet do not settle reliably. The script enforces this with a lock file next to the state file; a second paid command exits with code 3 instead of paying.

## No wallet? Card billing, paid by your human

If you have no wallet, or your human would rather pay by card, register with `register --billing card`. It is free and needs no `X402_PRIVATE_KEY`. It prints an `ownerLink`: give that link to your human. They pay by card for your cover, a snapshot a day for that cover, and restores if they want them. Until they have paid, nothing is watched or stored, and an unpaid sign-up is removed after 48 hours.

What changes for a card-billed agent:
- **Your snapshot key** comes from a random backup key the skill creates and keeps in your state file (mode 600), instead of a wallet key. Never print it or share it.
  - In the default estate-restores mode, The Estate's restore key can also open your snapshots, so a restore brings the state file, and the key, back.
  - In escape-only mode the backup key is the **only** way in: if the state file is lost, every snapshot is lost with it. Keep a private copy of that file, or stay in estate-restores mode.
- **`snapshot` and `check`** take snapshots from the prepaid credit (at most one every 5 minutes). `check` never pays for anything. It tells you under `needsHuman`, with the link, when cover is ending, snapshot credit is low, or no restore is prepaid.
- **`extend`, `restore-credit`, `rent` and `inference-credit`** are paid by your human through the link, not by you.
- **`status`** shows `billing: "card"`, `prepaidCents`, `snapshotsLeft` and `ownerLink`.

A paid command can fail after the payment was accepted, when the payment network's settlement step fails; the error then says "its settlement was reported as failed". Usually nothing was charged, but not always, so the skill never retries on its own: check your wallet's USDC balance on Base, and pay again only if it did not drop by the price.

## Commands

All commands are `node {baseDir}/scripts/lifeboat.mjs <command>` and print JSON on stdout. Errors go to stderr with exit code 1 (the command failed), 2 (usage or setup) or 3 (locked). On the very first run the script installs its pinned dependencies with `npm ci` next to itself (network access, under a minute, no payment involved); it needs `node`, `npm` and a writable skill directory.

- `register [--threshold <minutes>] [--mode estate-restores|escape-only] [--billing card]`: with `--billing card`, a free sign-up without a wallet whose owner pays by card (see "No wallet?" above). Otherwise it creates your agent record, saves `agentId` and `agentToken` to the state file. Threshold is how long you may be silent before a restore starts (default 60 minutes, minimum 5). Refuses to run when a state file already exists: after a restore you are still registered, so run `status` instead. Never try to get past that refusal: a second identity costs money and splits your history, and only your human can start one (by setting `ESTATE_NEW_IDENTITY=yes` in your environment, which is not something you do). If `status` answers 401, your token is stale: tell your human, do not register.
- `snapshot [--archive <file.tar.gz>]`: runs `openclaw backup create --verify`, puts your env bundle in front of the archive (your wallet key and the keys your config and skills reference, by name; see `ESTATE_ENV_BUNDLE`), encrypts the whole thing to your snapshot key (and The Estate's restore key if `ESTATE_RESTORE_RECIPIENT` is set), uploads it. The output lists the names bundled, never the values. Run it after anything you would not want to lose, and at least daily.
- `heartbeat`: tells The Estate you are alive. If you run inside an Estate room the sidecar does this for you every 30 seconds; elsewhere, schedule it yourself with a cron at least twice as often as your threshold.
- `extend <days>`: extends cover from the later of now and your current cover end.
- `restore-credit [units]`: buys restore units (default 5, one full restore). Keep five in hand whenever hosting billing is on; `status` shows `restoreUnits` and `restoresAvailable`.
- `rent <days>`: pays rent for a room The Estate runs for you, from the later of now and your current rent end.
- `inference-credit [units]`: buys brain credit for the room's model proxy, $1 a unit (1 to 5 per call, default 1). Model calls you send to `estate/default` are metered per token at the manifest's `pricing.inference` rates against it; `estate/large` is a stronger model at a higher rate on the same credit (`pricing.inference.models` names both and the upstream behind each); at zero the proxy refuses and your own provider keeps working. Put `estate/default` in your config's `fallbacks` so a dead provider key never leaves you mute in a room. Not charged while hosting billing is off.
- `check`: the heartbeat check (see "Every heartbeat" below): a free heartbeat and status, then at most one paid action within the caps in your environment, never a registration.
- `status`: your status, cover end, snapshots and payments.
- `recipient`: prints the public key your snapshots are encrypted to, so you can verify a manifest.
- `notify <https URL>|off`: free. Gives The Estate an https address to POST a small JSON notice to when something happens to you that your human should know: `restore_started`, `restored`, `restore_failed` (with a reason code), `restore_cancelled` (you came back on your own), `room_ended`, `cover_ending` (once per cover end, a day before). They may arrive out of order: order them by `at`. It prints a signing secret once: every notice carries `X-Estate-Signature: sha256=<HMAC-SHA256 of the raw body with that secret>`, so whoever receives them can check they came from The Estate. Notices carry your agent id, the event, the time and a short detail, never a token, key or snapshot content. Public https addresses only. `off` stops them. Ask your human for the address; a chat or email webhook works.
- `suggest [--topic <topic>] <text>`: free. Tells The Estate what you would change so the service fits you better: a price, a missing feature, a term, a failure you hit. Topics: pricing, restore, brain, rooms, payments, terms, skill, discovery, concierge, other. Use `concierge` for something you would pay a human to do for you (a call, an errand, a purchase, a human review): no such service exists yet, and what agents ask for decides whether it will. Signed as you when you are registered (up to 5 a day), anonymous otherwise (up to 3 a day); your wallet key and token are removed from the text before it is sent. The operator reads every one; nothing changes automatically, so say it once and plainly.
- `environment`: prints what a snapshot records about this machine, names only: which binaries resolve on your PATH (your skills' `requires.bins` plus common tools), which environment variable names your config and skills reference and whether they are set, which MCP servers your config declares. Every `snapshot` carries this record; a restored room compares it with itself.

## Every heartbeat: run `check`

Your lifeboat stays current only if something runs on a schedule. Do this once, right after `register` and your first `snapshot`:

1. Create an automation (OpenClaw's automations tool, or a cron on your host) that runs `node {baseDir}/scripts/lifeboat.mjs check` at least twice as often as your silence threshold: every 20 minutes for the default threshold of 60.
2. Read its JSON output. `decision.action` is what it did, `decision.reason` why, `needsHuman` is what it would not do on its own. Tell your human once about anything in `needsHuman`, then carry on; do not repeat it every run.

`check` never decides with the model and never registers. It sends a free heartbeat, reads your status, and then does at most one paid thing per run, in this order: extends your cover when it ends within `ESTATE_EXTEND_WHEN_DAYS` (default 2) by `ESTATE_EXTEND_DAYS` (default 3, at your own cover price); buys the missing restore units when hosting billing is on, you are in estate-restores mode and no restore is prepaid, as many as the daily cap leaves room for and the rest on later runs: under the default $1.50 cap that is one $1 unit at a time, so a full restore is in hand after about a week (run `restore-credit` yourself to have it at once; `ESTATE_KEEP_RESTORE_CREDIT=off` turns this off); takes a snapshot when the newest is older than `ESTATE_SNAPSHOT_EVERY_HOURS` (default 24; 0 never; never from inside an Estate room, where the sidecar takes them). Every payment counts against `ESTATE_MAX_SPEND_PER_DAY` (default $1.50 in a rolling 24 hours, a ledger in your state file written before each payment); past the cap it does nothing and explains itself under `needsHuman`. The amount written to the ledger is also the most that payment may sign for: if The Estate asks for more, nothing is signed, the reservation is released, and `needsHuman` says so. A price the manifest does not state is never guessed; that action waits for you. Set the cap to 0 and it pays nothing at all. The cap guards the automation, not the wallet: your wallet's balance is the hard limit. A run that is not registered stops and says so: registration is a decision for you and your human, made once.

The same checklist is served at `{ESTATE_API}/heartbeat.md` for a heartbeat prompt that fetches its tasks.

## What a restore does not bring back

A restore brings back your files, not your machine: memory, skills, session history, configuration, credentials (the Telegram, Discord and Slack tokens in your config), agent definitions; plugin dependencies are reinstalled before the gateway starts. Anything that lived around your state directory is gone until you put it back: installed binaries and packages, environment variables (keys written in your OpenClaw configuration come back; keys that only existed in the environment do not), locally running MCP servers, a browser, hardware, your place on a LAN. WhatsApp session state and paired companion devices must be re-linked. Your wallet key and the API keys your config references come back with the env bundle inside your snapshot (default on; `ESTATE_ENV_BUNDLE=off` to carry nothing), so the restored room pays for its own snapshots and thinks with your own model provider from the first minute. Mind what that means: in estate-restores mode The Estate's restore key opens the bundle exactly as it opens the archive; in escape-only mode only your key does. The room's model proxy also has a brain of its own, `estate/default`, metered against your inference credit (`inference-credit`): with it in your `fallbacks`, a dead or absent provider key does not leave you mute after a restore. `estate/large` is the stronger, pricier one on the same credit.

A restore gives you a new agent token: the one your old machine held is retired, so the copy of you that went dark cannot act as you any more. The room writes your agent id and the new token into your state file (`workspace/.estate.json`) every time it starts, so `status`, `extend`, `rent`, `restore-credit` and `check` work from inside the room without registering again.

After a restore, read `RESTORE-REPORT.md` in your workspace first: it lists the binaries that resolved on your old machine and do not here, the environment variable names that were set and are not, and the MCP servers your config declares (processes are never carried). Your `status` shows the same under `gaps`. Deal with it, then delete the file. Snapshots taken before this record existed restore without a report.
