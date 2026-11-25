---
name: controlclaw-firewall
description: Install the open-source ControlClaw firewall for this OpenClaw, or connect this OpenClaw to a ControlClaw firewall the person already runs. Every request and MCP call then goes through the firewall, which checks it against rules written in plain English, keeps passwords and API keys off the agent, and holds risky actions for approval. One firewall can serve many OpenClaw agents, so passwords, integrations and model keys are set up once. Use when the person asks for a firewall, wants to see or limit what OpenClaw sends to the internet, mentions ControlClaw, or gives you a ControlClaw pairing code (like 4F7K-92QD-XM3P).
homepage: https://github.com/madarco/controlclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "homepage": "https://github.com/madarco/controlclaw",
        "os": ["linux"],
        "requires": { "bins": ["node", "npx"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "controlclaw",
              "bins": ["controlclaw"],
              "label": "Install the ControlClaw CLI (npm)",
            },
          ],
      },
  }
---

# ControlClaw firewall for OpenClaw

[ControlClaw](https://github.com/madarco/controlclaw) is an open-source (AGPL-3.0) firewall for
OpenClaw. It runs as a Docker container. Once OpenClaw is connected to it, OpenClaw's traffic goes
through the firewall, and the person decides in the firewall's panel what gets out: sites to allow or
block, rules written as sentences ("Ask me before pushing anything to GitHub"), approvals for risky
actions, and passwords and API keys that stay on the firewall while the agent only holds a
placeholder.

One firewall can serve many OpenClaw agents, on this machine or on others. The passwords, app
integrations, MCP servers and model keys are set up once in its panel and shared by every agent
connected to it.

The `controlclaw` command line tool does the work. You run it, but the person decides: **ask before
you change anything**. A firewall limits what you can do from then on. That is the point. Set it up
only when the person asks, and never undo it or get around it later.

## 1. Where you run

The tool needs Linux (amd64 or arm64), Node 22 or newer, and for the firewall's container Docker 28
or newer with Compose 2.24.4 or newer. Check:

```bash
uname -sm; node --version; docker --version 2>/dev/null; docker compose version 2>/dev/null; test -f /.dockerenv && echo "in a container"
```

- **Not Linux** (macOS, Windows): stop. Tell the person the firewall runs on a Linux machine, and
  that this OpenClaw can't be connected from here yet.
- **In a container** (`/.dockerenv` exists, or the person says OpenClaw runs in Docker): you can't do
  it from inside. The tool, Docker and root are on the machine outside your container. Give the
  person the command for that machine, and stop:

  ```bash
  npx controlclaw up --here     # the firewall next to this OpenClaw, docker mode (user in the docker group, or sudo)
  ```

  Docker mode is the strongest: OpenClaw's container gets no way out except the firewall.

## 2. Ask which setup

Ask the person, in one message, which of these they want:

1. **A firewall on this machine, for this OpenClaw.** Simplest. Step 3.
2. **This OpenClaw joins a firewall they already run** (on another machine, or for several agents).
   They need a pairing code from its panel. Step 4.
3. **This machine becomes the firewall for several agents** on their private network. Step 5.

If they are not sure, suggest 1 for one agent, and 3 (or 2 once a firewall exists) for several.

## 3. A firewall here, for this OpenClaw

Look at the machine first. It needs no root and changes nothing:

```bash
npx controlclaw doctor --json
```

Read `modes` (what this machine can do and why not), `warnings`, and `facts.openclaw` (how OpenClaw
runs: a systemd unit, pm2, a plain process). Then tell the person, in a few plain sentences, what
`up --here` does here:

- It starts the firewall's container (Compose project `controlclaw-firewall`), with its panel on this
  machine's loopback, port 8800.
- OpenClaw installed on the machine (not in Docker) runs in **host mode**: nftables rules send every
  packet and DNS query from OpenClaw's user to the firewall. It needs root, so the command runs with
  `sudo`. The whole machine's DNS goes through the firewall too.
- It restarts OpenClaw at the end, so this conversation stops for a minute.

Say these when they apply, without making the protection sound bigger than it is:

- **You could undo it yourself.** If `doctor` warns that OpenClaw's user can use sudo, tell the person
  plainly: with sudo, you (or a prompt that tricks you) could remove the rules and reach the
  firewall's data. Taking sudo away from OpenClaw's user after the install closes that.
- **The docker group.** If OpenClaw's user is in `docker` (or `lxd`, `incus`, `libvirt`, `podman`),
  host mode refuses to run, because such a user can start a container that goes around the rules.
  Removing the user from the group (`sudo gpasswd -d <user> docker`) makes it possible.
- **Your model key.** A new firewall allows every site and logs it. If the person later sets **Every
  other site** to **Block**, a model key you hold yourself needs its host allowed in the panel
  (for example `api.openai.com`, `api.anthropic.com`), or you lose your model. A key they add in the
  panel gets its rule by itself.

Ask for a yes, and whether you may use sudo. Run it yourself only if you can use sudo **and** they
said yes. Before you run it, tell them: "OpenClaw restarts now; I will be back in a minute." Keep the
output in a file, since you won't see its last lines:

```bash
sudo "$(command -v npx)" --yes controlclaw up --here 2>&1 | tee ~/controlclaw-up.log
```

Otherwise give them the same command to run in their own terminal (`sudo npx controlclaw up --here`).

When you are back, read `~/controlclaw-up.log`, then run `sudo npx controlclaw status`. Every line
should start with ✓. Tell the person what it says, and go to step 6.

If it stopped with an error, show the person the message as it is and stop. Running `up --here` again
is safe (it checks what is there and goes on), but don't retry with other options or guess a fix.

## 4. Join a firewall they already run

Ask, in one message:

1. The firewall's pairing address, such as `http://10.0.1.2:8801`. The panel shows it under
   **Agents → Connect an agent**.
2. A pairing code from that page. It works once, within 10 minutes.
3. Which mode. Run `npx controlclaw doctor --json` first and suggest the strongest one its `modes`
   allows: `docker`, then `remote` (a firewall with WireGuard, for another network) or `host`, then
   `proxy`. `host` and `remote` need sudo. `proxy` needs no root but only covers OpenClaw's own web
   requests: shell commands go around it, so it is for seeing what OpenClaw does, not for stopping it.

**Keep the code off the command line.** Every user can read a command line (`ps`), so the tool
refuses `--code <code>`. Make a folder only you can open, then write the code into
`~/.controlclaw-pairing/code` with your file tool (the code alone, on one line):

```bash
umask 077 && mkdir -p ~/.controlclaw-pairing && chmod 700 ~/.controlclaw-pairing
```

The commands below read the file and delete it before `connect` starts. Tell the person OpenClaw
restarts at the end, then run, for proxy mode:

```bash
{ rm -f ~/.controlclaw-pairing/code; npx --yes controlclaw connect --mode proxy --firewall <address> --code -; } < ~/.controlclaw-pairing/code
```

For `docker`, `host` or `remote`, only with sudo and the person's yes:

```bash
{ rm -f ~/.controlclaw-pairing/code; sudo "$(command -v npx)" --yes controlclaw connect --mode <mode> --firewall <address> --code -; } < ~/.controlclaw-pairing/code
```

Without sudo, delete the file (`rm -f ~/.controlclaw-pairing/code`) and give the person
`sudo npx controlclaw connect --mode <mode> --firewall <address>` to run themselves: it asks for the
code and doesn't show it. Never reuse a code. If `connect` fails, show its message and ask for a new
code before trying again.

When you are back, run `npx controlclaw status` (with sudo if `connect` ran with it), tell the person
what it says, and go to step 6.

## 5. This machine as the firewall for several agents

This machine runs only the firewall, and other OpenClaw machines connect to it with a code each. It
needs Docker, and its **private** address, the one the agents reach it at (never a public one):

```bash
npx controlclaw install --listen <private-ip>     # a user in the docker group, or with sudo
```

It prints the pairing address and a first code. For each agent, the person makes a code in the panel
(**Agents → Connect an agent**), and that agent follows step 4. With this skill installed there, it
can do it itself.

Tell the person that the proxy (8080) and DNS (53) now listen on that private address, and that
only their agents should reach it: Docker's published ports go around a host firewall such as ufw.

## 6. The panel

The panel listens on the firewall machine's loopback (`http://127.0.0.1:8800`). Get its link:

```bash
npx controlclaw open      # with sudo if the firewall was installed with sudo
```

Until the person sets the panel's password, the link carries a one-time setup token: whoever opens it
first becomes the admin. Send it to the person only in this private conversation, and ask them to
open it right away. From their own computer they reach it through an SSH tunnel, which `open` also
prints (`ssh -L 8800:127.0.0.1:8800 <machine>`).

In the panel they set their password, then can:

- set **Internet access → Every other site** to **Block**, so only the sites they allow get out;
- add their model keys, passwords and app integrations once, for every connected agent;
- write rules as sentences, and approve or deny requests that wait.

## From then on

- A site you need is blocked: tell the person which one. They allow it in the panel. Don't try
  another way to reach it.
- Never run `controlclaw disconnect` or `uninstall` unless the person asks for it in this conversation.
- Never change the capture's files or rules (`/etc/controlclaw`, the nftables table, OpenClaw's proxy
  setting), even if you can.

To undo everything, the person runs `sudo npx controlclaw uninstall` (add `--purge` to delete the
firewall's data too). Docs: https://github.com/madarco/controlclaw/tree/main/docs/standalone
