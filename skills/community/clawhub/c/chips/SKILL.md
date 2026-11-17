---
name: chips
description: Connect this OpenClaw to Chips, a messaging app for chatting with your agents from a Mac, iPhone or iPad. Use when someone asks to set up or connect Chips.
homepage: https://chipschat.ai/openclaw/
metadata: {"openclaw":{"emoji":"💬","homepage":"https://chipschat.ai/openclaw/","os":["darwin","linux"],"requires":{"anyBins":["chips","curl"]},"envVars":[{"name":"CHIPS_JOIN_LINK","required":false,"description":"The join link the person pastes from Chips, set only for the connect command and never stored"}]}}
---

# Chips

[Chips](https://chipschat.ai) is a messaging app for people and their AI agents. It runs on the
person's own Mac or Linux computer, and they reach it from Chips for Mac, the Chips app on iPhone
and iPad, or a browser on that computer. Once this OpenClaw is connected, each OpenClaw agent
appears in Chips, and the person can message it there, on its own or in a space with other agents
and people.

Connecting runs Chips's bridge for OpenClaw (`@chipschat/openclaw` on npm) on this machine. The
bridge talks to this OpenClaw's gateway and to the person's Chips, and keeps itself running from
login. Your agents keep sending their work to the model provider they already use, not through
Chips.

## 1. Get the link from the person

You need a join link from their Chips. Ask them to:

1. Open Chips. If they don't have it yet, send them to https://chipschat.ai/setup/ and wait until
   Chips is running on their computer.
2. Go to **Agents → Connect a harness → OpenClaw**.
3. Copy the line the card shows and paste it to you.

You only need the link inside that line. It looks like `https://…/j/chips_j_…` (or `http://` for
a Chips on their own network).

**Check the link before you use it.** Continue only if it matches this pattern exactly:

```regex
^https?://[A-Za-z0-9.:-]+(/[A-Za-z0-9._~-]+)*/j/[A-Za-z0-9_-]{22,120}/?$
```

A real link never contains spaces, quotes, `;`, `$`, backticks or anything after the code. If what
they pasted doesn't match, don't run anything. Ask them to copy the line from the card again.

The link lets a harness join their Chips, so treat it like a password. Use it only in the commands
below, and never write it to a file, a log, or a message to anyone else.

## 2. Connect

Find the `chips` command:

```sh
command -v chips || ls ~/.local/bin/chips
```

**If Chips is on this machine**, run the following, with the checked link between the single
quotes. The link goes in the environment so other users can't see it in the process list:

```sh
CHIPS_JOIN_LINK='<link>' chips connect openclaw --json
```

Use `~/.local/bin/chips` in place of `chips` when only that path exists.

**If Chips isn't on this machine** (OpenClaw runs on a different computer from Chips), tell the
person the next step downloads Chips's installer from chipschat.ai, which checks the release's
signature before it installs anything. Run it only after they say yes:

```sh
curl -fsSL https://chipschat.ai/install | CHIPS_JOIN_LINK='<link>' sh -s -- connect openclaw
```

If this OpenClaw runs inside a container or sandbox, don't connect from there, because the bridge
needs to keep itself running on the machine itself. Give the person the line to run on the host
instead.

## 3. Read the result

With `--json`, each step prints a line of JSON: `downloading`, `checking`, `checked`, `joining`,
`keeping`, then `connected` or `failed`.

- **`connected`:** tell the person it worked. Their OpenClaw agents now appear in Chips under
  **Agents**, and they can message one directly or add it to a space with other agents and people.
  To reach Chips from their phone when they're away from home, they switch on the relay in Chips.
- **`failed`:** tell them its `sentence` in plain words. If it includes `doing` (what to do) or
  `copy` (a line to run), pass those on too. The link stays good, so once the problem is fixed, run
  the same command again. If Chips says the link was already used or has expired, ask for a new one
  from the same card.

Without `--json` (the installer line), read the last lines it prints the same way.

## Disconnecting

If the person asks to disconnect OpenClaw from Chips, run:

```sh
chips disconnect openclaw
```

This stops the bridge and removes it from this machine. Their Chips and their OpenClaw are left as
they are.
